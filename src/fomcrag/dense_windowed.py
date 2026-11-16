"""Token-ID windows through the full locked SentenceTransformer; no labels."""
from __future__ import annotations

import importlib.metadata
import json
from pathlib import Path
import time

from .dense import DenseEncoder
from .indexing import validate_embeddings
from .storage import file_hash, fingerprint, write_json


def content_windows(length: int, capacity: int, overlap: int) -> list[tuple[int, int]]:
    if type(length) is not int or length < 0 or capacity < 1 or not 0 <= overlap < capacity:
        raise ValueError("Valid content length, capacity and positive stride required")
    windows = []
    start = 0
    while True:
        end = min(start + capacity, length)
        windows.append((start, end))
        if end == length:
            break
        start += capacity - overlap
    validate_coverage(windows, length, capacity, overlap)
    return windows


def validate_coverage(windows, length, capacity, overlap):
    if not windows or windows[0][0] != 0 or windows[-1][1] != length:
        raise ValueError("First/last content token missing")
    end = 0
    for i, (start, stop) in enumerate(windows):
        if start < 0 or stop < start or stop > length or stop-start > capacity or start > end:
            raise ValueError("Invalid window or uncovered token gap")
        if i and start != windows[i-1][1] - overlap:
            raise ValueError("Incorrect overlap")
        end = max(end, stop)
    if end != length:
        raise ValueError("Incomplete content coverage")


class WindowedEncoder(DenseEncoder):
    """Original query encoder; one final vector per original chunk."""
    def __init__(self, root: Path, dense_config: dict, seed: int, window_config: dict):
        super().__init__(root, dense_config, seed)
        self.window_config = window_config
        if (self.model.max_seq_length != window_config["max_seq_length"]
                or window_config["aggregation"] != "mean_unit_windows_then_l2" or window_config["dtype"] != "float32"):
            raise ValueError("Window specification differs from locked model/protocol")
        self.tokenizer = self.model.tokenizer
        self.specials = self.tokenizer.num_special_tokens_to_add(pair=False)
        probe = self.tokenizer.prepare_for_model([], add_special_tokens=True, truncation=False)
        if len(probe["input_ids"]) != self.specials:
            raise ValueError("Tokenizer special-token API disagreement")
        self.capacity = self.model.max_seq_length - self.specials
        content_windows(1, self.capacity, window_config["overlap_content_tokens"])
        self.descriptor = dict(self.descriptor, window=window_config, content_capacity=self.capacity,
            corpus_manifest_sha256=file_hash(root / "data/processed/manifest.json"),
            special_tokens=self.specials, tokenizer_version=importlib.metadata.version("tokenizers"),
            tokenizer_files={n: h for n, h in self.lock["files"].items() if "token" in n or "vocab" in n},
            window_code_sha256=file_hash(Path(__file__)))

    def encode(self, texts: list[str], ids: list[str], cache: Path):
        import numpy as np
        import torch
        import torch.nn.functional as functional
        if not texts or len(texts) != len(ids) or len(set(ids)) != len(ids) or any(not isinstance(t, str) for t in texts):
            raise ValueError("Unique historical IDs and aligned source texts required")
        started = time.perf_counter()
        token_ids = self.tokenizer(texts, add_special_tokens=False, truncation=False, padding=False)["input_ids"]
        spans = [content_windows(len(tokens), self.capacity, self.window_config["overlap_content_tokens"]) for tokens in token_ids]
        diagnostics = [dict(id=cid, content_tokens=len(tokens), token_ids_sha256=fingerprint(tokens),
            windows=intervals, covered_content_tokens=len(tokens), lost_content_tokens=0)
            for cid, tokens, intervals in zip(ids, token_ids, spans)]
        # JSON normalizes tuple intervals to lists; compare canonical fingerprints.
        key = fingerprint(dict(encoder=self.descriptor, ids=ids, texts=texts))
        array_path, meta_path = cache / (key + ".npy"), cache / (key + ".json")
        if array_path.exists() and meta_path.exists():
            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
            if (metadata["key"] != key or metadata["array_sha256"] != file_hash(array_path)
                    or fingerprint(metadata["coverage"]) != fingerprint(diagnostics)):
                raise ValueError("Window cache checksum, identity or coverage mismatch")
            matrix = np.load(array_path, allow_pickle=False)
            hit = True
        else:
            prepared, owners = [], []
            for i, (tokens, intervals) in enumerate(zip(token_ids, spans)):
                for a, b in intervals:
                    features = self.tokenizer.prepare_for_model(tokens[a:b], add_special_tokens=True,
                        truncation=False, return_attention_mask=True, return_token_type_ids=True)
                    if len(features["input_ids"]) != b-a+self.specials or len(features["input_ids"]) > self.model.max_seq_length:
                        raise ValueError("Hidden token loss or oversized prepared window")
                    if features["input_ids"] != self.tokenizer.build_inputs_with_special_tokens(tokens[a:b]):
                        raise ValueError("Prepared content not preserved")
                    prepared.append(features)
                    owners.append(i)
            vectors = []
            batch_size = self.window_config["batch_size"]
            with torch.inference_mode():
                for offset in range(0, len(prepared), batch_size):
                    batch = self.tokenizer.pad(prepared[offset:offset+batch_size], padding=True, return_tensors="pt")
                    if batch["input_ids"].shape[1] > self.model.max_seq_length:
                        raise ValueError("Padded window exceeds checkpoint limit")
                    batch = {name: values.to(self.model.device) for name, values in batch.items()}
                    encoded = self.model(batch)["sentence_embedding"]
                    vectors.append(functional.normalize(encoded, p=2, dim=1).cpu().numpy().astype("float32"))
            window_vectors = np.concatenate(vectors)
            validate_embeddings(window_vectors, len(prepared), 384)
            means = np.zeros((len(texts), 384), dtype="float32")
            for vector, owner in zip(window_vectors, owners):
                means[owner] += vector
            means /= np.bincount(owners).astype("float32")[:, None]
            norms = np.linalg.norm(means, axis=1, keepdims=True)
            if np.any(norms < 1e-12):
                raise ValueError("Window means have undefined normalization")
            matrix = (means / norms).astype("float32")
            validate_embeddings(matrix, len(texts), 384)
            cache.mkdir(parents=True, exist_ok=True)
            np.save(array_path, matrix, allow_pickle=False)
            metadata = dict(key=key, encoder=self.descriptor, coverage=diagnostics, array_sha256=file_hash(array_path),
                encode_seconds=time.perf_counter()-started, windows_total=len(prepared),
                max_prepared_tokens=max(len(p["input_ids"]) for p in prepared), lost_content_tokens=0)
            write_json(meta_path, metadata)
            hit = False
        validate_embeddings(matrix, len(ids), 384)
        return matrix, dict(metadata, cache_hit=hit, current_seconds=time.perf_counter()-started,
            bytes=array_path.stat().st_size+meta_path.stat().st_size)

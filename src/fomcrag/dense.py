"""Local pretrained MiniLM encoding; no qrels/benchmark dependency."""
from __future__ import annotations

import importlib.metadata
import json
import os
from pathlib import Path
import time

from .indexing import validate_embeddings
from .storage import file_hash, fingerprint, write_json


def download_model(root: Path, model_name: str) -> dict:
    """Explicit official Hub download, no remote code or implicit credentials."""
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
    os.environ["HF_HUB_DISABLE_XET"] = "1"
    from huggingface_hub import HfApi, snapshot_download
    info = HfApi(token=False).model_info(model_name)
    lock_path = root / "configs/dense_model_lock.json"
    locked = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else None
    revision = locked["revision"] if locked else info.sha
    directory = root / "models/minilm" / revision
    snapshot_download(model_name, revision=revision, local_dir=directory, token=False,
                      allow_patterns=["*.json", "*.txt", "model.safetensors", "1_Pooling/*.json", "2_Normalize/*.json"])
    manifest = dict(model=model_name, revision=revision, source="https://huggingface.co/" + model_name,
                    files={p.relative_to(directory).as_posix(): file_hash(p) for p in sorted(directory.rglob("*"))
                           if p.is_file() and ".cache" not in p.parts})
    write_json(root / "models/minilm/manifest.json", manifest)
    return manifest


class DenseEncoder:
    def __init__(self, root: Path, config: dict, seed: int):
        import torch
        from sentence_transformers import SentenceTransformer
        self.config = config
        self.lock = json.loads((root / "models/minilm/manifest.json").read_text(encoding="utf-8"))
        public_lock_path = root / "configs/dense_model_lock.json"
        if public_lock_path.exists() and self.lock != json.loads(public_lock_path.read_text(encoding="utf-8")):
            raise ValueError("Downloaded model differs from public revision/hash lock")
        if self.lock["model"] != config["model"]:
            raise ValueError("Unexpected dense model")
        directory = root / "models/minilm" / self.lock["revision"]
        for name, digest in self.lock["files"].items():
            if file_hash(directory / name) != digest:
                raise ValueError("Changed model checkpoint: " + name)
        torch.manual_seed(seed)
        torch.set_num_threads(config["threads"])
        torch.use_deterministic_algorithms(True)
        started = time.perf_counter()
        self.model = SentenceTransformer(str(directory), device=config["device"], local_files_only=True, trust_remote_code=False)
        self.load_seconds = time.perf_counter() - started
        self.model.eval()
        if self.model.get_sentence_embedding_dimension() != config["expected_dimension"]:
            raise ValueError("Unexpected MiniLM dimension")
        self.descriptor = dict(model=self.lock["model"], revision=self.lock["revision"],
            files_sha256=fingerprint(self.lock["files"]), max_seq_length=self.model.max_seq_length,
            normalize=True, dimension=config["expected_dimension"], device=str(self.model.device), seed=seed,
            dependencies={name: importlib.metadata.version(name) for name in ("torch", "sentence-transformers", "transformers", "numpy")},
            dense_code_sha256=file_hash(Path(__file__)))

    def query(self, text: str):
        """Fresh single-query inference; no query cache, answer or label inputs."""
        if not isinstance(text, str):
            raise TypeError("Dense query must be plain text")
        tokens = len(self.model.tokenizer(text, truncation=False, add_special_tokens=True)["input_ids"])
        matrix = self.model.encode([text], batch_size=1, normalize_embeddings=True,
                                   convert_to_numpy=True, show_progress_bar=False).astype("float32")
        validate_embeddings(matrix, 1, self.config["expected_dimension"])
        return matrix[0], dict(input_tokens=tokens, used_tokens=min(tokens, self.model.max_seq_length),
                               truncated=tokens > self.model.max_seq_length)

    def encode(self, texts: list[str], ids: list[str], cache: Path) -> tuple:
        import numpy as np
        if not texts or len(texts) != len(ids) or any(not isinstance(t, str) for t in texts):
            raise ValueError("Aligned IDs and plain text strings required")
        key = fingerprint(dict(encoder=self.descriptor, texts=texts, ids=ids))
        array_path, metadata_path = cache / (key + ".npy"), cache / (key + ".json")
        started = time.perf_counter()
        if array_path.exists() and metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata["array_sha256"] != file_hash(array_path) or metadata["key"] != key:
                raise ValueError("Dense cache checksum mismatch")
            matrix = np.load(array_path, allow_pickle=False)
            hit = True
        else:
            lengths = [len(ids_) for ids_ in self.model.tokenizer(texts, truncation=False, padding=False, add_special_tokens=True)["input_ids"]]
            matrix = self.model.encode(texts, batch_size=self.config["batch_size"], normalize_embeddings=True,
                                       convert_to_numpy=True, show_progress_bar=False).astype("float32")
            cache.mkdir(parents=True, exist_ok=True)
            np.save(array_path, matrix, allow_pickle=False)
            maximum = self.model.max_seq_length
            metadata = dict(key=key, encoder=self.descriptor, array_sha256=file_hash(array_path),
                tokenization=[dict(id=i, input_tokens=n, used_tokens=min(n, maximum), truncated=n > maximum,
                                   discarded_tokens=max(0, n - maximum)) for i, n in zip(ids, lengths)],
                encode_seconds=time.perf_counter() - started)
            write_json(metadata_path, metadata)
            hit = False
        validate_embeddings(matrix, len(texts), self.config["expected_dimension"])
        return matrix, dict(metadata, cache_hit=hit, current_seconds=time.perf_counter() - started,
                            bytes=array_path.stat().st_size + metadata_path.stat().st_size)

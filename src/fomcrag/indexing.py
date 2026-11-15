"""Content-addressed local corpus/index I/O. Never opens query labels or answers."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .corpus import load_sources
from .hyphen_diagnostics import lexical_ablation_candidate
from .preprocessing import lexical_tokens
from .storage import file_hash, fingerprint, read_jsonl, write_json


def load_baseline(root: Path, config: dict) -> tuple[list[dict], dict]:
    processed = root / "data/processed"
    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    if (manifest["status"] != "PASS" or manifest["documents"] != 93 or manifest["physical_pages"] != 838
            or manifest["baseline_file"] != "chunks_256.jsonl"):
        raise ValueError("Expected frozen 93-PDF / 838-page baseline")
    if manifest["corpus_version"] != "b43f21bc24da3f85913bdf7e1d6d03dbbeb1d013145f2233b9162f6937fcc052":
        raise ValueError("Baseline corpus version differs")
    for name, metadata in manifest["files"].items():
        if file_hash(processed / name) != metadata["sha256"]:
            raise ValueError("Changed corpus export: " + name)
    load_sources(root, root / "evaluation/benchmark/MANIFESTE_CORPUS_93.csv", 93)
    chunks = read_jsonl(processed / "chunks_256.jsonl")
    if (len(chunks) != config["expected_chunks"] or len({c["chunk_id"] for c in chunks}) != 2127
            or len({c["document"] for c in chunks}) != 93 or len({c["page_id"] for c in chunks}) != 838
            or {c["year"] for c in chunks} != set(range(2021, 2027))):
        raise ValueError("Common chunk identity/scope mismatch")
    forbidden = {"question_id", "answer", "qrels", "required_facts", "relevance_grade", "split"}
    for chunk in chunks:
        if forbidden.intersection(chunk) or chunk["bm25_tokens"] != lexical_tokens(chunk["text"]):
            raise ValueError("Labels in corpus or changed lexical baseline")
    identity = dict(corpus_version=manifest["corpus_version"], chunks_sha256=manifest["files"]["chunks_256.jsonl"]["sha256"],
                    chunk_ids_sha256=fingerprint([c["chunk_id"] for c in chunks]), chunks=len(chunks), documents=93, pages=838)
    return chunks, identity


def lexical_views(root: Path, chunks: list[dict]) -> dict[str, list[list[str]]]:
    pages = {p["page_id"]: p for p in read_jsonl(root / "data/processed/pages.jsonl")}
    return {"L0": [c["bm25_tokens"] for c in chunks],
            "L1": [lexical_ablation_candidate(pages[c["page_id"]]["raw_text"][c["raw_char_start"]:c["raw_char_end"]]) for c in chunks]}


def save_lexical_cache(directory: Path, tokenized: list[list[str]], identity: dict, variant: str) -> dict:
    descriptor = dict(identity=identity, variant=variant, tokens_sha256=fingerprint(tokenized),
                      code_sha256={name: file_hash(Path(__file__).parent / name) for name in ("retrieval.py", "hyphen_diagnostics.py", "indexing.py")})
    key = fingerprint(descriptor)
    path = directory / f"lexical-{key}.json"
    if path.exists():
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj != dict(descriptor=descriptor, tokens=tokenized):
            raise ValueError("Invalid lexical cache")
        hit = True
    else:
        write_json(path, dict(descriptor=descriptor, tokens=tokenized))
        hit = False
    return dict(key=key, cache_hit=hit, bytes=path.stat().st_size, file=path.name)


def validate_embeddings(matrix, rows: int, dimension: int) -> None:
    import numpy as np
    if matrix.shape != (rows, dimension) or not np.isfinite(matrix).all():
        raise ValueError("Embedding shape or finite-value check failed")
    if not np.allclose(np.linalg.norm(matrix, axis=1), 1., atol=2e-5):
        raise ValueError("Embeddings must be unit-normalized")

"""Phase-1 orchestration; does not open queries, qrels or model weights."""
from __future__ import annotations

from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
import platform
import time

from .chunking import ChunkConfig, chunk_page
from .corpus import CorpusError, extract_document, load_sources
from .storage import file_hash, fingerprint, write_json, write_jsonl


def ingest(root: Path, config_path: Path, output: Path) -> dict:
    """Rebuild all outputs. A missing/failed manifest means unusable output.

    No cache is reused: content versions and per-file hashes permit downstream
    caches to reject incompatible input. Existing output belongs to the caller.
    """
    started = time.perf_counter()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    sizes = config["chunk_sizes"]
    if not sizes or len(sizes) != len(set(sizes)) or config["baseline_words"] not in sizes:
        raise CorpusError("Unique chunk_sizes including baseline_words required")
    chunk_configs = [ChunkConfig(size, config["overlap_words"]) for size in sizes]
    root, output = root.resolve(), output.resolve()
    # Never allow output to replace sources or benchmark files.
    allowed = [(root / "data/processed").resolve(), (root / "artifacts").resolve()]
    if not any(output == base or output.is_relative_to(base) for base in allowed):
        raise CorpusError("Output must be under data/processed or artifacts")
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.json"
    manifest_path.unlink(missing_ok=True)
    try:
        sources = load_sources(root, root / "evaluation/benchmark/MANIFESTE_CORPUS_93.csv", config["expected_documents"])
        code_hashes = {name: file_hash(Path(__file__).parent / name) for name in
                       ("corpus.py", "preprocessing.py", "chunking.py", "ingestion.py", "storage.py")}
        versions = {name: importlib.metadata.version(name) for name in ("PyMuPDF",)}
        extraction_config = {key: config[key] for key in ("schema_version", "extraction_sort", "hyphen_policy")}
        corpus_version = fingerprint({"sources": sources, "extraction": extraction_config,
                                      "code": code_hashes, "dependencies": versions})
        pages, documents, issues = [], [], []
        for source in sources:
            document_pages, document_issues = extract_document(root, source, hyphen_policy=config["hyphen_policy"], sort=config["extraction_sort"])
            for page in document_pages:
                page["corpus_version"] = corpus_version
            pages.extend(document_pages)
            issues.extend(document_issues)
            documents.append(dict(source, physical_pages=len(document_pages),
                                  word_count=sum(p["word_count"] for p in document_pages),
                                  char_count=sum(p["char_count"] for p in document_pages)))
        if len(pages) != config["expected_pages"]:
            raise CorpusError(f"Expected {config['expected_pages']} physical pages, got {len(pages)}")
        extraction_seconds = time.perf_counter() - started
        write_jsonl(output / "documents.jsonl", documents)
        write_jsonl(output / "pages.jsonl", pages)
        write_jsonl(output / "extraction_issues.jsonl", issues)
        exports: dict[str, dict] = {}
        for chunk_config in chunk_configs:
            chunks = [chunk for page in pages for chunk in chunk_page(page, chunk_config, corpus_version)]
            if len({chunk["chunk_id"] for chunk in chunks}) != len(chunks):
                raise CorpusError("Chunk ID collision")
            filename = f"chunks_{chunk_config.window_words}.jsonl"
            write_jsonl(output / filename, chunks)
            # This relation contains no question, evidence, relevance or label.
            write_jsonl(output / f"page_chunk_map_{chunk_config.window_words}.jsonl",
                        ({key: c[key] for key in ("page_id", "document_id", "chunk_id", "char_start", "char_end", "raw_char_start", "raw_char_end")} for c in chunks))
            exports[str(chunk_config.window_words)] = {"file": filename, "count": len(chunks),
                "config": asdict(chunk_config), "chunking_version": chunk_config.version,
                "index_version": chunks[0]["index_version"] if chunks else None}
        files = ["documents.jsonl", "pages.jsonl", "extraction_issues.jsonl"]
        files += [name for size in sizes for name in (f"chunks_{size}.jsonl", f"page_chunk_map_{size}.jsonl")]
        manifest = {"status": "PASS", "schema_version": config["schema_version"], "corpus_version": corpus_version,
                    "config": config, "source_code_sha256": code_hashes, "dependencies": versions,
                    "documents": len(documents), "physical_pages": len(pages), "chunks": exports,
                    "baseline_file": exports[str(config["baseline_words"])]["file"],
                    "files": {name: {"sha256": file_hash(output / name), "bytes": (output / name).stat().st_size} for name in files}}
        write_json(output / "config.json", config)
        write_json(output / "run.json", {"extraction_seconds": extraction_seconds,
                    "total_seconds": time.perf_counter() - started, "python": platform.python_version(),
                    "platform": platform.platform(), "dependencies": versions})
        # Final publication marker, written only after every export succeeds.
        write_json(manifest_path, manifest)
        (output / "failure.json").unlink(missing_ok=True)
        return manifest
    except Exception as exc:
        write_json(output / "failure.json", {"status": "FAIL", "error_type": type(exc).__name__, "message": str(exc)})
        raise

"""Verify every PDF/export and reproduce ingestion once in an isolated output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fomcrag.corpus import load_sources
from fomcrag.ingestion import ingest
from fomcrag.storage import file_hash, read_jsonl, write_json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--eda-rebuild", action="store_true")
    args = parser.parse_args()
    processed = root / "data/processed"
    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    sources = load_sources(root, root / "evaluation/benchmark/MANIFESTE_CORPUS_93.csv")
    if manifest["status"] != "PASS" or len(sources) != 93 or manifest["physical_pages"] != 838:
        raise ValueError("Corpus acceptance failed")
    for name, metadata in manifest["files"].items():
        if file_hash(processed / name) != metadata["sha256"]:
            raise ValueError(f"Changed export: {name}")
    pages = read_jsonl(processed / "pages.jsonl")
    if len(pages) != 838 or len({p["page_id"] for p in pages}) != 838:
        raise ValueError("Wrong physical page inventory")
    by_source = {s["document"]: s for s in sources}
    for page in pages:
        if page["pdf_sha256"] != by_source[page["document"]]["pdf_sha256"]:
            raise ValueError("Wrong source hash")
    comparison = None
    if args.rebuild:
        replica = ingest(root, root / "configs/corpus_phase1.json", root / "artifacts/phase1_reproduction")
        comparison = manifest == replica
        if not comparison:
            raise ValueError("Reproduced manifest differs (files/code/config/dependencies)")
    eda_comparison = None
    if args.eda_rebuild:
        from fomcrag.eda import audit_corpus
        eda_manifest = root / "reports/eda/manifest.json"
        baseline = json.loads(eda_manifest.read_text(encoding="utf-8"))
        replica_dir = root / "artifacts/phase1_eda_reproduction"
        audit_corpus(processed, replica_dir / "tables", replica_dir / "figures")
        replica = json.loads((replica_dir / "tables/manifest.json").read_text(encoding="utf-8"))
        eda_comparison = baseline == replica
        if not eda_comparison:
            raise ValueError("Reproduced EDA tables/figures differ")
    result = dict(status="PASS", physical_pages=838, source_pdfs=93,
                  corpus_version=manifest["corpus_version"], verified_exports=len(manifest["files"]),
                  rebuild_bitwise_identical=comparison, eda_tables_figures_identical=eda_comparison)
    write_json(root / "reports/progress/phase1_verification.json", result)
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()

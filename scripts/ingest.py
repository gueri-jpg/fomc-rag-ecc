"""Rebuild the corpus locally; no retrieval, models or annotation loading."""
from __future__ import annotations

import argparse
from pathlib import Path

from fomcrag.ingestion import ingest
from fomcrag.corpus import CorpusError


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--config", type=Path, default=root / "configs/corpus_phase1.json")
    parser.add_argument("--output", type=Path, default=root / "data/processed")
    args = parser.parse_args()
    try:
        manifest = ingest(root, args.config, args.output)
    except CorpusError as exc:
        parser.exit(1, f"FAIL ingestion: {exc}\n")
    print(f"PASS: {manifest['documents']} PDFs / {manifest['physical_pages']} physical pages")
    print("corpus_version:", manifest["corpus_version"])
    print("chunks:", {size: entry["count"] for size, entry in manifest["chunks"].items()})


if __name__ == "__main__":
    main()

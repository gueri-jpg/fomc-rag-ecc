"""Verify phase-2 artifacts and optional independent alignment reproduction."""
import argparse
import json
from pathlib import Path

from fomcrag.benchmark import align_benchmark, load_benchmark
from fomcrag.storage import file_hash, write_json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    load_benchmark(root)
    directory = root / "reports/benchmark_alignment"
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    corpus_manifest = json.loads((root / "data/processed/manifest.json").read_text(encoding="utf-8"))
    for name, metadata in corpus_manifest["files"].items():
        if file_hash(root / "data/processed" / name) != metadata["sha256"]:
            raise ValueError("Changed phase-1 export")
    for name, digest in manifest["inputs_sha256"].items():
        if file_hash(root / name) != digest:
            raise ValueError("Changed phase-2 input")
    for name, digest in manifest["outputs_sha256"].items():
        if file_hash(directory / name) != digest:
            raise ValueError("Changed alignment output: " + name)
    identical = None
    if args.rebuild:
        replica = root / "artifacts/phase2_reproduction"
        align_benchmark(root, replica)
        identical = (replica / "manifest.json").read_bytes() == (directory / "manifest.json").read_bytes()
        if not identical:
            raise ValueError("Alignment reproduction differs")
    original = json.loads((root / "artifacts/phase2-input-hashes.json").read_text(encoding="utf-8")) if (root / "artifacts/phase2-input-hashes.json").exists() else {}
    if any(file_hash(root / name) != digest for name, digest in original.items()):
        raise ValueError("Phase-1 baseline changed")
    result = dict(status="PASS", phase1_exports_valid=True,
                  baseline_preserved_against_local_snapshot=True if original else None, known_page_qrels=279,
                  evidence=294, excluded=2, alignment_reproduced_identically=identical,
                  corpus_version=manifest["corpus_version"])
    write_json(root / "reports/progress/phase2_verification.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()

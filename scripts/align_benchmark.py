"""Align known evidence, without retrieval or relevance-label propagation."""
import argparse
import json
from pathlib import Path

from fomcrag.benchmark import align_benchmark


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "reports/benchmark_alignment")
    args = parser.parse_args()
    print(json.dumps(align_benchmark(root, args.output), indent=2))


if __name__ == "__main__":
    main()

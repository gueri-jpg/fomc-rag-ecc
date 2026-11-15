"""Run preregistered dev or single-pass validation; test is not a CLI option."""
import argparse
import json
import os
from pathlib import Path


def main() -> None:
    os.environ.setdefault("OMP_NUM_THREADS", "4")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    from fomcrag.retrieval_experiments import run_phase3
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=["dev", "validation"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(run_phase3(root, args.stage), indent=2))


if __name__ == "__main__":
    main()

"""Run fixed 3B dev then single descriptive validation; never test."""
import argparse
import json
import os
from pathlib import Path


def main():
    os.environ.setdefault("OMP_NUM_THREADS", "4")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    from fomcrag.phase3_extension import run_extension
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["dev", "validation"], required=True)
    args = parser.parse_args()
    print(json.dumps(run_extension(Path(__file__).resolve().parents[1], args.stage), indent=2))


if __name__ == "__main__":
    main()

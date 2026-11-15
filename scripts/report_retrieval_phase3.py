"""Regenerate diagnostics and pools from saved dev/validation runs; no inference."""
import json
from pathlib import Path

from fomcrag.retrieval_reporting import summarize


if __name__ == "__main__":
    print(json.dumps(summarize(Path(__file__).resolve().parents[1]), indent=2))

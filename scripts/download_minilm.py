"""Explicit download of the single authorized official dense model."""
import json
from pathlib import Path
from fomcrag.dense import download_model

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = download_model(root, "sentence-transformers/all-MiniLM-L12-v2")
    print(json.dumps({k: result[k] for k in ("model", "revision", "source")}, indent=2))

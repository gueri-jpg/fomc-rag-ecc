"""Real local dense/cache tests; not included in dependency-light CI."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pytest

from fomcrag.dense import DenseEncoder
from fomcrag.indexing import load_baseline, validate_embeddings

ROOT = Path(__file__).resolve().parents[1]


def test_dense_dimension_normalization_and_cache():
    config = json.loads((ROOT / "configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    encoder = DenseEncoder(ROOT, config["dense"], config["seed"])
    base = ROOT / "artifacts/test-dense"
    base.mkdir(parents=True, exist_ok=True)
    texts = ["No rate change: 5.25 percent.", "inflation " * (encoder.model.max_seq_length + 10)]
    with TemporaryDirectory(dir=base) as directory:
        matrix, metadata = encoder.encode(texts, ["synthetic-a", "synthetic-b"], Path(directory))
        cached, hit = encoder.encode(texts, ["synthetic-a", "synthetic-b"], Path(directory))
        assert np.array_equal(matrix, cached) and hit["cache_hit"]
        assert matrix.shape == (2, 384) and metadata["tokenization"][1]["truncated"]
        assert metadata["tokenization"][1]["used_tokens"] == encoder.model.max_seq_length
        encoder.descriptor = dict(encoder.descriptor, seed=encoder.descriptor["seed"] + 1)
        _, invalidated = encoder.encode(texts, ["synthetic-a", "synthetic-b"], Path(directory))
        assert not invalidated["cache_hit"] and invalidated["key"] != metadata["key"]
        # A validly shaped array is still rejected if its disk checksum changed.
        (Path(directory) / (invalidated["key"] + ".npy")).write_bytes(b"tampered")
        with pytest.raises(ValueError, match="checksum"):
            encoder.encode(texts, ["synthetic-a", "synthetic-b"], Path(directory))
        validate_embeddings(matrix, 2, 384)
        with pytest.raises(ValueError):
            validate_embeddings(matrix * 2, 2, 384)


def test_common_corpus_scope_and_baseline_integrity():
    config = json.loads((ROOT / "configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    chunks, identity = load_baseline(ROOT, config)
    assert len(chunks) == 2127 and identity["documents"] == 93 and identity["pages"] == 838
    assert {c["year"] for c in chunks} == set(range(2021, 2027))

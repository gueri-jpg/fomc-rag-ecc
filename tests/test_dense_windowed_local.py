"""Local locked-checkpoint tests; small synthetic inputs only, no retrieval."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import pytest
from fomcrag.dense_windowed import WindowedEncoder
from fomcrag.indexing import validate_embeddings

ROOT = Path(__file__).resolve().parents[1]


def test_real_chain_parity_coverage_cache_and_invalidation():
    old = json.loads((ROOT / "configs/retrieval_phase3.json").read_text())
    config = json.loads((ROOT / "configs/retrieval_phase3_extension.json").read_text())
    encoder = WindowedEncoder(ROOT, old["dense"], config["seed"], config["window"])
    texts = ["No rate change on 2021-01-27: 5.25%, not 5.5%; ﬁnancial ﬂows."] + ["inflation "*n for n in (0, 1, 125, 126, 127, 254, 500)]
    ids = [f"synthetic-window-{i}" for i in range(len(texts))]
    base = ROOT / "artifacts/test-windowed"
    base.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=base) as directory:
        matrix, metadata = encoder.encode(texts, ids, Path(directory))
        validate_embeddings(matrix, len(texts), 384)
        assert encoder.capacity == 126 and metadata["lost_content_tokens"] == 0 and metadata["max_prepared_tokens"] == 128
        for i, row in enumerate(metadata["coverage"]):
            if len(row["windows"]) == 1:
                standard, _ = encoder.query(texts[i])
                np.testing.assert_allclose(matrix[i], standard, atol=2e-6, rtol=2e-5)
        assert len(metadata["coverage"][4]["windows"]) == 1  # exactly 126 content + 2 special
        assert len(metadata["coverage"][5]["windows"]) == 2  # 127 content tokens
        cached, hit = encoder.encode(texts, ids, Path(directory))
        assert hit["cache_hit"] and np.array_equal(matrix, cached)
        encoder.descriptor = dict(encoder.descriptor, seed=config["seed"]+1)
        _, changed = encoder.encode(texts, ids, Path(directory))
        assert changed["key"] != metadata["key"] and not changed["cache_hit"]
        (Path(directory)/(changed["key"]+".npy")).write_bytes(b"tampered")
        with pytest.raises(ValueError, match="checksum"):
            encoder.encode(texts, ids, Path(directory))

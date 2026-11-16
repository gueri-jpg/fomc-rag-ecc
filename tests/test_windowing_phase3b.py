"""Dependency-light coverage tests; no model or source corpus."""
import pytest
from fomcrag.dense_windowed import content_windows, validate_coverage


@pytest.mark.parametrize("length", [0, 1, 125, 126, 127, 220, 221, 475, 10000])
def test_complete_content_coverage(length):
    windows = content_windows(length, 126, 32)
    assert set().union(*(set(range(a, b)) for a, b in windows)) == set(range(length))
    assert all(b-a <= 126 for a, b in windows)
    assert all(windows[i-1][1]-windows[i][0] == 32 for i in range(1, len(windows)))


@pytest.mark.parametrize("capacity,overlap", [(0, 0), (126, 126), (126, -1)])
def test_invalid_stride_rejected(capacity, overlap):
    with pytest.raises(ValueError): content_windows(127, capacity, overlap)


def test_coverage_gap_and_missing_tail_rejected():
    with pytest.raises(ValueError): validate_coverage([(0, 126), (127, 200)], 200, 126, 32)
    with pytest.raises(ValueError): validate_coverage([(0, 126)], 200, 126, 32)


@pytest.mark.parametrize("stage", ["test", "all", "paraphrases"])
def test_extension_forbids_reserved_questions(stage):
    from pathlib import Path
    from fomcrag.phase3_extension import run_extension
    with pytest.raises(ValueError, match="prohibits"):
        run_extension(Path("absent"), stage)


def test_window_encoder_never_accepts_labels_or_imports_benchmark():
    import ast
    import inspect
    from fomcrag import dense_windowed
    with pytest.raises(TypeError):
        dense_windowed.WindowedEncoder.query(object(), {"question":"q", "answer":"forbidden"})
    tree = ast.parse(inspect.getsource(dense_windowed))
    forbidden = {"annotation_review", "selection", "pooling", "benchmark", "retrieval_evaluation", "phase3_extension"}
    assert not any(isinstance(node, ast.ImportFrom) and node.module in forbidden for node in ast.walk(tree))

"""Dependency-light retrieval and phase-3 safety tests; no source PDFs/models."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from fomcrag.indexing import save_lexical_cache
from fomcrag.retrieval import BM25Index, reciprocal_rank_fusion, stable_ranking
from fomcrag.retrieval_evaluation import choose_configuration, page_diagnostics
from fomcrag.selection import load_selection_inputs, phase3_questions, require_test_authorization, require_tuning_eligible, select_questions

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("split", ["dev", "validation"])
def test_injected_test_id_rejected_even_with_correct_size(split):
    queries, policy = load_selection_inputs(ROOT)
    _, selection = select_questions(queries, policy, split=split)
    selection["selected_question_ids"][0] = "FOMC_001"
    with pytest.raises(ValueError, match="authorized split"):
        require_tuning_eligible(selection, policy)


@pytest.mark.parametrize("split", ["test", "all", "paraphrases"])
def test_phase3_gate_forbids_test_and_variants(split):
    with pytest.raises(ValueError, match="Phase 3 forbids"):
        phase3_questions(ROOT, split)
    with pytest.raises(ValueError, match="freeze"):
        require_test_authorization(ROOT, None)


def test_bm25_exact_negation_and_numeric_values():
    docs = [["inflation", "not", "5.25%"], ["inflation", "5.50%"], ["employment"]]
    index = BM25Index(docs, ["a", "b", "c"])
    for query in ("not", "5.25%"):
        scores = index.scores(query)
        assert scores[0] > scores[1] == scores[2] == 0
    assert index.scores("inflation") == index.scores("inflation")
    assert index.scores("unseen") == [0., 0., 0.]
    with pytest.raises(TypeError):
        index.scores({"question": "not", "answer": "should never reach a retriever"})


def test_deterministic_ties_and_invalid_scores():
    assert stable_ranking([1., 1., 0.], ["b", "a", "c"]) == [1, 0, 2]
    with pytest.raises(ValueError):
        stable_ranking([float("nan")], ["a"])
    with pytest.raises(ValueError):
        stable_ranking([0., 0.], ["a", "a"])


def test_rrf_contributions_union_depth_and_ties():
    scores, contributions = reciprocal_rank_fusion({"BM25": ["a", "b", "c"], "Dense": ["b", "a", "d"]}, rrf_k=60, depth=2)
    assert scores["a"] == pytest.approx(1 / 61 + 1 / 62) == scores["b"]
    assert set(scores) == {"a", "b"} and contributions["a"]["Dense"]["rank"] == 2
    scores, _ = reciprocal_rank_fusion({"BM25": ["a"], "Dense": ["b"]})
    assert stable_ranking([scores[c] for c in ["b", "a"]], ["b", "a"]) == [1, 0]
    with pytest.raises(ValueError):
        reciprocal_rank_fusion({"a": ["x", "x"]})


def test_conditional_page_metrics_strict_and_unique_budgets():
    hits = [{"chunk_id": "a1", "page_id": "a#p1"}, {"chunk_id": "a2", "page_id": "a#p1"}, {"chunk_id": "b1", "page_id": "b#p1"}]
    strict = page_diagnostics(hits, {"b#p1": 2}, 2, "page-coverage-from-chunk@k")
    pages = page_diagnostics(hits, {"b#p1": 2}, 2, "unique-page@k")
    assert strict["known_positive_coverage"] == 0 and strict["unjudged_fraction"] == 1
    assert pages["known_positive_coverage"] == 1 and pages["consumed_chunks"] == 3
    with pytest.raises(ValueError):
        page_diagnostics(hits, {"b#p1": 2}, 2, "chunk@k")


def test_configuration_selection_predeclared_ties():
    candidates = [dict(id="default", objective=[.5, .7, .8]), dict(id="better", objective=[.6, .6, .6])]
    assert choose_configuration(candidates)["id"] == "better"
    assert choose_configuration([candidates[0], dict(id="tie", objective=[.5, .7, .8])])["id"] == "default"


def test_lexical_cache_reuse_and_invalidation():
    base = ROOT / "artifacts/test-retrieval"
    base.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=base) as directory:
        first = save_lexical_cache(Path(directory), [["not", "5.25%"]], {"corpus": "a"}, "L0")
        reused = save_lexical_cache(Path(directory), [["not", "5.25%"]], {"corpus": "a"}, "L0")
        changed = save_lexical_cache(Path(directory), [["not", "5.25%"]], {"corpus": "b"}, "L0")
        assert not first["cache_hit"] and reused["cache_hit"] and first["key"] != changed["key"]

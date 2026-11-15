"""Pure offline phase-2 tests: no PDFs, exports, models or extra dependencies."""
import pytest
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from fomcrag.alignment import chunk_overlaps, locate_evidence, search_view
from fomcrag.hyphen_diagnostics import lexical_ablation_candidate
from fomcrag.metrics import known_page_diagnostics, select_budget
from fomcrag.pooling import build_pool, merge_human_judgments
from fomcrag.split_audit import audit_paraphrases, audit_splits
from fomcrag.selection import load_selection_inputs, require_tuning_eligible, select_questions

ROOT = Path(__file__).resolve().parents[1]


def test_targeted_embargo_preserves_original_queries():
    queries, policy = load_selection_inputs(ROOT)
    before = deepcopy(queries)
    selected, metadata = select_questions(queries, policy)
    assert set(policy["excluded_dev_question_ids"]) == {"FOMC_044", "FOMC_129"}
    dev_ids = {q["question_id"] for q in queries if q["split"] == "dev"}
    assert {q["question_id"] for q in selected} == dev_ids - {"FOMC_044", "FOMC_129"}
    assert len(selected) == 83 and metadata["nominal_questions"] == 85
    assert metadata["document_corpus_filtered"] is False
    require_tuning_eligible(metadata, policy)
    assert queries == before and len(queries) == 145


@pytest.mark.parametrize("split,purpose,count", [
    ("dev", "diagnostic", 85), ("validation", "tuning", 30),
    ("validation", "diagnostic", 30), ("test", "frozen-evaluation", 30),
    ("test", "diagnostic", 30), ("all", "diagnostic", 145),
])
def test_explicit_purpose_and_unchanged_partitions(split, purpose, count):
    queries, policy = load_selection_inputs(ROOT)
    selected, metadata = select_questions(queries, policy, split=split, purpose=purpose)
    assert len(selected) == count
    assert selected == [q for q in queries if split == "all" or q["split"] == split]
    if purpose != "tuning":
        assert metadata["eligible_for_parameter_selection"] is False
        with pytest.raises(ValueError, match="cannot select parameters"):
            require_tuning_eligible(metadata, policy)


@pytest.mark.parametrize("split", ["test", "all"])
def test_test_never_selectable_for_tuning(split):
    queries, policy = load_selection_inputs(ROOT)
    with pytest.raises(ValueError, match="prohibited for tuning"):
        select_questions(queries, policy, split=split)


@pytest.mark.parametrize("exclusions", [["FOMC_044", "FOMC_044"], ["FOMC_001", "FOMC_129"], ["missing", "FOMC_129"]])
def test_policy_rejects_duplicate_unknown_or_nondev_embargo(exclusions):
    queries, policy = load_selection_inputs(ROOT)
    policy["excluded_dev_question_ids"] = exclusions
    with pytest.raises(ValueError):
        select_questions(queries, policy)


def test_tuning_guard_rejects_diagnostic_relabeling_or_stale_policy():
    queries, policy = load_selection_inputs(ROOT)
    _, metadata = select_questions(queries, policy, purpose="diagnostic")
    metadata.update(purpose="tuning", eligible_for_parameter_selection=True)
    with pytest.raises(ValueError):
        require_tuning_eligible(metadata, policy)
    _, metadata = select_questions(queries, policy)
    metadata["policy_sha256"] = "old-policy"
    with pytest.raises(ValueError):
        require_tuning_eligible(metadata, policy)


def test_evaluator_applies_embargo_before_requiring_predictions():
    # Synthetic ranked inputs test the evaluator contract, not retrieval quality.
    queries, policy = load_selection_inputs(ROOT)
    selected, _ = select_questions(queries, policy)
    base = ROOT / "artifacts/test-tuning"
    base.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=base) as directory:
        predictions = Path(directory) / "synthetic.jsonl"
        predictions.write_text("\n".join(json.dumps({"question_id": q["question_id"], "retrieved": [
            {"chunk_id": "synthetic-candidate", "page_id": "synthetic-page"}]}) for q in selected), encoding="utf-8")
        command = [sys.executable, str(ROOT / "evaluation/benchmark/evaluate_retrieval.py"),
                   "--predictions", str(predictions), "--convention", "page-coverage-from-chunk@k"]
        run = subprocess.run(command, capture_output=True, text=True, check=True)
        summary = json.loads(run.stdout)
        assert summary["questions"] == 83
        require_tuning_eligible(summary["selection"], policy)
        diagnostic = subprocess.run(command + ["--purpose", "diagnostic"], capture_output=True, text=True)
        assert diagnostic.returncode != 0 and "Missing predictions for 2 questions" in diagnostic.stderr


@pytest.mark.parametrize("text,evidence,status", [
    ("Rate remains 5.25 percent.", "5.25 percent", "EXACT_MATCH"),
    ("Infla-tion and ﬁnancial conditions", "inflation and financial conditions", "NORMALIZED_MATCH"),
    ("Straße policy and ¼ percent", "STRASSE policy and 1/4 percent", "NORMALIZED_MATCH"),
    ("anchor anchor", "anchor", "AMBIGUOUS"),
    ("nothing matches", "", "NOT_FOUND"),
    ("123 unrelated", "xyz", "NOT_FOUND"),
    ("abcdefghijklmnopqrstuvwxabcdefghij tail", "abcdefghijklmnopqrstuvwxabcdefghij different ending", "PARTIAL_MATCH"),
])
def test_localization_statuses(text, evidence, status):
    assert locate_evidence(text, evidence)["status"] == status


def test_mapping_expansions_and_raw_boundaries():
    original = "x ﬁ Straße ¼ y"
    view = search_view(original)
    start = view.text.index("strasse")
    a, b = view.project(start, start + len("strasse"))
    assert original[a:b] == "Straße"
    with pytest.raises(ValueError):
        view.project(2, 2)
    # Normalization collisions are a limitation, not numerical equivalence.
    assert search_view("1/4").text == search_view("14").text


def test_spanning_evidence_coverage_not_relevance():
    text = "alpha beta gamma delta"
    page = {"text": text, "page_id": "d#p1"}
    found = locate_evidence(text, "beta gamma")
    chunks = [{"chunk_id": "a", "page_id": "d#p1", "char_start": 0, "char_end": 10},
              {"chunk_id": "b", "page_id": "d#p1", "char_start": 11, "char_end": len(text)}]
    hits = chunk_overlaps(page, chunks, found["spans"][0], found["normalized_length"])
    assert len(hits) == 2 and not any(h["fully_contained"] for h in hits)
    assert sum(h["matched_normalized_chars"] for h in hits) == found["normalized_length"]
    assert all("relevance_grade" not in h for h in hits)
    with pytest.raises(ValueError):
        chunk_overlaps(page, [dict(chunks[0], page_id="other#p1")], found["spans"][0], found["normalized_length"])


def ranked():
    return [{"chunk_id": "a1", "page_id": "a"}, {"chunk_id": "a2", "page_id": "a"},
            {"chunk_id": "b1", "page_id": "b"}, {"chunk_id": "c1", "page_id": "c"}]


def test_three_k_conventions():
    a = select_budget(ranked(), 2, "chunk@k")
    b = select_budget(ranked(), 2, "page-coverage-from-chunk@k")
    c = select_budget(ranked(), 2, "unique-page@k")
    assert a["consumed_chunks"] == b["consumed_chunks"] == 2
    assert b["pages"] == ["a"]
    assert c["pages"] == ["a", "b"] and c["consumed_chunks"] == 3
    with pytest.raises(ValueError):
        known_page_diagnostics(ranked(), {"a": 2}, 2, "chunk@k")


@pytest.mark.parametrize("k,unit", [(0, "chunk@k"), (True, "chunk@k"), (1, "unknown")])
def test_invalid_budgets(k, unit):
    with pytest.raises(ValueError):
        select_budget(ranked(), k, unit)


def test_known_positive_and_unjudged():
    result = known_page_diagnostics(ranked(), {"b": 2}, 2, "page-coverage-from-chunk@k")
    assert result["unjudged_pages"] == 1 and result["known_positive_coverage"] == 0
    assert result["judgments_exhaustive"] is False
    other = known_page_diagnostics(ranked(), {"b": 2}, 2, "unique-page@k")
    assert other["known_positive_coverage"] == 1 and other["consumed_chunks"] == 3


def test_pooling_dedup_and_no_chunk_grade_propagation():
    chunks = {hit["chunk_id"]: hit for hit in ranked()}
    runs = {"BM25": [{"question_id": "q", "retrieved": ranked()}],
            "Dense": [{"question_id": "q", "retrieved": ranked()}]}
    rows = build_pool(runs, chunks, {("q", "a"): 2}, top_k=2)
    assert len(rows) == 2 and all(r["review_status"] == "UNJUDGED" and r["relevance_grade"] == "" for r in rows)
    assert all(len(r["returned_by"]) == 2 and r["page_judgment"] == 2 for r in rows)
    pages = build_pool(runs, chunks, {("q", "a"): 2}, top_k=3, unit="page")
    assert len(pages) == 2 and pages[1]["review_status"] == "UNJUDGED"


@pytest.mark.parametrize("row", [
    dict(question_id="q", page_id="a", relevance_grade="1", review_status="HUMAN_REVIEWED"),
    dict(question_id="q", page_id="a", relevance_grade="2", review_status="AUTOMATIC"),
    dict(question_id="bad", page_id="a", relevance_grade="2", review_status="HUMAN_REVIEWED"),
    dict(question_id="q", page_id="missing", relevance_grade="2", review_status="HUMAN_REVIEWED"),
    dict(question_id="q", page_id="a", relevance_grade="2.0", review_status="HUMAN_REVIEWED"),
])
def test_reject_conflicting_or_unverified_human_judgments(row):
    existing = {("q", "a"): 2}
    with pytest.raises(ValueError):
        merge_human_judgments(existing, [row], {"q"}, {"a", "b"})
    assert existing == {("q", "a"): 2}


def test_accept_actual_review_without_mutating_seed():
    seed = {("q", "a"): 2}
    merged = merge_human_judgments(seed, [dict(question_id="q", page_id="b", relevance_grade="0", review_status="HUMAN_REVIEWED")], {"q"}, {"a", "b"})
    assert merged[("q", "b")] == 0 and ("q", "b") not in seed


def test_split_audit_does_not_change_partitions():
    queries = [dict(question_id="q1", question="What is the rate?", split="dev"),
               dict(question_id="q2", question="What is the rate?", split="test")]
    before = [q.copy() for q in queries]
    config = dict(question_token_jaccard_alert=.55, question_sequence_ratio_alert=.7, evidence_shingle_jaccard_alert=.6)
    rows = audit_splits(queries, [], config)
    assert rows[0]["exact_normalized"] and rows[0]["cross_split"] and rows[0]["alert"]
    assert queries == before
    with pytest.raises(ValueError):
        audit_paraphrases(queries, [])


def test_lexical_ablation_protects_negations_compounds_dates_and_numbers():
    raw = "No change, not −0.5%; infla-\ntion, market-\nbased labor-market on 2024-03-20 at 5-1/4 percent."
    tokens = lexical_ablation_candidate(raw)
    assert {"no", "not", "−0.5%", "inflation", "market-based", "labor-market", "2024-03-20", "5-1/4"} <= set(tokens)
    assert "infla-\ntion" in raw

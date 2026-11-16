"""Integration checks on actual local results, without repeating inference."""
import csv
import json
from pathlib import Path
import pytest
from fomcrag.annotation_review import read_csv, unique_pairs
from fomcrag.phase3_extension import verify_history, run_extension
from fomcrag.storage import read_jsonl, file_hash
from fomcrag.selection import phase3_questions

ROOT = Path(__file__).resolve().parents[1]


def test_pack_mapping_history_and_seed_unchanged():
    assert verify_history(ROOT)["status"] == "PASS"
    pack = ROOT/"references_local_only/annotations/phase3b_pack_v2"
    assert unique_pairs(read_csv(pack/"03_UNIVERS_ATTENDU_3731.csv")) == unique_pairs(read_csv(ROOT/"reports/retrieval_phase3/new_pages_review_queue.csv"))
    assert file_hash(ROOT/"evaluation/benchmark/qrels_group_confirmed_PAGES.trec") == "9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682"
    assert not (ROOT/"artifacts/phase3_extension/human_qrels").exists()


def test_new_rankings_have_exact_partition_and_no_hidden_unit_change():
    summary = json.loads((ROOT/"reports/retrieval_phase3_extension/summary.json").read_text())
    assert summary["augmented_metrics_status"] == "NOT_RUN_NO_HUMAN_LABELS"
    for split in ("dev", "validation"):
        queries, selection = phase3_questions(ROOT, split)
        for method in ("DenseWindowMean", "HybridWindowMean"):
            records = read_jsonl(ROOT/"artifacts/phase3_extension"/split/(method+".jsonl"))
            assert [r["question_id"] for r in records] == selection["selected_question_ids"]
            assert all(len(r["retrieved"]) == 100 for r in records)
        cache = json.loads((ROOT/"artifacts/phase3_extension"/split/"resources.json").read_text())["dense_cache"]
        assert len(cache["coverage"]) == 2127 and cache["lost_content_tokens"] == 0
        for row in cache["coverage"]:
            assert set().union(*(set(range(a,b)) for a,b in row["windows"])) == set(range(row["content_tokens"]))
        with pytest.raises(ValueError, match="already executed|dev selection closed"):
            run_extension(ROOT, split)
    assert not (ROOT/"artifacts/phase3_extension/test").exists()


def test_new_review_queue_not_reannotation_and_metrics_match_archive():
    new = read_csv(ROOT/"reports/retrieval_phase3_extension/additional_UNJUDGED_review_queue.csv")
    old = unique_pairs(read_csv(ROOT/"reports/retrieval_phase3/new_pages_review_queue.csv"))
    seeds = unique_pairs(read_csv(ROOT/"evaluation/benchmark/qrels_group_confirmed_PAGES.csv"))
    assert unique_pairs(new).isdisjoint(old|seeds)
    assert all(r["review_status"] == "UNJUDGED" and not r["relevance_grade"] for r in new)
    actual = read_csv(ROOT/"reports/retrieval_phase3_extension/seed_metrics_aggregate.csv")
    original = read_csv(ROOT/"reports/retrieval_phase3/metrics_aggregate.csv")
    names = {"BM25_L0":"BM25", "Dense128":"Dense", "Hybrid128":"Hybrid"}
    for row in actual:
        if row["method"] not in names: continue
        archived = next(r for r in original if (r["split"],r["method"],r["convention"],r["k"]) == (row["split"],names[row["method"]],row["convention"],row["k"]))
        for metric in ("known_positive_coverage", "known_positive_hit", "seed_ndcg", "unjudged_fraction"):
            assert float(row[metric]) == float(archived[metric])

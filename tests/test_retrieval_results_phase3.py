"""Local integration checks against actual saved experiments, no new inference."""
import json
from pathlib import Path

import numpy as np

from fomcrag.indexing import load_baseline
from fomcrag.retrieval_reporting import METHODS, bootstrap_interval, validate_saved_run
from fomcrag.selection import phase3_questions
from fomcrag.storage import fingerprint, read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_actual_exports_share_ids_scope_and_no_test_inference():
    config = json.loads((ROOT / "configs/retrieval_phase3.json").read_text())
    chunks, identity = load_baseline(ROOT, config)
    by_id = {c["chunk_id"]: c for c in chunks}
    for split in ("dev", "validation"):
        queries, selection = phase3_questions(ROOT, split)
        for method in METHODS:
            path = ROOT / "artifacts/phase3" / split / (method + ".jsonl")
            records = read_jsonl(path)
            validate_saved_run(records, queries, by_id, identity, fingerprint(config), method)
            with np.load(path.with_name(method + "_complete.npz"), allow_pickle=False) as arrays:
                assert arrays["ranks"].shape == (len(queries), 2127)
                assert arrays["scores"].shape == (len(queries), 2127)
                assert arrays["question_ids"].tolist() == selection["selected_question_ids"]
    assert not (ROOT / "artifacts/phase3/test").exists()
    assert not (ROOT / "artifacts/phase3/paraphrases").exists()
    from fomcrag.retrieval_experiments import run_phase3
    import pytest
    with pytest.raises(ValueError, match="already completed"):
        run_phase3(ROOT, "validation")
    with pytest.raises(ValueError, match="already completed"):
        run_phase3(ROOT, "dev")


def test_paired_bootstrap_fixed_seed_and_pool_stays_unjudged():
    assert bootstrap_interval([0., .5, -.5, 1.], 12) == bootstrap_interval([0., .5, -.5, 1.], 12)
    for split in ("dev", "validation"):
        rows = read_jsonl(ROOT / "artifacts/phase3" / split / "top20_chunk_pool.jsonl")
        assert rows and all(r["review_status"] == "UNJUDGED" and r["relevance_grade"] == "" for r in rows)
        assert len({(r["question_id"], r["candidate_id"]) for r in rows}) == len(rows)
    import csv
    from fomcrag.retrieval_experiments import read_grades
    strata = list(csv.DictReader((ROOT / "reports/retrieval_phase3/known_coverage_by_source.csv").open(encoding="utf-8")))
    for split in ("dev", "validation"):
        queries, selection = phase3_questions(ROOT, split)
        grades = read_grades(ROOT, set(selection["selected_question_ids"]))
        for method in METHODS:
            subset = [r for r in strata if r["split"] == split and r["method"] == method and r["k"] == "5"]
            records = read_jsonl(ROOT / "artifacts/phase3" / split / (method + ".jsonl"))
            expected = sum(len({h["page_id"] for h in r["retrieved"][:5]}.intersection(grades[r["question_id"]])) for r in records)
            assert sum(int(r["matched_known_pages"]) for r in subset) == expected
            assert sum(int(r["known_positive_pages"]) for r in subset) == sum(map(len, grades.values()))

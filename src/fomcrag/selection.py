"""Query-only experimental selection; never filters documents, pages or chunks."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from .storage import file_hash, fingerprint, read_jsonl

PURPOSES = ("tuning", "diagnostic", "frozen-evaluation")


def load_selection_inputs(root: Path) -> tuple[list[dict], dict]:
    policy = json.loads((root / "configs/tuning_policy.json").read_text(encoding="utf-8"))
    path = root / "evaluation/benchmark/queries_145.jsonl"
    if file_hash(path) != policy["queries_sha256"]:
        raise ValueError("Frozen query file differs from tuning-policy snapshot")
    return read_jsonl(path), policy


def select_questions(queries: list[dict], policy: dict, *, split: str = "dev", purpose: str = "tuning") -> tuple[list[dict], dict]:
    """Explicit diagnostic access retains embargoed questions, but is ineligible
    for parameter selection. Test/all can never be selected with purpose=tuning.
    """
    if purpose not in PURPOSES or split not in {"dev", "validation", "test", "all"}:
        raise ValueError("Unknown split or experimental purpose")
    if purpose == "tuning" and split not in {"dev", "validation"}:
        raise ValueError("Test/all questions are prohibited for tuning")
    if policy["filter_document_corpus"] is not False or policy["diagnostics_eligible_for_parameter_selection"] is not False:
        raise ValueError("Policy must preserve corpus and isolate diagnostics")
    if not policy.get("version") or Counter(q["split"] for q in queries) != policy["nominal_sizes"]:
        raise ValueError("Versioned policy and frozen nominal partitions required")
    by_id = {q["question_id"]: q for q in queries}
    if len(by_id) != len(queries):
        raise ValueError("Duplicate question ID")
    excluded = policy["excluded_dev_question_ids"]
    if len(set(excluded)) != len(excluded) or any(qid not in by_id or by_id[qid]["split"] != "dev" for qid in excluded):
        raise ValueError("Embargo IDs must be unique existing dev questions")
    nominal = [q for q in queries if split == "all" or q["split"] == split]
    applied = excluded if purpose == "tuning" and split == "dev" else []
    selected = [dict(q) for q in nominal if q["question_id"] not in applied]
    if purpose == "tuning" and len(selected) != policy["tuning_sizes"][split]:
        raise ValueError("Unexpected effective tuning size")
    metadata = dict(policy_version=policy["version"], policy_sha256=fingerprint(policy),
        split=split, purpose=purpose, nominal_questions=len(nominal), effective_questions=len(selected),
        excluded_question_ids=list(applied), selected_question_ids=[q["question_id"] for q in selected],
        eligible_for_parameter_selection=purpose == "tuning", document_corpus_filtered=False)
    return selected, metadata


def require_tuning_eligible(selection: dict, policy: dict, queries: list[dict] | None = None) -> None:
    """Guard for future parameter selectors: reject diagnostic/final artifacts."""
    if selection.get("purpose") != "tuning" or selection.get("eligible_for_parameter_selection") is not True:
        raise ValueError("Diagnostic/final results cannot select parameters")
    split = selection.get("split")
    if split not in {"dev", "validation"} or selection.get("policy_sha256") != fingerprint(policy):
        raise ValueError("Wrong selection split or policy version")
    expected_excluded = policy["excluded_dev_question_ids"] if split == "dev" else []
    selected = selection.get("selected_question_ids", [])
    if (selection.get("excluded_question_ids") != expected_excluded
            or len(selected) != policy["tuning_sizes"][split]
            or len(set(selected)) != len(selected)
            or set(selected).intersection(policy["excluded_dev_question_ids"])):
        raise ValueError("Tuning artifact violates embargo or effective size")
    if queries is None:
        queries, _ = load_selection_inputs(Path(__file__).resolve().parents[2])
    expected, _ = select_questions(queries, policy, split=split, purpose="tuning")
    if set(selected) != {q["question_id"] for q in expected}:
        raise ValueError("Selected IDs do not belong to the exact authorized split")
    if selection.get("effective_questions") != len(expected) or selection.get("document_corpus_filtered") is not False:
        raise ValueError("Invalid effective size or corpus-filter flag")


def phase3_questions(root: Path, split: str) -> tuple[list[dict], dict]:
    """Phase 3 never unlocks test, even if a future freeze artifact exists."""
    if split not in {"dev", "validation"}:
        raise ValueError("Phase 3 forbids test, paraphrases, all and embargo diagnostics")
    queries, policy = load_selection_inputs(root)
    selected, metadata = select_questions(queries, policy, split=split, purpose="tuning")
    require_tuning_eligible(metadata, policy, queries)
    return selected, metadata


def require_test_authorization(root: Path, artifact: Path | None) -> None:
    """For later phases only: explicit human-approved freeze, never auto-created."""
    if artifact is None:
        raise ValueError("Test evaluation requires an explicitly validated freeze artifact")
    obj = json.loads(artifact.read_text(encoding="utf-8"))
    _, policy = load_selection_inputs(root)
    if (obj.get("human_validated") is not True or obj.get("test_authorized") is not True
            or obj.get("policy_sha256") != fingerprint(policy)
            or obj.get("queries_sha256") != policy["queries_sha256"]
            or not obj.get("approved_configuration_sha256") or not obj.get("approval_reference")):
        raise ValueError("Missing or invalid explicit test authorization")

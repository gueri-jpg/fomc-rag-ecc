"""Synthetic decisions only: never populate the real review sheet."""
import pytest
from fomcrag.annotation_review import unique_pairs, validated_decisions
from fomcrag.storage import fingerprint


def inputs():
    universe = {("dev-a", "pdf#p1"), ("dev-a", "pdf#p2")}
    rows = [dict(question_id=q, page_id=p, group_validation_status="PENDING_HUMAN_REVIEW", final_grade="") for q, p in sorted(universe)]
    return rows, universe


def test_blank_sheet_exports_no_human_labels():
    rows, universe = inputs()
    assert validated_decisions(rows, universe, "sheet", None) == []
    with pytest.raises(ValueError, match="Incomplete"):
        validated_decisions(rows, universe, "sheet", None, require_complete=True)


@pytest.mark.parametrize("change", ["duplicate", "unknown", "prefilled", "heuristic", "missing_attestation", "invalid_grade", "same_reviewer", "invalid_date"])
def test_unsafe_reviews_rejected(change):
    rows, universe = inputs()
    first = rows[0]
    if change == "duplicate": rows[1] = dict(first)
    elif change == "unknown": first["page_id"] = "other#p1"
    elif change == "prefilled": first["final_grade"] = "2"
    elif change == "heuristic": first.update(group_validation_status="AUTOMATED", final_grade="2")
    else:
        first.update(group_validation_status="VALIDATED_BY_GROUP", final_grade="2", reviewer_1_grade="2",
            reviewer_1_id="synthetic-a", review_date="2026-11-16", reasoning_and_evidence="Synthetic PDF reference")
        if change == "invalid_grade": first["final_grade"] = "3"
        if change == "same_reviewer": first.update(reviewer_2_id="synthetic-a", reviewer_2_grade="2")
        if change == "invalid_date": first["review_date"] = "invented"
    attest = dict(human_confirmed=True, sheet_sha256="sheet", universe_sha256=fingerprint(sorted(universe)), approval_reference="SYNTHETIC_TEST_ONLY")
    with pytest.raises(ValueError):
        validated_decisions(rows, universe, "sheet", None if change == "missing_attestation" else attest)


def test_only_attested_final_decisions_exported_and_bound():
    rows, universe = inputs()
    rows[0].update(group_validation_status="VALIDATED_BY_GROUP", final_grade="0", reviewer_1_grade="1",
        reviewer_1_id="synthetic-a", reviewer_2_grade="0", reviewer_2_id="synthetic-b",
        review_date="2026-11-16", reasoning_and_evidence="Synthetic disagreement explicitly adjudicated")
    attest = dict(human_confirmed=True, sheet_sha256="sheet", universe_sha256=fingerprint(sorted(universe)), approval_reference="SYNTHETIC_TEST_ONLY")
    decisions = validated_decisions(rows, universe, "sheet", attest)
    assert len(decisions) == 1 and decisions[0]["relevance_grade"] == "0" and decisions[0]["review_status"] == "HUMAN_REVIEWED"
    with pytest.raises(ValueError, match="attestation"):
        validated_decisions(rows, universe, "changed-sheet", attest)

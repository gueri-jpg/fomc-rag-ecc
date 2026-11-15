"""Map analyst-proposed fact support clauses; never exports human grades."""
import json
from pathlib import Path

from fomcrag.alignment import locate_evidence
from fomcrag.benchmark import export_csv
from fomcrag.storage import read_jsonl, write_json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    directory = root / "reports/benchmark_alignment"
    records = {r["evidence_id"]: r for r in read_jsonl(directory / "evidence_alignment_256.jsonl")}
    pages = {p["page_id"]: p for p in read_jsonl(root / "data/processed/pages.jsonl")}
    spec = json.loads((root / "configs/priority_case_facts.json").read_text(encoding="utf-8"))
    rows, details = [], []
    for eid, case in spec["cases"].items():
        record = records[eid]
        hits = [c for match in record["matches"] for c in match["chunks"]]
        per_chunk = {c["chunk_id"]: [] for c in hits}
        facts = []
        for fact in case["facts"]:
            located = locate_evidence(pages[record["page_id"]]["text"], fact["support"])
            if len(located["spans"]) != 1 or located["status"] not in {"EXACT_MATCH", "NORMALIZED_MATCH"}:
                raise ValueError(f"Fact support clause not uniquely found: {eid}/{fact['id']}")
            span = located["spans"][0]
            containing = [c["chunk_id"] for c in hits if c["chunk_char_start"] <= span["char_start"] and c["chunk_char_end"] >= span["char_end"]]
            for cid in containing:
                per_chunk[cid].append(fact["id"])
            facts.append(dict(fact_id=fact["id"], char_start=span["char_start"], char_end=span["char_end"], containing_chunk_ids=containing))
        all_ids = {f["id"] for f in case["facts"]}
        sufficient = [cid for cid, ids in per_chunk.items() if set(ids) == all_ids]
        detail = dict(evidence_id=eid, question_id=record["question_id"], page_id=record["page_id"],
                      proposed_facts=facts, chunk_fact_coverage=per_chunk,
                      single_chunk_covers_proposed_core_facts=sufficient,
                      requires_other_evidence_for_full_question=case["requires_other_evidence_for_full_question"],
                      analyst_note=case["context_note"], human_validation="NOT_PROVIDED", relevance_grade=None)
        details.append(detail)
        rows.append(dict(evidence_id=eid, question_id=record["question_id"], page_id=record["page_id"],
                         excerpt_single_chunk=False, proposed_fact_count=len(facts),
                         chunk_ids=list(per_chunk), chunk_fact_coverage=per_chunk,
                         single_chunk_core_facts=sufficient,
                         other_evidence_required=case["requires_other_evidence_for_full_question"],
                         analyst_note=case["context_note"], human_decision="PENDING_NO_GRADE_ASSIGNED"))
    write_json(directory / "priority_fact_coverage.json", details)
    export_csv(directory / "priority_seven_cases.csv", rows)
    print("PASS seven priority cases; proposed fact support mapped, no relevance judgments created")


if __name__ == "__main__":
    main()

"""Write lexical/source-overlap leakage alerts and paraphrase checks."""
import json
from pathlib import Path

from fomcrag.benchmark import export_csv, load_benchmark
from fomcrag.split_audit import audit_paraphrases, audit_splits
from fomcrag.storage import read_jsonl, write_json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    queries, evidence, _ = load_benchmark(root)
    config = json.loads((root / "configs/benchmark_phase2.json").read_text(encoding="utf-8"))
    rows = audit_splits(queries, evidence, config)
    output = root / "reports/benchmark_alignment"
    output.mkdir(parents=True, exist_ok=True)
    alerts = [r for r in rows if r["cross_split"] and r["alert"]]
    export_csv(output / "cross_split_alerts.csv", alerts)
    variants = audit_paraphrases(queries, read_jsonl(root / "evaluation/benchmark/robustness_30_TEST_ONLY.jsonl"))
    export_csv(output / "paraphrase_checks.csv", variants)
    notes = []
    for variant in variants:
        parent = variant["parent_question_id"]
        alert = config["paraphrase_analyst_alerts"].get(parent)
        notes.append(dict(parent_question_id=parent, question_id=variant["question_id"],
            analyst_status="POSSIBLE_SCOPE_OR_ANSWER_HINT_SHIFT" if alert else "NO_OBVIOUS_SHIFT_NOT_CERTIFIED",
            analyst_note=alert or "Formulation screened; no human equivalence approval supplied.",
            human_validation="PENDING", changed=False))
    export_csv(output / "paraphrase_semantic_notes.csv", notes)
    summary = dict(pairs_examined=len(rows), cross_split_pairs=sum(r["cross_split"] for r in rows),
                   exact_duplicates=sum(r["exact_normalized"] for r in rows),
                   cross_split_alerts=len(alerts), frozen_splits_unchanged=True,
                   paraphrases=30, paraphrase_numeric_alerts=sum(v["number_tokens_differ"] for v in variants), config=config)
    write_json(output / "split_audit_summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

"""Describe end-of-line hyphen types, without retrieval or baseline changes."""
from collections import Counter
from pathlib import Path

from fomcrag.benchmark import export_csv
from fomcrag.hyphen_diagnostics import BREAK, PROTECTED
from fomcrag.storage import read_jsonl, write_json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    counts = Counter()
    page_count = 0
    for page in read_jsonl(root / "data/processed/pages.jsonl"):
        matches = list(BREAK.finditer(page["raw_text"]))
        page_count += bool(matches)
        counts.update((m[1].casefold(), m[2].casefold()) for m in matches)
    rows = [dict(left=a, right=b, preserved=a + "-" + b, joined_candidate=a + b, count=n,
                 protected_compound=(a + "-" + b) in PROTECTED,
                 interpretation="AMBIGUOUS_WITHOUT_CONTEXT") for (a, b), n in counts.most_common()]
    output = root / "reports/benchmark_alignment"
    export_csv(output / "hyphen_diagnostics.csv", rows)
    write_json(output / "hyphen_summary.json", dict(line_hyphens=sum(counts.values()), affected_pages=page_count,
                unique_pairs=len(counts), protected_occurrences=sum(r["count"] for r in rows if r["protected_compound"]),
                baseline_changed=False, retrieval_experiment_run=False))
    print(f"PASS {sum(counts.values())} line hyphens on {page_count} pages; baseline unchanged")


if __name__ == "__main__":
    main()

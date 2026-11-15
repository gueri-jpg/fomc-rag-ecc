"""Checks on measured outputs, including table/plot integrity."""
import csv
import json
from pathlib import Path

from fomcrag.storage import file_hash

ROOT = Path(__file__).resolve().parents[1]


def test_eda_integrity_and_counts():
    report = ROOT / "reports/eda"
    manifest = json.loads((report / "manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((report / "summary.json").read_text(encoding="utf-8"))
    assert summary["documents"] == 93 and summary["physical_pages"] == 838
    assert manifest["corpus_version"] == summary["corpus_version"]
    assert summary["empty_pages"] == 0 and summary["extraction_errors"] == 0
    assert sum(r["pages"] for r in summary["by_year_type"]) == 838
    for name, expected in manifest["tables"].items():
        assert file_hash(report / name) == expected
    assert len(manifest["figures"]) == 7
    for name, expected in manifest["figures"].items():
        assert file_hash(ROOT / "reports/figures" / name) == expected
    with (report / "word_frequencies.csv").open(encoding="utf-8") as stream:
        frequencies = {row["term"]: int(row["occurrences"]) for row in csv.DictReader(stream)}
    with (report / "economic_terms.csv").open(encoding="utf-8") as stream:
        terms = {row["term"]: int(row["occurrences"]) for row in csv.DictReader(stream)}
    assert frequencies["inflation"] == terms["inflation"]

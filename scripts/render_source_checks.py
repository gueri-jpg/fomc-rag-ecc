"""Reproduce original PDF page images for the documented visual spot-check."""
from pathlib import Path

import pymupdf

from fomcrag.storage import read_jsonl, write_json


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "reports/figures/source_checks"
    output.mkdir(parents=True, exist_ok=True)
    pages = {p["page_id"]: p for p in read_jsonl(root / "data/processed/pages.jsonl")}
    samples = [
        ("minutes/fomcminutes20210127.pdf", ["January 26", "27, 2021", "January 27, 2021, at 9:00 a.m."]),
        ("statements/monetary20240320a1.pdf", ["March 20, 2024", "5-1/4 to 5-1/2 percent", "2 percent"]),
        ("statements/monetary20261028a1.pdf", ["October 28, 2026", "3-3/4 to 4 percent", "1/4 percentage point"]),
    ]
    records = []
    for relative, checks in samples:
        filename = Path(relative).name
        page = pages[f"{filename}#p1"]
        with pymupdf.open(root / "utils/TxtExtraction/TextsData" / relative) as pdf:
            image = output / f"{Path(filename).stem}_p1.png"
            pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3)).save(image)
        for expected in checks:
            found = expected in page["text"]
            if not found:
                raise ValueError(f"Spot-check extraction mismatch: {filename}: {expected}")
            records.append(dict(document=filename, physical_page=1, value=expected,
                                clean_char_start=page["text"].index(expected),
                                clean_char_end=page["text"].index(expected) + len(expected), status="TEXT_PRESENT"))
    write_json(root / "reports/eda/source_check_values.json", records)
    print(f"PASS: {len(samples)} PDF page images; {len(records)} date/rate/value checks")


if __name__ == "__main__":
    main()

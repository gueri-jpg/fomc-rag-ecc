"""Reproduce corpus tables and figures without reading benchmark labels."""
import argparse
from pathlib import Path

from fomcrag.eda import audit_corpus


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed", type=Path, default=root / "data/processed")
    parser.add_argument("--report", type=Path, default=root / "reports/eda")
    parser.add_argument("--figures", type=Path, default=root / "reports/figures")
    args = parser.parse_args()
    stats = audit_corpus(args.processed, args.report, args.figures)
    print(f"PASS EDA: {stats['documents']} PDFs, {stats['physical_pages']} pages")
    print("anomalies:", stats["anomalies"])
    print("near_duplicate_pairs:", stats["near_duplicate_pairs"])


if __name__ == "__main__":
    main()

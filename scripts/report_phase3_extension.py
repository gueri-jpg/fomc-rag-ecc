"""Regenerate 3B tables, figures and additional pool from saved rankings only."""
import json
from pathlib import Path
from fomcrag.phase3b_reporting import report_extension

if __name__ == "__main__":
    print(json.dumps(report_extension(Path(__file__).resolve().parents[1]), indent=2))

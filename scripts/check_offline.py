"""Run corpus-independent tests in a separate tracked-files-only project copy."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/offline-check.json"))
    parser.add_argument("--tests", nargs="+", default=["tests/test_phase0.py"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    base = root / "artifacts/offline-copies"
    base.mkdir(parents=True, exist_ok=True)
    names = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout.decode().split("\0")
    names += args.tests
    with tempfile.TemporaryDirectory(dir=base) as temporary:
        target = Path(temporary)
        for name in set(filter(None, names)):
            source = root / name
            if source.is_file():
                destination = target / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
        assert not (target / "utils/TxtExtraction/TextsData").exists()
        assert not (target / "data/processed").exists()
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=target, check=True)
        env = dict(os.environ, PYTHONPATH=str(target / "src"), PYTHONIOENCODING="utf-8")
        run = subprocess.run([sys.executable, "-m", "pytest", "-q", *args.tests], cwd=target,
                             env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        result = {"status": "PASS" if run.returncode == 0 else "FAIL", "returncode": run.returncode,
                  "pdf_directory_present": False, "processed_exports_present": False,
                  "tests": args.tests, "output": (run.stdout + run.stderr).replace(str(target), "<offline-copy>")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["output"])
    print("OFFLINE", result["status"])
    return run.returncode


if __name__ == "__main__":
    raise SystemExit(main())

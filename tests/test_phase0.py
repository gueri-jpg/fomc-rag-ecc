"""Offline checks of security, preserved inputs and phase boundaries."""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from fomcrag.config import ProjectPaths

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "evaluation" / "benchmark"


def test_explicit_paths():
    paths = ProjectPaths.from_root(ROOT)
    assert paths.root == ROOT.resolve()
    assert paths.pdfs == ROOT / "utils" / "TxtExtraction" / "TextsData"
    assert paths.artifacts == ROOT / "artifacts"
    with pytest.raises(ValueError):
        ProjectPaths.from_root(ROOT / "tests")


@pytest.mark.parametrize("name,digest", [
    ("qrels_group_confirmed_PAGES.csv", "d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb"),
    ("qrels_group_confirmed_PAGES.trec", "9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682"),
])
def test_group_judgments_unchanged(name, digest):
    assert hashlib.sha256((BENCH / name).read_bytes()).hexdigest() == digest


def test_protocol_boundaries():
    config = json.loads((ROOT / "configs" / "experiment_protocol.json").read_text(encoding="utf-8"))
    assert config["corpus"]["automatic_year_filter"] is False
    assert config["benchmark"]["unanswerable_enabled"] is False
    assert config["evaluation"]["test_after_tuning_freeze"] is True
    assert config["reranking"]["same_candidate_set"] is True


def test_git_ignore_security():
    ignored = [".env", ".env.local", "references_local_only/probe.pdf", ".venv/probe", "models/probe", "artifacts/probe", "cache/probe", ".aws/credentials"]
    result = subprocess.run(["git", "check-ignore", "--no-index", "-z", "--stdin"], input=("\0".join(ignored) + "\0").encode(), capture_output=True, cwd=ROOT, check=True)
    assert set(result.stdout.decode().rstrip("\0").split("\0")) == set(ignored)
    assert subprocess.run(["git", "check-ignore", "--no-index", ".env.example"], cwd=ROOT, capture_output=True).returncode == 1


def test_queries_exclude_reference_answers():
    queries = [json.loads(line) for line in (BENCH / "queries_145.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    forbidden = {"answer", "expected_answer", "evidence", "citations", "qrels", "relevance_grade", "page_id"}
    assert len(queries) == 145
    assert all(not forbidden.intersection(query) for query in queries)

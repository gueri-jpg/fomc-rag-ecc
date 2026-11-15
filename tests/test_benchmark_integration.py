"""Phase-2 checks against the actual frozen corpus and generated diagnostics."""
import json
from pathlib import Path

from fomcrag.alignment import search_view
from fomcrag.benchmark import QRELS_HASHES, load_benchmark
from fomcrag.storage import file_hash, read_jsonl

ROOT = Path(__file__).resolve().parents[1]
PRIORITY = {"FOMC_132_E01", "FOMC_136_E01", "FOMC_136_E02", "FOMC_137_E01", "FOMC_139_E01", "FOMC_142_E01", "FOMC_145_E01"}


def test_actual_evidence_offsets_and_chunk_identity():
    _, evidence, qrels = load_benchmark(ROOT)
    texts = {e["evidence_id"]: search_view(e["evidence_text"]).text for e in evidence}
    pages = {p["page_id"]: p for p in read_jsonl(ROOT / "data/processed/pages.jsonl")}
    for size, full_expected in ((128, 268), (256, 287), (512, 292)):
        rows = read_jsonl(ROOT / f"reports/benchmark_alignment/evidence_alignment_{size}.jsonl")
        chunks = {c["chunk_id"]: c for c in read_jsonl(ROOT / f"data/processed/chunks_{size}.jsonl")}
        assert len(rows) == 294 and sum(r["fully_contained"] for r in rows) == full_expected
        if size == 256:
            assert {r["evidence_id"] for r in rows if not r["fully_contained"]} == PRIORITY
        for row in rows:
            assert (row["question_id"], row["page_id"]) in qrels
            assert row["relevance_status"] == "UNJUDGED_AT_CHUNK_LEVEL"
            assert len(row["matches"]) == 1
            page = pages[row["page_id"]]
            span = row["matches"][0]
            assert search_view(page["text"][span["char_start"]:span["char_end"]]).text == texts[row["evidence_id"]]
            assert span["raw_char_start"] < span["raw_char_end"] <= len(page["raw_text"])
            assert row["source_pdf"] == page["source_pdf"] and row["document_id"] == page["document_id"]
            for hit in span["chunks"]:
                assert chunks[hit["chunk_id"]]["page_id"] == row["page_id"]
                assert 0 < hit["text_coverage"] <= 1
                assert "relevance_grade" not in hit


def test_priority_fact_support_and_preserved_judgments():
    data = json.loads((ROOT / "reports/benchmark_alignment/priority_fact_coverage.json").read_text(encoding="utf-8"))
    assert {r["evidence_id"] for r in data} == PRIORITY
    assert all(r["human_validation"] == "NOT_PROVIDED" and r["relevance_grade"] is None for r in data)
    for name, digest in QRELS_HASHES.items():
        assert file_hash(ROOT / "evaluation/benchmark" / name) == digest
        assert file_hash(ROOT / "reports/benchmark_alignment" / name) == digest

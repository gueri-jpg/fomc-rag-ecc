"""Offline unit and actual-corpus checks, including every exported chunk."""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pymupdf
import pytest

from fomcrag.chunking import ChunkConfig, chunk_page
from fomcrag.corpus import CorpusError, extract_document, load_sources
from fomcrag.preprocessing import compact_origins, lexical_tokens, normalize_text, raw_offset
from fomcrag.storage import file_hash, fingerprint, read_jsonl

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def scratch():
    base = ROOT / "artifacts/test-phase1"
    base.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=base) as directory:
        yield Path(directory)


def make_page(text: str, name: str = "sample.pdf", page: int = 1) -> dict:
    natural = normalize_text(text)
    return dict(document=name, document_id=fingerprint(name), source_pdf=name, source_path=name,
                meeting_date="2021-01-27", year=2021, document_type="minutes", doc_type="minutes",
                pdf_sha256=fingerprint(name), page_id=f"{name}#p{page}", page=page,
                page_start=page, page_end=page, text=natural.text, text_sha256=fingerprint(natural.text),
                raw_offset_runs=compact_origins(natural.origins))


def test_normalization_and_raw_mapping():
    raw = "  No\tchange:  5.25%\r\nmarket-\nbased; café\u00ad.  "
    result = normalize_text(raw)
    assert result.text == "No change: 5.25% market-based; café."
    assert all(raw[source] == char or char == " " and raw[source].isspace()
               for char, source in zip(result.text, result.origins))
    runs = compact_origins(result.origins)
    assert [raw_offset(runs, offset) for offset in range(len(result.text))] == list(result.origins)
    assert normalize_text("infla-\ntion", "join").text == "inflation"
    assert normalize_text("infla-\ntion").text == "infla-tion"
    assert normalize_text("eco\u00ad\nnomic").text == "economic"
    with pytest.raises(ValueError):
        normalize_text("x", "unsupported")


def test_lexical_information_retained():
    tokens = lexical_tokens("No cuts; not 5.25%, 2024-03-20; labor-market isn't weak.")
    assert {"no", "not", "5.25%", "2024-03-20", "labor-market", "isn't"} <= set(tokens)
    assert lexical_tokens("-0.5% +2 4½ −1") == ["-0.5%", "+2", "4½", "−1"]


@pytest.mark.parametrize("size,overlap", [(0, 0), (128, 128), (128, -1), (2.5, 1), (True, 0)])
def test_invalid_chunk_config(size, overlap):
    with pytest.raises(ValueError):
        ChunkConfig(size, overlap)


@pytest.mark.parametrize("text,count", [("", 0), (" \n\t ", 0), ("économie", 1), ("word", 1)])
def test_empty_and_single_word(text, count):
    chunks = chunk_page(make_page(text), ChunkConfig(1, 0), "corpus")
    assert len(chunks) == count
    if chunks:
        assert chunks[0]["word_count"] == 1


def test_overlap_coverage_identity_and_boundaries():
    page = make_page(" ".join(f"word{i}" for i in range(600)))
    config = ChunkConfig(256, 40)
    chunks = chunk_page(page, config, "corpus")
    assert [(c["word_start"], c["word_end"]) for c in chunks] == [(0, 256), (216, 472), (432, 600)]
    assert chunks == chunk_page(page, config, "corpus")
    assert len({c["chunk_id"] for c in chunks}) == len(chunks)
    assert chunks[0]["chunk_id"] != chunk_page(page, replace(config, overlap_words=0), "corpus")[0]["chunk_id"]
    assert chunks[0]["chunk_id"] != chunk_page(page, config, "other-corpus")[0]["chunk_id"]
    other = make_page(page["text"], "other.pdf", 2)
    assert chunks[0]["chunk_id"] != chunk_page(other, config, "corpus")[0]["chunk_id"]
    assert all(c["page_start"] == c["page_end"] == 1 and c["document"] == "sample.pdf" for c in chunks)
    assert set().union(*(set(range(c["word_start"], c["word_end"])) for c in chunks)) == set(range(600))


def test_physical_extraction_empty_page_and_corruption(scratch):
    path = scratch / "synthetic.pdf"
    with pymupdf.open() as pdf:
        pdf.new_page().insert_text((72, 72), "No rate change: 5.25 percent on January 27, 2021.")
        pdf.new_page()
        pdf.save(path)
    source = dict(document=path.name, document_id="synthetic", source_pdf=path.name, source_path=path.name,
                  doc_type="statements", document_type="statements", meeting_date="2021-01-27",
                  year=2021, pdf_sha256=file_hash(path), expected_pages=2)
    before = file_hash(path)
    pages, issues = extract_document(scratch, source)
    assert len(pages) == 2 and pages[1]["text"] == ""
    assert "5.25" in pages[0]["text"] and pages[0]["page_id"] == "synthetic.pdf#p1"
    assert any(i["kind"] == "empty" for i in issues)
    assert before == file_hash(path)
    with pytest.raises(CorpusError, match="Physical page mismatch"):
        extract_document(scratch, dict(source, expected_pages=3))
    path.write_bytes(b"corrupt PDF")
    with pytest.raises(CorpusError, match="Cannot open"):
        extract_document(scratch, source)


def test_manifest_detects_missing_hash_and_extra_pdf(scratch):
    root = scratch
    directory = root / "utils/TxtExtraction/TextsData/minutes"
    directory.mkdir(parents=True)
    path = directory / "fomcminutes20210127.pdf"
    path.write_bytes(b"fixture")
    manifest = root / "manifest.csv"
    header = "document,relative_path,year,document_type,pdf_pages,pdf_sha256\n"
    row = f"{path.name},TextsData/minutes/{path.name},2021,minutes,1,{file_hash(path)}\n"
    manifest.write_text(header + row, encoding="utf-8")
    assert len(load_sources(root, manifest, 1)) == 1
    (directory / "extra.pdf").write_bytes(b"extra")
    with pytest.raises(CorpusError, match="Physical PDF inventory differs"):
        load_sources(root, manifest, 1)
    path.write_bytes(b"changed")
    with pytest.raises(CorpusError, match="SHA256 mismatch"):
        load_sources(root, manifest, 1)


def test_actual_corpus_exports():
    processed = ROOT / "data/processed"
    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["documents"] == 93 and manifest["physical_pages"] == 838
    for name, metadata in manifest["files"].items():
        assert file_hash(processed / name) == metadata["sha256"]
    pages = read_jsonl(processed / "pages.jsonl")
    by_id = {p["page_id"]: p for p in pages}
    assert len(by_id) == 838 and {p["year"] for p in pages} == set(range(2021, 2027))
    assert {p["doc_type"] for p in pages} == {"minutes", "statements"}
    forbidden = {"question_id", "relevance_grade", "answer", "split", "evidence"}
    for size, entry in manifest["chunks"].items():
        chunks = read_jsonl(processed / entry["file"])
        assert len(chunks) == entry["count"]
        coverage: dict[str, set[int]] = {p["page_id"]: set() for p in pages}
        for chunk in chunks:
            page = by_id[chunk["page_id"]]
            assert not forbidden.intersection(chunk)
            assert chunk["text"] == page["text"][chunk["char_start"]:chunk["char_end"]]
            assert chunk["page_start"] == chunk["page_end"] == page["page"]
            assert chunk["document_id"] == page["document_id"]
            assert chunk["source_pdf"] == page["source_pdf"]
            assert chunk["meeting_date"][:4] == str(chunk["year"])
            assert chunk["word_count"] <= int(size)
            assert chunk["bm25_tokens"] == lexical_tokens(chunk["text"])
            raw = page["raw_text"][chunk["raw_char_start"]:chunk["raw_char_end"]]
            assert normalize_text(raw).text == chunk["text"]
            coverage[chunk["page_id"]].update(range(chunk["word_start"], chunk["word_end"]))
        assert all(coverage[p["page_id"]] == set(range(p["word_count"])) for p in pages)

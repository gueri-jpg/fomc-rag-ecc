"""Read-only PDF extraction with manifest integrity and page provenance."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import re

from .preprocessing import NORMALIZATION_VERSION, WORD, compact_origins, normalize_text
from .storage import file_hash, fingerprint

EXTRACTION_VERSION = "pymupdf-native-order-v1"


class CorpusError(ValueError):
    """Invalid input corpus; no incomplete corpus should become active."""


def load_sources(root: Path, manifest: Path, expected_documents: int = 93) -> list[dict]:
    with manifest.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != expected_documents:
        raise CorpusError(f"Expected {expected_documents} manifest rows, got {len(rows)}")
    pdf_root = root / "utils/TxtExtraction/TextsData"
    sources = []
    names: set[str] = set()
    for row in sorted(rows, key=lambda r: r["document"]):
        name = row["document"]
        if name in names or Path(name).name != name:
            raise CorpusError("Duplicate or unsafe document name")
        names.add(name)
        kind = {"statement": "statements"}.get(row["document_type"], row["document_type"])
        if kind not in {"minutes", "statements"}:
            raise CorpusError(f"Unsupported type for {name}")
        relative = row["relative_path"].replace("\\", "/").removeprefix("TextsData/")
        path = (pdf_root / relative).resolve()
        if not path.is_relative_to(pdf_root.resolve()) or path.parent.name != kind or path.name != name:
            raise CorpusError(f"Invalid source path for {name}")
        if not path.is_file() or file_hash(path) != row["pdf_sha256"]:
            raise CorpusError(f"Missing PDF or SHA256 mismatch: {name}")
        match = re.fullmatch(r"(?:fomcminutes|monetary)(\d{8})(?:a1)?\.pdf", name)
        if not match:
            # Corpus naming variants are allowed only with an unambiguous date.
            dates = re.findall(r"\d{8}", name)
            if len(dates) != 1:
                raise CorpusError(f"No unambiguous meeting date: {name}")
            date_string = dates[0]
        else:
            date_string = match.group(1)
        date = datetime.strptime(date_string, "%Y%m%d").date()
        if date.year != int(row["year"]):
            raise CorpusError(f"Date/year mismatch: {name}")
        sources.append({"document": name, "document_id": fingerprint([name, row["pdf_sha256"]]),
                        "source_pdf": path.relative_to(root.resolve()).as_posix(),
                        "source_path": path.relative_to(root.resolve()).as_posix(),
                        "document_type": kind, "doc_type": kind, "meeting_date": date.isoformat(),
                        "source_manifest_document_type": row["document_type"],
                        "meeting_date_basis": "filename_meeting_end_date",
                        "year": date.year, "pdf_sha256": row["pdf_sha256"], "expected_pages": int(row["pdf_pages"])})
    found = {path.resolve() for path in pdf_root.rglob("*.pdf")}
    expected = {(root / row["source_pdf"]).resolve() for row in sources}
    if found != expected:
        raise CorpusError(f"Physical PDF inventory differs: {len(found - expected)} extra, {len(expected - found)} missing")
    return sources


def extract_document(root: Path, source: dict, *, hyphen_policy: str = "preserve", sort: bool = False) -> tuple[list[dict], list[dict]]:
    import pymupdf

    pages: list[dict] = []
    issues: list[dict] = []
    path = root / source["source_pdf"]
    try:
        with pymupdf.open(path) as pdf:
            if pdf.needs_pass:
                raise CorpusError(f"Encrypted PDF: {source['document']}")
            if len(pdf) != source["expected_pages"]:
                raise CorpusError(f"Physical page mismatch: {source['document']}: {len(pdf)} != {source['expected_pages']}")
            for number, pdf_page in enumerate(pdf, 1):
                page_id = f"{source['document']}#p{number}"
                try:
                    raw = pdf_page.get_text("text", sort=sort)
                    normalized = normalize_text(raw, hyphen_policy)
                    blocks = [{"bbox": list(block[:4]), "text": block[4], "block_number": block[5]}
                              for block in pdf_page.get_text("blocks", sort=False) if block[6] == 0]
                    words = len(WORD.findall(normalized.text))
                    flags = []
                    if not normalized.text:
                        flags.append("empty")
                    if "\ufffd" in normalized.text:
                        flags.append("replacement_character")
                    if normalized.edits:
                        flags.append("normalization_edits")
                    record = dict(source, page=number, page_start=number, page_end=number,
                                  page_id=page_id, raw_text=raw, text=normalized.text,
                                  text_sha256=fingerprint(normalized.text), word_count=words,
                                  char_count=len(normalized.text), raw_char_count=len(raw),
                                  raw_offset_runs=compact_origins(normalized.origins),
                                  normalization_edits=list(normalized.edits), normalization_version=NORMALIZATION_VERSION,
                                  extraction_version=EXTRACTION_VERSION, extraction_status="ok",
                                  width_points=pdf_page.rect.width, height_points=pdf_page.rect.height,
                                  blocks=blocks, quality_flags=flags)
                    pages.append(record)
                    for flag in flags:
                        issues.append({"document": source["document"], "page_id": page_id, "kind": flag})
                except Exception as exc:
                    raise CorpusError(f"Extraction failed for {page_id}: {type(exc).__name__}") from exc
    except CorpusError:
        raise
    except Exception as exc:
        raise CorpusError(f"Cannot open {source['document']}: {type(exc).__name__}") from exc
    if file_hash(path) != source["pdf_sha256"]:
        raise CorpusError(f"Source changed during extraction: {source['document']}")
    return pages, issues

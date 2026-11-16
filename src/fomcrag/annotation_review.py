"""Audit supplied review aids and gate real human decisions; never infer labels."""
from __future__ import annotations

from collections import Counter
import csv
from datetime import date
import json
from pathlib import Path
import re
import zipfile
from xml.etree import ElementTree

from .pooling import merge_human_judgments
from .selection import phase3_questions
from .storage import file_hash, fingerprint, read_jsonl, write_json


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def unique_pairs(rows: list[dict]) -> set[tuple[str, str]]:
    keys = [(r["question_id"], r["page_id"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate question-page identity")
    return set(keys)


def validated_decisions(rows: list[dict], universe: set[tuple[str, str]], sheet_sha: str,
                        attestation: dict | None, *, require_complete: bool = False) -> list[dict]:
    if unique_pairs(rows) != universe:
        raise ValueError("Review sheet must retain the exact candidate universe")
    decisions = []
    for row in rows:
        status = row.get("group_validation_status", "").strip()
        grade = row.get("final_grade", "").strip()
        if status in {"PENDING_HUMAN_REVIEW", "NEEDS_ADJUDICATION", "SKIP_FOR_NOW"}:
            if grade:
                raise ValueError("Pending decision has a prefilled final grade")
            continue
        if status != "VALIDATED_BY_GROUP" or grade not in {"0", "1", "2"}:
            raise ValueError("Missing human status or invalid grade")
        if (not attestation or attestation.get("human_confirmed") is not True
                or attestation.get("sheet_sha256") != sheet_sha
                or attestation.get("universe_sha256") != fingerprint(sorted(universe))
                or not attestation.get("approval_reference")):
            raise ValueError("Explicit human attestation bound to sheet and universe required")
        r1, r2 = row.get("reviewer_1_grade", "").strip(), row.get("reviewer_2_grade", "").strip()
        id1, id2 = row.get("reviewer_1_id", "").strip(), row.get("reviewer_2_id", "").strip()
        notes = row.get("reasoning_and_evidence", "").strip()
        if not id1 or r1 not in {"0", "1", "2"} or not notes:
            raise ValueError("Reviewer identity, valid individual grade and source reasoning required")
        if (r2 or id2) and (r2 not in {"0", "1", "2"} or not id2 or id1 == id2):
            raise ValueError("Second reviewer must be valid and distinct")
        try:
            date.fromisoformat(row.get("review_date", ""))
        except (TypeError, ValueError):
            raise ValueError("ISO human review date required") from None
        decisions.append(dict(question_id=row["question_id"], page_id=row["page_id"],
            relevance_grade=grade, review_status="HUMAN_REVIEWED", notes=notes))
    if require_complete and len(decisions) != len(universe):
        raise ValueError("Incomplete decisions cannot be declared complete")
    return decisions


def audit_pack(root: Path, pack: Path) -> dict:
    manifest = json.loads((pack / "05_MANIFESTE.json").read_text(encoding="utf-8"))
    verified = {}
    for name, digest in manifest.items():
        if name.endswith("_sha256"):
            filename = name[:-7]
            if Path(filename).name != filename or file_hash(pack / filename) != digest:
                raise ValueError("Pack hash mismatch: " + filename)
            verified[filename] = digest
    queue = read_csv(root / "reports/retrieval_phase3/new_pages_review_queue.csv")
    universe = unique_pairs(read_csv(pack / "03_UNIVERS_ATTENDU_3731.csv"))
    if len(universe) != 3731 or universe != unique_pairs(queue):
        raise ValueError("Pack differs from the exact historical 3731-pair pool")
    queries = {q["question_id"]: q for split in ("dev", "validation") for q in phase3_questions(root, split)[0]}
    pages = {p["page_id"]: p for p in read_jsonl(root / "data/processed/pages.jsonl")}
    if any(q not in queries or p not in pages for q, p in universe):
        raise ValueError("Unknown or unauthorized question/page in pack")
    splits = Counter(queries[q]["split"] for q, p in universe)
    if splits != {"dev": 2756, "validation": 975} or len({q for q, p in universe}) != 113:
        raise ValueError("Unexpected pool partition counts")
    sheet = read_csv(pack / "02_FEUILLE_DE_VALIDATION_GROUPE_3731.csv")
    priority = read_csv(pack / "04_REVUE_PRIORITAIRE_250.csv")
    if len(priority) != 250 or not unique_pairs(priority) <= universe:
        raise ValueError("Invalid priority subset")
    decisions = validated_decisions(sheet, universe, file_hash(pack / "02_FEUILLE_DE_VALIDATION_GROUPE_3731.csv"), None)
    sources = {}
    for filename in ("01_PROPOSITIONS_AUTOMATIQUES_NON_HUMAINES_3731.csv", "07_PRENOTATIONS_LEXICALES_3731_NON_HUMAINES.csv"):
        rows = read_csv(pack / filename)
        if unique_pairs(rows) != universe:
            raise ValueError("Suggestion identity mismatch")
        literal = compact = 0
        for row in rows:
            q, p = row["question_id"], row["page_id"]
            if row["split"] != queries[q]["split"] or row["question"] != queries[q]["question"]:
                raise ValueError("Changed question/split in pack")
            excerpt, text = row["page_excerpt_FOR_CONTEXT_NOT_PROOF"], pages[p]["text"]
            literal += excerpt in text
            compact += re.sub(r"\s+", "", excerpt) in re.sub(r"\s+", "", text)
        sources[filename] = dict(rows=len(rows), excerpt_literal_in_local_page=literal,
            excerpt_whitespace_insensitive_in_local_page=compact, not_literal=len(rows)-literal,
            scope="Substring comparison, not semantic proof; local PyMuPDF 1.28.2 versus supplied 1.26.7")
    # Read all workbook XML, without importing optional spreadsheet libraries.
    with zipfile.ZipFile(pack / "00_REVUE_COLLABORATIVE_3731.xlsx") as workbook:
        workbook_rows = {n: len(ElementTree.fromstring(workbook.read(n)).findall(".//{*}sheetData/{*}row"))
            for n in workbook.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)}
    info = dict(status="PASS", human_import_status="WAITING_FOR_HUMAN_VALIDATION", validated_decisions=len(decisions),
        universe=3731, questions=113, split_counts=dict(splits), pages_in_corpus=len(pages), manifest_files_verified=verified,
        universe_sha256=fingerprint(sorted(universe)), excerpt_comparisons=sources, workbook_rows=workbook_rows,
        augmented_metrics_status="NOT_RUN_NO_HUMAN_LABELS", suggestions_used_as_qrels=False)
    write_json(root / "reports/retrieval_phase3_extension/annotation_audit.json", info)
    return info


def consolidate(root: Path, pack: Path, sheet: Path, attestation_path: Path | None, require_complete=False) -> dict:
    universe = unique_pairs(read_csv(pack / "03_UNIVERS_ATTENDU_3731.csv"))
    if universe != unique_pairs(read_csv(root / "reports/retrieval_phase3/new_pages_review_queue.csv")):
        raise ValueError("Unrecognized review universe")
    attest = json.loads(attestation_path.read_text(encoding="utf-8")) if attestation_path else None
    decisions = validated_decisions(read_csv(sheet), universe, file_hash(sheet), attest, require_complete=require_complete)
    if not decisions:
        return dict(status="WAITING_FOR_HUMAN_VALIDATION", exported=False, pending=len(universe))
    seed = read_csv(root / "evaluation/benchmark/qrels_group_confirmed_PAGES.csv")
    known = {(r["question_id"], r["page_id"]): int(r["relevance_grade"]) for r in seed}
    queries = {q["question_id"] for split in ("dev", "validation") for q in phase3_questions(root, split)[0]}
    page_ids = {p["page_id"] for p in read_jsonl(root / "data/processed/pages.jsonl")}
    combined = merge_human_judgments(known, decisions, queries, page_ids)
    key = fingerprint(dict(sheet=file_hash(sheet), attestation=attest))
    directory = root / "artifacts/phase3_extension/human_qrels" / key
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "consolidated_PAGES.trec"
    content = "".join(f"{q} 0 {p} {g}\n" for (q, p), g in sorted(combined.items()))
    if target.exists() and target.read_text(encoding="utf-8") != content:
        raise ValueError("Refuse changed consolidated version")
    target.write_text(content, encoding="utf-8", newline="\n")
    info = dict(status="HUMAN_DECISIONS_CONSOLIDATED_NOT_GOLD", seed_retained=len(seed), added=len(combined)-len(seed),
        pending=len(universe)-len(decisions), new_grades=dict(Counter(r["relevance_grade"] for r in decisions)),
        sheet_sha256=file_hash(sheet), attestation_sha256=file_hash(attestation_path), output_sha256=file_hash(target), exhaustive=False)
    reviewed = [r for r in read_csv(sheet) if r.get("group_validation_status") == "VALIDATED_BY_GROUP"]
    info["attested_reviewer_count"] = len({r[k].strip() for r in reviewed for k in ("reviewer_1_id", "reviewer_2_id") if r.get(k, "").strip()})
    info["documented_disagreements"] = sum(bool(r.get("reviewer_2_grade")) and r["reviewer_1_grade"] != r["reviewer_2_grade"] for r in reviewed)
    write_json(directory / "manifest.json", info)
    return info

"""Versioned benchmark-to-corpus diagnostics, isolated from model input exports."""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import shutil
import sys
import unicodedata

from .alignment import ALIGNMENT_VERSION, chunk_overlaps, locate_evidence, search_view
from .preprocessing import raw_offset
from .storage import file_hash, read_jsonl, write_json, write_jsonl

QRELS_HASHES = {
    "qrels_group_confirmed_PAGES.csv": "d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb",
    "qrels_group_confirmed_PAGES.trec": "9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682",
}


def export_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def load_benchmark(root: Path) -> tuple[list[dict], list[dict], dict]:
    directory = root / "evaluation/benchmark"
    for name, digest in QRELS_HASHES.items():
        if file_hash(directory / name) != digest:
            raise ValueError("Confirmed judgment bytes changed")
    queries = read_jsonl(directory / "queries_145.jsonl")
    if len({q["question_id"] for q in queries}) != 145 or Counter(q["split"] for q in queries) != {"dev": 85, "validation": 30, "test": 30}:
        raise ValueError("Frozen query partition identity failed")
    evidence = read_jsonl(directory / "evidence_citations_145.jsonl")
    qrels = {}
    for line in (directory / "qrels_group_confirmed_PAGES.trec").read_text(encoding="utf-8").splitlines():
        qid, _, page, grade = line.split()
        if (qid, page) in qrels or qid not in {q["question_id"] for q in queries}:
            raise ValueError("Duplicate or orphan judgment")
        qrels[(qid, page)] = int(grade)
    if len(qrels) != 279 or Counter(qrels.values()) != {2: 188, 1: 91}:
        raise ValueError("Confirmed page judgments failed")
    if len({e["evidence_id"] for e in evidence}) != 296:
        raise ValueError("Duplicate evidence ID or incorrect count")
    if sum(e["candidate_status"] != "EXCLUDE_SCOPE" for e in evidence) != 294:
        raise ValueError("Expected exactly 294 retained source excerpts")
    return queries, evidence, qrels


def align_benchmark(root: Path, output: Path) -> dict:
    output = output.resolve()
    allowed = [(root / "reports/benchmark_alignment").resolve(), (root / "artifacts").resolve()]
    if not any(output == base or output.is_relative_to(base) for base in allowed):
        raise ValueError("Alignment output must stay in reports/benchmark_alignment or artifacts")
    queries, evidence, qrels = load_benchmark(root)
    processed = root / "data/processed"
    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "PASS":
        raise ValueError("Incomplete source extraction")
    for name, info in manifest["files"].items():
        if file_hash(processed / name) != info["sha256"]:
            raise ValueError(f"Changed corpus export: {name}")
    pages = {p["page_id"]: p for p in read_jsonl(processed / "pages.jsonl")}
    output.mkdir(parents=True, exist_ok=True)
    by_query = {q["question_id"]: q for q in queries}
    summary, all_records = {}, {}
    for size, info in manifest["chunks"].items():
        chunks_by_page = defaultdict(list)
        for chunk in read_jsonl(processed / info["file"]):
            chunks_by_page[chunk["page_id"]].append(chunk)
        records, proposals = [], []
        for item in evidence:
            if item["candidate_status"] == "EXCLUDE_SCOPE":
                continue
            qid, pid = item["question_id"], item["page_id"]
            if qid not in by_query or pid not in pages or (qid, pid) not in qrels:
                raise ValueError("Unknown evidence identity or missing confirmed page association")
            page = pages[pid]
            if page["document"] != item["document"] or page["page"] != item["page"]:
                raise ValueError("Incorrect evidence source metadata")
            found = locate_evidence(page["text"], item["evidence_text"])
            matches = []
            for span in found["spans"]:
                source_start = raw_offset(page["raw_offset_runs"], span["char_start"])
                source_end = raw_offset(page["raw_offset_runs"], span["char_end"] - 1) + 1
                overlap = chunk_overlaps(page, chunks_by_page[pid], span, found["normalized_length"])
                matches.append(dict(span, raw_char_start=source_start, raw_char_end=source_end, chunks=overlap))
            full = any(c["fully_contained"] for m in matches for c in m["chunks"])
            status = found["status"]
            if status in {"EXACT_MATCH", "NORMALIZED_MATCH"} and not full:
                status = "PARTIAL_MATCH"
            record = dict(question_id=qid, evidence_id=item["evidence_id"], page_id=pid,
                document_id=page["document_id"], source_pdf=page["source_pdf"],
                required_facts=item.get("required_facts", ""),
                required_facts_status="SOURCE_FACT_IDS_ONLY" if item.get("required_facts") else "NOT_SUPPLIED",
                split=by_query[qid]["split"], year=page["year"], document_type=page["doc_type"],
                corpus_version=manifest["corpus_version"], chunking_version=info["chunking_version"],
                page_match_status=found["status"], match_status=status, alignment_method=found["method"],
                matches=matches, fully_contained=full, needs_human_review=status in {"PARTIAL_MATCH", "AMBIGUOUS", "NOT_FOUND"},
                semantic_coverage_status="NOT_HUMAN_JUDGED", relevance_status="UNJUDGED_AT_CHUNK_LEVEL")
            records.append(record)
            for match_index, match in enumerate(matches):
                for hit in match["chunks"]:
                    proposals.append(dict(question_id=qid, evidence_id=item["evidence_id"], page_id=pid,
                        document_id=page["document_id"], source_pdf=page["source_pdf"],
                        required_facts=record["required_facts"], corpus_version=manifest["corpus_version"],
                        chunking_version=info["chunking_version"], match_alternative=match_index,
                        evidence_char_start=match["char_start"], evidence_char_end=match["char_end"],
                        raw_char_start=match["raw_char_start"], raw_char_end=match["raw_char_end"],
                        alignment_method=found["method"], page_match_status=found["status"],
                        match_status=status, needs_human_review=record["needs_human_review"],
                        proposal_status="AUTO_ALIGNMENT_NOT_RELEVANCE_JUDGMENT", review_status="UNJUDGED",
                        relevance_grade="", **hit))
        write_jsonl(output / f"evidence_alignment_{size}.jsonl", records)
        export_csv(output / f"alignment_report_{size}.csv", proposals)
        all_records[size] = records
        summary[size] = dict(evidence=len(records), page_match_status=dict(Counter(r["page_match_status"] for r in records)),
                             match_status=dict(Counter(r["match_status"] for r in records)),
                             fully_contained=sum(r["fully_contained"] for r in records),
                             split_across_chunks=sum(not r["fully_contained"] and r["page_match_status"] in {"EXACT_MATCH", "NORMALIZED_MATCH"} for r in records),
                             not_found=sum(r["page_match_status"] == "NOT_FOUND" for r in records),
                             ambiguous=sum(r["page_match_status"] == "AMBIGUOUS" for r in records))
        if size == "256":
            export_csv(output / "human_review_cases.csv", [dict(evidence_id=r["evidence_id"], question_id=r["question_id"], page_id=r["page_id"], reason=r["match_status"], human_decision="", notes="") for r in records if r["needs_human_review"]],
                       ["evidence_id", "question_id", "page_id", "reason", "human_decision", "notes"])
            unique = {(r["question_id"], r["chunk_id"]): r for r in proposals}
            export_csv(output / "alignment_candidates_UNJUDGED.csv", [dict(question_id=q, chunk_id=c, page_id=r["page_id"], status="UNJUDGED", relevance_grade="") for (q, c), r in sorted(unique.items())])
    for name in QRELS_HASHES:
        shutil.copyfile(root / "evaluation/benchmark" / name, output / name)
    write_json(output / "excluded_associations.json", [{"evidence_id": e["evidence_id"], "candidate_status": "EXCLUDE_SCOPE"} for e in evidence if e["candidate_status"] == "EXCLUDE_SCOPE"])
    baseline = all_records["256"]
    groups = []
    for keys in (("year",), ("document_type",), ("split",), ("question_id",)):
        collected = defaultdict(list)
        for row in baseline:
            collected[tuple(row[k] for k in keys)].append(row)
        for values, rows in sorted(collected.items()):
            groups.append(dict(group_by=keys[0], group_value=str(values[0]), evidence=len(rows), full_single_chunk=sum(r["fully_contained"] for r in rows), needs_review=sum(r["needs_human_review"] for r in rows)))
    export_csv(output / "coverage_by_group.csv", groups)
    write_json(output / "summary.json", {"corpus_version": manifest["corpus_version"], "configurations": summary,
        "qrels_sha256": QRELS_HASHES, "confirmed_page_judgments": 279, "new_chunk_judgments": 0,
        "python": sys.version.split()[0], "unicode_database": unicodedata.unidata_version,
        "alignment_version": ALIGNMENT_VERSION})
    inputs = {"data/processed/manifest.json": file_hash(processed / "manifest.json")}
    inputs.update({"evaluation/benchmark/" + name: file_hash(root / "evaluation/benchmark" / name) for name in
        ("queries_145.jsonl", "evidence_citations_145.jsonl", *QRELS_HASHES)})
    output_names = [name for size in manifest["chunks"] for name in (f"evidence_alignment_{size}.jsonl", f"alignment_report_{size}.csv")]
    output_names += [*QRELS_HASHES, "excluded_associations.json", "coverage_by_group.csv", "summary.json", "human_review_cases.csv", "alignment_candidates_UNJUDGED.csv"]
    write_json(output / "manifest.json", {"corpus_version": manifest["corpus_version"], "inputs_sha256": inputs,
        "code_sha256": {name: file_hash(Path(__file__).parent / name) for name in ("alignment.py", "benchmark.py")},
        "outputs_sha256": {name: file_hash(output / name) for name in sorted(output_names)}})
    return summary

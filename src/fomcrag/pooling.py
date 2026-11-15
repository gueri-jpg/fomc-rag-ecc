"""Future top-k union and strict import of actual human judgments; no retrieval."""
from __future__ import annotations

from .metrics import select_budget


def build_pool(runs: dict[str, list[dict]], chunks: dict[str, dict], page_judgments: dict[tuple[str, str], int],
               *, top_k: int = 20, unit: str = "chunk") -> list[dict]:
    if unit not in {"chunk", "page"}:
        raise ValueError("Pooling unit must be chunk or page")
    union = {}
    for method, queries in sorted(runs.items()):
        seen_queries = set()
        for query in queries:
            qid = query["question_id"]
            if qid in seen_queries:
                raise ValueError("Duplicate query within retriever run")
            seen_queries.add(qid)
            selected = select_budget(query["retrieved"], top_k, "chunk@k")
            for rank, hit in enumerate(selected["chunks"], 1):
                chunk = chunks.get(hit["chunk_id"])
                if not chunk or hit["page_id"] != chunk["page_id"]:
                    raise ValueError("Unknown chunk or incorrect page metadata")
                identity = chunk["chunk_id"] if unit == "chunk" else chunk["page_id"]
                key = (qid, identity)
                row = union.setdefault(key, dict(question_id=qid, candidate_id=identity, unit=unit,
                    page_id=chunk["page_id"], candidate_chunk_ids=[], returned_by=[],
                    page_judgment=page_judgments.get((qid, chunk["page_id"])),
                    review_status="UNJUDGED", relevance_grade="", notes=""))
                if chunk["chunk_id"] not in row["candidate_chunk_ids"]:
                    row["candidate_chunk_ids"].append(chunk["chunk_id"])
                row["returned_by"].append(dict(method=method, rank=rank))
                if unit == "page" and (qid, chunk["page_id"]) in page_judgments:
                    row["review_status"] = "EXISTING_PAGE_JUDGMENT"
                    row["relevance_grade"] = page_judgments[(qid, chunk["page_id"])]
    return [union[key] for key in sorted(union)]


def merge_human_judgments(existing: dict[tuple[str, str], int], rows: list[dict],
                          query_ids: set[str], page_ids: set[str]) -> dict[tuple[str, str], int]:
    merged = dict(existing)
    for row in rows:
        qid, page = row.get("question_id"), row.get("page_id")
        if qid not in query_ids or page not in page_ids or row.get("review_status") != "HUMAN_REVIEWED":
            raise ValueError("Unknown identity or missing explicit HUMAN_REVIEWED decision")
        raw = str(row.get("relevance_grade", ""))
        if raw not in {"0", "1", "2"}:
            raise ValueError("Human relevance grade must be 0, 1 or 2")
        grade, key = int(raw), (qid, page)
        if key in merged and merged[key] != grade:
            raise ValueError("Conflicting human decision; existing judgments preserved")
        merged[key] = grade
    return merged

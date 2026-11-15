"""Explicit budgets and diagnostics for incomplete page judgments."""
from __future__ import annotations

CONVENTIONS = ("chunk@k", "page-coverage-from-chunk@k", "unique-page@k")


def select_budget(results: list[dict], k: int, convention: str) -> dict:
    if type(k) is not int or k < 1 or convention not in CONVENTIONS:
        raise ValueError("Positive integer k and explicit supported convention required")
    chunks, pages, seen = [], [], set()
    for hit in results:
        if not hit.get("page_id") or not hit.get("chunk_id"):
            raise ValueError("Each ranked chunk must carry chunk_id and page_id")
        if any(c["chunk_id"] == hit["chunk_id"] for c in chunks):
            raise ValueError("Duplicate chunk_id in ranked results")
        chunks.append(hit)
        if hit["page_id"] not in seen:
            seen.add(hit["page_id"])
            pages.append(hit["page_id"])
        if convention == "unique-page@k" and len(pages) >= k:
            break
        if convention != "unique-page@k" and len(chunks) >= k:
            break
    return dict(convention=convention, k=k, chunks=chunks, pages=pages, consumed_chunks=len(chunks))


def known_page_diagnostics(results: list[dict], page_grades: dict[str, int], k: int, convention: str) -> dict:
    if convention == "chunk@k":
        raise ValueError("Page qrels cannot score chunk@k; explicit chunk judgments required")
    selected = select_budget(results, k, convention)
    positives = {page for page, grade in page_grades.items() if grade > 0}
    if not positives:
        raise ValueError("No known positives; coverage denominator undefined")
    hits = [page in positives for page in selected["pages"]]
    return {"convention": convention, "k": k, "consumed_chunks": selected["consumed_chunks"],
            "known_positive_coverage": sum(hits) / len(positives),
            "first_known_positive_page_rank": next((i for i, hit in enumerate(hits, 1) if hit), None),
            "unjudged_pages": sum(p not in page_grades for p in selected["pages"]),
            "judgments_exhaustive": False}

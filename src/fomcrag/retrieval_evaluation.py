"""Page diagnostics for ranked chunks and incomplete positive judgments."""
from __future__ import annotations
import math

from .metrics import select_budget


def page_diagnostics(ranked: list[dict], grades: dict[str, int], k: int, convention: str) -> dict:
    if convention == "chunk@k":
        raise ValueError("Page labels cannot score chunk@k")
    selected = select_budget(ranked, k, convention)
    pages = selected["pages"]
    positives = {p for p, grade in grades.items() if grade > 0}
    if not positives:
        raise ValueError("No known positive denominator")
    hits = [i for i, page in enumerate(pages, 1) if page in positives]
    first = hits[0] if hits else None
    dcg = sum((2 ** grades.get(page, 0) - 1) / math.log2(i + 2) for i, page in enumerate(pages))
    ideal = sorted([v for v in grades.values() if v > 0], reverse=True)[:k]
    idcg = sum((2 ** grade - 1) / math.log2(i + 2) for i, grade in enumerate(ideal))
    unjudged = sum(page not in grades for page in pages)
    return dict(known_positive_coverage=len(hits) / len(positives), known_positive_hit=int(bool(hits)),
        first_known_positive_page_rank=first, known_positive_page_rr=1 / first if first else 0.,
        seed_ndcg=dcg / idcg if idcg else 0., unjudged_pages=unjudged,
        unjudged_fraction=unjudged / len(pages) if pages else 0., unique_pages=len(pages),
        unique_documents=len({p.rsplit("#p", 1)[0] for p in pages}), consumed_chunks=selected["consumed_chunks"])


def objective(rows: list[dict]) -> tuple[float, float, float]:
    if not rows:
        raise ValueError("Empty tuning diagnostics")
    return tuple(sum(float(r[key]) for r in rows) / len(rows) for key in
                 ("known_positive_coverage", "known_positive_hit", "known_positive_page_rr"))


def choose_configuration(candidates: list[dict]) -> dict:
    """Predeclared lexicographic criterion; stable order breaks 1e-12 ties."""
    if not candidates:
        raise ValueError("No candidate configurations")
    chosen = candidates[0]
    for candidate in candidates[1:]:
        for a, b in zip(candidate["objective"], chosen["objective"]):
            if a > b + 1e-12:
                chosen = candidate
                break
            if a < b - 1e-12:
                break
    return chosen

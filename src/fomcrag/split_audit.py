"""Explainable pairwise leakage screening, never tuning or changing splits."""
from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from itertools import combinations
import re

from .alignment import search_view


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a or b else 0.0


def audit_splits(queries: list[dict], evidence: list[dict], config: dict) -> list[dict]:
    """All pairs scored; thresholds are predeclared diagnostic alert rules.

    Shared source evidence is a stronger *screening* signal than shared words,
    not a semantic equivalence certificate. No split changes are performed.
    """
    by_query = {}
    for query in queries:
        qid = query["question_id"]
        source = [search_view(e["evidence_text"]).text for e in evidence
                  if e["question_id"] == qid and e["candidate_status"] != "EXCLUDE_SCOPE"]
        by_query[qid] = {text[i:i + 40] for text in source for i in range(0, max(0, len(text) - 39), 10)}
    rows = []
    for a, b in combinations(queries, 2):
        lexical = jaccard(words(a["question"]), words(b["question"]))
        sequence = SequenceMatcher(None, a["question"].casefold(), b["question"].casefold(), autojunk=False).ratio()
        evidence_similarity = jaccard(by_query[a["question_id"]], by_query[b["question_id"]])
        exact = search_view(a["question"]).text == search_view(b["question"]).text
        alert = exact or lexical >= config["question_token_jaccard_alert"] or sequence >= config["question_sequence_ratio_alert"] or evidence_similarity >= config["evidence_shingle_jaccard_alert"]
        rows.append(dict(question_a=a["question_id"], split_a=a["split"], question_b=b["question_id"], split_b=b["split"],
            cross_split=a["split"] != b["split"], exact_normalized=exact,
            token_jaccard=round(lexical, 6), sequence_ratio=round(sequence, 6), evidence_shingle_jaccard=round(evidence_similarity, 6),
            alert=alert, proposed_action="HUMAN_REVIEW_BEFORE_TUNING" if alert and a["split"] != b["split"] else "NO_AUTOMATIC_CHANGE"))
    return rows


def audit_paraphrases(queries: list[dict], variants: list[dict]) -> list[dict]:
    parents = {q["question_id"]: q for q in queries if q["split"] == "test"}
    if len(variants) != 30 or Counter(v["parent_question_id"] for v in variants) != Counter({q: 1 for q in parents}):
        raise ValueError("Exactly one paraphrase for each test parent required")
    if len({v["question_id"] for v in variants}) != 30 or any(v["split"] != "test" for v in variants):
        raise ValueError("Invalid paraphrase IDs or split")
    rows = []
    for variant in variants:
        parent = parents[variant["parent_question_id"]]
        # Date/numeric discrepancies are alerts, never proof of equivalence.
        numbers = lambda text: set(re.findall(r"\d+(?:[./-]\d+)*", text))
        mismatched = numbers(parent["question"]) != numbers(variant["question"])
        rows.append(dict(question_id=variant["question_id"], parent_question_id=parent["question_id"], split="test",
                         number_tokens_differ=mismatched,
                         token_jaccard=round(jaccard(words(parent["question"]), words(variant["question"])), 6),
                         semantic_status="NEEDS_HUMAN_REVIEW", active_for_tuning=False))
    return rows

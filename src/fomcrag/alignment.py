"""Evidence localization only. Never generates relevance judgments."""
from __future__ import annotations

from dataclasses import dataclass
import unicodedata

ALIGNMENT_VERSION = "nfkc-casefold-ascii-alnum-mapped-v1"


@dataclass(frozen=True)
class SearchView:
    text: str
    origins: tuple[int, ...]

    def project(self, start: int, end: int) -> tuple[int, int]:
        if not 0 <= start < end <= len(self.text):
            raise ValueError("Invalid normalized span")
        return self.origins[start], self.origins[end - 1] + 1


def search_view(text: str) -> SearchView:
    """Characterwise NFKC/casefold; ASCII letters/digits only.

    A permissive *localization* view reproducing the independent audit method.
    Fractions, signs and punctuation may collide: never use as a relevance or
    numerical-equivalence check. Every expansion maps back to its source char.
    """
    chars, origins = [], []
    for index, char in enumerate(text):
        for normalized in unicodedata.normalize("NFKC", char).casefold():
            if "a" <= normalized <= "z" or "0" <= normalized <= "9":
                chars.append(normalized)
                origins.append(index)
    return SearchView("".join(chars), tuple(origins))


def occurrences(haystack: str, needle: str) -> list[tuple[int, int]]:
    if not needle:
        return []
    spans, offset = [], 0
    while (start := haystack.find(needle, offset)) >= 0:
        spans.append((start, start + len(needle)))
        offset = start + 1
    return spans


def locate_evidence(text: str, evidence: str) -> dict:
    """Return all full match alternatives with true page-character offsets.

    PARTIAL_MATCH is reserved for exact contiguous fragments ≥32 normalized
    chars (not bags of common words). Such fragments require human review.
    """
    exact = occurrences(text, evidence)
    normalized = search_view(evidence).text
    if not normalized:
        return dict(status="NOT_FOUND", method=ALIGNMENT_VERSION, spans=[], normalized_length=0)
    view = search_view(text)
    hits = occurrences(view.text, normalized)
    spans = [dict(normalized_start=s, normalized_end=e, char_start=view.project(s, e)[0],
                  char_end=view.project(s, e)[1]) for s, e in hits]
    status = "AMBIGUOUS" if len(hits) > 1 else "EXACT_MATCH" if exact and hits else "NORMALIZED_MATCH" if hits else "NOT_FOUND"
    if not hits:
        from difflib import SequenceMatcher
        match = SequenceMatcher(None, normalized, view.text, autojunk=False).find_longest_match()
        if match.size >= 32:
            s, e = view.project(match.b, match.b + match.size)
            spans = [dict(normalized_start=match.b, normalized_end=match.b + match.size,
                          char_start=s, char_end=e, evidence_normalized_start=match.a,
                          evidence_normalized_end=match.a + match.size)]
            status = "PARTIAL_MATCH"
    return dict(status=status, method="literal" if status == "EXACT_MATCH" else ALIGNMENT_VERSION,
                spans=spans, normalized_length=len(normalized))


def chunk_overlaps(page: dict, chunks: list[dict], span: dict, evidence_length: int) -> list[dict]:
    view = search_view(page["text"])
    # Count matched normalized characters located within each true chunk span.
    origins = view.origins[span["normalized_start"]:span["normalized_end"]]
    rows = []
    for chunk in chunks:
        if chunk["page_id"] != page["page_id"]:
            raise ValueError("Cannot mix source pages during alignment")
        matched = sum(chunk["char_start"] <= origin < chunk["char_end"] for origin in origins)
        if not matched:
            continue
        full = matched == evidence_length
        rows.append(dict(chunk_id=chunk["chunk_id"], chunk_char_start=chunk["char_start"],
                         chunk_char_end=chunk["char_end"], overlap_char_start=max(span["char_start"], chunk["char_start"]),
                         overlap_char_end=min(span["char_end"], chunk["char_end"]),
                         matched_normalized_chars=matched, normalized_evidence_chars=evidence_length,
                         text_coverage=matched / evidence_length, fully_contained=full))
    return rows

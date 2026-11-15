"""Conservative, reversible-by-provenance text views; no learned transforms."""
from __future__ import annotations

import re
from dataclasses import dataclass

NORMALIZATION_VERSION = "whitespace-soft-hyphen-v1"
LEXICAL_VERSION = "unicode-casefold-numbers-negation-v1"
WORD = re.compile(r"\S+")
# Keep decimals, percentages, dates, hyphenated compounds and contractions.
LEXICAL = re.compile(r"[+\-−]?\d+(?:[.,/\-]\d+)*(?:[¼½¾⅛⅜⅝⅞])?(?:%)?|[¼½¾⅛⅜⅝⅞]|[^\W\d_]+(?:['’\-][^\W\d_]+)*|%", re.UNICODE)
HYPHEN_BREAK = re.compile(r"(?<=[^\W\d_])-[ \t]*\r?\n[ \t]*(?=[^\W\d_])", re.UNICODE)


@dataclass(frozen=True)
class NormalizedText:
    text: str
    origins: tuple[int, ...]
    edits: tuple[dict, ...]


def normalize_text(raw: str, hyphen_policy: str = "preserve") -> NormalizedText:
    """Offsets are Python Unicode character offsets, not byte/PDF coordinates.

    Visible end-of-line hyphens are retained by default (compound ambiguity).
    'join' is an explicit alternative, not a dictionary-based correction.
    Every resulting character maps to its raw source offset.
    """
    if hyphen_policy not in {"preserve", "join"}:
        raise ValueError("hyphen_policy must be preserve or join")
    skip: set[int] = set()
    edits: list[dict] = []
    for match in re.finditer(r"\u00ad[ \t]*\r?\n[ \t]*", raw):
        skip.update(range(match.start(), match.end()))
        edits.append({"raw_start": match.start(), "raw_end": match.end(), "kind": "soft_line_hyphen_removed"})
    for match in HYPHEN_BREAK.finditer(raw):
        start = match.start() if hyphen_policy == "join" else match.start() + 1
        skip.update(range(start, match.end()))
        edits.append({"raw_start": match.start(), "raw_end": match.end(), "kind": "line_hyphen_" + hyphen_policy})
    chars: list[str] = []
    origins: list[int] = []
    for i, char in enumerate(raw):
        if i in skip:
            continue
        if char == "\u00ad":
            edits.append({"raw_start": i, "raw_end": i + 1, "kind": "soft_hyphen_removed"})
            continue
        if char.isspace():
            if chars and chars[-1] != " ":
                chars.append(" ")
                origins.append(i)
        elif ord(char) < 32 and char not in "\n\r\t":
            # Keep suspicious glyphs visible rather than silently dropping text.
            chars.append("\ufffd")
            origins.append(i)
            edits.append({"raw_start": i, "raw_end": i + 1, "kind": "control_replacement"})
        else:
            chars.append(char)
            origins.append(i)
    if chars and chars[-1] == " ":
        chars.pop()
        origins.pop()
    return NormalizedText("".join(chars), tuple(origins), tuple(edits))


def compact_origins(origins: tuple[int, ...]) -> list[dict]:
    """Run-length encode linear clean→raw offsets, including deletion jumps."""
    runs: list[dict] = []
    for clean, raw in enumerate(origins):
        if runs and runs[-1]["raw_start"] + clean - runs[-1]["clean_start"] == raw:
            runs[-1]["clean_end"] = clean + 1
        else:
            runs.append({"clean_start": clean, "clean_end": clean + 1, "raw_start": raw})
    return runs


def raw_offset(runs: list[dict], offset: int) -> int:
    for run in runs:
        if run["clean_start"] <= offset < run["clean_end"]:
            return run["raw_start"] + offset - run["clean_start"]
    raise ValueError("Offset outside normalized text")


def lexical_tokens(text: str) -> list[str]:
    """No stopword removal, lemmatization, stemming or numeric deletion."""
    return LEXICAL.findall(text.casefold())

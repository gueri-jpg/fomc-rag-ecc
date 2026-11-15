"""Unsupervised diagnostics and a future lexical-only ablation candidate."""
import re

from .preprocessing import lexical_tokens

BREAK = re.compile(r"([^\W\d_]+)-[ \t]*\r?\n[ \t]*([^\W\d_]+)", re.UNICODE)
PROTECTED = {"market-based", "labor-market", "longer-term", "short-term", "supply-side", "interest-rate", "non-housing", "year-over-year"}


def lexical_ablation_candidate(raw_text: str) -> list[str]:
    """Proposed only: join documented line-break hyphens, protect compounds.

    Does not mutate the page or its natural text; this is not a tuned method.
    Ambiguous/non-whitelisted compounds can still be harmed, a tested limitation.
    """
    def replace(match):
        compound = match[1] + "-" + match[2]
        return compound if compound.casefold() in PROTECTED else match[1] + match[2]
    return lexical_tokens(BREAK.sub(replace, raw_text))

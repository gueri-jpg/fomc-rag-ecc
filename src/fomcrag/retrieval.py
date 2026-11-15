"""Label-free deterministic BM25 and rank fusion. No benchmark imports or I/O."""
from collections import Counter, defaultdict
import math

from .preprocessing import lexical_tokens


def stable_ranking(scores, chunk_ids: list[str]) -> list[int]:
    if len(scores) != len(chunk_ids) or len(set(chunk_ids)) != len(chunk_ids):
        raise ValueError("Unique chunk identities and aligned scores required")
    if any(not math.isfinite(float(s)) for s in scores):
        raise ValueError("Non-finite retrieval score")
    return sorted(range(len(scores)), key=lambda i: (-float(scores[i]), chunk_ids[i]))


class BM25Index:
    """BM25 with positive Lucene-style Robertson IDF; repeated query terms count."""
    def __init__(self, tokenized: list[list[str]], chunk_ids: list[str], k1: float = 1.5, b: float = .75):
        if not tokenized or len(tokenized) != len(chunk_ids) or k1 <= 0 or not 0 <= b <= 1:
            raise ValueError("Invalid BM25 corpus or parameters")
        if len(set(chunk_ids)) != len(chunk_ids):
            raise ValueError("Duplicate chunk IDs")
        self.chunk_ids, self.k1, self.b = list(chunk_ids), k1, b
        self.lengths = [len(tokens) for tokens in tokenized]
        self.average_length = sum(self.lengths) / len(self.lengths) or 1.
        self.postings = defaultdict(list)
        for i, tokens in enumerate(tokenized):
            for term, frequency in Counter(tokens).items():
                self.postings[term].append((i, frequency))

    def scores(self, query: str) -> list[float]:
        if not isinstance(query, str):
            raise TypeError("Retriever accepts query text only, never label-bearing records")
        scores = [0.] * len(self.chunk_ids)
        for term, qtf in Counter(lexical_tokens(query)).items():
            postings = self.postings.get(term, [])
            if not postings:
                continue
            idf = math.log1p((len(scores) - len(postings) + .5) / (len(postings) + .5))
            for index, tf in postings:
                norm = self.k1 * (1 - self.b + self.b * self.lengths[index] / self.average_length)
                scores[index] += qtf * idf * tf * (self.k1 + 1) / (tf + norm)
        return scores


def reciprocal_rank_fusion(rankings: dict[str, list[str]], *, rrf_k: int = 60, depth: int = 100) -> tuple[dict[str, float], dict]:
    if type(rrf_k) is not int or rrf_k < 1 or type(depth) is not int or depth < 1:
        raise ValueError("Positive integer RRF constant/depth required")
    scores, contributions = defaultdict(float), defaultdict(dict)
    for method, ranked in sorted(rankings.items()):
        if len(set(ranked)) != len(ranked):
            raise ValueError("Duplicate IDs in source ranking")
        for rank, chunk_id in enumerate(ranked[:depth], 1):
            value = 1 / (rrf_k + rank)
            scores[chunk_id] += value
            contributions[chunk_id][method] = {"rank": rank, "contribution": value}
    return dict(scores), dict(contributions)

# Phase 3 — preregistered retrieval protocol

Written before the first real dev retrieval run. Settings are in
configs/retrieval_phase3.json; phase-2 tuning policy remains unchanged.
The baseline is exactly 2,127 chunks, 256 words/40 overlap, 93 PDFs, 838 pages.
PDF/export hashes and source identities are checked before indexing. No date,
year or document-type filter exists. The optional 128/512 exports are not part
of this primary comparison.

## Partition protection

Dev has exactly 83 eligible IDs, excluding FOMC_044 and FOMC_129. Validation
has 30 IDs. require_tuning_eligible now compares selected IDs to the actual
frozen split rather than merely checking cardinality. Phase-3 CLI accepts only
dev and validation. Test/all/paraphrases/embargo diagnostics are refused even
if a future freeze file exists. The generic historical page evaluator also
requires a human-validated authorization artifact before any test/all use.
The phase-3 dev-selection artifact is **not** this authorization: it explicitly
sets human_validated=false and test_authorized=false. No test inference or
retrieval diagnostic is produced in this phase.

## BM25

Use existing bm25_tokens and lexical_tokens(query) (casefold, numbers,
negations, dates and fractions retained; no learned transformation).
For N chunks, document frequency df(t), chunk length dl and mean avgdl:

`IDF(t) = ln(1 + (N - df(t) + 0.5)/(df(t) + 0.5))`

`score(q,d) = sum_t qtf(t) IDF(t) tf(t,d)(k1+1) /
             (tf(t,d) + k1(1-b+b dl/avgdl))`.

This is positive smoothed Robertson/Lucene-style IDF, not rank-bm25's alternate
negative-IDF floor. Repeated query terms count with multiplicity. Unknown terms
contribute zero. Ties sort by lexicographic chunk_id, not source year or labels.
Defaults k1=1.5,b=0.75. Predeclared grid in order: (1.5,.75), (1.2,.75), (1.5,.5).
The pure-Python inverted postings implementation avoids an extra dependency.
Local token caches validate corpus, variant, token content and code hashes;
postings are rebuilt deterministically and construction time measured.

## Dense

Official model: https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2.
Download only that checkpoint, record exact Hub commit and every file hash,
and load it locally with trust_remote_code=false. No fine-tuning or API inference.
CPU float32, seed 20261115, four Torch threads, batch size 16, unit-normalized
384-dimensional embeddings, similarity by dot product (=cosine). Full exact
matrix search, no approximate index or FAISS. Query encoder receives only text.
Weights, document matrix and caches stay ignored in models/ and artifacts/.

The model's saved max_seq_length is retained, not silently enlarged. Measure
untruncated token lengths with special tokens for every source chunk and query;
record input/used/discarded tokens and truncation flags. Thus a 256-word chunk
may be only partly represented by Dense. No claim of full encoding if truncated.
Document matrix keys include exact texts, ordered IDs, model revision/hashes,
software versions, code, normalization and seed; arrays are SHA-checked and
loaded with allow_pickle=false. Validate dimensions, finite values and norms.
Fresh single-query inference is timed without query cache; repeated same-query
inference checks deterministic rankings.

## Hybrid RRF and fair selection

Take the same top-100 depth from BM25 L0 and Dense, then sum
`1/(rrf_k + rank)` for each candidate; absent candidates contribute zero.
The union has at most 200 chunks, all from the same 2,127-item universe.
Unseen items have zero score in full ranking exports. Retain source ranks and
individual contributions. Tie rule is the same chunk_id rule. No reranker.
RRF constants in predeclared order: 60,10,30,100.

Selection on 83 dev only: lexicographically maximize mean strict
page-coverage-from-chunk@5 known_positive_coverage, then known-positive hit,
then first-known-positive reciprocal page rank. Differences ≤1e-12 tie and
prefer the first declared configuration. Select BM25 L0 parameters, then RRF
constant against the same Dense ranks. Report all grid results. Recommend a
phase-4 candidate-source method using this dev criterion, **not** validation.
Persist bound dev selection before validation; reject changed policy, corpus,
model/environment or settings. One validation pass, no iterative adjustment.

L1 is a separate BM25 ablation, with the selected L0 k1/b, same chunks and
queries, same query tokens. Only raw line-break hyphens within each chunk's
true raw span are joined, with the phase-2 fixed compound protections. No
source text/IDs/embeddings changed. The primary Hybrid always uses L0.
Choose any L1 recommendation on dev; evaluate both once on validation.

## Diagnostics, exports and timing

Budgets 1,3,5,10,20. Primary: pages represented in strictly the first k chunks;
secondary: first k unique pages with consumed chunk count. No chunk-level
relevance metrics from page qrels. Known-positive coverage/hit/page rank and
conditional seed-nDCG are qualified as incomplete-judgment diagnostics;
UNJUDGED is never a negative annotation. Include unjudged proportions,
page/document diversity and source year/type distributions.

All complete score/rank matrices and query/chunk identities are stored locally
as NPZ. Local top-100 JSONL includes text, rank, raw score, source metadata,
latency and index configuration. Public reports contain aggregates/IDs/offsets,
not large text/ranking copies. Pool the real three-method top-20 union over
authorized dev+validation; prioritize high-rank unjudged pages and cross-year
sources for review, without assigning grades or repeating accepted judgments.

Report index construction, model load, document encoding/cache size, p50/p95
fresh and repeated retrieval. "First call" is not cold process start for every
query: the model is already loaded and earlier queries may warm kernels. Hybrid
latency is the **serial sum of measured source retrieval and fusion components**,
not a separately measured parallel service latency. Persistence time is outside
per-query retrieval timings. Disclose these conditions. Use paired bootstrap
over query needs for differences, descriptively; confidence intervals cannot
correct missing qrels and validation n=30 has substantial uncertainty.

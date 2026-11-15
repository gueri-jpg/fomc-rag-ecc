# Architecture cible locale — fichiers, pas Docker/infra imposée

## Ébauche de structure attendue après implémentation (NON incluse comme code fini)

```text
src/fomcrag/
  corpus.py         # manifest + PyMuPDF page-level extract
  chunking.py       # deterministic, provenance-preserving
  eda.py            # verified corpus statistics
  indexing.py       # BM25 + Dense embedding persistent cache
  retrieval.py      # BM25/Dense/Hybrid RRF interfaces
  reranking.py      # None, MiniLM CrossEncoder, optional BGE
  benchmark.py      # queries, group qrels, pool, fact coverage
  metrics.py        # known_positive metrics & explicit judged metrics
  generation.py     # grounded LLM or clearly marked extractive baseline
  pipeline.py       # orchestration, logging, latency
app/streamlit_app.py
scripts/ingest.py scripts/eda.py scripts/retrieve.py
scripts/evaluate.py scripts/rerank.py scripts/build_pool.py
scripts/run_demo_smoke.py
configs/ experiments/ reports/ docs/ tests/
```

Current legacy scripts stay under `utils/`. PostgreSQL/pgvector is **optional**; prefer self-contained deterministic files such as JSONL/NumPy/FAISS as compatible with the available PC. No mandatory FastAPI or Docker.

## Canonical page record
```json
{"document":"fomcminutes20210127.pdf","doc_type":"minutes","meeting_date":"2021-01-27","year":2021,"page":1,"page_id":"fomcminutes20210127.pdf#p1","text":"<source readable text>","pdf_sha256":"<hash>"}
```

## Canonical chunk record
```json
{"chunk_id":"<stable hash>","document":"fomcminutes20210127.pdf","page":1,"page_id":"fomcminutes20210127.pdf#p1","year":2021,"doc_type":"minutes","meeting_date":"2021-01-27","char_start":0,"char_end":512,"text":"<raw source passage>","chunking_version":"words256_overlap40_v1"}
```
A `chunk_id` is a deterministic ID of `(PDF_hash, page, start/end, chunking config)`, not arbitrary numbering. No chunk may cross a document boundary; baseline preferably no page-crossing. Keep PDF physical pages 1-indexed for references.

## Retrieval run record
```json
{"question_id":"FOMC_001","method":"BM25","retrieved":[{"rank":1,"chunk_id":"<id>","page_id":"<document>#p<page>","score":1.0,"document":"<filename>","page":1,"text":"<passage>"}],"retrieval_ms":10.0,"config_id":"<hash>"}
```
Values are illustrative schemas, **not experimental findings**. Ranks are 1-indexed, ordered, no duplicate chunk IDs. Save top20 per method for pooling. If evaluating pages: collapse duplicate page IDs in ranking, preserving first hit and documented k.

## Rerank run record
Persist original `candidate_chunk_ids`, model name/version, `reranked_chunk_ids`, retrieval_ms, reranking_ms, feature flags, configuration hash. Assert same original candidate set before comparing rerankers and retain a no-rerank baseline.

## Answer record
Persist `question_id`, `answer`, `citations` with actual `(document,page,chunk_id)`, model/backend/version, `status: answered|abstained|error`, total_ms. Do not fabricate citations; verify chunks support sentence before displaying.

## Demo Streamlit acceptance
Run `streamlit run app/streamlit_app.py` locally and browse the UI. Show question field, method selection, optional rerank, retrieved source passages, clear type/date/page, evidence snippets, latency, generator mode and cited answer/abstention. Also show **measured** comparison table/plots from persisted experiment outputs, never fake bar charts. App should run CPU where feasible with explicit model download instructions and graceful missing-weight errors. No deployment account necessary.

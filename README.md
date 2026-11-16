# FOMC RAG: A Reproducible Benchmark for Retrieval and Reranking

Academic Machine Learning project, subject 5, École Centrale Casablanca.
The objective is to compare retrieval and reranking strategies for grounded
question answering over FOMC Minutes and Statements.

**Branch update: phases 0–3.** Corpus processing, benchmark alignment and
BM25 / Dense MiniLM / Hybrid RRF retrieval are implemented and executed on
83 eligible development questions and 30 validation questions. Test retrieval
remains disabled. Reranking, generation and Streamlit await later phases.
See [phase-3 measured results and limitations](reports/progress/PHASE_3.md).

## Corpus and measured outputs

| Item | Current snapshot |
|---|---|
| Corpus | 93 FOMC PDFs, 838 physical pages, 2021–2026 |
| Types | 46 Minutes and 47 Statements |
| Baseline | 2,127 chunks, up to 256 words, overlap 40 |
| Alternatives | 128 words: 4,563 chunks; 512 words: 1,124 chunks |
| Questions | 145: 85 development / 30 validation / 30 test |
| Effective tuning dev | 83, excluding FOMC_044 and FOMC_129; original partitions unchanged |
| Group-confirmed judgments | 279 question–page pairs: 188 grade 2, 91 grade 1 |
| Test paraphrases | 30, reserved for frozen configurations |
| Unanswerable candidates | 10, disabled pending human validation |
| Phase-1 checks | 22 tests passed; extraction and EDA reproduction verified |
| Phase-2 alignment | All 294 retained excerpts located; 287 fully within baseline chunks, seven split |
| Post-audit tests | 47 full / 29 corpus-independent tests passed locally |
| Phase-3 tests | 80 full local / 57 corpus-independent tests passed |
| Retrieval recommendation | BM25 L0, k1=1.2, b=0.75, selected on dev only |
| Dense limitation | Locked checkpoint max_seq_length=128; 1,955/2,127 chunks truncated |

PDFs, extracted corpus, model weights, private course materials and page
screenshots stay local. Source metadata, benchmark files, descriptive tables
and generated charts are included. See [data restoration](docs/data_sources.md).

## Architecture and layout

Each PDF is validated by SHA256 and physical page count, then extracted per page.
Raw and readable text, source metadata and offsets are retained. Page-bounded
windows export readable passages and separate lexical tokens; no labels or
reference answers are loaded when constructing the corpus.

```text
src/fomcrag/             extraction, preprocessing, chunking, storage, EDA
scripts/                ingestion, EDA, integrity and security commands
tests/                  offline unit and corpus integration tests
configs/                corpus settings and experimental protocol
evaluation/benchmark/   questions, source manifest, judgments, legacy tools
docs/                   architecture, preprocessing, data and risk notes
reports/eda/            measured CSV/JSON outputs and observations
reports/figures/        generated EDA charts
reports/progress/       phase and publication reports
utils/                  historical prototype, not the active pipeline
app/                    documentation for the future local application
data/processed/         generated corpus and chunks (local only)
```

Historical scripts in `utils/` and benchmark helpers are preserved for
traceability. Some have import-time database/model side effects; do not use them
as the active pipeline or treat their presence as validated retrieval.

## Installation

Validated environment: **Python 3.13.14, Windows x64**. Python 3.12 is not used.
No database, Docker or cloud account is required. Corpus processing and the
lightweight tests need no model download; Dense phase 3 downloads its official
checkpoint once and then runs locally.

For a fresh clone only, create a Python 3.13 virtual environment. Skip creation
if the project's `.venv` already exists.

```powershell
git clone https://github.com/gueri-jpg/fomc-rag-ecc.git
cd fomc-rag-ecc
py -3.13 -m venv .venv
& .venv\Scripts\python.exe -m pip install -r requirements-phase1.lock.txt
& .venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
```

PyMuPDF, NumPy and matplotlib cover phase 1; pytest supplies tests.
The lock records the phase-1 environment. The separate phase-3 lock pins the
tested CPU retrieval environment; application dependencies are for a later phase.

## Reproduce extraction and EDA

Restore the exact 93 PDFs at the relative paths in
[docs/data_sources.md](docs/data_sources.md). A fresh clone does not contain them;
full corpus tests require restored PDFs and regenerated outputs.

```powershell
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
& .venv\Scripts\python.exe scripts/verify_kit_v2.py
& .venv\Scripts\python.exe scripts/ingest.py
& .venv\Scripts\python.exe scripts/eda.py
& .venv\Scripts\python.exe scripts/render_source_checks.py
& .venv\Scripts\python.exe scripts/verify_phase1.py --rebuild --eda-rebuild
```

Phase-2 diagnostics, using the frozen phase-1 outputs:

```powershell
& .venv\Scripts\python.exe scripts/align_benchmark.py
& .venv\Scripts\python.exe scripts/audit_benchmark_splits.py
& .venv\Scripts\python.exe scripts/diagnose_priority_evidence.py
& .venv\Scripts\python.exe scripts/audit_hyphens.py
& .venv\Scripts\python.exe scripts/verify_phase2.py --rebuild
```

See [alignment and evaluation conventions](docs/benchmark_alignment.md) and
[cross-split decisions needed before tuning](reports/benchmark_alignment/SPLIT_AUDIT.md).
Aligned chunks remain unjudged: localization is not a new relevance annotation.

Settings: [configs/corpus_phase1.json](configs/corpus_phase1.json). Generated
corpus and structural page-to-chunk maps go to `data/processed/`; the common
baseline for future retrievers is `chunks_256.jsonl`. Rendering creates ignored
local screenshots. No relevance grades are assigned to chunks.

- [EDA observations](reports/eda/OBSERVATIONS.md)
- [Phase-1 report](reports/progress/PHASE_1.md)
- [Year/type chart](reports/figures/phase1_year_type.png)
- [Chunk distributions](reports/figures/phase1_chunks.png)
- [Preprocessing and provenance](docs/corpus_preprocessing.md)

## Tests and security

After reconstructing corpus outputs:

```powershell
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m pip check
& .venv\Scripts\python.exe evaluation/benchmark/validate_benchmark.py
& .venv\Scripts\python.exe scripts/audit_security.py
```

Without PDFs, run the six phase-0 checks with
`.venv\Scripts\python.exe -m pytest -q tests/test_phase0.py`.
The full suite covers extraction, metadata, offsets, word coverage, overlap,
stable IDs, preserved judgments and EDA integrity. Before publication, run
`scripts/audit_security.py --staged` with the same interpreter.
Security scans are heuristic, not a guarantee.

The offline path test checks resolution only; it never requires a PDF directory.
Integration tests explicitly validate all 93 physical PDFs and their hashes.
To reproduce the public-clone condition locally, without moving your PDFs, run
`.venv\Scripts\python.exe scripts/check_offline.py`. GitHub Actions runs the
six phase-0 and 37 phase-2 unit checks on Python 3.13, without PDFs or models.
Run all 43 offline checks with:

```powershell
& .venv\Scripts\python.exe -m pytest -q tests/test_phase0.py tests/test_benchmark_phase2.py
& .venv\Scripts\python.exe scripts/check_offline.py --tests tests/test_phase0.py tests/test_benchmark_phase2.py
```

## Evaluation methodology and limits

Future BM25, MiniLM Dense and Hybrid RRF systems must share corpus/chunks/top-k,
without automatic year filtering. Cross-Encoder rerankers will receive identical
top-20 candidates. Tuning uses 83 dev questions (FOMC_044/FOMC_129 embargoed)
and the unchanged 30 validation questions, through configs/tuning_policy.json.
Full diagnostics retain all original questions but are ineligible for parameter
selection; inspect them only after freeze or with an independent analyst. Test
and paired paraphrases remain reserved until configuration freeze.

The 279 page judgments are accepted according to the group's reported double
annotation. Individual annotation sheets were not supplied; no measured
inter-annotator agreement is claimed. Judgments are **not exhaustive**:
unjudged items are not negatives and a positive page does not make all its
chunks positive. Metrics must disclose judgment coverage and evaluated unit.
See the [protocol](project_spec/PROTOCOLE_EXPERIMENTAL.md) and
[qrels status](project_spec/VALIDATION_BENCHMARK_ET_QRELS.md).

Current limits: partial 2026 coverage, repeated policy language, retained
line-end hyphens, short covers, private-use glyphs and PDF footnotes interrupting
reading order. Word windows are not neural-token budgets. EDA is not a measure
of retrieval quality. Official URLs may be unavailable or serve different
bytes; source hashes must not be silently replaced.

## Reproduce retrieval (phase 3)

After restoring the PDFs and regenerating phase-1 exports, use the existing
Python 3.13 environment. These inference commands assume a fresh experiment
directory; a completed validation deliberately blocks further tuning/replays.

```powershell
& .venv\Scripts\python.exe -m pip install -r requirements-phase3.lock.txt
& .venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
& .venv\Scripts\python.exe scripts/download_minilm.py
& .venv\Scripts\python.exe scripts/run_retrieval_phase3.py --stage dev
& .venv\Scripts\python.exe scripts/run_retrieval_phase3.py --stage validation
& .venv\Scripts\python.exe scripts/report_retrieval_phase3.py
& .venv\Scripts\python.exe -m pytest -q
```

On an already completed experiment, rerun only `report_retrieval_phase3.py`
to regenerate tables/figures/pools without inference. Full rankings and texts
stay local under `artifacts/phase3/`; lightweight results and the prioritized
UNJUDGED review queue are in [reports/retrieval_phase3](reports/retrieval_phase3/).
Known-positive coverage is conditional on incomplete page judgments, not gold
recall. BM25/Dense/Hybrid validation coverage at five chunks is respectively
35.56% / 10.56% / 27.78%. No test experiment has been run.

Public-clone tests require neither PDFs nor model downloads:

```powershell
& .venv\Scripts\python.exe -m pytest -q tests/test_phase0.py tests/test_benchmark_phase2.py tests/test_retrieval_phase3.py
```

See [retrieval protocol](docs/retrieval_methodology.md),
[error analysis](reports/retrieval_phase3/ERROR_ANALYSIS.md) and the
[complete phase-3 report](reports/progress/PHASE_3.md).

## Phase 3B: controlled review and complete-token Dense

The original phase-3 outputs remain immutable. The separate extension uses
the same MiniLM checkpoint with 126 content tokens per window, overlap 32,
mean of normalized window embeddings and final L2 normalization. BM25/RRF
parameters remain fixed. Validation is descriptive because it was already
observed in phase 3; test remains locked.

The supplied 3,731 lexical suggestions are **not human judgments**. Original
review sheets stay local; imports wait for real attested group decisions.
No augmented reference is created from automatic proposals. See
[review protocol](docs/annotation_pool_review.md),
[window methodology](docs/dense_windowing_methodology.md) and
[extension report](reports/progress/PHASE_3_EXTENSION.md).

```powershell
& .venv\Scripts\python.exe scripts/review_annotations_phase3b.py
& .venv\Scripts\python.exe scripts/run_phase3_extension.py --stage dev
& .venv\Scripts\python.exe scripts/run_phase3_extension.py --stage validation
& .venv\Scripts\python.exe scripts/report_phase3_extension.py
```

These commands require the original local phase-3 artifacts, restored corpus
and locked checkpoint. On completed experiments run only the report command:
the inference CLI refuses repeated validation or further dev selection.
New artifacts stay in `artifacts/phase3_extension/`; lightweight seed diagnostics
and additional UNJUDGED review candidates are under
`reports/retrieval_phase3_extension/`. No new dependencies are needed.

## Progress

| Phase | Status |
|---|---|
| 0 — Audit, security, architecture | Complete |
| 1 — Corpus, extraction, preprocessing, EDA, chunking | Complete |
| 2 — Benchmark alignment | Merged via PR #1; targeted dev embargo adopted |
| 3 — Retrieval | Implemented and measured on 83 dev / 30 validation; new judgments pending |
| 3B — Full-token Dense and controlled review | Measured on seed only; 111 local / 84 offline tests; human decisions pending |
| 4 — Reranking | Not started |
| 5 — Grounded RAG generation | Not started |
| 6 — Evaluation and error analysis | Not started |
| 7 — Local Streamlit application | Not started |
| 8 — Report, slides and demonstration video | Not started |

Each next phase requires separate authorization. Branch conventions:
[CONTRIBUTING.md](CONTRIBUTING.md).

## Attribution and licensing

Source material is attributed to the Federal Reserve Board. Its
[website disclaimer](https://www.federalreserve.gov/disclaimer.htm) permits
distribution of Board website information unless otherwise indicated; third-party
material can have separate restrictions. Original PDFs, logos and page-image
copies are excluded.

No software or benchmark reuse license has been selected by the project owners.
Public visibility does not establish an open-source license. Private course
slides, screenshots and individual annotator sheets are not distributed.

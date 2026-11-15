# FOMC RAG: A Reproducible Benchmark for Retrieval and Reranking

Academic Machine Learning project, subject 5, École Centrale Casablanca.
The objective is to compare retrieval and reranking strategies for grounded
question answering over FOMC Minutes and Statements.

**Current release: phases 0–1 only.** Security, architecture, PDF extraction,
preprocessing, EDA and deterministic chunking are implemented. BM25, Dense,
Hybrid retrieval, rerankers, RAG generation and the local Streamlit application
are planned, **not implemented**. No retrieval or generation scores are reported.

## Corpus and measured outputs

| Item | Current snapshot |
|---|---|
| Corpus | 93 FOMC PDFs, 838 physical pages, 2021–2026 |
| Types | 46 Minutes and 47 Statements |
| Baseline | 2,127 chunks, up to 256 words, overlap 40 |
| Alternatives | 128 words: 4,563 chunks; 512 words: 1,124 chunks |
| Questions | 145: 85 development / 30 validation / 30 test |
| Group-confirmed judgments | 279 question–page pairs: 188 grade 2, 91 grade 1 |
| Test paraphrases | 30, reserved for frozen configurations |
| Unanswerable candidates | 10, disabled pending human validation |
| Phase-1 checks | 22 tests passed; extraction and EDA reproduction verified |

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
No database, Docker, cloud account or model download is required. Installation
needs PyPI; subsequent corpus processing and tests are local.

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
The lock records the full effective environment. Retrieval/application extras
in `pyproject.toml` describe future dependencies and are not installed here.

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
six phase-0 checks on Python 3.13, without source PDFs, models or secrets.

## Evaluation methodology and limits

Future BM25, MiniLM Dense and Hybrid RRF systems must share corpus/chunks/top-k,
without automatic year filtering. Cross-Encoder rerankers will receive identical
top-20 candidates. Select hyperparameters on development/validation only; test
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

## Progress

| Phase | Status |
|---|---|
| 0 — Audit, security, architecture | Complete |
| 1 — Corpus, extraction, preprocessing, EDA, chunking | Complete |
| 2 — Benchmark alignment | Not started |
| 3 — Retrieval | Not started |
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

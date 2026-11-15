# Collaboration

`main` represents validated, stable work. Create these branches only when their
phase starts; run checks and document actual results before merging.

| Branch | Scope |
|---|---|
| feature/benchmark-alignment | Phase 2 |
| feature/retrieval | Phase 3 |
| feature/reranking | Phase 4 |
| feature/rag-generation | Phase 5 |
| feature/streamlit-demo | Local application |

Read `AGENTS.md` and the relevant phase prompt. Use `.venv/Scripts/python.exe`.
Keep PDFs, derived corpus, secrets, page screenshots, references and weights
local. Review every selected path before staging. Before committing run
`git diff --cached --check` and
`.venv/Scripts/python.exe scripts/audit_security.py --staged`.

Preserve the 279 group-confirmed judgments. Never tune on test or turn unjudged
items into negatives. Do not rewrite shared history or force-push main.
No software or benchmark reuse license has been chosen yet.

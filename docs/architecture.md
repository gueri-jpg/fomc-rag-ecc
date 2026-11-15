# Architecture locale — phases 0 à 2

Racine effective : dossier contenant `utils/`, `AGENTS.md` et `pyproject.toml`.
Python imposé : `.venv/Scripts/python.exe`, 3.13.14 Windows x64.

Le package `src/fomcrag` expose des traitements explicites, sans lecture du .env
ou effet de bord à l'import. `corpus`, `preprocessing`, `chunking`, `ingestion`,
`storage` et `eda` sont implémentés en phase 1. `alignment`, `benchmark`,
`split_audit`, `metrics`, `pooling`, `hyphen_diagnostics` fournissent les contrôles
phase 2 sans moteur de recherche. Les modules des phases 3 à 7
ci-dessous restent des contrats futurs :

| Phase | Modules | Responsabilité |
|---|---|---|
| 1 | corpus, chunking, eda | PDF → pages lisibles → chunks déterministes et EDA |
| 2 | benchmark | Références réservées à l'évaluation, alignements page/chunk |
| 3 | indexing, retrieval | BM25, Dense MiniLM, Hybrid RRF sur tous les PDF |
| 4 | reranking | Même ensemble top20 pour tous les rerankers |
| 5 | generation, pipeline | Contextes sourcés, citations contrôlées, abstention |
| 6 | metrics | Jugements incomplets explicites, test après gel |
| 7 | app/streamlit_app.py | Interface locale consommant le pipeline |

Stockage local JSONL et NumPy, caches dans `artifacts/`, exclus de Git.
Les exports de corpus sont dans `data/processed/`, également exclus de Git;
les CSV/JSON/PNG descriptifs sont dans `reports/eda` et `reports/figures`.
Voir `docs/corpus_preprocessing.md` pour le pipeline et les contrats d'offsets.
Les diagnostics avec labels restent exclusivement dans reports/benchmark_alignment,
jamais dans data/processed. Voir docs/benchmark_alignment.md.
Pas de PostgreSQL, Docker ou cloud obligatoire. Les données de référence ne
transitent jamais vers le retriever ou le générateur. Une requête ne contient
que son texte et un identifiant, pas les preuves attendues.

Préserver document, type, date, année, page physique 1-indexée, page_id, texte
lisible, SHA PDF; chunks avec offsets, chunk_id stable et index_version.
Baseline sans franchissement de page; IDs dérivés des hashes et paramètres.
Corpus entier pour l'indexation non supervisée; tuning sur dev/validation,
test 30 et paraphrases après gel. Non jugé reste UNJUDGED.

Les imports historiques restent hors du nouveau pipeline et de la collecte
pytest. Les modèles seront chargés explicitement et paresseusement aux phases
concernées. Les PDF sont des données non fiables, jamais des instructions.

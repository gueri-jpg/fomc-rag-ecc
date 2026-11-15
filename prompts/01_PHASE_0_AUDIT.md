# PHASE 0 — Audit, sécurité et architecture (commencer ici)

**Objectif :** transformer un prototype de scripts hétérogènes en dépôt Python structuré **sans encore lancer le calcul des embeddings ou le benchmark**. Lis `AGENTS.md`, `CODEX_MASTER_PROMPT.md`, `project_spec/CONSIGNES_OFFICIELLES.md` et `project_spec/VALIDATION_BENCHMARK_ET_QRELS.md`.

1. Établir état réel : `pwd`, arborescence, version Python, environnement `.venv`, Git status/remotes/branches **sans imprimer le `.env`**, licences et README. Décrire les scripts historiques Pdf2Txt/StockVectors/main et problèmes d'extraction, pertes de provenance et doublons.
2. Sécurité : vérifier que `.env`, secrets, poids de modèles, caches et matériaux `references_local_only` sont bien ignorés. Si `.env` ou secret a déjà été suivi par Git : **ne jamais imprimer le contenu**, prévenir l'utilisateur et recommander une rotation et une procédure sûre. Ne pas réécrire Git historique sans autorisation.
3. Vérifier sources : lancer `python scripts/preflight_codex.py --hash-pdfs` puis `python scripts/verify_kit_v2.py`, compter 46 Minutes + 47 Statements, 838 pages ; comparer manifeste SHA256 ; si anomalie, la diagnostiquer sans modifier PDF.
4. Vérifier données : 145 requêtes (85/30/30), 279 paires qrels groupe acceptées, 294 extraits retenus et 2 exclus, 30 variantes TEST, 10 negatives inactives. Confirmer qu'aucune donnée de vérité terrain n'est utilisée pour construire les requêtes.
5. Créer architecture (`src/fomcrag`, `app`, `tests`, `docs`, `reports/progress`, `experiments`, `configs`) et `pyproject.toml`/dépendances réalistes pour Windows, sans dépendance PostgreSQL/Docker. PyMuPDF, numpy, pandas, rank-bm25 ou équivalent, sentence-transformers, scikit-learn, streamlit, matplotlib, pytest selon phases. Ne pas imposer tous les poids/model téléchargés phase 0.
6. Rédiger `docs/architecture.md`, `docs/risk_register.md`, `docs/decision_log.md`, `README.md` minimal et tests smoke ne nécessitant ni DB ni Internet. Conserver `utils/` existant et les sources.
7. Consigner dans `reports/progress/PHASE_0.md` : inventaire, commandes exactes, sorties de test, décisions, bloquants, risques de fuite de données, prochaines étapes.

**Acceptation :** contrôle PDF/kit PASS ou problèmes documentés; `.env` non commité; architecture existante; `pytest -q` sur smoke local; aucune action destructrice. **S'arrêter après phase 0**.

# PHASE 1 — Corpus, extraction, prétraitement et EDA (obligatoire ECC)

**Prérequis :** phase 0 validée et état Git propre. Lire `project_spec/PROTOCOLE_EXPERIMENTAL.md` et contrats architecture.

1. Extraire chacun des **93 PDF** à l'aide de PyMuPDF, page physique 1-indexed, enregistrer `data/processed/pages.jsonl` par exemple avec `source_path`, `document`, `doc_type` (`minutes|statements`), `meeting_date`, `year`, `page`, `page_id`, texte brut lisible, SHA256. Vérifier 838 pages. Noter pages vides, erreurs, problèmes césure, en-tête/pied de page. Aucune fusion inter-document.
2. Paramétrer le nettoyage **non destructif** (normalisation espace et césures documentées, conservation nombres/ponctuation) ; dans BM25 seulement une normalisation distincte. Ne pas enlever stopwords/lemmatiser le contexte fourni au dense/LLM.
3. Construire chunks déterministes sans traverser page pour baseline, 256 *mots* avec overlap 40 (et possibilité 128,512). Conserver `char_start,char_end`, `page_id`, paramètres, hash et texte exact. Tester limites 1 mot/texte vide, overlap, UTF-8, reproductibilité et non-mélange des documents.
4. EDA réelle : nombre PDFs/pages par année/type; longueurs de pages/chunks (histogrammes et quantiles), doublons exacts et proches, volumes de termes, couverture chronologique, fréquences d'extraction vide; spécificités et limites de 2026 partielle. Conserver scripts `scripts/eda.py`, tableaux CSV, graphiques PNG dans `reports/figures/` et notes interprétatives.
5. Comparer quelques échantillons extraits avec PDF originaux, vérifier à la main une date/taux/valeur et page. Les doublons Statement/Minutes sont parfois historiquement légitimes : ne pas supprimer toute répétition ni filtrer des années.
6. Marquer un `corpus_version`, `chunking_version` et manifeste index ; invalider caches si fichiers/paramètres changent. Documenter code et diagramme de pipeline.
7. Tests `pytest` et smoke CLI d'ingestion; compte rendu réel `reports/progress/PHASE_1.md`.

**Acceptation :** 93 PDF/838 pages traités; provenance reproductible et EDA obligatoire satisfaites, aucune expérience retrieval/rerank encore présentée. **S'arrêter après phase 1.**

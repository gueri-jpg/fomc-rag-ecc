# Checklist de remise : 30 novembre 2026

## Conformité scientifique
- [ ] Théorie de BM25, bi-encoder Dense, cosine, fusion RRF, cross-encoder reranking, RAG, chunking, métriques.
- [ ] Extraction/EDA du corpus complet (93 PDF/838 pages) et preuves des statistiques originales.
- [ ] Splits 85/30/30 gelés avant tout tuning, variantes dans même split que parent, pas de fuite.
- [ ] Corpus unique, mêmes chunks/topk, pas de filtre annuel automatique.
- [ ] BM25 baseline seule comparée à Dense et Hybrid (sans rerank).
- [ ] Reranking comparé sans rerank sur même top20 candidats, avec temps et plafond de rappel.
- [ ] Qrels page existants (279) préservés, statut validé par groupe documenté; non jugés ≠ 0.
- [ ] Nouveaux résultats pertinents interannuels intégrés si vérifiés; état du pooling décrit honnêtement.
- [ ] 30 paraphrases test seulement après gel; 10 négatifs candidates inactives si non vérifiées.
- [ ] Étude d'interprétabilité via analyse détaillée d'erreurs basée sur vrais cas.
- [ ] Rapport métriques adaptées à la couverture du qrels, CI et test 30 interprétés avec prudence.
- [ ] Génération de réponse et citation PDF/page vérifiées, abstention et limites documentées.

## Livrables visibles
- [ ] `pytest -q` et scripts d'indexation/évaluation reproductibles.
- [ ] `streamlit run app/streamlit_app.py` donne une **démo locale testable** sur Windows.
- [ ] `README.md` installation, sources, commandes, hardware et clés sans dévoiler valeurs.
- [ ] Dépôt Git propre avec consignes, scripts, données (ou mécanisme d'accès légal aux PDF) et versions.
- [ ] Rapport écrit, tableaux et graphiques réellement calculés, bibliographie.
- [ ] PowerPoint de présentation.
- [ ] Vidéo de 15–20 minutes **enregistrée par l'équipe**, contenant démo et résultats.
- [ ] Archive de remise sans `.env`, cache secret ou données privées.

**Non requis :** Docker, cloud, FastAPI ou serveur PostgreSQL. Les ajouter seulement si le groupe a du temps après les résultats et la démo Streamlit.

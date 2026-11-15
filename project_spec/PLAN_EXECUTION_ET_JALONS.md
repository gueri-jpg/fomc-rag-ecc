# Plan séquentiel détaillé — 15 au 30 novembre 2026

**Priorités :** audit → extraction/EDA → récupération → reranking → génération → évaluation → Streamlit local → livrables. Les spécifications officielles acceptent explicitement une démonstration testable sans déploiement. Il n'y a **aucune tâche Docker ni cloud obligatoire**. Chaque phase se termine par des fichiers réels et tests, pas un résumé sans code.

| Phase | Échéance indicative | Travail attendu | Critère de passage |
|---|---|---|---|
| **0 — Audit/sécurité** | 15 nov. | Examiner dépôt réel, `.env`/Git sans exposer secrets, vérifier les 93 sources et le kit, dépendances, architecture, base pytest et `pyproject.toml` | Préflight et vérification kit passent; rapport phase 0; aucun fichier source perdu |
| **1 — Corpus, extraction, EDA** | 15–17 nov. | PyMuPDF page à page, contrôle 93 PDF/838 pages, offsets/metadata, texte lisible, chunks déterministes, tableaux/courbes distributions, qualité PDF | Manifest/reproductibilité, tests d'extraction, EDA réelle, aucun document perdu |
| **2 — Référentiel/alignement** | 17–18 nov. | Exploiter 145Q, 279 qrels acceptés, aligner extraits/page/chunks, vérifier split, audits d'ambiguïté/duplicats | Traçabilité couverture qrels et rapport des non jugés; pas de nouvelle double annotation forcée |
| **3 — Retrieval** | 18–21 nov. | BM25 baseline, Dense MiniLM, Hybrid RRF; tests limites; k 1/3/5/10/20, dev/val; latence/cout; candidats pool interannuel | Comparaison sans rerank, index commun, tests équité et journal des métriques connues |
| **4 — Reranking** | 21–23 nov. | Same-top20 candidates, CrossEncoder MiniLM, BGE si possible, ablations N/résultat; latence additionnelle | Comparaison rerank vs sans-rerank réelle, limites matérielles explicites |
| **5 — Génération RAG** | 23–25 nov. | Réponse contrôlée à partir de contexte, citations PDF/page, abstention, baseline extractif clairement nommé, modèle LLM effectif si possible | Démo CLI de question → sources → réponse / abstention; tests citations |
| **6 — Évaluation/erreurs** | 25–27 nov. | Score dev/validation puis test gelé, métriques adaptées aux qrels, couverture faits, 30 paraphrases test, analyse qualitative erreurs, bootstrap si fondé | Pas de réglage après test, tableaux réels, désaccord qrels/limites documentés |
| **7 — Streamlit local** | 26–28 nov. | Interface recherche + QA, choix retriever/reranker, passages source, citation, latences, monitoring local, paramètres cache | `streamlit run app/streamlit_app.py` et test manuel réels sur ordinateur |
| **8 — Rapport/PPT/vidéo** | 27–29 nov. | Théorie/EDA/méthode/résultats/erreurs, PPTX, script et plan de tournage vidéo 15–20 min, README et archive de remise | Matrice de conformité satisfaite et fichiers de dépôt prêts |
| **Remise** | **30 nov. 2026** | Fichiers finaux, lien Git, vérification archives et captures de démo | Aucun secret, toutes commandes de reproduction documentées |

Les dates intermédiaires sont une proposition, pas des obligations imposées par l'enseignant.

## Recommandations sur l'ordre
- **Phase 0 et 1 tout de suite.** Ne pas coder une jolie interface avant d'avoir un corpus exact, indexable, traçable et des métriques cohérentes.
- **Phase 2 courte :** la double annotation des références existantes est déjà confirmée par l'équipe. La tâche n'est PAS de refaire 279 jugements; l'alignement page→chunk et l'import d'annotations de pooling déjà faites restent nécessaires.
- **Phase 3 d'abord sans rerank**, sinon attribution des gains scientifiquement impossible.
- **Reranking après retrieval** sur un ensemble de candidats identique pour chacun des rerankers, avec recall ceiling.
- **Pas de fuite** : partitions des requêtes gelées avant tuning/apprentissage. Un index lexical ou embeddings calculé sans utiliser les labels sur tous les PDF est admissible. Regrouper questions très proches et leurs paraphrases dans même split.
- **Mesures exploratoires possibles** avec 279 pages jugées; déclarer les limitations de complétude plutôt que de bloquer le code à cause de feuilles A/B non remises.

## Livrables répétables par phase
`reports/progress/PHASE_0.md` ... `PHASE_8.md`, instructions de commandes Windows et Linux, tests `pytest -q`, un tableau des décisions et limitations, seeds, `requirements`/`pyproject.toml`, suivi des temps, mémoire, versions de modèles et configs.

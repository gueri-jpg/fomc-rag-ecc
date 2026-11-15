# Décisions de projet figées pour le kit V2

| Sujet | Décision | Justification |
|---|---|---|
| Application | Streamlit locale testable, pas de Docker/cloud obligatoires | Conforme à l'alternative « démonstration permettant de tester » des consignes ECC |
| Corpus | 93 PDF/838 pages, 2021–2026, tous indexés et recherchables | Évite biais interannuel |
| Source historique | garder `utils/` d'origine en lecture/audit | traçabilité et comparaison avant/après |
| Référence | 145 questions + 279 qrels question–page acceptés par équipe | travail humain déclaré terminé, grades identiques aux propositions |
| Qrels non jugés | NE PAS convertir en 0 | limite scores biasés |
| Ancien pool TF-IDF | optionnel, annoter uniquement ce qui manque et qui n'est pas déjà documenté ailleurs | éviter double travail |
| Splits | 85 dev, 30 validation, 30 test gelés | anti-fuite |
| Variantes | 30 paraphrases sur test après gel | robustesse appariée |
| Sans réponse | 10 candidates, inactives jusqu'à preuve corpus complet | évaluation abstention RAG |
| Retrieval | BM25 sans rerank, Dense MiniLM, Hybride RRF | comparaison équitable |
| Reranking | CrossEncoder MiniLM, BGE si possible, sur top20 identiques | attribution correcte des gains |
| Génération | LLM authentique si accessible + baseline extractif identifié | QA sourcée, éviter fausses démos |
| Stockage | local fichiers/NPY/FAISS, DB optionnelle | simplicité pour école et PC |
| Interprétabilité | analyse détaillée des erreurs obligatoire | conforme au cours |
| Livraison | Git README, rapport, PPTX, vidéo 15–20 min, démo locale | exigences officielles |

Toute modification doit être justifiée AVANT de consulter les scores du test et consignées dans `docs/decision_log.md`.

# Protocole expérimental reproductible — Sujet 5 RAG FOMC

## Questions de recherche
RQ1 : BM25, Dense MiniLM et Hybrid RRF ont-ils des performances différentes de récupération, à k et chunking constants ?
RQ2 : un reranker améliore-t-il le classement à candidats top20 strictement identiques et à quel coût de latence ?
RQ3 : les gains de retrieval se traduisent-ils en réponses plus fidèles et mieux sourcées ?
RQ4 : quelle est la sensibilité aux reformulations lexicales/sémantiques, au type de question, aux années des preuves et aux erreurs de contexte ?

## Données / anti-fuite
- **93 PDF FOMC**, 46 Minutes et 47 Statements ; 838 pages, années 2021–2026 (octobre 2026 pour dernières Statements).
- Split préenregistré **145 besoins distincts : 85 dev, 30 validation, 30 test**, tester similarités cross-split (migration seulement si correction de fuite documentée AVANT toute expérience). Les variantes du test restent avec leur parent.
- Sources PDF intégrales indexées pour tous les systèmes : **pas de filtre d'année automatique**. Corpus non supervisé d'indexation commun; entraînement de modèles à partir de qrels test interdit.
- Texte brut lisible sauvegardé; métadonnées et SHA256; transformations lexicales de BM25 distinctes du texte envoyé au dense/LLM. Taille 128/256/512 *unité explicitée*, overlap 0/40 ou paramétré. Choisir uniquement sur dev/validation.

## Référence humaine
- Équipe confirme double annotation et maintien des pertinences proposées : **279 couples question-page confirmés** ; 188 grade 2 et 91 grade 1. Pas de formulaires A/B dans ce kit, pas de κ calculable. 294 extraits source positifs et 2 exclus.
- `qrels_group_confirmed_PAGES.trec` : vérité terrain déclarative pour les preuves connues, **pas preuve d'exhaustivité de toutes les pages ou chunks**. `POOLING_TO_REVIEW_1740.csv` reste un pool TF-IDF non jugé DANS LE FICHIER; extraire uniquement les nouveaux résultats non documentés pour revue. Les pages d'autres années ne sont jamais exclues par principe.
- Un chunk d'une page positive n'est pas automatiquement positif; matching au niveau page uniquement après déduplication des pages; matching chunk seulement après annotation explicite et version de chunking gelée.
- Paires de passages « alternatifs » : une seule preuve qui couvre les faits requis peut être suffisante; ne pas mesurer la complétude des informations en exigeant tous les documents paraphrasant la même idée. Couverture de faits (facet recall) séparée de recall passages.
- Si la couverture des jugements demeure partielle, rapporter métriques sous noms `known_positive_*` avec réserves; les vrais Precision@k/Recall@k/nDCG@k peuvent être biaisés et ne doivent pas être présentés comme non biaisés.

## Baselines retrieval (aucun reranking)
- BM25 déterministe et documenté (tokenisation et paramètres k1,b).
- Dense `sentence-transformers/all-MiniLM-L12-v2`, normalisation / cosine ou produit scalaire explicité; cache embeddings index et latence CPU/GPU.
- Hybrid = Reciprocal Rank Fusion, constant `rrf_k` optimisé dev/validation, pas de rerank interne.
- Comparer sur **mêmes chunks**, mêmes questions, top k 1/3/5/10/20, mêmes filtres de source (tous). Sauvegarder résultats détaillés par requête et index fingerprint.
- Principal : (sous couverture suffisante) Recall@5, nDCG@5, MRR@5, HitRate@5, Precision@5; sinon `known_positive_coverage@5`, `first_known_positive_rr`, et seed-nDCG descriptif, plus mesure d'étendue du jugement. Latence p50/p95 et coût d'indexation.

## Reranking
- Source de candidats : top20 du retriever sélectionné et **exactement les mêmes chunks** pour None/MiniLM/BGE. L'ordre initial de départ peut différer selon les retrievers, mais aucun reranker ne peut ajouter un candidat absent.
- Mesurer nDCG@5/Hit@5 ou proxies, MRR@5, couverture de facettes et latence additionnelle, ainsi que recall ceiling du top20. Ablations : tailles topN 10/20/50 si supportées et ressources disponibles, sans élargir artificiellement le budget du modèle comparé.

## Génération / abstention
- Baseline extractif et générateur LLM authentique distingués. Réponses doivent pouvoir citer `[nomdupdf.pdf, p. N]` et être supportées par les chunks récupérés; contrôle des citations par IDs source, abstention si insuffisance.
- Métriques : exactitude des faits attendus, fidélité à la source, pertinence de la réponse, justesse des citations, erreurs de non-abstention, latence, avec échantillon de vérification manuelle. RAGAS/LLM-as-judge éventuels, pas une preuve de vérité sans validation.

## Test/robustesse/statistiques
- N'utiliser le TEST 30 qu'une fois systèmes et hyperparamètres figés; les 30 paraphrases `robustness_30_TEST_ONLY.jsonl` se lancent APRÈS le test principal, sans entraîner ni ajuster.
- Écart apparié pour chaque besoin `delta = score(paraphrase) - score(originale)`; ne pas gonfler N à 60 indépendants pour CI/statistiques. Bootstrap sur les 30 besoins, graine fixée; rappeler grande incertitude d'échantillon.
- 10 questions candidates sans réponse uniquement après preuve humaine corpus complet; elles servent surtout à tester abstention et hallucination, pas les métriques de rappel sur questions sans positifs.
- Analyses qualitatives obligatoires : au moins 15–20 cas vérifiés, fautes de date, lexical overlap trompeur, preuve hors année, mauvaise taille chunk, répétitions Statement/Minutes, preuves partielles, perte d'une facette, hallucinations.

## Reproductibilité et publication
- Enregistrer seeds, versions de packages/modèles, config YAML/JSON, hash corpus/index, métadonnées hardware, latences warm/cold, logs et commandes réellement exécutées.
- Ne jamais utiliser chiffres jouets comme résultats réels. Graphiques de résultats uniquement depuis résultats persistés; conserver erreurs et limitations. Inclure théorie dans rapport, sources des PDF, conformité consignes.

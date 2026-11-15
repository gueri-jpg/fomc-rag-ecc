# PHASE 3 — Indexation et récupération (SANS reranking)

1. Indexer **les mêmes chunks et les 93 PDF** pour BM25, Dense MiniLM (`all-MiniLM-L12-v2`) et Hybrid RRF. Log version des modèles, tokenisation, normalisation, hash d'index, device CPU/GPU, seed, temps et taille des index. Aucun filtre implicite par année.
2. Construire un baseline simple BM25 déterministe, puis dense cosine avec encodage par lot et cache, puis Hybrid RRF avec scores/rangs et constante documentée. Paramètres choisis sur dev/validation seulement. Vérifier l'ordre des scores et les requêtes exactes.
3. Exécuter top k=1,3,5,10,20 en configs équitables sur 85 dev puis 30 validation, sauvegarder toutes les prédictions en JSONL (avec chunk, page, texte, rang, score, latence) et tableau diagnostic de métriques. Sur qrels de pages partiels, le script ne donne pas un Recall gold non biaisé.
4. Pour éviter pénalisation interannuelle, construire **pool union des top20** (BM25/Dense/Hybrid) sur toutes années, dédupliquer, soustraire jugements confirmés et annotés par ailleurs; exporter uniquement candidats nouveaux pour validation. **N'exiger pas que l'équipe refasse la double annotation existante.**
5. Comparer temps cold/warm p50/p95, taille index, extraction, ressources; qualitative erreurs de retrieval. Ablations chunk size sur DEV/VAL uniquement si temps disponible.
6. Tests d'équité et no-rerank ; `reports/progress/PHASE_3.md`, graphiques basés sur fichiers mesurés. Ne pas consulter score test pour choisir configuration.

**Acceptation :** BM25/Dense/Hybrid réels, corpus complet, sorties répétables, rapport comparatif initial, nouveaux candidats pool. **S'arrêter**.

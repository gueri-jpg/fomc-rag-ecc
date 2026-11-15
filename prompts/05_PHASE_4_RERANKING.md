# PHASE 4 — Reranking et études d'ablation

1. Charger **les mêmes top20 chunks** produits par chaque retriever de la phase 3. Comparer `None` (ordre d'origine), `cross-encoder/ms-marco-MiniLM-L-6-v2` et reranker BGE approprié si disponibilité/ressources ; télécharge modèles si l'environnement l'autorise et log les versions exactes.
2. Un reranker n'ajoute aucun nouveau chunk et ne revoit pas le corpus entier. Conserver l'input top20 identique, tracer `candidate_ids`, scores d'entrée et scores réordonnés, rangs finaux, temps rerank et CPU/RAM.
3. Comparer top5 sans rerank et après chaque reranker, plafonnement par rappel des candidats, passages partiellement pertinents, gain nDCG/first-hit/coverage si labels disponibles; ablations topN 10/20/50 uniquement si faisables et indiquées.
4. Analyser échecs et régressions par question; aucun ajustement sur test; résultats réels et rapport `reports/progress/PHASE_4.md`.

**Acceptation :** même ensemble de candidats, baseline None, au moins un vrai cross-encoder et limitation BGE explicitée si impossible. **S'arrêter**.

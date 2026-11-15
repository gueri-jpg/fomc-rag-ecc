# PHASE 2 — Benchmark confirmé, alignement et contrôle des qrels

**Ne jamais répéter les 279 jugements déjà validés par le groupe.** Lire `evaluation/benchmark/GROUP_VALIDATION_STATUS.json`, `project_spec/VALIDATION_BENCHMARK_ET_QRELS.md`.

1. Charger `queries_145.jsonl` (85 dev/30 validation/30 test) + qrels de référence `qrels_group_confirmed_PAGES.trec` et citations `evidence_citations_145.jsonl`. Vérifier 188 notes 2 + 91 notes 1, total 279 paires question-page. Conserver questions/réponses de référence hors du contexte offert au moteur.
2. Associer les extraits vérifiés aux pages du corpus et à un/des `chunk_id` effectivement créés. Ne pas attribuer note 2 à un chunk tronqué quand la page est 2; produire `alignment_report.csv` avec `exact_match`, `partial_match`, `not_found` et raison. Vérifier par échantillon des cas multi-facettes et hors année.
3. Audit des questions très similaires entre partitions et équivalence du sens des 30 paraphrases; si risque de leakage, proposer correction AVANT consulter test et l'enregistrer. Pas de tuning ici.
4. Rechercher éventuelles annotations de pooling déjà fournies par groupe (dans fichiers réellement accessibles) et les importer sans les inventer ; dans `POOLING_TO_REVIEW_1740.csv`, les colonnes A/B sont encore vides. **Ne pas traiter ce CSV comme 1740 positifs ni 1740 négatifs**.
5. Générer diagnostics de couverture des preuves/par année/type/question; les pages non jugées sont `UNJUDGED`. Exporter qrels conditionnels, vérifier nombre et version hash. Maintenir seulement le statut « preuve acceptée par groupe, potentiellement incomplete » tant que complétude n'est pas prouvée.
6. Mettre en place génération du pool à partir des résultats de retrieval futurs; ne pas bloquer la phase 3. `reports/progress/PHASE_2.md` avec validation effective et limitations.

**Acceptation :** IDs cohérents, alignement sourcé, 279 grades préservés, statut exact, audit splits et import possible des nouvelles notes. **S'arrêter**.

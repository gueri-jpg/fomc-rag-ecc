# Benchmark V2 — quoi utiliser maintenant ?

| Fichier | Usage | Statut |
|---|---|---|
| `queries_145.jsonl` | requêtes sans passage de vérité terrain | actif, 145 |
| `qrels_group_confirmed_PAGES.trec` | notes question/page acceptées par le groupe | actif, 279 paires (188 grade 2; 91 grade 1) |
| `qrels_group_confirmed_PAGES.csv` | identique avec provenance de la confirmation | actif |
| `GROUP_VALIDATION_STATUS.json` | preuve documentaire de la déclaration de validation | actif ; pas de calcul de kappa |
| `silver_qrels_PAGES.*` | historique proposé avant confirmation | conservé, ne pas préférer à qrels_group_confirmed |
| `evidence_citations_145.jsonl` | provenance et extraits PDF | actif, 296 lignes dont deux exclus |
| `qrels_double_annotation_TEMPLATE.csv` | formulaire individuel A/B si originaux fournis | ARCHIVE/template, ne plus traiter comme statut du groupe |
| `POOLING_TO_REVIEW_1740.csv` | candidats TF-IDF non jugés DANS LE CSV | optionnel, jamais des négatifs automatiques |
| `robustness_30_TEST_ONLY.jsonl` | 30 paraphrases de test | seulement après freeze |
| `unanswerable_10_NOT_GOLD.csv` | 10 candidates non répondables | désactivées |
| `validate_benchmark.py` | contrôle structurel du dossier | corrigé : ne demande plus fichier absent |

La validation du groupe concerne les grades présents (non le fait que **toutes** les pages possibles du corpus aient été jugées). Un résultat expérimental n'est jamais présenté comme « définitif » si le protocole n'explique pas le traitement des pages non jugées.

Pour vérifier le kit, depuis sa racine : `python scripts/verify_kit_v2.py`; pour valider le benchmark seul : `python evaluation/benchmark/validate_benchmark.py`.

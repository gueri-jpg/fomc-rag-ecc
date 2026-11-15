# Phase 2 — alignement, incertitude et budgets

Le benchmark reste séparé du corpus fourni aux modèles. Les rapports sous
`reports/benchmark_alignment/` sont réservés à l'audit et à l'évaluation;
aucun retriever/générateur ne doit charger leurs réponses, faits ou jugements.

## Reproduction

Préparer les exports de phase 1 sans changer sa configuration, puis utiliser
uniquement le Python du venv (aucune nouvelle dépendance) :

```powershell
& .venv\Scripts\python.exe scripts/align_benchmark.py
& .venv\Scripts\python.exe scripts/audit_benchmark_splits.py
& .venv\Scripts\python.exe scripts/diagnose_priority_evidence.py
& .venv\Scripts\python.exe scripts/audit_hyphens.py
& .venv\Scripts\python.exe scripts/verify_phase2.py --rebuild
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe scripts/check_offline.py --tests tests/test_phase0.py tests/test_benchmark_phase2.py
```

## Localisation et offsets

On recherche une sous-chaîne **contiguë**, d'abord littérale, puis dans une
vue caractère par caractère NFKC + casefold limitée aux lettres ASCII/chiffres.
Cette vue reproduit la méthode de l'audit indépendant, avec un index d'origine
pour chaque caractère émis. Ligatures et fractions peuvent être développées;
plusieurs caractères normalisés peuvent donc pointer vers le même caractère.
Les bornes projetées sont `[origin[start], origin[end-1]+1)` dans `pages.text`.
Le mapping raw_offset_runs de phase 1 fournit ensuite les offsets dans raw_text.
Les positions normalisées ne sont jamais utilisées directement comme offsets
source. Les alternatives de correspondance sont conservées, sans choisir
arbitrairement une occurrence répétée.

La normalisation est **permissive** : `1/4` et `14` peuvent avoir la même vue,
les signes et négations doivent être relus dans le texte original. Ce mécanisme
localise un extrait connu sur une page connue; il ne démontre ni équivalence
numérique ni pertinence. Il ne sert pas de tokenizer de récupération.

| Statut | Définition |
|---|---|
| EXACT_MATCH | Une occurrence intégrale, avec sous-chaîne littérale |
| NORMALIZED_MATCH | Une occurrence intégrale seulement dans la vue normalisée |
| PARTIAL_MATCH | Fragment contigu ≥32 caractères normalisés, ou preuve page complète mais aucun chunk ne la contient intégralement; distinguer page_match_status et match_status |
| NOT_FOUND | Aucune occurrence intégrale ni fragment suffisant |
| AMBIGUOUS | Plusieurs occurrences intégrales; alternatives conservées |
| NEEDS_HUMAN_REVIEW | État de revue, utilisé dans les diagnostics sémantiques; ne remplace pas le statut de localisation |

`text_coverage` est une proportion de **caractères normalisés** de l'extrait,
pas une métrique sémantique, ni une conservation de sa ponctuation. Un chunk
ne reçoit aucun grade pour cette raison. Les cas partiels ont une file de revue;
les sept diagnostics utilisent des clauses de faits proposées par l'analyste,
explicitement non validées humainement. Les `required_facts` originaux restent
des identifiants quand ils existent; aucune ontologie de faits gold inventée.

## Trois conventions @k distinctes

Soit le classement de chunks `[A1(page A), A2(page A), B1(page B), C1(page C)]`.

| Convention k=2 | Éléments pris | Pages représentées | Chunks consommés |
|---|---|---|---:|
| chunk@k | A1, A2 | A | 2 |
| page-coverage-from-chunk@k | A1, A2 puis déduplication | A | 2 |
| unique-page@k | A1, A2, B1 jusqu'à deux pages | A, B | 3 |

`chunk@k` requiert des jugements de chunks explicites pour calculer une qualité
au niveau chunk; les 279 qrels page ne suffisent pas. La seconde convention
mesure les pages connues positives présentes dans un budget strict de chunks.
La troisième travaille avec un budget de pages, et peut lire plus de k chunks.
Toujours publier `convention`, k, chunks consommés et nombre de pages distinctes.
Le rang de première page positive est le rang dans les pages dédupliquées; il
n'est pas un rang de chunk et n'est pas interchangeable avec un MRR de chunks.

Les deux scripts historiques evaluate_retrieval/evaluate_robustness demandent
désormais une convention explicite et des IDs chunk/page. Leurs noms de métriques
sont préfixés par convention. Le premier refuse chunk@k avec des qrels page.
Le mode silver produit seulement des diagnostics conditionnels aux positifs
connus; les valeurs non jugées utilisées comme gain nul par seed-nDCG ne sont
pas des étiquettes négatives. Le mode gold historique reste réservé à une
future revue exhaustive documentée; un formulaire de déclaration ne prouve
pas à lui seul l'exhaustivité. Aucun de ces scripts n'a été lancé sur un vrai
classement BM25/Dense/Hybrid pendant la phase 2.

## Pooling futur et revue humaine

`build_review_pool.py` lit des fichiers existants, jamais un modèle :

```powershell
# Exemple à utiliser en phase 3 seulement, après création de vrais classements.
& .venv\Scripts\python.exe scripts/build_review_pool.py --run BM25=outputs/bm25.jsonl --run Dense=outputs/dense.jsonl --run Hybrid=outputs/hybrid.jsonl --top-k 20 --unit chunk --output artifacts/review_pool.csv
```

Chaque requête contient `question_id` et `retrieved`, liste ordonnée de
`chunk_id,page_id`. Top-k est pris **avant** union; la feuille garde chaque
méthode et rang. Déduplication par chunk ou page, identités contrôlées contre
le corpus, aucun score fusionné ou nouveau candidat récupéré.

En mode chunk, tout candidat sans jugement chunk reste UNJUDGED, même si sa
page a une note (conservée dans page_judgment). En mode page, seules les pages
déjà jugées reprennent leur note, les autres restent UNJUDGED. Une feuille
automatique n'est jamais une annotation humaine. Les 1 740 lignes TF-IDF
historiques sont encore un pool non documenté en tant que labels.

Si le groupe fournit de vraies décisions, CSV avec
`question_id,page_id,relevance_grade,review_status,notes`, statut HUMAN_REVIEWED.
`scripts/merge_reviewed_qrels.py --additional <csv>` vérifie identités, pages
physiques valides et notes entières 0/1/2; conflits et tentative d'écrasement
des qrels sources sont refusés. Sans nouveau fichier humain, aucun import ni
fichier gold n'est créé. Le résultat consolidé ne certifie pas l'exhaustivité.

## Limites et décisions avant phase 3

Deux paires cross-split partagent des preuves substantielles; aucune partition
n'a été déplacée. Examiner SPLIT_AUDIT.md avant tuning. Les notes sémantiques
sur les 30 paraphrases sont un diagnostic analytique, pas une validation humaine
de l'équivalence. Les dix questions sans réponse restent désactivées.

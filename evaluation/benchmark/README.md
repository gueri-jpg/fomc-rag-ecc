# NOTE V2 — Lire `README_V2_STATUS.md` et `GROUP_VALIDATION_STATUS.json` avant ce README historique. Les 279 qrels initiaux ont été confirmés par le groupe; les anciens passages « pending review » ne reflètent plus ce retour.

# Benchmark FOMC 2021–2026 — Jeu d'évaluation retrieval (SILVER)

Date : **14 novembre 2026**. Corpus : **93 PDF, 838 pages**, couvrant 2021 au 28 octobre 2026. La base est celle fournie par le groupe (`ML-RAG-master.zip`) et **ne doit pas être filtrée par année**.

## Résultat de la curation

| Jeu | Questions | Statut |
|---|---:|---|
| Questions principales | **145** | Prêtes pour le développement et les tests exploratoires de retrieval |
| Paraphrases officielles du test | **30** | Une variante par question de test ; activer après fixation des modèles |
| Questions a priori sans réponse | **10** | **NON VALIDÉES** ; ne pas les inclure dans les métriques retrieval |
| Total maximum si validation des négatives | **185** | Moins de 200 |

**Important :** 294 passages candidats positifs ont été retrouvés textuellement dans les PDF (**279 paires question/page**). Une présence textuelle ne garantit ni la pertinence définitive ni l'exhaustivité. Deux associations initiales ont été écartées car hors du sens ou de la période demandée. Une preuve de 2022 a été ajoutée à la question 2021 `FOMC_021`.

## Quels fichiers utiliser ?

1. **`benchmark_fomc_evaluation_silver_145.json`** : **fichier unique** lisible contenant les 145 questions, leurs sources et passages, les métadonnées, les 30 paraphrases de test et les 10 candidates sans réponse.
2. `queries_145.jsonl` : fichier de requêtes pour BM25, Dense ou Hybride. Ne contient PAS les preuves attendues ni les réponses.
3. `silver_qrels_PAGES.trec` (ou `.csv`) : jugements **provisoires** question → page PDF. Ne pas publier ses chiffres comme gold.
4. `evidence_citations_145.jsonl` : extraits sources exacts ou normalisés de façon transparente ; sources PDF et pages.
5. `qrels_double_annotation_TEMPLATE.csv` : annotations indépendantes A/B et adjudication à faire.
6. `POOLING_TO_REVIEW_1740.csv` : pages TF-IDF de toutes les années à juger. Il faut également ajouter les top-k de BM25, Dense et Hybride.
7. `robustness_30_TEST_ONLY.jsonl` : les **30 variantes du test**, par paire avec les 30 questions de test.
8. `unanswerable_10_NOT_GOLD.csv` : questions candidates non répondables, sans statut gold.
9. `RUBRIC_RELECTURE_145.csv` : attentes factuelles/notes de lecture pour les annotateurs.
10. `AUDIT_VERACITE_ET_LIMITES.md` et `JOURNAL_CORRECTIONS.csv` : corrections vérifiées et limites scientifiques.
11. `MANIFESTE_CORPUS_93.csv` : noms, années, types, SHA256 des PDF, pour la reproductibilité.

## Intégrer au projet : récupérer des pages avec les chunks

**Tous les modèles indexent les mêmes 93 PDF et le même découpage.** Chaque chunk retourné doit porter sa provenance :

```json
{"chunk_id":"chunk_123","document":"fomcminutes20211103.pdf","page":10,"text":"...","score":0.81}
```

Votre programme de recherche doit écrire des prédictions JSONL, triées du meilleur au moins bon, par exemple :

```json
{"question_id":"FOMC_001","retrieved":[{"page_id":"monetary20210127a1.pdf#p1"},{"page_id":"fomcminutes20210127.pdf#p19"}]}
```

Dans `page_id`, **`p1` = première page physique du PDF**. Le document doit avoir le même basename que dans les références. Si un chunk couvre deux pages, il faudra ajouter une correspondance explicite vers les pages couvertes et adapter le protocole de matching. L'évaluation fournie est **au niveau des pages source, par proxy**, pas au niveau des chunks exacts.

## Exécuter une évaluation exploratoire

```bash
python validate_benchmark.py
python evaluate_retrieval.py --predictions vos_resultats.jsonl --mode silver --split dev --k 5
python evaluate_retrieval.py --predictions vos_resultats.jsonl --mode silver --split validation --k 5
python evaluate_retrieval.py --predictions vos_resultats.jsonl --mode silver --split test --k 5 --output diagnostic_test.json
```

Le script fournit `known_positive_hit@5`, `known_positive_coverage@5`, `first_known_positive_rr` et un `seed_nDCG@5` **exploratoire**. En mode SILVER, les pages non annotées ne sont PAS des négatifs : ces chiffres ne sont pas des mesures non biaisées de la vraie précision, du vrai rappel ou du nDCG définitif. La latence doit être mesurée dans le moteur, pas déduite des qrels.

Pour préparer les véritables qrels après revue humaine :

```bash
python gold_qrels_builder.py --annotations qrels_double_annotation_TEMPLATE.csv --pooling POOLING_TO_REVIEW_1740.csv --output validated_qrels.csv
```

Ne passer à `--mode gold` qu'après finalisation des annotations, validation du pooling **multi-modèle** et autorisation explicite dans votre propre manifeste gold. Le script officiel refuse les résultats contenant des pages récupérées non jugées, plutôt que de compter ces pages comme 0.

## Ordre expérimental recommandé

1. **Révision des questions** : conserver les 145 besoins informationnels, les critères de réponse et les périodes demandées.
2. **Récupération initiale** : même corpus, mêmes chunks, BM25 / Dense / Hybride, top 5 / 10 / 20 ; conserver classement et latence.
3. **Pooling interannuel** : union des résultats des trois récupérateurs + TF-IDF exploratoire ; supprimer doublons ; double annotation des pertinences 0/1/2, adjudication et revue des faits complémentaires. Ne pas imposer `year(question) = year(passage)`.
4. **Répartition** : fichier déjà fixé à **85 dev / 30 validation / 30 test**, avec groupes de questions proches conservés dans la même partition. Les paramètres doivent être choisis en dev/validation, **sans regarder les scores du test**.
5. **Évaluation des modèles figés** sur les 30 questions de test. Le test ne sert pas à choisir BM25 k1, Dense embeddings ou poids Hybride.
6. **Robustesse** : faire passer les **30 variantes du test** aux mêmes modèles figés. Comparer les métriques **par paires** (même fait attendu, même qrels), idéalement avec intervalle de confiance bootstrap. Les cinq variantes 2021 du test ne suffisaient pas seules ; les variantes actives couvrent donc les 30 sujets de test.
7. **Questions sans réponse** : après confirmation qu'aucun des 93 PDF ne fournit une réponse, les tester séparément avec la génération RAG et la règle d'abstention. Mesurer exactitude de l'abstention, réponses non justifiées, faux étayage, et éventuellement seuil de confiance. **Ne pas calculer Recall@5/MRR@5 sur des questions sans positifs.**
8. **Reranking et génération** : après avoir établi le socle retrieval. Ajouter des réponses de référence validées pour évaluer la génération, puis comparer la qualité bout-en-bout.

## Limites à ne pas masquer

- Les qrels ne sont pas exhaustifs. Une page hors liste est **non jugée**, et non non pertinente.
- Un maximum de cinq *citations initiales* par question n'autorise pas à ignorer d'autres pages réellement pertinentes : le pooling peut conduire à plus de cinq qrels positifs.
- Une page peut contenir plusieurs chunks, dont certains non pertinents. Une évaluation de retrieval au **niveau chunk** requiert des annotations sur les chunks ou des preuves alignées par spans et offsets.
- Les gradations 1/2 de ce dossier sont **proposées**, pas issues de deux annotateurs. Le fichier est finalisé **pour lancer le pipeline et sa validation**, pas certifié gold.
- Les 10 candidats sans réponse ne sont pas encore prouvés non répondables. Ne pas les fusionner au jeu test officiel avant contrôle.

Le rapport `AUDIT_VERACITE_ET_LIMITES.md` décrit le contrôle de provenance, les corrections sémantiques, les lacunes et les biais évités.

## Évaluation finale à la granularité des **chunks**

Pour un mémoire scientifique, la recommandation est d'évaluer les **chunks retournés**, pas seulement leurs pages. Après les premiers passages sur BM25/Dense/Hybride, construisez une liste commune des chunks à juger :

```bash
python make_chunk_pool.py \
  --bm25 predictions_bm25.jsonl \
  --dense predictions_dense.jsonl \
  --hybrid predictions_hybrid.jsonl \
  --topk 20 --output POOL_CHUNKS_TO_ANNOTATE.csv
```

Chaque candidat contient le `chunk_id`, le texte, le PDF, la page et les rangs observés dans les trois moteurs. Deux annotateurs indépendants doivent remplir les grades 0/1/2, les faits soutenus, puis arbitrer les désaccords. Ces **qrels de chunks** peuvent ensuite être employés pour des métriques de retrieval précises ; les qrels de pages livrés dans ce dossier restent un substitut exploratoire.

## Robustesse : exemple

Après avoir évalué le test principal **et figé les modèles**, récupérer les 30 variantes du fichier `robustness_30_TEST_ONLY.jsonl` (une par question du test), puis lancer :

```bash
python evaluate_robustness.py \
  --main-predictions predictions_all145.jsonl \
  --variant-predictions predictions_variants30.jsonl \
  --k 5 --output comparaison_robustesse.json
```

Les deltas et intervalles de confiance sont exploratoires avant validation des qrels ; le script ne fabrique pas de résultats de modèle. Les variantes historiques de développement ne font pas partie des **175 requêtes actives**.

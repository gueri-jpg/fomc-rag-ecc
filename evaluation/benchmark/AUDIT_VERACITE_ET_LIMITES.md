# FOMC — audit de véracité, version de travail finalisée pour le pipeline

**Date : 14 novembre 2026. Corpus fixe : 93 PDF (2021–octobre 2026), 838 pages.**

## Ce qui a été vérifié

- Les références PDF de **294 extraits candidats positifs** ont été contrôlées dans les pages du corpus. Les citations originales du jeu 2021/110 sont conservées ; les 28 passages retenus depuis le supplément 2023–2024 ont été remplacés par des extraits lisibles directement récupérés dans les PDF.
- Deux associations supplémentaires ont été **écartées des positifs** car elles ne répondaient pas à la période/au sens de la question.
- Une association avait **la mauvaise page PDF** (ménages modestes/aisés en juillet 2024, page 8 et non 9) : corrigée.
- Une nouvelle preuve **de janvier 2022** a été ajoutée à la question issue de 2021 sur l'inflation pendant la réouverture. Cela montre pourquoi les jugements doivent porter sur **toutes les années**.
- Les **294 extraits** couvrent **279 couples question–page distincts** : des passages différents se trouvent parfois sur la même page ; ils ne doivent pas augmenter artificiellement les scores.
- Les **145 questions**, leurs IDs et leurs trois ensembles sont figés dans les exports. Les catégories sont proposées : 68 factuelles, 42 explicatives, 31 comparatives et 4 multi-documents comme catégorie principale (plusieurs comparatives sont également multi-documents).

## Ce qui n'est pas démontré

**Vérifier qu'une citation apparaît dans un PDF n'est pas démontrer que toutes les preuves existantes ont été identifiées.** Nous pouvons vérifier le texte, la date, la page et corriger les incohérences apparentes ; nous **ne pouvons pas garantir des qrels gold exhaustifs par comparaison textuelle seule**. Il faut deux annotateurs indépendants, une adjudication des divergences, et la revue de candidats BM25, Dense et Hybride de toutes les années (pooling).

Les grades 1/2 dans `silver_qrels_PAGES.csv` sont **provisoires**, et aucun grade 0 n'est déduit d'un passage absent de la liste. Pour l'évaluation scientifique finale, utilisez le modèle `qrels_double_annotation_TEMPLATE.csv` enrichi par le pooling ; renseignez des grades 0 explicites après examen. Les métriques silver ne sont que des résultats de diagnostic sur des **positifs connus**.

## Corrections individuelles principales

| Élément | Constat | Action |
|---|---|---|
| FOMC_021 | Question 2021 demandant des déséquilibres particuliers non détaillés par la preuve ; risque d'ignorer 2022 | Reformulation + communiqué de janvier 2022 p.1 ajouté comme corroboration |
| FOMC_131 | Passage de 2024 utilisé pour une question sur juin 2023 | Exclu des positifs |
| FOMC_132 | Baisse des rendements de janvier 2024 utilisée pour expliquer une hausse en automne 2023 | Exclu des positifs |
| FOMC_133 | Preuve de juillet 2024 pour une question trop précisément limitée au début 2024 | Période reformulée : discussions de 2024 |
| FOMC_134 | Source exacte à la page 8 et non 9 | Page, citation et référence corrigées |
| FOMC_138 | Taux du repo et reverse repo incomplets dans le texte lemmatisé | Citations des deux décisions reconstituées depuis les PDF |
| FOMC_141 | Passage tronqué ne donnait que le taux maintenu | Citation agrandie au contexte macroéconomique |
| FOMC_144 | Conditions de prêts CRE 2024 | Textes originaux des quatre revues restaurés |

Le journal complet avec les motifs est dans `JOURNAL_CORRECTIONS.csv`.

## Biais et stratégie

1. **Biais d'année :** le corpus contient 93 PDF ; tous les récupérateurs doivent l'interroger sans filtre d'année, même pour une question créée à partir de 2021. Les passages d'autres années sont à juger si leur contenu répond au besoin exact.
2. **Biais d'annotation :** BM25/Dense/Hybride doivent fournir des pools de candidats avec les mêmes valeurs de k ; les résultats non annotés restent `UNJUDGED`. Une page contenant les mêmes mots ne suffit pas à être positive.
3. **Biais de paraphrase :** la version historique proposait surtout des variantes 2021 ; la version active utilise **une variante pour chacun des 30 besoins du test**, toutes années confondues.
4. **Biais de redondance :** les formulations répétées des communiqués (2 % inflation, données futures, etc.) exigent des annotations multiples ou des questions spécifiquement contextualisées.
5. **Granularité :** page = substitut de provenance stable. **Pas de fausse équivalence avec les chunks.** Pour publier Recall@k sur des chunks, annoter les chunks effectivement retournés (avec texte, page et offsets) et pas seulement leurs pages.

## Statut des fichiers

- `queries_145.jsonl` + `silver_qrels_PAGES.trec` : **prêts pour tests techniques et exploratoires**, pas pour score final gold.
- `qrels_double_annotation_TEMPLATE.csv` + `POOLING_TO_REVIEW_1740.csv` : **travail humain nécessaire**.
- `robustness_30_TEST_ONLY.jsonl` : 30 variantes à utiliser **après** avoir figé les modèles, en comparaison appariée avec les 30 questions de test.
- `unanswerable_10_NOT_GOLD.csv` : **candidats**, aucun jugement d'impossibilité certifié ; à utiliser pour évaluer l'abstention RAG **après vérification**.

**Limite :** l'étude de génération demandera en plus des réponses de référence validées, et des mesures de fidélité aux sources, non seulement des qrels de récupération.

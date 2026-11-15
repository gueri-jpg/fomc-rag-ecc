# Guide de validation de la verite terrain

## Pourquoi une annotation humaine est indispensable

Les 145 questions s'appuient sur des citations textuellement retrouvees dans les PDF; **ceci ne prouve pas** que chaque passage repond a la question, que son importance est identique ni que des preuves d'autres annees ont toutes ete trouvees. Il serait faux d'imposer une annee de provenance comme filtre aux nouveaux candidats.

## Procedure

1. L'agent charge le benchmark, produit les resultats top20 pour BM25, Dense et Hybrid sur les **93 PDF**, puis construit un pool deduplique. Ajouter les pages silver et d'autres passages trouves par des recherches complementaires, y compris annees differentes.
2. Un annotateur A juge sans voir les noms de modeles ni les scores; un annotateur B fait de meme independamment.
3. Label 0 : ne repond pas / hors sujet. Label 1 : information pertinente, mais seulement partielle pour la question. Label 2 : passage suffisant a lui seul pour repondre de facon exacte a la question. Si la question necessite plusieurs passages, ceux-ci peuvent tous valoir 1, et la **couverture des faits** reste une metrique separee.
4. En cas de desaccord, arbitrage trace par un tiers ou discussion documentee. Saisir les faits `required_facts` couverts par chaque passage.
5. Ajouter les passages valides hors annee, ne jamais supposer que page hors annee = negatif.
6. Exporter qrels de chunks ET qrels de pages (pour les diagnostics) ; conserver les non juges en `UNJUDGED`, jamais en 0 par defaut.
7. Verifier les questions dont la reponse varie selon l'annee ou dont les paraphrases changent les faits demandes; reformuler uniquement si une ambiguite factuelle l'exige, puis versionner modification du benchmark.
8. Calculer taux de couverture, desaccord et nombre de documents/pages juges par question et par annee.

## Criteres de validation du benchmark gold

- Deux jugements effectifs + arbitrage ; preuves supplementaires des six annees revues ; decisions de pertinence documentees ; aucun label automatiquement attribue en fonction du nom de PDF ou de l'origine du groupe ; les comparaisons utilisent les memes jugements.
- Les qrels gold ne doivent **pas** etre construits uniquement en prenant les 294 citations positives initiales, ou en notant 0 tous les autres.
- Les dix candidates non-repondables ne sont gold qu'apres une recherche ciblee et une verification humaine de l'absence de preuve dans le corpus fixe.

## Role des scripts fournis

Le repertoire `evaluation/benchmark` contient `make_chunk_pool.py`, `gold_qrels_builder.py` et des fichiers `qrels_double_annotation_TEMPLATE.csv`, `POOLING_TO_REVIEW_1740.csv`. Lire leur schema, les tester, puis les adapter aux resultats courants du pipeline; **ne pas supposer qu'ils couvrent automatiquement toutes les variantes de colonnes ou que le pool TF-IDF est complet**.

# Phase 3 — indexation et récupération documentaire

Date : 15 novembre 2026. Phase exécutée sur `feature/retrieval` à partir de
`main` intégrant la fusion de PR #1, commit
`4236a3fd186393d9bfc6e0f386d46850e18aafd5`. L'arbre était propre au départ.
La mission autorise uniquement BM25, Dense MiniLM et Hybrid RRF, sans reranking.

## Résultat et périmètre

Pipeline exécuté sur les **93 PDF, 838 pages et 2 127 chunks baseline**,
2021–2026, sans filtre de date/année/type. Les trois systèmes partagent les
mêmes identifiants, textes sources et métadonnées. Les neuf exports de corpus,
leur manifeste et les deux fichiers de qrels sont inchangés par rapport au
snapshot local de phase 2 : 12 empreintes identiques. Les 279 jugements
(188 grade 2, 91 grade 1), les 145 questions et leurs partitions sont conservés.

Expériences : **83 dev éligibles**, puis **30 validation en une seule passe**.
FOMC_044 et FOMC_129 sont exclus de la sélection, aucun de leurs documents ne
l'est. Aucune inférence, recherche, métrique ou analyse de retrieval sur les
30 questions test ou leurs paraphrases. Les six paraphrases en attente et les
dix candidats sans réponse restent inchangés et désactivés.

La recommandation de développement est **BM25 L0, k1=1,2, b=0,75**.
Hybrid retient **RRF k=10**, profondeur 100 par composant. Dense utilise le
checkpoint officiel `sentence-transformers/all-MiniLM-L12-v2`, sans apprentissage.
La supériorité réelle de pertinence demeure incertaine avec ces qrels incomplets.

## Architecture, protocole et prévention des fuites

Modules : `indexing.py` vérifie et charge le corpus, construit les vues/caches ;
`retrieval.py` implémente BM25 et RRF ; `dense.py` gère le modèle et les
embeddings ; `retrieval_evaluation.py` calcule les diagnostics ;
`retrieval_experiments.py` orchestre les calculs et exports ;
`retrieval_reporting.py` relit les résultats, agrège et construit le pool.
Aucun traitement lourd à l'import. Les retrievers reçoivent uniquement du
texte de question : aucune réponse, annotation ou sélection de page attendue.
Les grades entrent uniquement dans l'évaluation des IDs autorisés.

`require_tuning_eligible()` compare désormais les IDs au split figé réel,
au-delà de la cardinalité. Des injections d'IDs test dans dev et validation
sont rejetées. Le CLI de phase 3 n'accepte que dev et validation ; le test reste
interdit même si un futur artefact de gel existe. L'ancien évaluateur générique
exige une validation humaine explicite pour test/all. Aucun tel gel autorisant
le test n'a été créé.

Configuration et procédure préenregistrées dans le commit **b1854a0**, avant
le premier retrieval réel. Grille BM25, dans l'ordre : (1,5;0,75),
(1,2;0,75), (1,5;0,5). Grille RRF : 60,10,30,100. Critère lexicographique
sur dev seulement : couverture connue moyenne à cinq chunks, puis hit connu,
puis rang réciproque de la première page positive ; tolérance 1e-12, première
configuration déclarée en cas d'égalité. Tous les objectifs de grille sont
conservés dans `reports/retrieval_phase3/dev_selection.json`.

L'artefact de sélection a été écrit **avant** validation, lié au corpus, à la
politique d'embargo, au modèle et à l'environnement. Il porte explicitement
`human_validated=false`, `test_authorized=false`, `validation_consulted=false`.
Après la validation, une protection supplémentaire refuse aussi de recommencer
la sélection dev dans la même expérience. Aucun nouveau calcul de sélection
n'a été effectué après lecture de validation. Les rapports se régénèrent sans
inférence ni nouvel usage de validation pour les paramètres.

Config ID : `342417c8c40e38ca523408777042324d6fa9d2e275b7ab33b62b98108b72c5e8`.
Corpus version : `b43f21bc24da3f85913bdf7e1d6d03dbbeb1d013145f2233b9162f6937fcc052`.
Hash chunks : `0489ac8494e25d06b282548f55a4c845c1be2a64f1dbf45a9987145ab049cbb5`.
Le risque résiduel d'exposition humaine aux constats cross-split antérieurs
n'est pas supprimé par l'embargo. Les tailles nominales restent 85/30/30.

## Détails des récupérateurs

BM25 utilise les `bm25_tokens` existants et la même tokenisation des requêtes,
sans suppression de négations/nombres/taux/dates. IDF positive lissée :
`ln(1+(N-df+0,5)/(df+0,5))`. Fréquence des termes de requête conservée ;
normalisation standard k1/b de la longueur des chunks. Aucun paquet rank-bm25
n'est nécessaire. Formule complète dans `docs/retrieval_methodology.md`.

Dense : Python **3.13.14**, Torch **2.9.0+cpu**, sentence-transformers **5.1.2**,
Transformers **4.57.1**, NumPy **2.5.4**, CPU float32, quatre threads Torch,
lots de 16, seed 20261115. Embeddings 384 dimensions normalisés L2, recherche
exacte par produit scalaire, équivalent au cosinus. Chargement local,
`trust_remote_code=false`, aucune API d'inférence. Révision officielle verrouillée :
`a50ef00143b4d5391434df20ae11632588ac25be` ; onze fichiers vérifiés par SHA256
dans `configs/dense_model_lock.json`.

**Anomalie importante : la configuration effectivement enregistrée dans ce
checkpoint (`sentence_bert_config.json`) fixe max_seq_length=128.** Elle n'a
pas été remplacée par une limite supposée de 256/512. Les 2 127 chunks font
22–475 tokens avant troncature, médiane 320, p95 386,7. **1 955 chunks,
soit 91,91 %, sont tronqués** ; 362 573 tokens sur 625 100 sont au-delà de
la limite. Les tokens spéciaux sont inclus dans ces décomptes. Les requêtes
ne sont pas tronquées (dev 14–36 tokens, validation 16–29). Dense ne représente
donc pas intégralement la plupart des chunks. Cette limite concerne aussi
sa contribution à Hybrid. Son effet causal n'est pas isolé dans cette phase.

Hybrid additionne `1/(rrf_k+rang)` sur les top-100 BM25 L0 et Dense. Union
au plus 200 chunks ; les autres ont un score nul dans l'export complet.
Les rangs et contributions des composants sont enregistrés. Tous les tris
utilisent le score décroissant puis chunk_id lexicographique. Aucun reranker.

Caches locaux adressés par contenu : textes/IDs/corpus/versions/code,
normalisation et modèle. Les matrices NPY sont SHA-vérifiées, dimensions,
valeurs finies et normes contrôlées, chargement sans pickle. Les poids, caches,
index, corpus extrait et classements textuels ne sont pas publiés.

## Résultats réels — jugements incomplets

Budget principal : **les cinq premiers chunks**, pages dédupliquées dans cet
ordre (`page-coverage-from-chunk@5`). Couverture = fraction des pages positives
**connues** retrouvées ; hit = présence d'au moins une telle page. Ces valeurs
ne sont ni Recall exhaustif, ni précision, ni preuve de suffisance du chunk.

| Split / méthode | Couverture connue @5 | Hit connu @5 | RR première page connue @5 | seed-nDCG @5 conditionnel | Pages non jugées (moyenne des proportions) |
|---|---:|---:|---:|---:|---:|
| Dev BM25 | 31,73 % | 44,58 % | 0,2781 | 0,2528 | 88,88 % |
| Dev Dense | 14,86 % | 28,92 % | 0,1741 | 0,1228 | 93,98 % |
| Dev Hybrid | 30,42 % | 43,37 % | 0,2938 | 0,2501 | 89,88 % |
| Validation BM25 | 35,56 % | 43,33 % | 0,3139 | 0,2875 | 89,50 % |
| Validation Dense | 10,56 % | 20,00 % | 0,1000 | 0,0779 | 96,00 % |
| Validation Hybrid | 27,78 % | 40,00 % | 0,2011 | 0,1878 | 91,17 % |

Le rang est un rang de **page unique**, pas de chunk ; le RR vaut zéro si
aucune page positive connue n'est dans le budget. La moyenne de rang parmi
les seuls hits est exportée séparément. seed-nDCG utilise gains 2^grade−1,
discount logarithmique et idéal des seuls positifs connus ; l'absence de grade
contribue zéro au diagnostic, **sans créer d'annotation négative**. Ce diagnostic
conditionnel n'est pas une nDCG gold et n'est pas garanti borne inférieure de
la vraie nDCG avec labels complets.

Les 80 agrégats et 4 520 lignes question/méthode/budget couvrent k=1,3,5,10,20,
avec les deux conventions. Pour `unique-page@5`, la couverture BM25/Dense ne
change pas ; Hybrid dev atteint 31,02 % au lieu de 30,42 %, en consommant
5,12 chunks en moyenne. En validation, Hybrid reste à 27,78 % pour 5,13 chunks.
La convention pages donne donc un budget de chunks différent, explicitement
mesuré. `chunk@k` ne reçoit aucune métrique de pertinence depuis les qrels pages.

Diversité @5 : BM25 dev 4,83 pages et 4,52 documents ; Dense 4,95 et 4,61 ;
Hybrid 4,89 et 4,55. En validation : BM25 4,80/4,53, Dense 4,97/4,47,
Hybrid 4,87/4,53. `sources_top20.csv` détaille chaque année et type.
`known_coverage_by_source.csv` stratifie aussi les positifs connus par année/type
de source : effectifs de besoins, pages connues et retrouvées, couverture macro
par besoin et micro par page connue. Ces sous-groupes peuvent se recouvrir pour
une question multi-source ; ils décrivent les résultats sans filtrer la recherche.

Bootstrap apparié par question, 2 000 rééchantillonnages, seed fixe, IC
percentile 95 %, descriptif sans correction de multiplicité :

| Différence de couverture @5 | Dev [IC 95 %] | Validation [IC 95 %] |
|---|---:|---:|
| Hybrid − BM25 | −1,31 points [−7,43 ; +4,22] | −7,78 points [−20,56 ; +3,33] |
| Dense − BM25 | −16,87 points [−25,70 ; −9,33] | −25,00 points [−42,78 ; −9,44] |
| Hybrid − Dense | +15,56 points [+8,63 ; +23,29] | +17,22 points [+5,00 ; +31,68] |

Les IC Hybrid/BM25 incluent zéro. Les résultats dev ont servi au tuning et ne
sont pas une estimation indépendante de généralisation. Les IC ne corrigent ni
les labels manquants, ni le biais du référentiel, ni la petite validation de
30 besoins. Les résultats plus faibles de Dense concernent **cette configuration
tronquée** ; ils n'établissent pas une infériorité générale des modèles denses.

## Ablation des césures

L0 reste inchangée. L1 corrige uniquement les césures visibles suivies d'un
saut de ligne dans les vrais offsets raw du chunk, avec huit composés protégés
préexistants. Reconstruction L0 vérifiée sur les 2 127 spans : zéro différence
et aucun soft hyphen dans ces spans. **1 240 chunks modifiés**, 9 010 jointures
et 39 occurrences protégées **en comptant les overlaps** ; ces décomptes ne
doivent pas être confondus avec les 7 877 césures uniques du diagnostic phase 2.

Mêmes k1/b retenus, requêtes, corpus et budgets. Texte naturel, IDs, Dense et
Hybrid L0 inchangés. Couverture @5 L1 : dev 31,12 % (−0,60 point), validation
33,89 % (−1,67 point). Zéro gain et une perte de couverture par split ;
certains rangs s'améliorent (FOMC_005 : 3→2 ; FOMC_132 : 2→1).
La préférence **L0 a été choisie sur dev**, pas sur validation. Des composés
non protégés peuvent être fusionnés à tort ; L1 n'est pas adoptée par défaut.

## Pool et analyse des erreurs

Union réelle des top-20 BM25/Dense/Hybrid, dédupliquée par question et unité :

| Split | Chunks candidats | Pages candidates | Pages déjà jugées | Nouvelles pages UNJUDGED |
|---|---:|---:|---:|---:|
| Dev | 3 100 | 2 842 | 86 | 2 756 |
| Validation | 1 110 | 1 003 | 28 | 975 |

Les 114 couples déjà jugés présents dans ce pool ne sont pas renvoyés à
l'annotation ; les 165 autres jugements originaux restent intacts, qu'ils
appartiennent au test, aux questions sous embargo ou soient hors pool.
Les **4 210 candidats chunks restent UNJUDGED au niveau chunk**, même lorsque
leur page a un grade. Aucun grade 0 ou positif n'a été créé. Les pools complets
restent dans `artifacts/phase3/{dev,validation}/top20_*_pool.jsonl`.

La file publique `new_pages_review_queue.csv` contient **3 731 couples
question–page nouveaux**, avec PDF, chunks, méthodes, rangs et statut UNJUDGED.
Priorité transparente : 100/(1+meilleur rang de chunk), +5 si l'année de la
source diffère d'une année explicitement écrite dans la question. Sans année
explicite, aucun écart n'est déduit des réponses ou qrels. Ce signal ne filtre
pas l'index et ne constitue pas un jugement de pertinence. Une validation
humaine supplémentaire est nécessaire avant toute prétention d'exhaustivité.

`reports/retrieval_phase3/ERROR_ANALYSIS.md` et `error_cases.csv` présentent
20 cas réels : répétitions de langage économique, confusions de réunions/taux,
décalages lexicaux, preuves multiples, césures et pertes/gains RRF. Exemple :
FOMC_084, deux chunks distincts d'une même page soutiennent les composants,
mais leur accord de page ne se cumule pas en RRF de chunks. FOMC_132 conserve
la réserve phase 2 sur l'extrait réparti : un hit page ne certifie pas les faits.
Aucune note qualitative n'est importée comme nouveau grade.

## Ressources et latences mesurées

Windows, CPU uniquement (roue Torch CPU, huit processeurs logiques disponibles,
quatre threads Torch), pas de GPU utilisé. Encodage documentaire initial :
**160,61 s**. Validation réutilise exactement la matrice SHA
`49be8495d38a41be9c591d9294d37962ac1226705a7282adf834746539b5f358`,
chargement/contrôle du cache **0,040 s**. Matrice seule : 3 267 200 octets ;
matrice + métadonnées : 3 694 865 octets. Onze fichiers modèle :
134 205 111 octets. Vues lexicales sérialisées : environ 7,07 Mo chacune ;
ce sont des caches de tokens, pas des postings persistés. Construction des
postings BM25 sélectionné : dev 0,163 s, validation 0,351 s. Hybrid ne possède
pas d'index documentaire distinct : listes des deux composants et fusion à la
requête. Sa taille d'index supplémentaire persisté est nulle.

Chargement du checkpoint dans SentenceTransformer : 0,212 s dev / 0,227 s val.
Ce temps **exclut l'import initial de Torch et le démarrage Python** ; ce n'est
pas le temps de démarrage à froid d'une application. Pic de working set du
processus mesuré par Windows GetProcessMemoryInfo : 560 709 632 octets dev,
617 095 168 octets val. Ces pics globaux n'isolent pas chaque méthode.

| Split / méthode | Requête fraîche p50 / p95 (ms) | Répétition p50 / p95 (ms) |
|---|---:|---:|
| Dev BM25 | 6,41 / 10,58 | 6,52 / 10,91 |
| Dev Dense | 63,19 / 99,09 | 60,99 / 104,86 |
| Dev Hybrid | 71,92 / 110,04 | 71,29 / 113,00 |
| Validation BM25 | 5,22 / 9,10 | 4,75 / 10,03 |
| Validation Dense | 42,64 / 64,47 | 40,11 / 59,13 |
| Validation Hybrid | 50,37 / 72,49 | 46,84 / 67,18 |

Modèle/index déjà chargés, aucune mise en cache des requêtes ; une seconde
inférence identique vérifie le classement. Les requêtes précédentes peuvent
chauffer les noyaux CPU : « fraîche » n'est pas un processus froid par question.
Hybrid mesure la **somme sérielle des temps sources et fusion**, pas une
latence de service parallèle mesurée séparément. I/O des exports hors mesure.
Les écarts entre splits peuvent refléter charge et échauffement, pas la seule
complexité des questions. Fichiers détaillés : `latencies.csv`, `summary.json`.

## Graphiques et livrables

Cinq figures réelles sous `reports/figures/phase3_*` : couverture selon budget
avec IC descriptifs, latences p50/p95, différences appariées, troncature et
années des sources retrouvées. Les tableaux réutilisables sont sous
`reports/retrieval_phase3/`, les résultats lourds sous `artifacts/phase3/`.
Pour chaque méthode et split : scores/rangs **complets des 2 127 chunks** dans
`METHOD_complete.npz`, IDs ordonnés inclus ; top-100 avec texte/provenance,
scores/rangs/contributions/latences dans `METHOD.jsonl`, métadonnées séparées.
La cohérence NPZ/JSONL, le tri déterministe, les IDs des requêtes, les offsets
et les versions sont vérifiés lors de la génération du rapport.

## Commandes et contrôles exécutés

Toutes les commandes Python ont utilisé `.venv\Scripts\python.exe` de Python
3.13.14. La résolution binaire et les imports ont précédé les calculs ; aucune
réparation de Python 3.12. Dépendances ML choisies explicitement et roue Torch
CPU téléchargée depuis l'index officiel. Un téléchargement SciPy a nécessité
une reprise réseau ; installation et vérification finales réussies.

Sur un clone frais, restaurer les 93 PDF et régénérer les exports phase 1
comme dans README, puis exécuter depuis la racine du projet :

```powershell
& .venv\Scripts\python.exe -m pip install -r requirements-phase3.lock.txt
& .venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
& .venv\Scripts\python.exe -m pip check
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
& .venv\Scripts\python.exe scripts/verify_kit_v2.py
& .venv\Scripts\python.exe scripts/download_minilm.py
& .venv\Scripts\python.exe scripts/run_retrieval_phase3.py --stage dev
& .venv\Scripts\python.exe scripts/run_retrieval_phase3.py --stage validation
& .venv\Scripts\python.exe scripts/report_retrieval_phase3.py
& .venv\Scripts\python.exe -m pytest -q
```

Les deux commandes d'inférence ne se relancent pas sur une expérience contenant
déjà `validation/completed.json` ; c'est un garde-fou volontaire. Dans cet
espace de travail, régénérer seulement le rapport relit les calculs sauvegardés,
sans nouvelle passe validation. Sur un autre système les scores devraient
être reproductibles dans l'environnement verrouillé ; les temps/mémoire ne
sont pas garantis identiques. Les wheels CPU Windows 3.13 sont celles vérifiées,
pas une certification de toutes les plateformes.

Contrôles exécutés :

- `pytest -q` : **80 tests réussis**, phases 0–2 et nouveaux tests, modèle réel
  et corpus local inclus. Cache corrompu rejeté, changement de version
  invalidant le cache, troncature et norme/dimension testés.
- Suite légère sans PDF/modèle : **57 tests réussis** ; cible CI mise à jour.
- Preflight avec hashes des 93 PDF : **PASS**, seul avertissement `.env` local
  présent (contenu jamais affiché, fichier ignoré et non publié).
- Vérification kit V2 : **PASS**. `pip check` : **aucune dépendance cassée**.
- Comparaison des 12 SHA au snapshot phase 2 : **PASS**, voir
  `baseline_integrity.json`. Les SHA des qrels CSV/TREC sont aussi testés.
- Régénération des tableaux, pools et cinq figures depuis les classements
  sauvegardés : **identiques octet par octet**, sans nouvelle inférence.
- Première génération des graphiques : cache matplotlib utilisateur refusé
  par le sandbox ; figures produites via cache temporaire, puis configuration
  corrigée vers `artifacts/matplotlib` dans l'espace de travail et régénération
  réussie. La mesure mémoire par CIM était indisponible ; API processus Windows
  utilisée avec repli explicite si indisponible.

L'audit heuristique des blobs préparés : **PASS, aucune alerte** ;
`git diff --cached --check` : **PASS** après retrait d'une ligne vide finale.
Les poids, index et classements détaillés restent ignorés ; seuls
code, configurations, tableaux légers, file de revue et graphiques sont proposés.

## Décision pour la suite et arrêt

BM25 L0 sélectionné sur dev est le candidat recommandé pour la future phase 4,
avec conservation de Dense et Hybrid comme comparaisons et futures sources de
candidats sous protocole commun. Les IC et labels incomplets interdisent de
proclamer un vainqueur universel. Toute étude de limite Dense différente devra
être annoncée comme nouvelle expérience, sans réutiliser discrètement cette
validation pour la sélectionner. Les nouveaux candidats attendent de véritables
jugements humains ; aucun résultat final gold n'est revendiqué.

Références techniques : [checkpoint officiel MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)
et [API officielle SentenceTransformer](https://sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html).
La configuration locale et les SHA font foi pour la limite effectivement exécutée.

**Arrêt en fin de phase 3.** Pas de CrossEncoder/BGE, génération RAG, Streamlit,
expérience test, fusion automatique ou phase suivante.

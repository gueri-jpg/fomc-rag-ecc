# Phase 1 — Corpus, extraction PDF, prétraitement, EDA et chunking

Date : 15 novembre 2026. Périmètre autorisé : phase 1 uniquement.
Racine : `<project-root>`.
Interpréteur exclusif : `.venv\Scripts\python.exe`, Python 3.13.14 Windows x64.

## Résultat et critères d'acceptation

Le pipeline est exécuté sur **93 PDF / 838 pages physiques** : 46 Minutes
(661 pages) et 47 Statements (177 pages), couvrant les six années 2021–2026.
Les SHA256 des originaux concordent avant/après extraction. Aucune erreur
d'extraction, page vide, modification ou déplacement des PDF.

Le baseline commun futur BM25/Dense/Hybride contient **2 127 chunks de 256 mots
maximum, overlap 40**, séparés par page. Les exports 128 et 512 mots contiennent
4 563 et 1 124 chunks. La couverture de chaque mot est vérifiée automatiquement.
Neuf exports sont reproductibles à l'octet près lors d'une seconde ingestion.
Sept graphiques et 18 tableaux CSV décrivent le corpus; les résultats sont
expliqués dans `reports/eda/OBSERVATIONS.md`.

Les 279 jugements validés sont inchangés (hashes contrôlés par les tests).
Les 145 questions gardent leurs splits 85/30/30; les 30 paraphrases restent
réservées au test après gel et les dix candidates sans réponse désactivées.
Le pipeline n'ouvre ni questions, ni preuves de référence, ni qrels pour
construire les pages/chunks. Aucun tuning, retrieval, reranking, téléchargement
de modèle, génération ou lancement Streamlit.

## Lectures, état initial et dépendances

Les sept lectures demandées ont été réalisées intégralement, ainsi que les
autres lectures obligatoires de `AGENTS.md` et le texte joint à la demande.
La mention « phase 0 uniquement » du prompt maître est dépassée par
l'autorisation explicite de phase 1 donnée par l'utilisateur.

Git demeure sur main, sans commit ni remote. Le prérequis indicatif « état
Git propre » n'était pas satisfait : les fichiers de phase 0 étaient encore
non suivis, comme consigné dans son rapport validé. Aucun commit automatique
n'a été créé; les fichiers existants et le prototype ont été préservés.

Seules PyMuPDF 1.28.2 et matplotlib 3.11.2 et leurs dépendances transitives
ont été installées après résolution binaire compatible Windows/Python 3.13.
NumPy sert aux quantiles; CSV/JSON et fréquences utilisent la bibliothèque
standard. Pas de pandas, spaCy/NLTK, sentence-transformers, rank-bm25,
Streamlit ou PostgreSQL installé. `requirements-phase1.lock.txt` fige
l'environnement effectif complet, outils de tests inclus. PyPI n'est requis
que pour l'installation; traitement, EDA et tests sont locaux.

## Code et exports

Fichiers créés :

- `src/fomcrag/storage.py` : JSON/JSONL UTF-8 déterministes, hashes de fichiers.
- `src/fomcrag/corpus.py` : inventaire strict, métadonnées, vérification SHA,
  ouverture PyMuPDF en lecture seule, comptage physique, extraction par page,
  blocs avec coordonnées, détection d'erreurs et conservation du brut.
- `src/fomcrag/preprocessing.py` : vue naturelle et lexicale distinctes,
  normalisation conservatrice, transformations tracées et mapping d'offsets.
- `src/fomcrag/chunking.py` : fenêtres paramétrables, offsets, provenance,
  IDs déterministes, versions corpus/chunking/index.
- `src/fomcrag/ingestion.py` : orchestration sans labels, exports avec marqueur
  final de validité, rapport d'échec et séparation des mesures temporelles.
- `src/fomcrag/eda.py` : analyses et graphiques reproductibles.
- `scripts/ingest.py`, `scripts/eda.py`, `scripts/render_source_checks.py`,
  `scripts/verify_phase1.py` : commandes de reproduction et contrôles.
- `configs/corpus_phase1.json`, `requirements-phase1.lock.txt`.
- `tests/test_corpus_phase1.py`, `tests/test_eda_phase1.py`.
- `docs/corpus_preprocessing.md`, `reports/eda/*`,
  `reports/figures/phase1_*.png`, trois captures de pages sources et ce rapport.

Fichiers mis à jour : `.gitignore` (exports et cache graphique),
`pyproject.toml` (extra corpus minimal), `README.md`, `docs/architecture.md`,
`docs/decision_log.md`. Les fichiers de référence du kit, les PDF, les
annotations et les scripts `utils/` n'ont pas été modifiés.

Exports régénérables, ignorés par Git, sous `data/processed/` :

| Export | Contenu |
|---|---|
| documents.jsonl | 93 identités, dates, types, pages physiques, longueurs, SHA |
| pages.jsonl | 838 pages, texte brut/lisible, blocs PDF, mapping clean/raw |
| chunks_128/256/512.jsonl | Texte exact, tokens lexicaux séparés, provenance, versions |
| page_chunk_map_128/256/512.jsonl | Relation page/chunk/offsets sans question ni grade |
| extraction_issues.jsonl | Alertes de normalisation ou extraction |
| manifest.json | Version, configuration, dépendances, SHA/taille des neuf exports |
| config.json / run.json | Configuration effective / durées et environnement |

Les neuf exports représentent 47 298 103 octets (environ 45,1 Mio), hors
manifestes et reproduction isolée sous `artifacts/`.

Le manifeste est publié uniquement après succès complet. En cas d'échec, il
est retiré et `failure.json` est écrit; d'éventuels exports partiels restants
ne doivent pas être consommés. Pas d'ingestions concurrentes dans la même
destination. Toutes les relances recalculent les sorties; aucun cache ancien
n'est réutilisé silencieusement.

## Prétraitement et provenance

Le texte natif PyMuPDF, `sort=False`, est conservé intégralement dans
`raw_text`. La vue lisible réunit les espaces/sauts de ligne, retire les
césures discrétionnaires U+00AD et conserve chiffres, dates, taux, signes,
ponctuation, négations et casse. Les traits visibles en fin de ligne sont
conservés et la coupure jointe sans espace; option agressive `join` disponible
mais non activée. Les en-têtes, pieds, notes, couvertures et répétitions ne
sont pas supprimés. Aucun texte source n'est remplacé par un contenu deviné.

Les tokens BM25 sont une représentation **séparée**, casefold + regex
Unicode, sans suppression de stopwords/lemmatisation. Les tests couvrent
`not`, `no`, contractions, décimales, pourcentages, signes négatifs, dates,
composés et fractions. Les mots de chunking sont des séquences non blanches,
pas des wordpieces d'un tokenizer neural.

Chaque page/chunk garde document/document_id, source_pdf, date de fin de
réunion, année, type, page physique, page_id et SHA source. Les chunks gardent
page_start=page_end et offsets Unicode `[char_start,char_end)` dans le texte
lisible, offsets bruts correspondants, word_start/end et configuration.
La convention `meeting_date` est la date du nom de fichier, explicitement
tracée; ce n'est pas la date de publication des Minutes.

Le `chunk_id` SHA256 dépend du document et de son hash, page, offsets, texte,
configuration et corpus_version. `corpus_version` inclut sources, extraction,
version PyMuPDF et hashes du code. `index_version` prépare l'invalidation des
caches futurs, sans construire d'index de recherche. Version effectivement
produite : `b43f21bc24da3f85913bdf7e1d6d03dbbeb1d013145f2233b9162f6937fcc052`.

Les maps page→chunk préparent l'alignement futur des références sans lire
les extraits ou attribuer de labels. Le matching des 294 extraits et les
jugements au niveau chunk relèvent de la phase 2; ils ne sont pas présentés
comme réalisés ici.

## Choix de segmentation et mesures

256 mots / overlap 40 est le baseline du kit, pas une configuration choisie
après observation du test. Le stride est W−40; on s'arrête dès que la fenêtre
atteint la fin de page. Tous les mots sont couverts, aucune fenêtre ne
traverse une page ou un document, aucun padding ni fragment supprimé.

| Fenêtre | Chunks | Min / max mots | Moyenne | Médiane | <40 mots | Facteur de volume mots |
|---|---:|---|---:|---:|---:|---:|
| 128 | 4 563 | 14 / 128 | 120,18 | 128 | 17 | 1,3731 |
| 256 | 2 127 | 14 / 256 | 212,00 | 256 | 17 | 1,1291 |
| 512 | 1 124 | 14 / 512 | 365,49 | 383 | 17 | 1,0286 |

Pour le baseline, P05=57, P25=168, P75=P95=256 mots. Les 17 fragments courts
proviennent des 16 pages très courtes et d'une page de 37 mots. Les conserver
préserve le corpus; ils peuvent produire des candidats peu informatifs.
La segmentation par mots ne garantit pas de rester sous le budget wordpieces
d'un futur encodeur : contrôle à faire avant les embeddings en phase 3.

La première exécution de la version finale a mesuré 7,55 s d'inventaire et
extraction, 11,05 s de traitement total (extraction + exports/chunking), selon
`data/processed/run.json`. Ce sont des mesures locales d'un lancement,
pas des latences retrieval ni un benchmark matériel; les relances ont des
durées différentes et restent séparées des fichiers déterministes.

## EDA observée et qualité

Voir `reports/eda/OBSERVATIONS.md` pour l'interprétation complète et
`reports/eda/summary.json` pour les quantiles et statistiques réutilisables.

| Année | Minutes PDF / pages | Statements PDF / pages |
|---|---|---|
| 2021 | 8 / 113 | 8 / 33 |
| 2022 | 8 / 104 | 8 / 32 |
| 2023 | 8 / 87 | 8 / 32 |
| 2024 | 8 / 109 | 8 / 32 |
| 2025 | 8 / 150 | 8 / 31 |
| 2026 | 6 / 98 | 7 / 17 |

399 374 mots de segmentation au total, dont 360 800 dans les Minutes et
38 574 dans les Statements. Pages : 14–855 mots, médiane 455, moyenne 476,58.
Documents : 498–13 654 mots; 2–21 pages. 2026 est partielle : Minutes jusqu'au
16 septembre, Statements jusqu'au 28 octobre. Les volumes bruts par année
ne sont donc pas comparables comme indicateurs de fréquence thématique.

- **0 page vide, 0 erreur d'extraction et 0 caractère U+FFFD.**
- **16 pages <30 mots** : 15 couvertures et une fin de liste de participants.
  Elles ne sont ni retirées ni assimilées à des échecs d'extraction.
- **75 glyphes privés U+F0B7 sur 15 pages** : alertes typographiques,
  compatibles avec des puces Symbol; aucun mot économique reconstitué.
- **347 pages avec règles décoratives et sept avec longues URL**. Le premier
  diagnostic trop général « long_word » a été séparé pour éviter de présenter
  des lignes graphiques comme corruption linguistique.
- **7 877 césures visibles sur 401 pages**, conservées pour fidélité mais
  pouvant réduire le matching lexical. Exemples et transformations traçables.
- **Trois groupes de pages exactement identiques**, tailles 2, 22 et 2;
  aucun PDF identique par SHA256. **312 paires proches** au Jaccard ≥0,8 sur
  ensembles de 5-grammes lexicaux, incluant les exactes. Aucune suppression.
- **1 414 lignes présentes sur au moins trois pages**. Les formules de
  politique, procédures et listes de participants créent une redondance
  réelle; une petite différence de taux/date ne doit pas être écrasée.
- Termes fréquents : federal 3 638, inflation 3 381, participants 3 108,
  board 3 106, market 2 979. Les fréquences économiques et séquences exactes
  sont détaillées par page/année/type. Les stopwords supprimés dans un
  graphique descriptif ne sont jamais supprimés des entrées des modèles.

Sept PNG avec titres/axes/unités/légendes : répartition annuelle, distributions
de longueurs, mots fréquents, expressions économiques, longueurs des chunks,
chronologie mensuelle, comparaison par type et chunks baseline. Les figures
annuelles, de chunking et de mots fréquents ont été inspectées visuellement.
Leurs hashes et ceux des tables sont dans `reports/eda/manifest.json`.

## Vérification visuelle des originaux

Trois pages originales ont été rendues puis consultées visuellement, avec
neuf contrôles textuels reproductibles dans `source_check_values.json` :

| PDF / page physique | Valeurs observées et retrouvées dans l'extraction |
|---|---|
| fomcminutes20210127.pdf p.1 | Réunion 26–27 janvier 2021; reprise le 27 à 9:00 a.m. |
| monetary20240320a1.pdf p.1 | 20 mars 2024; fourchette 5-1/4 à 5-1/2 percent; cible 2 percent |
| monetary20261028a1.pdf p.1 | 28 octobre 2026; 3-3/4 à 4 percent; hausse dissidente 1/4 point |

Les captures sont sous `reports/figures/source_checks/`. Le contrôle 2021
confirme les deux colonnes mais révèle une limite d'ordre natif : une note
de bas de colonne peut interrompre le flux avant la colonne suivante.
Les coordonnées de blocs et le brut permettent de l'auditer. Ce spot-check
n'est pas une lecture humaine exhaustive ni une authentification externe
de tous les documents.

## Commandes exactes exécutées

Les lectures intégrales via `Get-Content -Encoding UTF8`, l'inventaire Git et
les commandes Python de diagnostic ont précédé les modifications. Commandes
de traitement et validation réellement exécutées (certaines relancées après
correction) :

```powershell
git status --short
& .venv\Scripts\python.exe -m pip list
& .venv\Scripts\python.exe -m pip --disable-pip-version-check install --dry-run --only-binary=:all: --report reports/progress/dependencies-phase1.json PyMuPDF==1.28.2 matplotlib==3.11.2
& .venv\Scripts\python.exe -m pip --disable-pip-version-check install --only-binary=:all: PyMuPDF==1.28.2 matplotlib==3.11.2
& .venv\Scripts\python.exe scripts/ingest.py
& .venv\Scripts\python.exe scripts/eda.py
& .venv\Scripts\python.exe scripts/render_source_checks.py
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe scripts/verify_phase1.py --rebuild
& .venv\Scripts\python.exe scripts/verify_phase1.py --rebuild --eda-rebuild
& .venv\Scripts\python.exe -m pip freeze --exclude fomcrag
& .venv\Scripts\python.exe -m pip --disable-pip-version-check install --no-build-isolation --no-deps -e .
& .venv\Scripts\python.exe -m pip check
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs --json-report reports/progress/preflight-phase1.json
& .venv\Scripts\python.exe scripts/verify_kit_v2.py
& .venv\Scripts\python.exe scripts/audit_security.py
& .venv\Scripts\python.exe -m pip --disable-pip-version-check install --dry-run --no-index -r requirements-phase1.lock.txt
git check-ignore data/processed/pages.jsonl reports/eda/_cache/matplotlib/fontlist.json .env references_local_only
Get-FileHash evaluation/benchmark/qrels_group_confirmed_PAGES.csv,evaluation/benchmark/qrels_group_confirmed_PAGES.trec -Algorithm SHA256
```

Reproduction depuis les PDF : installer le lock phase 1, installer le package
local, puis exécuter ingest → eda → render_source_checks → verify_phase1
--rebuild --eda-rebuild → pytest. Les commandes complètes sont dans le README
et `docs/corpus_preprocessing.md`.

## Tests, incidents corrigés et limites

Les tests couvrent extraction physique, page synthétique vide, PDF corrompu,
écart de pagination, SHA et PDF supplémentaires, types/dates/provenance,
UTF-8, signes/négations/nombres, mapping raw/clean, vide/un mot, paramètres
invalides, overlap, couverture intégrale, identifiants stables/invalidation,
non-mélange de documents, hashes des neuf exports, métadonnées de chaque
chunk, séparation des labels et intégrité des sorties EDA.

Incidents réellement rencontrés :

- Premier lancement : arrêt sécurisé car le manifeste dit `statement` au
  singulier, contrairement au type canonique `statements` du kit. Mapping
  explicite ajouté, valeur source conservée, manifeste original intact.
- Premier EDA : avertissement d'ACL du cache matplotlib Windows; le cache est
  désormais placé dans `reports/eda/_cache/`, ignoré par Git.
- Contrôles de qualité : séparation règles graphiques/longues URL et comptage
  des glyphes privés; pas de réparation textuelle inventée.
- Comptage des expressions économiques rendu strict aux frontières de tokens
  pour ne pas compter `inflation` à l'intérieur d'un composé. Un test de
  concordance fréquences/termes économiques protège ce comportement.

Les 21 premiers tests ont passé avant ajout du contrôle EDA; le contrôle final
comprend 22 tests. Les sorties finales détaillées sont consignées ci-dessous.

| Contrôle exécuté | Résultat final |
|---|---|
| pytest complet | **22 passed in 8.69s**, aucune erreur |
| Ingestion complète | PASS : 93 PDF, 838 pages physiques |
| Réingestion indépendante | PASS : neuf exports et manifeste identiques à l'octet |
| Reproduction EDA indépendante | PASS : 18 CSV et sept PNG aux mêmes SHA256 |
| Comparaison des versions | Même corpus_version pour corpus, chunks, EDA et reproduction |
| Spot-check | PASS : trois pages visualisées, neuf valeurs textuelles retrouvées |
| Preflight --hash-pdfs | PASS; seul avertissement : .env local présent, ignoré |
| Kit V2 | PASS : splits, jugements, preuves, variantes et candidates désactivées |
| pip check | No broken requirements found |
| Lock phase 1 hors ligne, dry-run | Tous les paquets déjà installés aux versions exactes |
| Sécurité texte | PASS : 96 fichiers publiables scannés, aucun motif de secret |
| Git ignore | .env, références locales, corpus dérivé et caches exclus |

Preuves machine : `reports/progress/phase1_verification.json`,
`preflight-phase1.json`, `dependencies-phase1.json`,
`reports/eda/manifest.json` et `data/processed/manifest.json`.

SHA256 des jugements validés, identiques à la phase 0 :

- CSV : `d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb`
- TREC : `9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682`

Risques scientifiques résiduels : texte économique répété entre réunions,
césures conservées, notes/colonnes, couverture courte, taille words≠wordpieces,
2026 partielle, qrels non exhaustifs. Aucune annotation humaine nouvelle,
aucun grade 0 implicite, aucune propagation de grade de page aux chunks,
aucune mesure de performance retrieval/LLM. La similarité cross-split des
questions et l'alignement des preuves attendent la phase 2.

**Arrêt à la fin de la phase 1.** Aucun blocage corpus identifié pour préparer
ultérieurement l'alignement, sous réserve des limites documentées.

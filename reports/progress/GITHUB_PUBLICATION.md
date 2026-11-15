# Publication GitHub — phases 0 et 1

Date : 15 novembre 2026. Publication expressément autorisée par le propriétaire.
Périmètre : préparer et publier le travail validé; aucune phase 2 ni expérience
de retrieval/reranking lancée.

## Dépôt et commits

- Dépôt public : https://github.com/gueri-jpg/fomc-rag-ecc
- Remote : `https://github.com/gueri-jpg/fomc-rag-ecc.git`.
- Branche publiée : `main`, suivi local `origin/main`.
- Commit initial de code : **`73a03911ce00c84f482d78a28d860c6c1aae3753`**.
- Message : `feat: establish reproducible FOMC RAG baseline (phases 0-1)`.
- Ce compte rendu est ajouté dans un second commit de documentation après
  vérification du commit initial distant. Son propre identifiant se consulte
  dans l'historique de `main`; il n'est pas auto-inséré dans son contenu.

Git local était initialisé mais sans commit et sans remote. Le compte GitHub
connecté correspond au propriétaire du dépôt; l'identité Git locale était déjà
configurée et concordante. Aucun nom/adresse inventé ou changement global
d'identité n'a été nécessaire. `origin` a été ajouté avec l'URL demandée.
`git ls-remote origin` a confirmé un dépôt vide avant le premier push; aucun
historique distant n'a été remplacé. Push normal via l'authentification Git
existante, sans token dans une commande, un rapport ou la conversation.

## Contenu publié

Le commit initial contient **137 fichiers**, **5 094 483 octets** de contenu.
Chaque chemin a été sélectionné explicitement, contrôlé dans l'index et relu
depuis une copie indépendante du dépôt public; les 137 blobs distants sont
identiques aux fichiers locaux inspectés. Ce rapport ajoute un fichier léger
de documentation, portant la sélection publique à 138 fichiers.

La sélection comprend :

- `src/fomcrag/` : huit modules du pipeline phase 1 et de sa configuration.
- `tests/` : les trois fichiers de tests (22 cas exécutés).
- `scripts/` : huit commandes d'ingestion, EDA, contrôles, audit et gestion
  des jugements; les aides historiques ne sont pas des expériences exécutées.
- `configs/` : trois configurations non sensibles.
- `docs/`, `project_spec/`, `prompts/` : architecture, choix techniques,
  protocole et consignes écrites de projet; aucun support de cours original.
- `evaluation/benchmark/` : 30 fichiers de questions, variantes, candidates
  désactivées, manifeste, provenance, qrels, statuts, gabarits et outils
  historiques. Les extraits FOMC sont attribués; aucun formulaire nominatif
  d'annotateur n'est fourni ou inventé.
- `reports/eda/` : 18 CSV, quatre JSON et les observations méthodologiques.
- `reports/figures/` : sept PNG de graphiques générés, sans capture de page PDF.
- `reports/progress/` : les deux rapports de phase expurgés des chemins
  personnels, trois résultats de contrôle machine et ce rapport de publication.
- `utils/` : huit scripts historiques conservés à l'identique, hors corpus.
- Fichiers racine : README anglais, CONTRIBUTING, règles du projet,
  `.gitignore`, `.gitattributes`, `.env.example` fictif, pyproject, deux locks,
  initialiseur et ancien script test. `app/` et `experiments/` contiennent
  seulement leur documentation de préparation.

L'état réel reste phases 0–1. Le README ne présente ni BM25, Dense, Hybrid,
rerankers, génération RAG ou Streamlit comme fonctionnels.

## Exclusions et sécurité

Les éléments suivants restent présents localement mais ne sont pas publiés :

- `.env` et toutes les vraies valeurs d'accès, `.venv`, credentials et clés.
- Les **93 PDF**, toute copie PDF et les trois captures de pages originales
  sous `reports/figures/source_checks/`.
- `references_local_only/` : supports pédagogiques privés et captures de cours.
- `data/processed/` : textes extraits et chunks; `artifacts/` : reproductions
  et traces locales de publication; poids, modèles, index, caches, bases, logs.
- `.vscode/` : configuration du poste; rapports pip `dependencies-phase*.json`
  contenant des chemins du poste; fichiers d'installation du kit et son ancien
  manifeste, non nécessaires à l'exécution du pipeline.

`.gitignore` a été renforcé pour les PDF, captures de sources, configuration
éditeur, rapports pip locaux et fichiers de passation du kit. Aucun fichier
source/PDF/résultat local n'a été supprimé. Les rapports PHASE_0 et PHASE_1
ont uniquement été expurgés des chemins et identifiants Windows inutiles;
leurs mesures et limites n'ont pas été modifiées.

`scripts/audit_security.py` conserve son audit existant et ajoute `--staged` :
lecture des **blobs de l'index**, y compris CSV/TREC et fichiers cachés;
détection de motifs de secrets, chemins Windows personnels, chemins interdits,
contenu PDF, binaires non approuvés et fichiers >5 Mio. Les seules images
acceptées sont les graphiques EDA explicitement sélectionnés. Aucun contenu
de `.env` n'a été ouvert, affiché ou copié.

Résultat sur les 137 fichiers indexés : **PASS, zéro motif de secret,
zéro chemin personnel, zéro fichier interdit, zéro fichier >5 Mio**. Plus gros
fichier : `reports/eda/chunks.csv`, 1 196 291 octets. La sélection de l'index
correspond exactement à la liste revue, sans ajout global de tous les fichiers.
Le contrôle n'est pas une garantie cryptographique d'absence de tout secret.

`.gitattributes` empêche les conversions de fins de ligne sur tous les fichiers
afin de conserver leurs SHA256 à chaque clone. Le contrôle d'espaces reconnaît
CRLF. Deux exceptions ciblées préservent les espaces de données du pool CSV et
du prototype historique `Pdf2Txt.py`; aucun qrel ou script legacy n'a été
réécrit pour satisfaire un simple contrôle de format.

## Données, droits et reproduction

Le [disclaimer du Federal Reserve Board](https://www.federalreserve.gov/disclaimer.htm)
a été consulté : les informations du site du Board sont dans le domaine public
sauf indication contraire, avec exceptions pour les contenus tiers. La
sélection publiée contient des extraits textuels FOMC attribués et les données
de benchmark/EDA du projet, autorisées par l'instruction de publication du
propriétaire. Les PDF, logos et copies de pages restent exclus.
Aucune licence logicielle ou du benchmark n'a été inventée : ce choix reste
à faire par les propriétaires. Les documents de cours privés ne sont pas
redistribués.

`docs/data_sources.md` indique les chemins de restauration et SHA256 attendus,
les archives officielles et les conventions d'URL. Tous les liens PDF n'ont pas
été téléchargés ni authentifiés pour cette publication; si un fichier manque
ou diffère, restaurer le snapshot local exact, sans inventer un remplacement.
Un clone public doit recevoir les PDF puis reconstruire le corpus avant les
tests d'intégration. Les six tests de phase 0 restent exécutables sans PDF.

## Vérifications exécutées

Toutes les commandes Python ont utilisé `.venv\Scripts\python.exe` 3.13.14.
Aucun modèle ou dépendance ML supplémentaire installé pour publier.

| Contrôle | Résultat réellement observé |
|---|---|
| Pytest complet | **22 passed in 11.98s** |
| pip check | No broken requirements found |
| scripts/verify_kit_v2.py | PASS, 145 questions, splits 85/30/30, 279 qrels |
| scripts/preflight_codex.py --hash-pdfs | PASS, 93 PDF, 838 pages du manifeste, tous SHA conformes |
| evaluation/benchmark/validate_benchmark.py | PASS, intégrité des questions/preuves/variantes/candidates |
| scripts/verify_phase1.py | PASS, neuf exports vérifiés |
| scripts/verify_phase1.py --rebuild --eda-rebuild | PASS, corpus/chunks/EDA reproduits à l'identique |
| Audit existant | PASS, aucun motif détecté |
| Audit des 137 blobs indexés | PASS, aucun secret/chemin personnel/fichier interdit |
| git diff --cached --check | PASS après attribution ciblée des fins de ligne/espaces historiques |
| SHA qrels indexés | CSV et TREC identiques aux empreintes phases 0–1 |
| Push initial | main publié, suivi origin/main configuré |
| Clone indépendant du dépôt public | 137 chemins attendus, tous les octets identiques |
| README via connecteur GitHub | Texte anglais et titre présents sur main |
| Page web GitHub | HTTP 200, titre, tables et blocs PowerShell rendus en HTML |

Les 279 jugements humains sont **inchangés** :

- CSV SHA256 : `d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb`
- TREC SHA256 : `9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682`

## Incidents et résolution

- Un premier contrôle d'espaces traitait CRLF comme des espaces en fin de
  ligne; les attributs Git ont été ajustés sans changer les octets des données.
  Les deux exceptions historiques ciblées sont explicites ci-dessus.
- Une première commande de lancement d'un sous-processus Windows avec un
  chemin relatif à slash a échoué; utilisation de `sys.executable` du venv.
- L'API GitHub anonyme de rendu README a répondu HTTP 403, limite de requêtes.
  Le fichier a été relu par le connecteur et le rendu vérifié sur la page
  publique, HTTP 200. Aucun jeton demandé ou exposé.
- Le contrôle simple de phase 1 remplace ses indicateurs de reproduction par
  `null` lorsqu'aucune reproduction n'est demandée; une reproduction complète
  a ensuite été relancée et son résultat `true/true` est celui publié.

## Vérification distante et suite

Après le push, `git ls-remote origin refs/heads/main` a retourné le commit de
code `73a03911ce00c84f482d78a28d860c6c1aae3753`. Une copie indépendante du dépôt
public a confirmé l'ensemble exact des fichiers, leurs octets et l'absence
des chemins interdits. Le dépôt est confirmé public, avec main par défaut.
Ce rapport est ensuite livré dans un commit de documentation distinct;
aucune réécriture d'historique ni force-push.

Convention de branches dans `CONTRIBUTING.md` : main stable;
feature/benchmark-alignment, feature/retrieval, feature/reranking,
feature/rag-generation, feature/streamlit-demo pour les phases futures.
Ces branches n'ont pas été créées inutilement.

Publié : code, tests, configurations, documentation, benchmark non privé et
résultats EDA légers des phases 0–1. Restent locaux : PDF, corpus dérivé,
références privées, environnement, secrets, images de pages et caches.
La phase 2 n'a pas commencé.

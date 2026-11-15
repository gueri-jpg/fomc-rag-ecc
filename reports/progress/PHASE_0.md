# Phase 0 — Audit et sécurisation

Date : 15 novembre 2026. Périmètre : phase 0 uniquement. Python exclusivement
`.venv\Scripts\python.exe` (3.13.14, Windows x64). Python 3.12 non utilisé.

## État et inventaire

Racine effective : `<project-root>`.
Les cinq fichiers demandés et les huit lectures obligatoires AGENTS ont été lus
intégralement avant modification. Première tentative depuis le dossier parent :
fichiers absents; localisation corrigée sans déplacer le projet.

- 46 Minutes et 47 Statements présents; 93 hashes PDF conformes au manifeste.
- 838 pages **déclarées dans le manifeste**; pas de nouvelle extraction ni de
  recomptage physique des pages par PyMuPDF en phase 0.
- Années : 2021–2025, 16 PDF/an; 2026, 13 PDF.
- 145 questions, splits 85 dev / 30 validation / 30 test.
- 279 couples validés, 188 grade 2 et 91 grade 1; CSV et TREC concordants.
- 294 preuves retenues, deux exclues; 30 paraphrases exclusivement test;
  dix candidates sans réponse désactivées.
- Champs des requêtes : question, question_id, question_type, split, topic.
  Aucune réponse attendue, preuve ou référence page dans les requêtes.
  Zéro texte de question exactement dupliqué après casse/espaces; ce contrôle
  ne remplace pas le diagnostic sémantique cross-split de phase 2.
- Aucun LICENSE ni README général initial; README du kit présent.
- Environnement initial : pip 26.1.2 uniquement. Aucun Git local ou parent.

## Audit du prototype préservé

`utils/TxtExtraction/Pdf2Txt.py` fusionne le texte de plusieurs PDF avant
segmentation, perd pages/documents/offsets, retire ponctuation et stopwords,
lemmatise le texte destiné au dense. `tokens` désigne des phrases, pas des
tokens. Le découpage par sommes de phrases ne garantit pas une limite stricte
de 128 mots, n'a pas d'overlap et échoue sur liste vide (`LenDocs[0]`).
Les PDF ne sont pas ouverts dans un gestionnaire de contexte; spaCy/NLTK
nécessitent des ressources externes; MiniLM est rechargé à chaque batch.

`utils/database/StockVectors.py` impose PostgreSQL/pgvector et dimension 384,
sans initialisation de l'extension, provenance, contrainte d'unicité ou upsert.
Les relances peuvent dupliquer les lignes et recréer des index. Transactions
et fermeture en cas d'exception ne sont pas sécurisées.

`utils/main.py` charge .env, encode puis écrit en DB au niveau module, sans
garde `__main__`, avec chemins relatifs au cwd, batchs codés en dur et
appariement année/mois fragile. Le `test.py` racine importe `database.test`,
dont l'ouverture DB se produit à l'import. Aucun de ces scripts n'a été exécuté.

## Corrections et fichiers

- `.gitignore` renforcé : credentials AWS, secrets Streamlit, clés de comptes
  de service, sorties de build; exclusions existantes .env, références, venv,
  poids, caches et index conservées.
- Git initialisé localement sur main; zéro commit, zéro remote, zéro fichier
  suivi. Ni publication ni réécriture d'historique.
- Propriétaire du nouveau `.git` corrigé vers <local-user> après erreur Windows
  `dubious ownership` entre compte sandbox et compte utilisateur. Aucun
  `safe.directory=*` ou changement global de configuration Git.
- `pyproject.toml`, `src/fomcrag/__init__.py`, `src/fomcrag/config.py` : package
  installable, chemins explicites, imports sans DB, secrets ou modèle.
- `tests/test_phase0.py` : six smoke tests offline (chemins, deux hashes qrels,
  protocole, règles Git, séparation requêtes/références).
- `scripts/audit_security.py` : scan heuristique des textes publiables; sorties
  limitées aux chemins/nombres, jamais aux contenus trouvés.
- `docs/architecture.md`, `docs/risk_register.md`, `docs/decision_log.md`,
  `README.md`, `app/README.md`, `experiments/README.md` créés.
- `requirements-phase0.lock.txt` fige les outils installés. Rapports machine :
  `preflight-phase0.json`, `dependencies-phase0.json` dans ce dossier.
  `configs/experiment_protocol.json` conservé sans changement.
- Aucun PDF, fichier benchmark ou script historique modifié/déplacé/supprimé.

## Dépendances et reproductibilité

Installation effective : pytest 9.2.0, setuptools 84.2.1 et leurs petites
dépendances (voir lock). Package fomcrag 0.0.1 installé en mode éditable.
Extras séparés corpus/retrieval/app; aucune bibliothèque ML ni poids installé.

Résolution binaire des extras exacts du pyproject obtenue sur PyPI :
PyMuPDF 1.28.2, numpy 2.5.4, pandas 3.1.1, rank-bm25 0.2.2,
sentence-transformers 6.3.0, scikit-learn 1.9.1, streamlit 1.67.0,
matplotlib 3.11.2. Roues CPython 3.13, ABI stable ou Python pur compatibles
Windows trouvées, y compris dépendances transitives. Ce résultat certifie
la résolution des distributions, **pas leur fonctionnement applicatif**.
Le JSON pip conserve versions, URLs et hashes des distributions résolues;
il ne constitue pas un lock fonctionnel des phases futures.

## Commandes exécutées et résultats

Toutes depuis la racine effective sauf le premier repérage. Les commandes
de lecture Get-Content/Get-ChildItem/rg ont servi à l'inventaire et aux lectures
obligatoires; aucun affichage du .env. Principales commandes exactes :

```powershell
& .venv\Scripts\python.exe -V
& .venv\Scripts\python.exe -m pip list
git --version
git rev-parse --show-toplevel
Get-FileHash evaluation/benchmark/qrels_group_confirmed_PAGES.csv,evaluation/benchmark/qrels_group_confirmed_PAGES.trec -Algorithm SHA256
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
& .venv\Scripts\python.exe scripts/verify_kit_v2.py
git init -b main
& .venv\Scripts\python.exe -m pip install --dry-run --only-binary=:all: pytest setuptools PyMuPDF numpy pandas rank-bm25 sentence-transformers scikit-learn streamlit matplotlib
& .venv\Scripts\python.exe -m pip install --dry-run --only-binary=:all: --report reports_dependency_check.tmp.json pytest setuptools PyMuPDF numpy pandas rank-bm25 sentence-transformers scikit-learn streamlit matplotlib
& .venv\Scripts\python.exe -m pip install --only-binary=:all: pytest setuptools
& .venv\Scripts\python.exe -m pip install --dry-run --only-binary=:all: --report reports/progress/dependencies-phase0.json '.[corpus,retrieval,app]'
& .venv\Scripts\python.exe -m pip install --no-build-isolation -e .
icacls .git /setowner <local-user> /T /Q
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m pip check
& .venv\Scripts\python.exe -m pip freeze --exclude fomcrag
git status --short
git branch --show-current
git remote
git log --all --oneline
git ls-files
git ls-files .env
git check-ignore .env .env.local references_local_only/probe.pdf models/probe artifacts/probe cache/probe .aws/credentials .streamlit/secrets.toml
& .venv\Scripts\python.exe scripts/audit_security.py
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs --json-report reports/progress/preflight-phase0.json
& .venv\Scripts\python.exe evaluation/benchmark/validate_benchmark.py
& .venv\Scripts\python.exe -m pip install --dry-run --no-index --no-deps --no-build-isolation .
& .venv\Scripts\python.exe -m pip --disable-pip-version-check install --dry-run --no-build-isolation --only-binary=:all: --report reports/progress/dependencies-phase0.json '.[corpus,retrieval,app]' > reports/progress/dependency-resolution.log
```

| Vérification | Résultat |
|---|---|
| Preflight initial et final avec SHA PDF | PASS |
| Kit V2 | PASS |
| Validation benchmark seule | PASS |
| pytest final (après rédaction du rapport) | 6 passed in 0.11s |
| pip check | No broken requirements found |
| Package éditable importé | 0.0.1 |
| Sécurité texte, rapport inclus | 72 fichiers, aucun motif détecté, aucun secret suivi |
| Ignore Git | .env, références, caches, poids, credentials protégés |
| Jugements validés | CSV/TREC inchangés, hashes ci-dessous |

Échecs intermédiaires réels : accès réseau sandbox refusé WinError 10013
sur première résolution; accès PyPI hors sandbox ensuite autorisé. Première
résolution des extras : dossier de rapport encore absent, relancée après
création. pytest : 5 succès/1 échec sous compte utilisateur à cause du
propriétaire Git; puis 4 succès/1 échec/1 erreur (CRLF sur stdin Git et droits
du répertoire temporaire partagé). Correction : protocole Git NUL binaire,
test de chemins sans fichiers temporaires, cache pytest désactivé pour éviter
les ACL entre comptes. Les six tests passent après correction. Une redirection
PowerShell a interprété une notification pip sur stderr comme NativeCommandError;
résolution relancée avec notification désactivée et code retour pip explicite.
Le fichier temporaire de première résolution a été supprimé; ce n'était pas
une donnée source. Le journal brut `.log` reste local et ignoré.

Dernière résolution des extras : code retour pip 0. Dernier `git diff --check` :
code 0; comme aucun fichier n'est encore suivi, ce dernier contrôle ne certifie
pas les espaces des nouveaux fichiers. État Git final : uniquement fichiers
non suivis, aucun secret ni référence privée dans cette liste.

## Intégrité des 279 jugements

SHA256 avant modifications et vérifiés après par pytest :

- CSV : `d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb`
- TREC : `9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682`

Double annotation reconnue selon déclaration du groupe; aucune feuille A/B
inventée, aucun kappa calculé. Aucun candidat non jugé converti en négatif.

## Limites et arrêt

Aucun blocage pour commencer ultérieurement la phase 1. Le .env existe et
reste privé; aucune preuve d'exposition dans ce nouveau dépôt sans historique.
Un ancien historique externe non fourni ne peut pas être certifié. Le scan
heuristique n'est pas une garantie d'absence de tout secret. Le dépôt distant
et la licence du code restent à définir; aucun identifiant ou accès n'est
nécessaire à ce stade. Les pages ont été contrôlées via manifeste et hashes,
pas réextraites. Aucune expérience, extraction, EDA, segmentation, indexation,
génération ou interface Streamlit fonctionnelle réalisée en phase 0.

Architecture prête : fichiers locaux, métadonnées traçables, séparation stricte
corpus/benchmark/application, comparaison future équitable sur tous les PDF.
Arrêt ici. Phase 1 uniquement sur nouvelle demande explicite.

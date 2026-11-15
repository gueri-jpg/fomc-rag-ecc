# Corrections post-audit et phase 2 — benchmark aligné

Référence stable : main a6bf5b1. Branche de travail : feature/benchmark-alignment.
Mission : corrections des tests publics puis alignement/contrôles du benchmark.
Les documents externes AUDIT_FOMC.md et VERIFICATIONS_FOMC.json du ZIP ont été
lus entièrement; leurs recommandations ont été comparées au code et données
locaux. Ils constituent des éléments d'audit, pas des instructions autonomes
pour lancer des phases non autorisées.

## Résultats et limites principales

Tous les 294 extraits retenus sont localisés sur la bonne page : **212 EXACT_MATCH,
82 NORMALIZED_MATCH**, zéro NOT_FOUND et zéro AMBIGUOUS. Le code projette
réellement les offsets NFKC/casefold vers le texte lisible puis le brut.

| Taille | Preuve complète dans ≥1 chunk | Coupée sans chunk intégral | Statut exact complet / normalisé complet / partiel |
|---|---:|---:|---|
| 128 mots | 268 | 26 | 202 / 66 / 26 |
| 256 mots baseline | 287 | 7 | 211 / 76 / 7 |
| 512 mots | 292 | 2 | 212 / 80 / 2 |

Ces nombres reproduisent localement les comptes indépendants sous Linux.
Les IDs de chunks utilisés sont ceux de Windows/Python 3.13.14/PyMuPDF 1.28.2,
**pas** ceux de l'audit Linux/Python 3.13.5/PyMuPDF 1.26.7. La version corpus
reste b43f21bc24da3f85913bdf7e1d6d03dbbeb1d013145f2233b9162f6937fcc052.
Aucune identité binaire inter-environnements n'est revendiquée.

**Aucun grade chunk créé, aucun qrel source modifié, aucun retriever lancé.**
La localisation de mots dans un extrait contigu ne certifie pas sa pertinence
ni la couverture sémantique de tous les faits. Les 279 jugements page sont
acceptés selon déclaration du groupe, potentiellement incomplets.

## A — correction hors ligne

Voir CORRECTIONS_AUDIT.md et premier commit dédié
`fix: make offline tests reproducible without source PDFs`.
Défaut réellement reproduit dans une copie sans PDF : 5 succès/1 échec.
Après correction : six tests phase 0 passent sans corpus, 22 tests initiaux
passent avec le corpus. L'existence et les SHA des 93 PDF restent contrôlés
par intégration, aucune assertion essentielle désactivée. CI minimale Python
3.13 sur PR/push main, sans corpus, modèle ou secret; commandes équivalentes
exécutées localement. La phase 2 étend le groupe offline à 29 tests.

Le code et les résultats baseline de prétraitement/chunking/EDA sont inchangés.
Le manifeste et les neuf exports sont identiques aux hashes capturés avant
travail. 93 PDF valides, 838 pages physiques et 2 127 chunks baseline. Le
rapport de vérification phase 1 historique est conservé, sans remplacer ses
mesures par celles d'une autre phase.

## B — méthode et exports d'alignement

`src/fomcrag/alignment.py` produit une vue NFKC caractère par caractère,
casefold, lettres ASCII/chiffres, avec origine pour chaque caractère expansé.
Recherche contiguë, pas sac de mots. Tous les matches complets sont conservés;
les fragments ≥32 caractères normalisés servent seulement de diagnostic en
cas d'échec de match complet. Les textes de page et chunks ne sont pas changés.

Chaque ligne evidence_alignment_128/256/512.jsonl contient IDs question/preuve/
page/document, source PDF, corpus/chunking versions, statut de page et de chunk,
méthode, faits fournis, offsets clean/raw et tous les chunks chevauchants avec
couverture. Les CSV alignment_report_* sont les relations aplaties par chunk.
La couverture est mesurée en caractères **normalisés**, et n'inclut pas une
garantie sur ponctuation/signes; `1/4` et `14` peuvent partager cette vue.
Ce mécanisme localise des citations connues et ne doit pas être utilisé pour
affirmer une équivalence de taux ou entraîner un modèle.

Les sorties, sous reports/benchmark_alignment/, contiennent des IDs/offsets/
statistiques, pas de grandes copies du texte intégral. Deux exports page qrels
sont des copies exactes des jugements existants. alignment_candidates_UNJUDGED
ne porte aucune nouvelle note; human_review_cases conserve les décisions vides.
Deux associations historiques restent EXCLUDE_SCOPE et ne sont pas alignées
comme positives. Les statuts et conventions sont définis dans
docs/benchmark_alignment.md. Les manifestes conservent hashes d'entrée, code
et sorties; un second traitement indépendant vérifie la reproductibilité.

248 extraits n'ont pas de required_facts fournis; 46 ont seulement des IDs
de faits. Ce manque n'est pas comblé en inventant un référentiel validé. Pour
les sept cas prioritaires seulement, les clauses de faits proposées sont
explicitement analystiques, traçables et non jugées humainement.

## C — les sept preuves coupées

Chaque preuve chevauche deux chunks baseline. Le fichier priority_seven_cases.csv
et priority_fact_coverage.json donnent leurs IDs complets et les offsets des
clauses de support proposées dans configs/priority_case_facts.json.

| Preuve | Page physique | Analyse des faits centraux proposés et risque |
|---|---|---|
| FOMC_132_E01 | Minutes 2023-11-01 p7 | Premier chunk : rendements → hypothèques, primes de terme, offre Treasury/incertitude et chemin taux/neutre. Le second porte la fin prudente et la surveillance. Un chunk peut couvrir les causes demandées sans reprendre tout l'extrait. |
| FOMC_136_E01 | Minutes 2024-01-31 p8 | Premier chunk : détente salariale + participation/immigration/job matching. Le second poursuit les limites et risques. Ne pas en déduire une causalité chiffrée. |
| FOMC_136_E02 | Minutes 2024-03-20 p8 | Second chunk : meilleur équilibre du travail, détente salariale et offre liée à participation/immigration. Le début descriptif est ailleurs; extrait source lui-même tronqué avant pied de page. |
| FOMC_137_E01 | Minutes 2024-03-20 p8 | Second chunk : attentes ancrées et facteurs d'offre soutenant la désinflation; premier : horizon 2 % et réserves sectorielles. Le noyau proposé n'est pas une validation de suffisance pour toute réponse. |
| FOMC_139_E01 | Minutes 2024-03-20 p4 | Premier : transition douce et risque de baisse accélérée des réserves. Second : aucune décision prise. Utiliser les deux si la réponse couvre aussi le statut de décision. |
| FOMC_142_E01 | Minutes 2024-09-18 p9 | Premier : volet septembre/progrès inflation/risques/recalibrage. La question compare novembre : une autre preuve temporelle reste indispensable. |
| FOMC_145_E01 | Minutes 2024-03-20 p3 | Second : baisses envisagées plus tardives et plus faibles, et facteurs expliquant le changement. Le mouvement futures initial est amorcé dans le premier; une preuve septembre est requise pour toute la comparaison. |

Les clauses minimales proposées sont toutes contenues dans un chunk pour
chacun des sept cas. **Cela ne signifie pas sept nouvelles notes positives** :
les listes de faits sont des propositions de lecture, non des annotations
humaines exhaustives. Deux questions requièrent explicitement une autre
période. La file de revue demeure ouverte pour vérifier le niveau de suffisance
avant toute évaluation finale au niveau chunk.

## D — partitions et paraphrases

10 440 paires examinées, dont 6 000 cross-split; zéro doublon normalisé.
Deux chevauchements substantiels, détaillés dans SPLIT_AUDIT.md :

- FOMC_044 dev / FOMC_102 validation partagent le volet 2022 des pénuries
  sectorielles et salaires; 102 ajoute 2021.
- FOMC_070 test / FOMC_129 dev partagent la preuve janvier 2025 sur l'offre;
  une réponse dev pourrait révéler la réponse test, même avec peu de mots communs.

Les seuils pré-déclarés combinent Jaccard lexical, ratio SequenceMatcher et
chevauchement de sous-chaînes de preuves. Aucun modèle appris ou tuning test.
Aucun déplacement/embargo appliqué automatiquement. Proposition à décider
avant phase 3 : embargo de 044 et 129 pendant tuning (dev effectif 83, fichier
nominal 85), ou split groupé approuvé et rééquilibré. Ce n'est pas encore fait.

Les 30 paraphrases sont uniques, un parent test chacune. Les alertes numériques
sur 010 (COVID-19) et 141 (fractions vs décimales) ne signalent pas à elles seules
une différence de sens. Lecture des 30 paires documentée sans prétendre à une
validation humaine. Six risques de portée/aide de réponse proposés : 002, 020,
025, 054, 068, 087. Ne pas réécrire les variantes; demander validation avant
robustesse, uniquement après gel. Dix candidates sans réponse restent désactivées.

## E — métriques et pooling préparés

Trois budgets implémentés/testés : chunk@k, page-coverage-from-chunk@k,
unique-page@k. Sur A1/A2/B1, k=2 consomme deux chunks mais une page en budget
chunk; unique-page@2 consomme trois chunks. Les qrels page ne permettent pas
de noter chunk@k. Chaque diagnostic garde convention et consommation; les
scripts historiques exigent désormais la convention, les métriques sont
préfixées, sans confusion avec des scores chunk complets.

Pooling : union des top-k de fichiers de classements futurs, déduplication
chunk/page, contrôle IDs, méthodes/rangs, UNJUDGED explicite. Pas de retrieval
exécuté pour alimenter le mécanisme; seuls les tests utilisent des exemples
synthétiques clairement isolés. Import de notes réellement HUMAN_REVIEWED,
pages connues, notes 0/1/2 et conflits refusés. Aucun fichier supplémentaire
d'annotation humaine fourni; aucun import/gold fabriqué. Le pool TF-IDF de
1 740 lignes n'est pas traité comme déjà jugé.

## F — césures et préparation phase 3

7 877 césures sur 401 pages, 1 782 paires distinctes; 34 occurrences de composés
protégés dans le prototype lexical. Baseline et texte naturel inchangés.
Protocole docs/hyphen_ablation_protocol.md : comparaison future de L0 et vue
lexicale corrigée seulement aux césures attestées, mêmes chunks/budgets,
tests négations/composés/dates/taux; choix dev/validation après décision de
partition. Aucun gain de retrieval prétendu ou mesuré maintenant.

## Code modifié et validation

Ajouts : alignment.py, benchmark.py, metrics.py, pooling.py, split_audit.py,
hyphen_diagnostics.py; six scripts de diagnostics/pooling/vérification;
configs phase 2 et propositions de faits; tests unitaires/intégration;
rapports d'alignement et documentation. Corrections : deux tests phase 0/1,
workflow CI, scripts historiques evaluate_retrieval/evaluate_robustness et
merge_reviewed_qrels (budget explicite et contrôles de décisions humaines).
README et architecture mis à jour. Aucune dépendance installée, Python
3.13.14 et paquets existants; base PyMuPDF 1.28.2, Unicode version dans summary.

Commandes réellement exécutées :

```powershell
& .venv\Scripts\python.exe scripts/check_offline.py --output artifacts/offline-before.json
& .venv\Scripts\python.exe scripts/check_offline.py --output artifacts/offline-after.json
& .venv\Scripts\python.exe scripts/align_benchmark.py
& .venv\Scripts\python.exe scripts/audit_benchmark_splits.py
& .venv\Scripts\python.exe scripts/diagnose_priority_evidence.py
& .venv\Scripts\python.exe scripts/audit_hyphens.py
& .venv\Scripts\python.exe scripts/verify_phase2.py --rebuild
& .venv\Scripts\python.exe scripts/check_offline.py --tests tests/test_phase0.py tests/test_benchmark_phase2.py --output artifacts/offline-phase2.json
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m pip check
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
& .venv\Scripts\python.exe evaluation/benchmark/evaluate_retrieval.py --help
& .venv\Scripts\python.exe evaluation/benchmark/evaluate_robustness.py --help
```

Résultats locaux : **47 passed in 6.91s**, dont 29 checks offline sans PDF ni
exports (**29 passed in 0.47s**). pip check PASS. Localisation exacte/normalisée,
ligatures/fractions/expansions, offsets, partiels/ambiguïtés, sept cas réels,
qrels, budgets et UNJUDGED sont testés. Le test de collision numérique explicite
la limite de la normalisation permissive, il ne la masque pas.

Les 279 qrels sont strictement identiques, y compris dans l'index avant push :

- CSV : d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb
- TREC : 9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682

## Acceptation, publication et arrêt

- Correction hors corpus reproduite et vérifiée : oui.
- Statut explicite et offsets sourcés sur 294 preuves : oui.
- Sept cas, texte vs faits distingués : oui, propositions analytiques seulement.
- Qrels originaux, corpus, chunks et EDA préservés : oui.
- Partitions/paraphrases auditées sans changements silencieux : oui.
- Budgets et pooling préparés, tests synthétiques séparés : oui.
- Reproductibilité d'alignement : contrôle indépendant exécuté, voir
  phase2_verification.json.
- Revue humaine encore nécessaire : décisions sur les deux chevauchements,
  suffisance des propositions de faits et six paraphrases signalées. Les
  annotations individuelles et exhaustivité ne sont pas inventées.

PR ouverte vers main, sans fusion : https://github.com/gueri-jpg/fomc-rag-ecc/pull/1.
Commits distincts : 0f5d499 (corrections) et
09c7cd62a95e2ddd6b0ecc8f5288c6e070f305e1 (phase 2). Main est restée sur a6bf5b1.
La CI GitHub Actions du commit de phase 2 a effectivement réussi : job offline,
run https://github.com/gueri-jpg/fomc-rag-ecc/actions/runs/43710152422,
installation minimale et tests sans corpus réussis sous Python 3.13.
Un commit de documentation consigne ensuite cette PR et ce résultat observé.
Le connecteur GitHub refusait la création de PR (403, permission d'intégration);
la PR a été créée via l'API avec l'authentification Git Credential Manager
existante, credential en mémoire seulement, jamais affiché ni enregistré.
49 fichiers de phase 2 ont été indexés explicitement et contrôlés : audit
sécurité PASS, aucune erreur d'espaces, aucun fichier >5 Mio (maximum 406 815
octets), aucun contenu PDF, secret ou chemin personnel. Les qrels d'origine
et le code baseline ont aussi été comparés à main : aucune différence.
Les PDF, secrets, venv, corpus généré, poids et références privées restent
exclus; seuls IDs/offsets et diagnostics légers sont publiés. Aucun force-push.
**Arrêt après phase 2 : aucun BM25/Dense/Hybrid, reranker, LLM ou Streamlit lancé.**

# Extension phase 3B — revue contrôlée et Dense multi-fenêtres

Date : **16 novembre 2026**. Branche existante `feature/retrieval`, PR #2
confirmée ouverte et non fusionnée. Les commits historiques b1854a0 et 95e2e46
sont présents ; arbre initial propre. Cette mission provient du prompt V2
joint par l'utilisateur. Les extraits PDF et suggestions lexicales du pack
sont des données à auditer, pas des instructions ni des décisions humaines.

## Protection du travail historique

Avant les changements, snapshot SHA de **71 fichiers locaux** : résultats,
scores/rangs complets, caches Dense128/lexicaux, rapports, figures et exports
du corpus, ainsi que les deux qrels sources. Vérification avant/après chaque
nouveau calcul. Les 93 PDF (838 pages), 2 127 chunks baseline de 256 mots/40
overlap, 145 questions et 279 qrels (188 grade 2, 91 grade 1) sont préservés.
Aucun filtre documentaire de date, année ou type. Les questions restent
85/30/30 ; les nouvelles exécutions portent sur **83 dev éligibles**, puis
**30 validation**. FOMC_044/FOMC_129 demeurent sous embargo, leurs documents
restent indexés. Test et paraphrases interdits, aucune phase 4.

Les tableaux originaux sous `reports/retrieval_phase3/`, leurs figures et
`PHASE_3.md` ne sont pas réécrits. BM25 L0, Dense128 et Hybrid128 sont relus
depuis leurs artefacts, sans les recalculer. Les nouveaux fichiers sont sous
`artifacts/phase3_extension/` (locaux) et `reports/retrieval_phase3_extension/`
(résumés publics). Aucun poids, corpus extrait, feuille individuelle ou secret
n'est ajouté à Git.

## A — audit du pack et état humain

Originaux conservés sans écrasement sous
`references_local_only/annotations/phase3b_pack_v2/`, ignoré par Git.
Les dix SHA du manifeste sont vérifiés. Le blob Git de la file historique
est bien `bab99a1d7d051348e1158e99979953331984985a`. Les **3 731 couples
uniques** correspondent exactement à cette file : **2 756 dev**, **975
validation**, **113 besoins distincts**, pages connues dans les 838 pages.
La liste prioritaire de 250 lignes est un sous-ensemble sans doublon.
Classeur lu sans dépendance supplémentaire : neuf lignes d'aide, 3 732 lignes
de feuille incluant son en-tête. Aucune donnée personnelle n'est publiée.

Les 3 731 extraits des propositions et préannotations : **1 708** se retrouvent
littéralement dans le texte local ; **2 023** ne sont pas littéralement
identiques. Les **3 731** correspondent après suppression des espaces.
Cette comparaison distingue les vues fournies (PyMuPDF 1.26.7) et locales
(1.28.2), sans attribuer tous les écarts à la seule version de PyMuPDF : le
traitement des césures/espaces peut aussi expliquer les différences. Supprimer
les espaces est un diagnostic de sous-chaîne permissif, pas une validation
sémantique ni une certification des frontières de mots. Le PDF original et
ses pages entières restent la preuve à lire. Aucun texte source n'est remplacé.

**Aucune décision humaine nouvelle disponible.** La feuille contient 3 731
statuts PENDING_HUMAN_REVIEW, sans note finale. Les propositions automatiques
0/1/2 (2 190 / 1 309 / 232) sont des heuristiques non étalonnées : elles ne sont
utilisées ni en qrels, ni en métrique de pertinence, ni en sélection du retrieval.
Aucun fichier humain rempli ou statut HUMAN_REVIEWED n'a été fabriqué.

État de l'import : **WAITING_FOR_HUMAN_VALIDATION**. Série augmentée :
**NOT_RUN_NO_HUMAN_LABELS**. Pas de TREC consolidé créé et pas de κ inventé.
L'infrastructure figure dans le commit **dc6b1dd**. Elle exige les clés exactes,
grades valides, IDs individuels réels, date ISO, notes de preuve/arbitrage et
une attestation humaine séparée liée par SHA à la feuille et à l'univers.
Une ligne pending préremplie, des doublons/identités inconnues, des conflits,
une provenance absente ou une fausse complétude sont refusés. La déclaration
liée par hash ne prouve pas matériellement la lecture humaine : cette limite
est explicitée dans `docs/annotation_pool_review.md`.

## B — variante fixe et préenregistrement

Code, configuration, CLI, méthodologie et premiers tests committés dans
**9bc9477 avant toute expérience de corpus**. Pas de grille ni MaxSim.
Même `sentence-transformers/all-MiniLM-L12-v2`, révision
`a50ef00143b4d5391434df20ae11632588ac25be`, onze SHA vérifiés ; Python
**3.13.14**, Torch **2.9.0+cpu**, sentence-transformers **5.1.2**, Transformers
**4.57.1**, NumPy **2.5.4**. Aucune nouvelle dépendance installée. CPU float32,
quatre threads Torch, lots de 16, seed **20261115** conservée.

Tokenisation complète du chunk sans troncature ni tokens spéciaux. Le vrai
tokenizer confirme deux spéciaux : capacité de contenu **126**, overlap
**32 tokens de contenu**, stride **94**. Couverture de premier/dernier token
et union sans trou vérifiées. Les IDs des tokens sont transmis directement à
`prepare_for_model`, sans décodage/retokenisation. Taille et contenu préparés
contrôlés ; chaîne SentenceTransformer complète (Transformer + pooling),
padding sans troncature. Vecteur unitaire de chaque fenêtre, moyenne arithmétique
non pondérée, puis L2 : **un seul vecteur de 384 dimensions par chunk_id
historique**. Les fenêtres ne deviennent pas de nouveaux chunks ou pages.

Parité numérique single-window vérifiée sur le vrai modèle, tolérances
`atol=2e-6`, `rtol=2e-5` motivées par le batching/padding CPU float32. Tests
de frontière 126/127 tokens de contenu, textes vides, longues séquences,
ligatures, négations, taux et dates. Détails : `docs/dense_windowing_methodology.md`.

Le cache séparé inclut textes, IDs, manifeste corpus, checkpoint/SHA, vocabulaire,
tokenizer et dépendances, code, longueur/overlap/agrégation, dtype et seed.
NPY sans pickle ; SHA, finitude, dimension, normes et couverture recalculée
contrôlés. Le cache Dense128 est inchangé.

## C — protocole d'évaluation distinct

Méthodes : BM25_L0, Dense128, DenseWindowMean, Hybrid128, HybridWindowMean.
BM25 fixé à k1=1,2/b=0,75, RRF **k=10**, profondeur **100** identiques à la
phase 3. Encodeur de requête original, uniquement le texte de la question.
Qrels seed lus après retrieval dans le code d'évaluation, jamais par l'encodeur.
Budgets 1/3/5/10/20 : principal strict k chunks avec déduplication des pages,
secondaire k pages uniques avec nombre de chunks consommés. Aucun grade de
chunk propagé depuis sa page.

Dev précède le scellement de la configuration, des empreintes de code/modèle,
corpus et objectifs. Une seule passe validation descriptive après scellement.
**La validation a déjà été observée en phase 3 : indépendance limitée.**
Aucun nouveau paramètre ne sera choisi à partir de cette validation. La
recommandation suit le critère dev préenregistré (couverture connue @5,
puis hit et rang réciproque de page, ordre des méthodes pour égalités).
Les garde-fous interdisent un deuxième calcul validation et une nouvelle
sélection dev après son début.

Les scores sont conditionnels aux seuls positifs connus, avec UNJUDGED
explicite. seed-nDCG est exploratoire : un gain nul pour une page non jugée
n'est pas un grade 0. Pas de Recall/Precision/nDCG gold, pas d'exhaustivité
revendiquée. Bootstrap apparié descriptif de 2 000 réplications par besoin,
seed fixe, sans correction des labels manquants ni de multiplicité.

## Résultats mesurés sur les seed uniquement

| Méthode | Couverture connue @5 dev | Hit dev | Couverture connue @5 validation | Hit validation |
|---|---:|---:|---:|---:|
| BM25_L0 historique | 31,73 % | 44,58 % | 35,56 % | 43,33 % |
| Dense128 historique | 14,86 % | 28,92 % | 10,56 % | 20,00 % |
| DenseWindowMean | 9,64 % | 18,07 % | 16,11 % | 20,00 % |
| Hybrid128 historique | 30,42 % | 43,37 % | 27,78 % | 40,00 % |
| HybridWindowMean | 31,22 % | 44,58 % | 28,33 % | 40,00 % |

Budget strict de cinq chunks, pages dédupliquées. Les moyennes historiques
recalculées depuis leurs fichiers sont identiques aux valeurs originales.
Les 100 agrégats et 5 650 lignes question/méthode/budget exposent les deux
conventions à tous les k. Le rang de première page positive est conservé par
question, avec RR moyen (rang de page unique, pas rang de chunk).

RR @5 nouveau Dense : dev **0,1245**, validation **0,1028** ; nouveau Hybrid :
**0,2629** et **0,2733**. seed-nDCG exploratoire : Dense **0,0901 / 0,1105**,
Hybrid **0,2372 / 0,2479**. Proportions moyennes de pages non jugées @5 :
Dense **95,90 % / 96,00 %**, Hybrid **89,52 % / 92,00 %**. Les résultats ne
peuvent donc pas être interprétés comme qualité exhaustive des résultats.

| Différence appariée de couverture @5 | Dev, points [IC descriptif 95 %] | Validation, points [IC descriptif 95 %] |
|---|---:|---:|
| DenseWindowMean − Dense128 | −5,22 [−11,25 ; +0,60] | +5,56 [−8,89 ; +21,12] |
| HybridWindowMean − Hybrid128 | +0,80 [−3,82 ; +5,62] | +0,56 [−12,22 ; +13,33] |
| DenseWindowMean − BM25_L0 | −22,09 [−31,43 ; −13,05] | −19,44 [−36,11 ; −3,33] |
| HybridWindowMean − BM25_L0 | −0,50 [−6,02 ; +4,92] | −7,22 [−16,67 ; 0,00] |

Les IC des changements par rapport à Dense128/Hybrid128 incluent zéro. La
couverture totale des tokens n'a pas entraîné un gain systématique sur les
positifs connus. Dense régresse en dev et progresse en validation ; cette
hétérogénéité interdit une généralisation sur 30 besoins déjà observés.
Recommandation fixée sur dev : **BM25_L0**, conservée sans changement après
validation. DenseWindowMean reste une ablation documentée ; aucune nouvelle
variante n'a été essayée pour améliorer artificiellement ces résultats.

## Couverture des tokens, ressources et latences

**2 127/2 127 chunks entièrement couverts**, **620 846 tokens de contenu**,
**zéro token de contenu perdu**, maximum préparé **128 tokens**. Les nombres
historiques de 625 100 tokens incluaient deux spéciaux par chunk ;
625 100 − 2×2 127 = 620 846. Les **7 021 fenêtres** représentent en moyenne
**3,301** fenêtres/chunk, p95 **4**, maximum **5**. Les tokens d'overlap sont
traités plusieurs fois ; la couverture à 100 % compte l'union des intervalles,
pas une somme artificiellement gonflée par répétition.

Encodage documentaire initial réel : **687,12 s**, contre 160,61 s archivées
pour Dense128. Ce sont deux séances et charges différentes, pas un benchmark
CPU strictement isolé. Matrice finale toujours **3 267 200 octets** pour
2 127×384 float32 (+ en-tête NPY). Cache matrice+métadonnées : **4 274 851
octets**. Validation réutilise ce cache, contrôle complet compris **1,367 s**,
aucun nouvel encodage des documents. Les embeddings de fenêtres intermédiaires
ne deviennent pas un index de nouvelles unités.

CPU uniquement, huit processeurs logiques disponibles, quatre threads Torch.
Pics working set du processus (Windows GetProcessMemoryInfo) : **657 973 248
octets dev**, **584 990 720 octets validation**. Chargement du checkpoint dans
SentenceTransformer : **0,489 s / 0,596 s**, hors import de Torch/démarrage
Python. Aucune capacité RAM globale ni mesure de mémoire par méthode inventée.

| Méthode nouvelle | Dev p50/p95 (ms) | Validation p50/p95 (ms) |
|---|---:|---:|
| DenseWindowMean | 75,92 / 89,20 | 73,40 / 80,95 |
| HybridWindowMean | 87,95 / 102,01 | 83,38 / 91,87 |

Répétition de chaque requête sans cache de requêtes, classement identique :
Dense p50/p95 **76,13/85,10 ms** dev et **73,90/79,82 ms** validation ;
Hybrid **87,36/97,63 ms** et **84,36/92,41 ms**. Modèle déjà chargé ; aucune
latence de processus froid par requête revendiquée. Les historiques sont
explicitement marqués archivés dans les tableaux/graphes. HybridWindow est
une **somme sérielle** des nouveaux coûts Dense/fusion et de la composante
BM25 historique, pas une mesure de service parallèle ni un nouveau BM25.
Le nombre de vecteurs recherchés reste 2 127, même requête originale : les
écarts de latence entre séances ne s'attribuent pas directement aux fenêtres.

## Pool complémentaire et analyse d'erreurs

Union top-20 des **deux nouvelles méthodes**, sans supprimer le pool original :

| Split | Chunks candidats | Pages candidates | Pages seed connues présentes | Nouvelles paires hors seed et pool initial |
|---|---:|---:|---:|---:|
| Dev | 2 345 | 2 166 | 70 | **796** |
| Validation | 847 | 768 | 25 | **251** |

File complémentaire **1 047 couples UNJUDGED**, distincts des 3 731 initiaux
et des 279 seed, avec PDF, chunk IDs, méthodes et rangs. Aucun grade attribué,
aucun candidat absent assimilé à un négatif, aucun couple déjà confirmé renvoyé
à réannotation. Les pools complets sont locaux, les nouvelles clés légères
sous `additional_UNJUDGED_review_queue.csv`. Priorité héritée du protocole
historique (rang et différence avec année explicitement écrite dans la question),
sans heuristique de grade du pack.

`ERROR_ANALYSIS.md` discute dix cas réellement lus, et `question_deltas.csv`
expose tous les écarts. Exemple : FOMC_132, le premier chunk d'une page connue
passe de rang 47 à 1 en Dense, mais la réserve sur les faits répartis en phase 2
subsiste. FOMC_045 passe de 4 à 16 malgré le même top-1. FOMC_016 passe de 5 à 6
en Hybrid, illustrant le seuil de budget ; FOMC_140 progresse mais conserve une
première source Dense d'une autre période. Ces lectures n'ajoutent aucune note.

Explications plausibles : dilution d'un fait localisé par moyenne non pondérée,
overlap surreprésenté, mélange de facettes, formulations récurrentes entre
réunions, consensus RRF de chunks. **L'effet causal de la couverture seule
n'est pas isolé**, car l'agrégation change simultanément. Les qrels manquants
peuvent aussi modifier le classement des méthodes après une vraie revue.

Quatre figures réelles dans le dossier d'extension : courbes de couverture,
IC appariés, distribution des fenêtres et latences. Tous les résultats et
graphiques proviennent des classements persistés, sans chiffres simulés.

## Reproduction

Depuis la racine profonde du projet, avec `.venv` Python 3.13.14 existant,
les 93 PDF, exports baseline, modèle verrouillé et résultats de phase 3 restaurés :

```powershell
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
& .venv\Scripts\python.exe scripts/verify_kit_v2.py
& .venv\Scripts\python.exe scripts/review_annotations_phase3b.py
& .venv\Scripts\python.exe scripts/review_annotations_phase3b.py --sheet references_local_only/annotations/phase3b_pack_v2/02_FEUILLE_DE_VALIDATION_GROUPE_3731.csv
& .venv\Scripts\python.exe scripts/run_phase3_extension.py --stage dev
& .venv\Scripts\python.exe scripts/run_phase3_extension.py --stage validation
& .venv\Scripts\python.exe scripts/report_phase3_extension.py
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m pip check
```

Les deux commandes d'inférence concernent une **nouvelle expérience locale**,
avec artefacts historiques restaurés et sans sortie 3B déjà complétée. Dans
l'espace actuel, seules l'audit et la régénération du rapport se relancent :
les nouveaux classements sont terminés et une réexécution de validation est
refusée, même si sa première passe a échoué après son démarrage. Aucun nettoyage
automatique de ces preuves pour contourner le verrou. Les temps ne sont pas
garantis identiques sur d'autres machines. Aucune nouvelle installation requise.

## Vérifications effectivement exécutées et limites restantes

- État initial : PR #2 ouverte/non fusionnée, feature/retrieval propre et
  historique b1854a0/95e2e46 présent ; pas de push sur main.
- Rebaseline avant changements : **80 tests réussis en 101,15 s**.
- Tests initiaux de couverture et vrai modèle : **14 réussis en 19,72 s** ;
  puis extension des contrôles de partitions et absence d'accès aux labels.
- Suite légère actuelle : **84 réussis en 2,36 s**, sans besoin de PDF/modèle.
- Copie séparée composée uniquement des fichiers suivis, sans PDF, corpus
  extrait, modèle ni feuilles privées : **84 réussis en 2,33 s, OFFLINE PASS**.
- Suite complète après expériences : **111 réussis en 35,53 s** : les 80
  précédents et 31 nouveaux, dont mapping réel du pack, rejets de fausses
  décisions, frontières/overlap, contenu intégral, single-window parity,
  float32/normes/dimension, invalidation/corruption de cache, IDs historiques,
  embargo, verrou de réexécution et égalité des métriques archivées.
- `pip check` : PASS, aucune dépendance cassée ; kit V2 : PASS ; preflight
  avec hashes des **93 PDF** : PASS. Avertissement historique `.env` présent,
  ignoré et jamais lu/affiché/publié.
- Audit du pack : PASS ; tentative d'import de la feuille fournie :
  WAITING_FOR_HUMAN_VALIDATION, exported=false, pending=3731, aucun TREC créé.
- Snapshot historique : **71/71 fichiers identiques** après les deux nouvelles
  exécutions ; empreinte canonique du snapshot
  `9ed9dc9252882802f7a62946fd6125660c3bee8b4111ecd84a6a1d884b0772e9`.
- Régénération des tableaux, pools et quatre figures : **identiques octet par
  octet**, sans inférence, en 14,25 s ; puis trois tests d'intégration des
  résultats réussis en 3,94 s. Le post-traitement a été accéléré en chargeant
  chaque matrice NPZ une seule fois au lieu de la décompresser pour chaque
  hit ; les résultats sont inchangés et aucune validation n'a été répétée.
- `git diff --cached --check` : PASS. Audit heuristique des 24 fichiers du
  dernier lot préparé : **PASS, aucune alerte**. Les commits d'infrastructure
  et préenregistrement ont aussi été audités avant leur enregistrement.
  Diff Git des configurations, encodeur, orchestration et rapports originaux
  de phase 3 par rapport à 95e2e46 : vide. Les fichiers lourds/privés restent ignorés.

Le tokenizer a signalé qu'une séquence complète dépassait 128 tokens pendant
la mesure **sans troncature** ; elle n'a pas été envoyée telle quelle au modèle.
Chaque entrée réellement encodée est préparée séparément et vérifiée ≤128.
L'avertissement de performance recommande l'API rapide au lieu de pad : le
padding manuel est ici intentionnel pour garder exactement les IDs des fenêtres.
Une lecture exploratoire des CSV avant la fin du post-traitement a renvoyé
FileNotFoundError ; les sorties ont été lues après son achèvement, sans nouvel
appel d'inférence ni répétition validation. Aucune erreur de modèle ou
extraction n'a été masquée. L'ancien nom de ZIP dans le prompt est traité comme
historique ; le pack réellement fourni est PACK_FOMC_PHASE3B_PREANNOTATIONS_V2.zip.

**Verdict conditionnel :** couverture technique des tokens atteinte ; aucun
gain systématique de récupération démontré avec les seed incomplets. La
moyenne des fenêtres et la couverture changent ensemble, donc pas d'attribution
causale à la seule suppression de troncature. Conserver BM25 L0 recommandé sur
dev, garder les cinq méthodes pour comparaison future sous protocole commun.
Une véritable revue humaine reste nécessaire pour enrichir les qrels ; ni
le pool original ni son complément ne sont déclarés exhaustifs.

Code/configuration/méthodologie, CLI, tests, nouveaux tableaux/figures et file
complémentaire constituent les livrables de cette extension. La PR #2 doit
rester ouverte sans fusion pour revue technique et décisions humaines.
**Arrêt après 3B : aucune requête de partition test, aucun reranking,
générateur ou Streamlit exécuté.**

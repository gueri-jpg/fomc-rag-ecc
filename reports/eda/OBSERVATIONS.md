# Observations EDA — corpus FOMC fourni

Ces observations décrivent les PDF locaux validés par SHA256; elles ne
constituent ni une évaluation de retrieval ni une vérification externe de
l'authenticité de chaque document. Les valeurs proviennent de `summary.json`
et des CSV de ce dossier. Graphiques sous `../figures/phase1_*.png`.

## Composition et chronologie

| Année | Minutes PDF | Minutes pages | Statements PDF | Statements pages |
|---|---:|---:|---:|---:|
| 2021 | 8 | 113 | 8 | 33 |
| 2022 | 8 | 104 | 8 | 32 |
| 2023 | 8 | 87 | 8 | 32 |
| 2024 | 8 | 109 | 8 | 32 |
| 2025 | 8 | 150 | 8 | 31 |
| 2026 | 6 | 98 | 7 | 17 |
| Total | 46 | 661 | 47 | 177 |

2026 est partielle : dernière réunion des Minutes au 16 septembre, dernier
Statement au 28 octobre. Il ne faut pas interpréter les volumes annuels bruts
comme une évolution de l'importance des sujets. Les Minutes dominent le volume
textuel : 360 800 mots contre 38 574 pour les Statements. Une comparaison
retrieval future doit maintenir les deux types et peut analyser leurs erreurs
séparément, sans filtrage silencieux.

## Longueurs et qualité

Le texte lisible comporte 399 374 mots de segmentation (`\S+`). Une page contient
14 à 855 mots, médiane 455, moyenne 476,58; les quantiles 5 % et 95 % sont 57
et 815,15. Un document contient 498 à 13 654 mots, médiane 1 156 : la médiane
globale masque les différences de type (Minutes médiane 7 589 mots).
La pagination physique varie de 2 à 21 pages.

Aucune page vide, aucune erreur d'extraction, aucun U+FFFD. Les 16 pages
de moins de 30 mots comprennent 15 couvertures de Minutes à partir de décembre
2024 et une dernière page de liste de participants (juin 2026, p. 15). Elles
sont conservées. Une page courte n'est donc pas automatiquement un échec.

On observe 75 glyphes U+F0B7 sur 15 pages : code privé compatible avec des
puces typographiques, signalé `encoding_suspect`, sans invention de mot.
347 pages contiennent une longue règle décorative; les sept pages marquées
`long_word` contiennent surtout de longues URL. Ces catégories sont des
alertes descriptives, pas 369 pages inutilisables; elles peuvent se recouper.

7 877 césures visibles sont détectées sur 401 pages. Le trait est conservé
pour éviter la corruption de composés; les coupures de mots peuvent donc
réduire le matching lexical (`infla-tion`). L'option plus agressive `join`
reste disponible et devra être évaluée sur dev/validation si nécessaire,
sans ajustement sur les questions test. Les textes bruts rendent ce choix
réversible et auditable.

## Mots, économie et répétitions

Les mots fréquents incluent `federal` (3 638), `inflation` (3 381),
`participants` (3 108), `board` (3 106), `market` (2 979). La présence de noms
institutionnels et listes de participants explique une partie du volume;
la fréquence seule n'indique pas la pertinence pour une question.
Les expressions économiques sont comptées comme séquences lexicales exactes,
sans stemming ni cumul artificiel de variantes. Les CSV détaillent les
occurrences, pages, années et types; les fréquences des composés peuvent être
sous-estimées par les césures conservées.

Trois groupes de pages strictement identiques après normalisation contiennent
2, 22 et 2 pages. Il n'y a aucun groupe de PDF ayant le même SHA256.
Le Jaccard ≥0,8 sur ensembles de 5-grammes identifie 312 paires de pages
proches, **y compris des paires exactes**. Ce nombre ne désigne ni 312
documents distincts ni 312 preuves redondantes à supprimer. Par exemple,
des pages d'instructions de politique monétaire et formules réglementaires
réapparaissent entre réunions; des différences de taux peuvent rester cruciales.
Le fichier `recurrent_lines.csv` contient 1 414 lignes présentes sur au moins
trois pages. La plus fréquente est une règle décorative (347 pages).

## Découpage et conséquences

| Fenêtre / overlap | Chunks | Moyenne mots | Médiane | <40 mots | Survolume lié à l'overlap |
|---|---:|---:|---:|---:|---:|
| 128 / 40 | 4 563 | 120,18 | 128 | 17 | +37,31 % |
| 256 / 40 | 2 127 | 212,00 | 256 | 17 | +12,91 % |
| 512 / 40 | 1 124 | 365,49 | 383 | 17 | +2,86 % |

Les 17 fragments courts par configuration correspondent aux 16 pages très
courtes et à une page de 37 mots (Minutes septembre 2026, p. 15). Ils ne sont
pas supprimés. Le baseline 256 est celui du kit, pas le gagnant d'une expérience.
L'overlap réduit certaines coupures intrapage mais augmente volume et
redondance. Une phrase franchissant une page peut rester coupée. Les 512 mots
peuvent dépasser le contexte en wordpieces des futurs modèles; cette
contrainte sera mesurée lors de l'introduction des tokenizers.

Toutes les configurations couvrent tous les mots de chaque page, sans
franchissement de page ou PDF. Des informations administratives et notes de
bas de page restent présentes pour fidélité. Il faudra étudier leur effet
sur le ranking, les répétitions de sources et la déduplication en phase 3.
Aucun diagnostic EDA ne crée de pertinence : une page connue positive ne
rend pas tous ses chunks positifs et un chunk non annoté n'est jamais un zéro.

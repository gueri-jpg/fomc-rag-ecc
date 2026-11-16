# Erreurs observées — DenseWindowMean et fusion

Lecture locale de dix cas dev/validation, choisis après calcul pour illustrer
des gains et pertes, sans prétendre représenter leur fréquence. Les textes de
questions et premiers résultats ont été consultés ; `question_deltas.csv`
donne les écarts de tous les besoins. Aucune note nouvelle n'est attribuée.

Les rangs désignent le premier **chunk issu d'une page positive connue**,
pas une pertinence annotée au niveau chunk. Une page hors qrels reste non jugée.

| Cas | Constat réel | Interprétation prudente |
|---|---|---|
| FOMC_045 dev, budgets des ménages décembre 2022 | Dense128 : premier support connu au rang 4 ; WindowMean : 16. Même top-1 de février 2023 p9. | Une première source stable masque des changements dans la suite du classement. Plus de contenu n'assure pas la présence de la réunion exacte dans le budget 5. |
| FOMC_065 dev, lecture des données emploi septembre 2024 | Dense : 3→19 pour le premier support connu ; top-1 inchangé décembre 2025 p11. | Formules répétées sur les indicateurs du travail et décalage de réunion persistent. Ne pas prétendre résoudre les dates par couverture seule. |
| FOMC_076 dev, tarifs et inflation juin 2025 | Dense : 8→1 ; la source initiale passe de mai 2025 p11 à juin 2025 p9. | Gain concret de classement d'une page connue avec la variante complète ; couverture et agrégation changent ensemble, attribution causale non identifiée. |
| FOMC_016 dev, réductions mensuelles illustratives septembre 2021 | Hybrid : 5→6 ; la page connue sort du budget de cinq chunks. | Sensibilité au seuil k. Les discussions de réductions d'achats à d'autres dates ne garantissent pas les chiffres demandés. |
| FOMC_017 dev, indicateurs de plein emploi en 2021 | Hybrid : 12→2, alors que son top-1 devient mars 2025 p2. | Le premier support connu s'améliore sans que la première source soit nécessairement la bonne réunion. Un top-1 hors qrels n'est pas automatiquement faux. |
| FOMC_092 validation, projection septembre 2026 jusqu'à 2028 | Dense : 3→18 ; top-1 de septembre 2025 p7 vers janvier 2024 p7. | Proximité du vocabulaire de prévision insuffisante pour discriminer période et horizon. Aucun filtre d'année ajouté pour corriger ce cas. |
| FOMC_084 validation, pétrole et tarifs | Dense : 1→16 ; mars 2026 p8 remplacé en tête par avril 2026 p9. | Discours voisins sur l'énergie et les tarifs ; le support connu recule malgré la couverture complète. La nouvelle page n'est pas annotée négative. |
| FOMC_132 validation, rendements et hypothèques automne 2023 | Dense : 47→1 ; Hybrid : 7→1, novembre 2023 p7 en tête. | Gain net sur les seed. L'extrait de référence était réparti entre chunks selon phase 2 : le hit de page ne certifie pas tous les faits ni la fin prudente de l'extrait. |
| FOMC_140 validation, banques centrales étrangères avant septembre 2024 | Dense : absent top-100→2 ; Hybrid : 9→1. | Un support connu est avancé, mais Dense met d'abord décembre 2021 p3. Il reste nécessaire de vérifier dates et contexte complet. |
| FOMC_102 validation, pénuries sectorielles et salaires | Hybrid : 4→19 ; couverture connue @5 diminue de 0,5. | Les discussions 2022 proches se concurrencent ; la fusion peut perdre une facette même avec plus de tokens. Le lien avec dev044 demeure traité par l'embargo initial, pas par un déplacement de question. |

Globalement, DenseWindowMean gagne/perd en couverture connue @5 sur **5/13**
questions dev et **5/5** validation. HybridWindowMean gagne/perd sur **5/4** dev
et **3/4** validation. Le faible gain moyen Hybrid ne signifie donc pas un
gain uniforme par besoin.

Hypothèses explicatives : moyenne non pondérée pouvant diluer une information
localisée, répétition des overlaps, sections générales dominant la représentation,
concurrence entre réunions proches et RRF au niveau chunk. Ces mécanismes sont
plausibles, **pas isolés causalement** par cette expérience. Ne pas choisir une
nouvelle pondération, un overlap ou MaxSim à partir de la validation déjà vue.

La nouvelle union top-20 ajoute 1 047 couples question–page hors seed et hors
pool initial. Leur statut est UNJUDGED : des alternatives pertinentes peuvent
manquer aux seed et inverser certaines comparaisons. Ni cette analyse ni les
suggestions lexicales fournies ne remplacent une véritable décision humaine.

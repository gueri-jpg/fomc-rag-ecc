# Analyse qualitative — développement et validation uniquement

Les 20 cas ci-dessous ont été choisis après calcul pour expliquer des écarts,
pas pour estimer leur fréquence. Les textes des top résultats et les pages
positives connues ont été examinés localement. `error_cases.csv` régénère leurs
rangs et sources depuis les exports ; les commentaires restent une analyse
humaine de développement, **pas une nouvelle annotation de pertinence**.

Les rangs ci-dessous sont ceux du premier **chunk provenant d'une page positive
connue**, dans le top-100. Ils ne prouvent ni la pertinence du chunk ni la
suffisance de son contenu. « >100 » signifie absent du top-100 enregistré.
Les pages non jugées, y compris celles évoquées ici, restent UNJUDGED.

| Question / split | Rangs BM25 / Dense / Hybrid | Observation et conséquence |
|---|---|---|
| FOMC_003 dev | 3 / 94 / 5 | Les facteurs d'inflation de début de reprise sont concurrencés par des discussions PCE de 2025. Hybrid conserve la page connue mais la recule. L1 la recule de 3 à 5. |
| FOMC_004 dev | 13 / >100 / 26 | La caractérisation de la reprise de mars 2021 ressemble aux minutes d'avril/juin. Bonne proximité thématique possible, faible précision de réunion ; aucune page connue dans les cinq chunks. |
| FOMC_007 dev | >100 / >100 / >100 | Question à deux volets, communiqué et anticipations des participants. Les résultats portent sur des pressions inflationnistes d'autres réunions, jusqu'à 2025 pour BM25. Aucun des deux supports connus retrouvé au top-100. |
| FOMC_009 dev | 2 / 17 / 7 | La comparaison du taux ON RRP avril/juin 2021 exige deux dates. Hybrid met en avant un ajustement technique discuté en janvier 2025 et perd la couverture connue au budget 5. |
| FOMC_013 dev | 12 / 2 / 2 | La formulation sémantique sur les objectifs d'achats aide Dense et Hybrid : couverture de 1/3 contre 0 à cinq chunks. Le top-1 de juillet 2021 p13 n'est pas une des pages annotées ; ne pas le déclarer incorrect sans revue. |
| FOMC_014 dev | 7 / 14 / 4 | Les deux facilités repo de 2021 apparaissent aussi dans des discussions de 2026. La fusion fait entrer une page connue au top-5 alors qu'aucun composant ne l'y plaçait seul. |
| FOMC_015 dev | 1 / 17 / 5 | Le tapering de septembre est concurrencé par juillet et décembre 2021. BM25 couvre les deux pages connues au top-5, Hybrid et L1 une seule. Une première bonne page ne suffit pas à représenter tous les supports. |
| FOMC_018 dev | 1 / 1 / 1 | La vague Delta est lexicalement distinctive ; les trois systèmes retrouvent p7 de septembre. Couverture limitée à 1/3 : secteurs vulnérables et services demandent d'autres pages. |
| FOMC_032 dev | 2 / 4 / 1 | Hybrid avance une page connue sur la guidance conditionnelle. Les trois méthodes ne couvrent que 1/3 des supports, malgré un rang initial favorable ; limite des questions multi-passages. |
| FOMC_048 dev | >100 / 1 / 1 | La sélection des emprunteurs sous pression de financement est mieux captée par Dense. Hybrid couvre 1/2 des pages connues au top-5 ; BM25 privilégie une discussion de ménages de 2024. |
| FOMC_120 dev | >100 / 1 / 6 | Dense retrouve une page connue sur productivité et technologie. La fusion la repousse au rang 6 : compromis RRF défavorable au budget 5, sans preuve que le consensus des listes soit meilleur. |
| FOMC_005 validation | 3 / >100 / 5 | Les pénuries et contraintes d'offre se répètent entre mars et juin 2021. L1 avance le premier support de 3 à 2, mais la couverture à 5 reste identique ; gain de rang sans gain de couverture. |
| FOMC_008 validation | 2 / 40 / 4 | Les taux de rémunération des réserves d'avril/juin 2021 sont concurrencés par 4,65 % en 2023 et 5,4 % en 2024. BM25 couvre les deux pages connues à 5, Hybrid/L1 une ; nombres conservés ne signifient pas raisonnement temporel. |
| FOMC_051 validation | >100 / >100 / >100 | La pause de juin 2023 pour observer l'information est proche de justifications de pause/baisse d'autres dates. Hybrid met en avant décembre 2025 ; l'intention générale ne distingue pas le communiqué exact. |
| FOMC_058 validation | 18 / 41 / 22 | L'écart PCE total/sous-jacent de janvier 2024 exige les bonnes données mensuelles. Les top-1 renvoient à 2025, décembre 2023 ou janvier 2021. L1 avance seulement 18 à 17, hors budget 5. |
| FOMC_084 validation | 1 / 1 / 6 | Les composants retrouvent d'abord mars 2026, mais sur des chunks différents de la même page. RRF fusionne les **chunks**, pas les pages ; leur accord au niveau page ne s'additionne pas automatiquement. Hybrid perd les deux pages connues du top-5. |
| FOMC_102 validation | 16 / 3 / 4 | Les pénuries de recrutement et salaires sectoriels favorisent la proximité sémantique. Dense/Hybrid couvrent 1/2 des supports connus. La question reste inchangée malgré son lien avec dev044 sous embargo. |
| FOMC_104 validation | 6 / 2 / 3 | Dense/Hybrid font entrer un des trois supports sur richesse et consommation ; plusieurs années sont explicitement demandées. Ne pas traiter une seule page comme réponse complète à 2022–2025. |
| FOMC_106 validation | 1 / 9 / 1 | Hybrid étend la couverture de 1/3 à 2/3 sur les ménages modestes, sans améliorer le rang du premier support. L'extension de couverture complète le diagnostic de rang. |
| FOMC_132 validation | 2 / 47 / 7 | Hausse des rendements et taux hypothécaires : formulations récurrentes sur les primes de terme en 2021/2025/2026. L1 avance 2 à 1 ; Hybrid sort la page connue du top-5. L'extrait de référence est réparti sur deux chunks (constat phase 2), même si ses faits centraux peuvent se trouver dans le premier ; un hit de page ne certifie pas cette couverture. |

## Ce que ces cas permettent de conclure

Le bruit temporel est réel dans les listes observées, sans justifier un filtre
par année : les questions transversales exigent plusieurs années et certaines
preuves interannuelles ont déjà été acceptées par le groupe. Une page d'une
autre réunion n'est donc pas automatiquement un faux positif. La file de revue
priorise les années différentes de celles explicitement écrites dans la question,
sans attribuer de grade.

La troncature Dense de 91,91 % des chunks est un facteur plausible de perte
d'information ; cette expérience ne l'isole pas causalement du modèle, de la
formulation des questions ou des césures. Aucun second encodage avec une autre
limite n'a été lancé après lecture de validation. L1 ne change ni texte naturel
ni embeddings. Ses changements de rang peuvent venir des fréquences et longueurs
dans l'index entier ; on ne les attribue pas tous à un mot corrigé dans la question.

Les 7 gains et 10 pertes Hybrid/BM25 en couverture @5 sur dev, puis 3 gains et
4 pertes sur validation, viennent de `paired_bootstrap.csv`. L1 ne gagne aucune
couverture @5, en perd sur une question de chaque split, mais améliore certains
rangs (005,132) : métriques et analyse qualitative sont complémentaires.

Ni cette analyse ni le pool ne rendent les qrels exhaustifs. Les limites de
chunking déjà documentées, les réserves de suffisance des faits et la validation
humaine des six paraphrases restent ouvertes pour les phases ultérieures.

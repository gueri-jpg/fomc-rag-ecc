# Audit des partitions et paraphrases — aucune partition modifiée

Constats et propositions historiques conservés ci-dessous. La décision
ultérieure d'embargo ciblé, consignée à la fin, remplace ces propositions
pour la sélection de paramètres sans modifier les partitions originales.

Méthode explicable : toutes les 10 440 paires de questions, dont 6 000
cross-split. Jaccard de tokens, ratio SequenceMatcher et Jaccard de sous-chaînes
de preuves normalisées (40 caractères, stride 10), sans modèle appris.
Seuils de signalement fixés dans configs/benchmark_phase2.json avant lecture
des résultats : 0,55 / 0,70 / 0,60. Ces seuils ne sont pas des hyperparamètres
de retrieval. Aucune performance test calculée ni optimisation sur test.

Résultat : zéro doublon textuel normalisé, deux alertes cross-split. Ces
signaux ne prouvent pas à eux seuls une équivalence sémantique; lecture des
questions et des extraits partagés réalisée pour proposer les actions suivantes.

| Paire | Constat vérifié | Risque et proposition avant tuning |
|---|---|---|
| FOMC_044 dev / FOMC_102 validation | Même passage de novembre 2022 sur pénuries sectorielles et salaires; 102 demande aussi 2021 | Chevauchement d'un volet, validation potentiellement favorisée. Proposer embargo de 044 pendant le réglage ou nouveau split groupé approuvé. |
| FOMC_070 test / FOMC_129 dev | Même passage de janvier 2025 sur offre de travail, investissement et productivité; 129 ajoute deux Statements 2026 | Une réponse de dev peut dévoiler directement celle du test. Proposer embargo de 129 pour tout choix de paramètres avant test, ou split groupé rééquilibré et validé. |

Les fichiers originaux restent 85/30/30. **Aucun embargo ou déplacement n'est
appliqué silencieusement.** Si les deux embargos étaient approuvés, l'ensemble
effectif de tuning dev serait 83 questions, tandis que le fichier nominal
conserverait 85; il faudrait publier cette différence. Un regroupement peut
modifier les tailles/strates et doit être décidé avant les expériences.
Les listes test n'ont été consultées que pour l'audit de fuites autorisé.

Les alertes lexicales peuvent manquer des reformulations à faibles mots
communs. Le canal de preuve partagée détecte ici 070/129 malgré Jaccard lexical
nul. Ce n'est pas une garantie d'absence d'autres fuites sémantiques.

## Paraphrases test

30 IDs uniques, exactement un parent test chacun, statut test et aucune
activation pour tuning. Lecture analytique des 30 paires effectuée, sans
création de validation humaine. Fichier paraphrase_semantic_notes.csv pour les
propositions individuelles. Les deux alertes de chiffres automatiques sont :

- FOMC_010 : COVID-19 ajoute le token 19 sans changer la date mid-2021.
- FOMC_141 : 5¼–5½ et 5.25–5.50% expriment ici le même intervalle; l'alerte
  syntaxique n'est pas un désaccord économique constaté.

Points sémantiques à soumettre au groupe :

- FOMC_002 : Treasury bonds peut être plus restrictif que Treasury securities.
- FOMC_020 : mois explicites novembre/décembre vs « following two months »;
  confirmer la convention temporelle du besoin original.
- FOMC_025 : second half of 2021 devient late-2021, possible réduction de portée.
- FOMC_054 : « banking sector viewed as resilient » fournit une partie de la
  réponse que l'original demande encore; portée et difficulté peuvent changer.
- FOMC_068 : la paraphrase fournit quarter-point, une information de réponse.
- FOMC_087 : productivity et housing-services sont ajoutés, orientant les deux
  sources attendues de désinflation au lieu de les demander librement.

Les autres paires n'ont pas de changement manifeste repéré dans cette lecture;
cela ne constitue pas une certification d'équivalence. Conserver le statut
pending human review et n'exécuter la robustesse qu'après gel. Les dix
candidates sans réponse restent désactivées.

## Décision utilisateur lors de la revue PR #1 : embargo ciblé

Les deux exclusions de tuning sont approuvées, versionnées dans
configs/tuning_policy.json et appliquées par src/fomcrag/selection.py.
FOMC_044 et FOMC_129 ne contribuent à aucun choix de paramètres sur dev.
Le fichier original conserve 145 questions, **85 dev / 30 validation / 30 test**;
la sélection de tuning contient **83 dev**, validation et test restant à 30.
Aucun déplacement ni rééquilibrage. Les 93 PDF et tous les chunks restent dans
le corpus, y compris les pages partagées des deux paires signalées.

L'évaluation distingue tuning, diagnostic et frozen-evaluation. Les diagnostics
complets sont inéligibles à la sélection et doivent attendre le gel ou être
confiés à un analyste indépendant : ne pas choisir un modèle depuis un résultat
sur les questions sous embargo ou un agrégat qui les inclut. Les sorties gardent
IDs sélectionnés/exclus, finalité, tailles effectives, version et hash de politique.

Risque résiduel : retirer deux besoins du tuning ne prouve ni indépendance
totale des partitions ni oubli des réponses déjà vues. La couverture thématique
des 83 questions diffère légèrement; déclarer cette taille et ne pas comparer
silencieusement avec des scores sur 85. Les six paraphrases restent inchangées
et en attente de validation humaine avant robustesse.

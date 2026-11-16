# Revue contrôlée du pool — extension 3B

Le pack V2 est une aide fournie par l'utilisateur, pas un référentiel humain.
Ses originaux sont conservés sous `references_local_only/annotations/phase3b_pack_v2`,
ignorés par Git. Ne pas utiliser les propositions lexicales 0/1/2 comme qrels,
comme métriques de pertinence ou comme objectifs de sélection. Elles peuvent
ancrer la lecture ; annoter les PDF complets indépendamment des suggestions.

La commande suivante vérifie les SHA du manifeste, les identités du pool
historique (3 731 couples, 113 questions, 2 756 dev et 975 validation), les
pages réelles et les différences d'extraits entre environnements PyMuPDF :

```powershell
& .venv\Scripts\python.exe scripts/review_annotations_phase3b.py
```

Les extraits fournis ne remplacent pas le corpus local ni la consultation du
PDF. Un écart de sous-chaîne peut venir de césures/espaces/ordre d'extraction ;
un match n'est pas une preuve de pertinence. Le rapport ne publie aucun extrait
ou identifiant personnel. Aucune donnée individuelle du classeur n'est suivie.

Pour un futur import, conserver une copie de travail de la feuille complète,
ses clés exactes et uniquement de véritables décisions VALIDATED_BY_GROUP.
Les champs individuels, notes de preuve, date ISO et éventuel arbitrage doivent
être réellement renseignés par le groupe. Un second réviseur doit avoir un ID
distinct ; sa présence n'est jamais inventée. Une note finale sur ligne pending
est refusée. Le simple recopiage des heuristiques ne constitue pas une revue.

L'import exige aussi une attestation séparée **fournie par les humains**, avec
`human_confirmed=true`, `sheet_sha256`, `universe_sha256` (empreinte JSON canonique
des clés triées) et `approval_reference`. Aucun fichier d'attestation rempli
n'est généré automatiquement. Les empreintes lient la déclaration à sa version ;
elles ne prouvent pas à elles seules que les humains ont effectivement relu.

```powershell
& .venv\Scripts\python.exe scripts/review_annotations_phase3b.py --sheet references_local_only/annotations/decisions.csv --attestation references_local_only/annotations/attestation.json
```

`--require-complete` interdit un export partiel. Sans décisions, aucun TREC
augmenté n'est créé : WAITING_FOR_HUMAN_VALIDATION et NOT_RUN_NO_HUMAN_LABELS.
Les sorties consolidées futures restent dans `artifacts/phase3_extension/`,
versionnées par contenu, sans écraser les 279 qrels sources. Un conflit, une
identité inconnue ou dupliquée, un grade invalide ou une provenance insuffisante
est refusé. Les nouvelles notes portent sur des pages, jamais leurs chunks.

Un pool complètement relu n'est pas une annotation exhaustive des 838 pages
pour chaque besoin. Les nouveaux résultats multi-fenêtres peuvent proposer
d'autres pages UNJUDGED. Leur revue est distincte et ne réétiquette pas les
279 couples déjà acceptés. Aucun accord inter-annotateurs n'est inventé.

# Statut des qrels et validation du groupe — instructions opérationnelles

## Confirmé par l'utilisateur le 15 novembre 2026
L'équipe indique avoir effectué une **double annotation** des preuves proposées et accepté les grades 1/2 sans modification. Elle indique aussi avoir vérifié les associations entre années. **On enregistre cela comme une confirmation du groupe**, pas comme un calcul indépendant d'accord inter-annotateurs : les feuilles A/B et leurs identités n'ont pas été transmises. En conséquence, ne pas inventer de scores Cohen κ/Krippendorff α, de signatures ni de dates des relecteurs.

### Ce que contient précisément le kit
- 145 questions principales, réparties **85 dev / 30 validation / 30 test**.
- 294 extraits candidats positifs dont la présence textuelle dans les PDF a été vérifiée. Deux candidats historiques sont exclus ; ne pas les restaurer.
- 279 paires `(question_id, page_id)` annotées (188 x grade 2 et 91 x grade 1), exportées en `qrels_group_confirmed_PAGES.csv` et `.trec`, directement exploitables pour les **diagnostics basés sur pages connues pertinentes**.
- 1740 lignes `POOLING_TO_REVIEW_1740.csv` issues d'une recherche exploratoire TF-IDF. Le CSV conservé contient encore `UNJUDGED_NEEDS_REVIEW` et des annotations vides. **L'équipe a peut-être fait une vérification hors de ce CSV : cette donnée n'a pas été transmise**. Ne pas présumer que toutes les lignes ont été jugées ; ne pas demander de refaire ce qui a réellement déjà été fait.
- Aucun passage non jugé ne reçoit automatiquement `0`. La vérité terrain positive par page ne signifie pas que tous les chunks de cette page sont pertinents.

## Qu'est-ce qu'un pooling ?
Un pooling consiste à rassembler des candidats (par exemple top 20 de BM25, Dense et Hybride sur **les 93 PDF**) et à comparer au registre de jugements existant. **Ce n'est pas uniquement chercher des passages d'autres années.** L'objectif est d'identifier les candidats NOUVEAUX non encore étiquetés. S'il n'y a pas de nouveaux candidats importants ou si un enregistrement externe permet de valider tout le pool, on passe directement à la consolidation finale sans réannotation systématique.

## Quand créer les qrels définitifs ?
1. **Dès maintenant** : utiliser `qrels_group_confirmed_PAGES.trec` pour la baseline et les contrôles structurels. Ce sont les 279 jugements acceptés par le groupe (référence *validée par déclaration*). Aucun nouveau jugement n'est nécessaire pour ces couples.
2. **Pendant phase 2** : relier chaque passage de référence à sa vraie page et aux chunks qui le contiennent. En cas de chunk coupé, ne pas l'étiqueter 2 au seul motif que la page est 2.
3. **Après premiers résultats de retrieval (phase 3)** : calculer l'union des top20 et détecter candidats non jugés. Importer les vérifications que le groupe a déjà faites si disponibles; sinon ne relire que les candidats manquants, sur n'importe quelle année.
4. **Avant les scores définitifs (phase 6)** : fixer un qrels versionné adapté à l'unité évaluée (*page* ou *chunk*), conserver séparément les `UNJUDGED`, consigner couverture des jugements, hypothèses d'exhaustivité, annotateurs quand documents disponibles. Si non exhaustif, publier des scores **conditionnels aux jugements disponibles** et non un « gold Recall » sans biais.

## Export des nouvelles décisions (facultatif)
Créer un CSV UTF-8 `evaluation/benchmark/reviewed_additional_qrels.csv` avec en-têtes :

```csv
question_id,page_id,relevance_grade,review_status,notes
```

Chaque ligne doit être **une revue humaine effective**. `relevance_grade` entier 0, 1 ou 2 ; `review_status` doit valoir `HUMAN_REVIEWED`. Ne pas générer des notes par IA. La commande `python scripts/merge_reviewed_qrels.py --additional evaluation/benchmark/reviewed_additional_qrels.csv` produit un fichier consolidé à partir des notes déjà confirmées ; **elle ne certifie pas à elle seule l'exhaustivité** et refuse les conflits de grades. Laisser ce CSV absent tant qu'aucun nouveau jugement n'existe.

## Si l'équipe possède déjà des feuilles A/B ou des qrels validés ailleurs
Importer ces fichiers dans le dossier local, vérifier identité `(question_id,page_id)` et notes, tracer la procédure. Ne pas écraser les 279 jugements acceptés sans correction délibérée et documentée par les humains. Ne pas publier de feuilles contenant des données personnelles d'annotateurs si non nécessaires.

## Bonnes pratiques de métriques
- Sur un référentiel **de pages positives incomplètes**, rapporter `known-positive-coverage@k`, `first-known-positive-rank`, et éventuellement `seed-nDCG` **avec mention explicite de leur portée**; le rappel vrai ne peut pas être estimé comme si l'on connaissait tous les positifs.
- Pour une évaluation page, convertir les top chunks en **pages uniques classées** et documenter la déduplication. Pour une évaluation chunk, faire juger les chunks retournés; ne pas propager le grade positif à toutes les découpes d'une même page.
- Les questions multi-facettes doivent disposer d'une couverture par faits exigés; des passages alternatifs indépendants peuvent satisfaire une même facette.
- Les **30 paraphrases** interviennent seulement APRES gel des configurations (phase 6). Leurs jugements sont hérités par équivalence du besoin, à confirmer si le sens change.
- Les **10 questions potentiellement non répondables** ne sont PAS utilisables tant que leur absence de réponse n'est pas confirmée sur l'ensemble du corpus. Elles évaluent principalement l'abstention du RAG complet, pas Recall@k (dénominateur nul).

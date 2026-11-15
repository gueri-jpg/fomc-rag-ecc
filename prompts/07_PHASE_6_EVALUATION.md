# PHASE 6 — Évaluation finale, interprétabilité et robustesse

1. Vérifier les qrels page et chunk effectivement jugés, les labels non jugés, les annotations supplémentaires du pool et la preuve éventuelle de complétude. Si incomplet, résultats bornés/diagnostics descriptifs, pas d'affirmation de 'Recall gold exact'.
2. FIGER choix modèles/hyperparamètres sur développement/validation, puis calculer une seule évaluation finale des **30 questions test**, classées par type et année, erreurs et coûts, IC bootstrap si appropriés.
3. Après gel et premier test : lancer **les 30 paraphrases test**, comparer différences appariées par question ; vérifier que la reformulation n'a pas altéré le besoin. Ne pas compter 30 nouvelles questions indépendantes ni réoptimiser sur elles.
4. Les **10 questions candidates sans réponse** : vérifier qu'elles sont vraiment non répondables sur les 93 PDF avec équipe avant activation; sinon les exclure. Tester abstention du RAG complet distinctement du Recall@k.
5. Interprétabilité ECC : au moins 15–20 erreurs réelles classées (mauvais document, date, chunking, lexique, rerank, hallucination, preuves interannuelles), exemple de score et raison probable. Graphiques et statistiques depuis logs réels.
6. Évaluer génération : exactitude des faits, fidélité aux preuves, citations correctes, abstention, erreurs (RAGAS ou juge automatique complémentaire, pas sans validation).
7. `reports/progress/PHASE_6.md` avec limitations, intervalles et version de référence.

**Acceptation :** pas de fuite test, robustesse interprétée par paires, limites qrels explicitement déclarées, analyse qualitative substantielle. **S'arrêter**.

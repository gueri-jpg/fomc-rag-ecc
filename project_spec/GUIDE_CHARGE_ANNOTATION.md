# Guide allégé : annotation et traitement des nouveaux candidats

L'utilisateur a confirmé le **15/11/2026** que la double annotation des 279 associations question–page était terminée et identique aux grades proposés. **NE PAS les refaire.** La collecte des originaux individuels est facultative pour la traçabilité/statistiques de concordance, pas une condition pour lancer la phase 0/1/3.

Après BM25, Dense et Hybride, générer le pool de leurs top20 (145 × 3 × 20 occurrences maximum avant dédoublonnage). Soustraire les paires déjà connues/validées et les décisions externes de l'équipe disponibles. **Seuls les nouveaux candidats sans jugement doivent être soumis à relecture**. Ils peuvent être de n'importe quelle année 2021–2026. Prioriser les candidats apparaissant haut dans plusieurs récupérateurs et les questions de validation/test, sans optimiser sur test.

Les 1740 lignes TF-IDF existantes sont une liste exploratoire, pas 1740 décisions de pertinence enregistrées. Si le groupe les a jugées hors du CSV, importer leurs annotations plutôt que tout reprendre. Noter explicitement toute couverture incomplète. La double annotation indépendante des nouveaux candidats est recommandée pour la validité scientifique; sans elle, des métriques finales non biaisées ne sont pas garanties, mais développement et démonstration restent possibles.

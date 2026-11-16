# DenseWindowMean — protocole 3B préenregistré

Variante fixe, sans grille : même checkpoint et tokenizer verrouillés que
Dense128, longueur totale 128, overlap de **32 tokens de contenu**, CPU float32,
384 dimensions, lots de 16, quatre threads, seed 20261115. Aucun entraînement.
Configuration et code committés avant le premier calcul sur le corpus.

Tokeniser le texte complet sans tokens spéciaux ni troncature. Interroger le
tokenizer pour le nombre de tokens spéciaux (vérifié par prepare_for_model),
soustraire de 128 pour la capacité de contenu. Avec BERT : deux spéciaux,
capacité 126, stride 94. Construire les intervalles [start,end), couvrir premier
et dernier token et vérifier l'union sans trou. Les fenêtres peuvent couper
un mot en WordPieces ; elles passent directement en IDs, sans décodage ni
retokenisation susceptible de modifier dates, ligatures ou négations.

Ajouter les spéciaux par prepare_for_model, vérifier tailles avant/après et
encoder via la chaîne SentenceTransformer complète (Transformer et pooling
configuré). Aucun appel encode(text) qui pourrait tronquer la fenêtre. Masques
d'attention et de segments sont paddés sans troncature. Normaliser chaque
vecteur fenêtre, moyenne arithmétique non pondérée, puis normalisation L2 finale.
Les overlaps sont donc représentés plusieurs fois : biais assumé de cette
agrégation, distinct d'une moyenne pondérée par tokens uniques.

Un seul vecteur final par chunk_id historique ; aucune nouvelle unité évaluée.
La requête utilise l'encodeur original (aucune requête dev/validation n'excède
128 tokens). Une fenêtre doit être numériquement équivalente à encode standard,
à atol=2e-6, rtol=2e-5 (padding/batching CPU float32). Les textes vides sont
représentés par les spéciaux, sans inventer de contenu.

Les caches locaux NPY sans pickle incluent source/IDs/textes, corpus,
checkpoint/révision/fichiers, tokenizer/vocabulaire, dépendances, code, overlap,
longueur, agrégation, dtype et seed. Vérification SHA de matrice, normes,
dimension et couverture recalculée au chargement. Les caches Dense128 restent
intacts et séparés. Aucune suggestion lexicale du pack ne participe au modèle.

Comparer cinq méthodes, budgets 1/3/5/10/20 : BM25_L0, Dense128 et Hybrid128
relus depuis les classements originaux ; nouveaux DenseWindowMean et
HybridWindowMean. Hybrid fixe k=10, profondeur 100, BM25 historique identique.
Seule cette variante Mean est étudiée ; MaxSim facultatif n'est pas implémenté.

Dev=83 sous embargo, puis scellement avant une passe validation=30,
**descriptive et non indépendante de la phase 3 déjà observée**. Aucune nouvelle
sélection d'overlap/longueur/agrégation sur validation. Recommandation par
critère dev historique (couverture connue @5, hit, RR, ordre des méthodes).
Test, paraphrases, reranking et génération interdits.

Seed historique uniquement tant qu'aucune décision humaine réelle n'est fournie.
Les scores sont conditionnels aux qrels incomplets, avec budgets chunks stricts
et pages uniques séparés. IC bootstrap appariés descriptifs par besoin, non
preuve causale. Toute amélioration mêle couverture et agrégation : sans ablation
supplémentaire, ne pas attribuer causalement le gain à la seule couverture.

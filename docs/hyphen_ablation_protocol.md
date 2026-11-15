# Protocole préparé — césures, phase 3 uniquement

Baseline inchangé : corpus_version b43f21bc24da3f85913bdf7e1d6d03dbbeb1d013145f2233b9162f6937fcc052,
chunks 256 mots/40 overlap. Les 7 877 césures visibles de 401 pages forment
1 782 paires lexicales distinctes. Elles mêlent mots cassés (`infla-tion`),
composés vrais, noms, liens et parfois effets de colonnes. Les déduire d'une
simple liste de mots est insuffisant. Rien n'est supprimé du texte naturel.

Ablation proposée, **non exécutée** :

1. Variante L0 : tokens baseline préservés.
2. Variante L1 : correction lexicale uniquement aux césures attestées par un
   saut de ligne dans raw_text, avec liste versionnée de composés protégés.
   L'illustration testable `lexical_ablation_candidate` protège notamment
   market-based, labor-market, longer-term, supply-side et interest-rate.
   Cette liste fixe n'est pas présentée comme complète (34 occurrences
   protégées dans le diagnostic); des composés inconnus peuvent être dégradés.
3. Pour les futurs chunks, projeter chaque césure raw vers ses offsets clean et
   ne corriger que les tokens du chunk concerné. Pas de resegmentation, nouveaux
   IDs ou mélange entre pages. Le prototype page entier n'est pas encore un
   index BM25 prêt à comparer.
4. Conserver corpus, IDs, budgets, qrels, ordre des candidats et seed. Dense,
   reranking et génération reçoivent le même texte naturel qu'en L0. Comparer
   uniquement les vues lexicales BM25; la fusion hybride pourra être évaluée
   dans une expérience séparée pour attribuer les effets.
5. Choisir sur dev/validation seulement, après décision sur les deux risques
   cross-split. Geler la configuration avant test; les paraphrases ne servent
   pas au choix de politique de césures.
6. Mesurer couverture des mots corrigés, faux regroupements de composés,
   diagnostics connus positifs selon un @k explicite, latences et erreurs de
   chiffres/dates/négations. Ne pas annoncer de gain avant mesure.

Tests préparés : no/not, contractions, composés économiques, dates ISO, taux
fractionnaires, pourcentages et signes négatifs; aucun changement du texte
naturel ou de son mapping. Le prototype n'utilise aucun qrel pour apprendre
des corrections et n'a téléchargé aucun modèle.

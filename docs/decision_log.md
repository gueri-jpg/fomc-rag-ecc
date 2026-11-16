# Décisions — 15 novembre 2026

- D01 : conserver l'emplacement du corpus et tous les scripts initiaux; documenter
  leurs défauts plutôt que les exécuter ou les réécrire en phase 0.
- D02 : Python 3.13 uniquement, aucun diagnostic/réparation Python 3.12.
- D03 : dépendances par extras de phase; environnement minimal phase 0.
  La résolution de roues compatibles ne prouve pas le fonctionnement ML.
- D04 : initialiser Git local sur main; aucun remote, commit ou push implicite.
- D05 : tests offline isolés des tests historiques qui ouvrent PostgreSQL.
- D06 : préserver bit à bit CSV/TREC validés; SHA256 contrôlés par tests.
- D07 : architecture fichiers et Streamlit locale; modules de phases futures
  documentés sans fausse implémentation ni lancement anticipé.

## Phase 1

- D08 : 256 mots/overlap 40 selon kit; exports 128 et 512 pour études futures,
  aucun tuning sur les questions ou scores.
- D09 : texte brut conservé, espaces normalisés avec mapping raw/clean;
  césures visibles conservées par prudence, soft hyphens retirés et tracés.
- D10 : ordre natif PyMuPDF sans tri géométrique automatique; blocs et
  coordonnées conservés, contrôle visuel sur trois pages de périodes différentes.
- D11 : aucun retrait de couverture, formule récurrente ou doublon; conserver
  la fidélité au corpus et mesurer le risque de répétition.
- D12 : corpus non supervisé uniquement; maps page/chunk sans question ni grade.
  L'alignement des références reste phase 2.
- D13 : installation minimale PyMuPDF/matplotlib et transitives; pas de pandas,
  spaCy/NLTK, bibliothèques retrieval, modèles ou Streamlit nécessaires phase 1.

## Revue PR #1 — embargo ciblé approuvé par l'utilisateur

- D14 : adopter configs/tuning_policy.json, version targeted-dev-embargo-v1.
  FOMC_044 et FOMC_129 restent dans leurs partitions originales mais sont
  exclues de toute sélection de paramètres sur dev. Tailles nominales 85/30/30;
  tailles de sélection 83 dev et 30 validation, test 30 réservé après gel.
  Aucun PDF, page ou chunk associé n'est exclu du corpus documentaire.
- D15 : diagnostics complets possibles explicitement, étiquetés inéligibles
  à la sélection. Les exécuter après gel des paramètres ou via un analyste
  indépendant ne participant pas à leur choix. Un sélecteur futur doit appeler
  require_tuning_eligible et conserver le hash de politique. Ces garde-fous ne
  peuvent empêcher une réutilisation humaine indirecte : les constats déjà lus
  et d'autres similarités restent un risque résiduel.
- D16 : les six paraphrases signalées restent en attente de validation humaine.
  Aucune reformulation, nouvelle annotation, fusion de PR ou phase 3 autorisée
  dans cette mise à jour de revue.

## Phase 3 — autorisation suivante, PR #1 fusionnée

- D17 : main intègre 4236a3f ; travail sur feature/retrieval. Protocole et
  grille enregistrés dans b1854a0 avant le premier calcul réel. Corpus unique
  de 2 127 chunks, portée intégrale ; aucun apprentissage sur labels.
- D18 : appartenance effective au split vérifiée, pas seulement la taille.
  Phase 3 refuse test/all/paraphrases et diagnostics sous embargo. Dev=83,
  validation=30 une seule passe ; pas de gel humain autorisant le test.
  Après validation, nouvelle sélection dev et réexécution validation refusées.
- D19 : sélectionner sur dev uniquement par couverture connue à cinq chunks,
  puis hit et RR ; grille préenregistrée, égalités déterministes. Résultat :
  BM25 k1=1,2,b=0,75 ; RRF k=10 ; recommandation BM25 L0. Validation n'a
  provoqué aucun ajustement. Garder aussi les deux autres méthodes.
- D20 : conserver le max_seq_length réel du checkpoint MiniLM verrouillé,
  soit 128 tokens. Déclarer 1 955/2 127 chunks tronqués (91,91 %) ; ne pas
  attribuer causalement toutes les erreurs à cette limite. Une autre limite
  nécessiterait une nouvelle expérience annoncée, sans tuning sur ce contrôle.
- D21 : exécuter l'ablation lexicale L1 seulement sur les vrais spans raw,
  sans changement de source, segmentation ou Dense. L0 reste préféré sur dev.
  Les gains de rang ne sont pas nécessairement des gains de couverture.
- D22 : métriques conditionnelles aux pages positives connues, deux budgets
  distincts ; pas de grade chunk déduit d'une page. Pool réel top-20 :
  3 731 nouveaux couples question–page UNJUDGED, aucun grade inventé et pas
  de réannotation des couples déjà jugés. IC appariés descriptifs, pertinence
  exhaustive et gagnant universel non établis. Analyse de 20 cas documentée.
- D23 : poids/index/rankings textuels locaux ; tableaux, graphiques et file
  de revue légers publiables après audit. PR séparée sans fusion automatique.
  Aucune phase 4, génération, application ou expérience test commencée.

## Extension 3B — 16 novembre 2026

- D24 : PR #2 confirmée ouverte/non fusionnée ; continuer feature/retrieval,
  conserver les commits et sorties historiques. Snapshot SHA de 71 fichiers
  locaux avant travail, y compris les caches, classements et rapports originaux.
- D25 : traiter le pack V2 comme aide de revue non humaine. Vérifier ses SHA,
  les 3 731 clés et le blob historique ; feuille entièrement pending. Attendre
  une véritable attestation liée à la feuille avant consolidation. Ne pas
  utiliser ses propositions 0/1/2 en métrique ou en tuning. Infrastructure
  enregistrée dans dc6b1dd ; aucune note humaine nouvelle intégrée.
- D26 : variante fixe DenseWindowMean préenregistrée dans 9bc9477 avant tout
  calcul de corpus : limite 128, 126 tokens de contenu, overlap 32 tokens,
  moyenne des fenêtres normalisées puis L2, mêmes IDs. Pas de MaxSim ni grille.
  Chaîne complète et parité single-window vérifiées sur le vrai checkpoint.
- D27 : BM25 L0, Dense128 et Hybrid128 relus depuis leurs artefacts immuables.
  Nouveaux DenseWindowMean/HybridWindowMean, k RRF=10 et profondeur=100 inchangés.
  Dev=83 ; scellement avant une seule validation descriptive de 30 besoins.
  L'observation antérieure de validation limite son indépendance ; aucun
  paramètre nouveau ne sera choisi à partir de ces scores. Test fermé.
- D28 : série seed séparée ; série augmentée NOT_RUN_NO_HUMAN_LABELS tant
  que les humains n'ont pas fourni de décisions réelles. Nouveaux couples
  hors du pool original et des seed restent UNJUDGED. Aucun gain ne démontre
  causalement l'effet de la couverture seule, car l'agrégation change aussi.

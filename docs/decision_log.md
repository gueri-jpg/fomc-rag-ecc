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

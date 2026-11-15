# DÉMARRAGE — Kit V2 Codex ECC, démo locale Streamlit

**Date : 15/11/2026.** Système FOMC RAG sujet 5. **Pas besoin de Docker ni de déploiement cloud.** Les consignes officielles acceptent explicitement une démo testable à défaut de déploiement. Deadline : 30/11/2026.

## Ce que contient le kit
- Instructions `AGENTS.md` (automatiquement détectées par Codex), `CODEX_MASTER_PROMPT.md`, les prompts des phases dans `prompts/`.
- Consignes officielles et protocole scientifique dans `project_spec/`.
- **145 questions**, **279 qrels page validés par confirmation du groupe**, **294 extraits positifs sourcés**, 30 paraphrases TEST, 10 questions non répondables CANDIDATES non validées. Les 279 couples page ont grade 1/2 uniquement ; les pages non évaluées restent inconnues.
- Sources de cours et capture dans `references_local_only/` (NE PAS publier), manifeste SHA256 des 93 PDF, scripts de contrôle et export.
- Aucun modèle installé, aucune expérience effectuée, aucun rapport statistique fabriqué.

## Installation du kit — attention au bon dossier
1. Sauvegarde ton dossier projet actuel (ou commit des sources, sans secrets).
2. Sur Windows, ouvre **le dossier le plus profond `ML-RAG-master`** contenant `utils`, `test.py`, `.vscode`, `__init__.py` : sur ta capture il apparaît après `ML-RAG > ML-RAG-master > ML-RAG-master`.
3. Extrais **le CONTENU de ce ZIP** dans ce dossier. Au niveau de `utils/` doivent apparaître `AGENTS.md`, `CODEX_MASTER_PROMPT.md`, `project_spec/`, `prompts/`, `evaluation/`, `scripts/`. Ne pas mettre ces fichiers dans `utils/`, ni garder un niveau de dossier ZIP en trop.
4. Ne pas remplacer ni publier le `.env` existant. `.gitignore` exclut `.env` et `references_local_only/`. Les identifiants présents dans un historique Git public doivent être révoqués/rotatés.
5. Dans VS Code > Terminal PowerShell, depuis la racine :

```powershell
py -3 scripts/preflight_codex.py --hash-pdfs
py -3 scripts/verify_kit_v2.py
```

Si `py -3` n'est pas disponible : `python scripts/...`. Aucun package supplémentaire n'est requis pour ces deux scripts. Un message PASS signifie **intégrité des fichiers**, pas entraînement réussi ni exhaustivité des qrels.

6. Ouvre `CODEX_MASTER_PROMPT.md` et colle son contenu dans Codex, ou colle le petit message dans `PROMPT_DEPART_A_COPIER.txt`.
7. Codex démarre UNIQUEMENT `prompts/01_PHASE_0_AUDIT.md`. Après vérification du compte-rendu, demander `prompts/02_PHASE_1_CORPUS_EDA.md`, puis phases suivantes.

## Phases et commandes futures

- Phase 0: audit secrets/Git, dépendances, architecture sans supprimer le prototype.
- Phase 1: extraction 93 PDF, 838 pages, EDA, segmentation; tests et statistiques réelles.
- Phase 2: import des grades acceptés, alignement extraits/chunks; ne refaire ni la double annotation ni les 1740 vérifications si elles existent déjà réellement.
- Phase 3: BM25, Dense, Hybrid-RRF sans reranking (première comparaison), sélection des nouveaux candidats non jugés.
- Phase 4: reranking + ablations avec top20 constant.
- Phase 5: génération sourcée, abstention.
- Phase 6: métriques/robustesse/erreurs et intervalles de confiance sous réserve qrels suffisants.
- Phase 7: **application Streamlit locale** et tests E2E; exemple cible `streamlit run app/streamlit_app.py` (à coder par Codex; ne fonctionne pas encore).
- Phase 8: rapport/PPT/vidéo 15–20 min, empaquetage reproduction.

## Ce qui n'est PAS inclus dans le ZIP
- Les PDF FOMC ne sont PAS dupliqués : ils sont déjà dans le dépôt `utils/TxtExtraction/TextsData/`.
- Le fichier `.env` et des secrets : jamais inclus.
- Des modèles ML, embeddings, index préconstruits ou résultats d'expériences : Codex doit les créer et les documenter.
- Les formulaires individuels des deux annotateurs : non transmis. Les 279 grades ont été **confirmés par déclaration de l'équipe** ; l'accord chiffré n'est donc pas calculable ici.

## Protocole scientifique
Pour les qrels à utiliser : `evaluation/benchmark/qrels_group_confirmed_PAGES.trec` (grade confirmé par groupe, **jeu de pages positif annoté, potentiellement incomplet**). Le `POOLING_TO_REVIEW_1740.csv` comporte des candidats non jugés dans le fichier ; ne pas supposer qu'ils sont négatifs, ni refaire arbitrairement les preuves que l'équipe a déjà jugées. Pour intégrer d'autres jugements manuels disponibles, se reporter à `project_spec/VALIDATION_BENCHMARK_ET_QRELS.md`.

## Application locale
Le livrable attendu est une interface de recherche et question-réponse utilisable sur le PC, avec possibilité de saisir une question, sélectionner BM25/Dense/Hybride et reranker, voir le texte récupéré, ses sources, score, temps et une réponse générée citée ou une abstention. Les captures et la démonstration vidéo doivent être fondées sur un vrai lancement, pas des maquettes.

# PHASE 7 — APPLICATION STREAMLIT LOCALE (PAS de Docker / Cloud)

**C'est l'alternative permise par les consignes ECC. Ne PAS perdre du temps à créer Dockerfiles/FastAPI ni à demander un compte cloud.**

1. Construire `app/streamlit_app.py` exécutée avec `streamlit run app/streamlit_app.py`, compatible avec Windows et CPU si possible. Gérer proprement absence de poids de modèles (message précis + commande de préparation), timeouts et absence d'API externe.
2. UI : question libre, sélection BM25/Dense/Hybrid, activation reranking None/MiniLM/BGE selon disponibilité, topk, génération LLM si réellement disponible ou extraction de secours explicitement étiquetée.
3. Montrer les meilleurs chunks classés, textes, PDF source, type, date, page, scores, latences. Afficher les preuves qui justifient la réponse, bouton/option d'abstention quand insuffisant.
4. Vue démo scientifique : graphique comparatif depuis résultats **réellement calculés**, différencier métriques basées sur qrels partiels vs jugés complets; page EDA et limites; pas de tableaux inventés.
5. Tests smoke Streamlit et tests manuels navigables; capturer preuves (captures d'écran), générer guide `README` 3 commandes Windows et 3 commandes Linux. Ne jamais exposer `.env` dans UI/logs.
6. `reports/progress/PHASE_7.md` preuves de lancement/réponse, temps et limites.

**Acceptation :** une personne du groupe peut lancer Streamlit et tester des questions, sans Docker, DB, API ou déploiement. **S'arrêter**.

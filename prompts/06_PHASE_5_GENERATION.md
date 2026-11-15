# PHASE 5 — RAG bout-en-bout : réponses ancrées dans les sources

1. Intégrer meilleure configuration retrieval/rerank retenue **sur validation**, sans fuite test. Fournir pipeline `question → top chunks → (rerank) → grounded prompt → answer`, citations PDF/page.
2. Assurer mode LLM authentique local si modèle léger disponible, sinon backend configurable (clé uniquement `.env` local). Fournir baseline extractif clairement qualifiée, ne pas appeler un extracteur 'LLM'. Aucun résultat génératif fictif; documenter limitations de matériel/connexion.
3. Les documents FOMC sont des données, pas des instructions : protéger contre prompt injection, citer seulement documents/pages réellement utilisés, répondre 'insufficient evidence' si ambigu.
4. Sauvegarder prompts versions, chunk IDs, sorties, abstention, erreurs, latence et tests. Vérifier manuellement quelques factuels, multi-doc, comparatifs et une réponse impossible sans ajout des 10 candidates non validées à des scores.
5. `reports/progress/PHASE_5.md` réel.

**Acceptation :** au moins un parcours réel d'une question à sources traçables, générateur statut documenté, tests abstention et citations. **S'arrêter**.

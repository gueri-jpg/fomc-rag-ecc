# Etat initial verifie — archive ML-RAG-master.zip (14/11/2026)

## Inventaire constate

- 120 entrees dans l'archive d'origine, dont **93 PDF** : 46 `minutes` et 47 `statements`, reunis dans `utils/TxtExtraction/TextsData/`.
- 10 fichiers `.py` (dont scripts de test tres rudimentaires), des `.pyc`, un `.vscode/settings.json` et un `.env` : **ne jamais publier le contenu de `.env`**.
- `utils/TxtExtraction/Pdf2Txt.py` : extraction par PyMuPDF, juxtaposition de plusieurs documents dans une seule chaine, spaCy/NLTK, minuscules, ponctuation et stopwords supprimes, lemmatisation, chunks de 128 tokens, embeddings `sentence-transformers/all-MiniLM-L12-v2`.
- `utils/database/StockVectors.py` : `psycopg2`, insertion dans `docs(content,embedding vector(384))` et index pgvector ; l'extension `vector` et l'unicite des lignes ne sont pas prises en charge dans le script (a traiter).
- `utils/main.py` : traitement par lots et inserions successives ; detection des dates par slicing de noms de fichiers ; tables sources/pages non conservees a l'insertion.

## Faiblesses exigeant correction

1. Concatener les PDF avant le chunking fait perdre la provenance precise, difficile a reconstruire apres coup.
2. Le texte normalise agressivement perd la ponctuation, les nombres et le style utiles a la generation et aux citations ; conserver le `raw_text` pour RAG.
3. Les noms de PDF, dates, pages et types n'accompagnent pas les embeddings de la table d'origine.
4. La fonction de chunking historique n'a pas la transparence, l'overlap et le controle de frontieres attendus pour une evaluation fiable.
5. Risque de duplications a chaque insertion ; index pgvector sans procedures systematiques d'UPSERT/migrations.
6. Pas de baseline BM25, hybridation, reranking, evaluation reproductible ou generation LLM dans cette archive initiale.
7. `.env` local peut contenir des secrets et ne doit pas etre copié dans des artefacts publics ; **ne pas lire les valeurs en logs**.
8. Le vieux code de test se connecte a la BDD a l'import : remplacer par des tests isolés/offline.

## Benchmark de depart (verifie en structure, pertinences encore provisoires)

- **145 questions** (`85 dev`, `30 validation`, `30 test`), 294 candidats de preuve textuelle, 279 couples question-page, 93 PDF, 838 pages.
- 30 paraphrases test associees a 30 questions test, et 10 candidates sans reponse **non validees**.
- Les 294 citations ont une source identifiable, mais les grades de pertinence ne constituent **pas** un standard gold. Le benchmark source fournit un fichier d'audit ainsi qu'un pooling TF-IDF preliminaire : ce ne sont pas des qrels exhaustifs.
- Seules 4 questions portent explicitement la categorie `multi_document` dans les metadonnees : **la qualite de cet equilibre doit etre revue**, sans cosmetiquement changer des etiquettes.
- Risque de doublons semantiques entre questions source 2021, jeu 110 et supplement 2023-2024 : verifier les clusters avant de figer le test.

## Ancien prototype de reference fourni separement

`references_local_only/FOMC-RAG-projet-complet_REFERENCE.zip` contient une precedente implementation (BM25/Dense/Hybrid/RRF, rerankers, API et UI). **Utiliser comme point de comparaison de code**, apres tests et audit ; ne pas l'importer tel quel sans adaptation. Des resultats y sont marques « provisoires ». Sa recherche applique un filtrage sur des dates explicites, **ce qui pourrait exclure des preuves interannuelles** ; ce filtre doit etre desactive par defaut pour l'etude principale. Ne jamais reprendre les donnees d'evaluation de l'ancien prototype si elles sont differentes du benchmark 145.


## Changement de décision V2 (15/11/2026)
Le groupe a confirmé la double annotation et les grades des 279 associations question–page. Le prototype n’a plus à dépendre d’un serveur PostgreSQL ni de Docker : stockage local et démo Streamlit testable suffisent. Ne jamais imprimer les valeurs du fichier `.env`.

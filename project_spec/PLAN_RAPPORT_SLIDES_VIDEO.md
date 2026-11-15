# Structure de rapport, PPTX et video conforme aux exigences ECC

## Rapport ecrit — trame conseillee

1. Page de garde, equipe, sujet exact, resume, mots-cles.
2. Contexte : FOMC, Minutes, Statements, recherche documentaire; problematique et questions RQ1–RQ5.
3. Etat de l'art avec sources : RAG, recherche lexicale BM25, embeddings, dual encoder, fusion RRF, reordonnancement CrossEncoder, MMR et evaluation de la recherche d'information.
4. Methodologie : source des PDF, licence/acces, date de collecte, donnees, analyse exploratoire, extraction, chunking et metadonnees.
5. Evaluation : constitution 145 Q, provenance initiale, biais interannuel, pooling, double annotation, qrels, dev/val/test, variantes et non repondables.
6. Implementations : BM25, Dense, Hybrid, CrossEncoders, generateur LLM, citations, interface Streamlit locale, choix d'outils, calcul/hardware.
7. Resultats reels : tableaux metrics, ablations, latences, graphiques IC apparies.
8. Interpretabilite : analyse detaillee d'erreurs, explications de scores et echecs de retrieval; mentionner comme methode explicative conforme a la consigne.
9. Resultats de generation : fidelite aux sources, citations, exactitude, abstention, robustesse.
10. Discussion : biais du corpus, qrels incomplets, taille test 30, controle qualite, compromis performances/cout.
11. Conclusion, perspectives et reproductibilite; bibliographie, annexes configs/commandes et attribution des roles.

## Presentation PowerPoint — 14 diapositives proposees

1. Titre / projet / equipe ; 2. probleme ; 3. objectifs/RQ ; 4. corpus/EDA ; 5. pipeline ; 6. benchmark, splits et biais ; 7. BM25 vs Dense vs Hybrid ; 8. reranking ; 9. metriques/evaluation ; 10. resultats retrieval ; 11. resultats reranking/ablations ; 12. demo QA sourcée ; 13. interpretabilite et limites ; 14. conclusions/démo locale.

## Video 15–20 min — storyboard possible (18 min)

- 0:00–1:30 : contexte et besoin utilisateur.
- 1:30–3:30 : corpus, extraction et EDA.
- 3:30–6:00 : architecture retrieval BM25/Dense/Hybrid.
- 6:00–8:00 : benchmark, qrels, prevention des fuites et biais interannuels.
- 8:00–10:30 : comparaison retrieval, reranking et results **reels**.
- 10:30–13:00 : analyse d'erreurs / robustesse.
- 13:00–16:30 : demonstration en direct ou capture de l'application (question, sources, reponse et citations).
- 16:30–18:00 : deployment, limites, conclusion.

Codex doit rediger les textes, produire slides, une checklist d'enregistrement et verifier les captures de resultats ; **la video elle-meme est un travail humain/de montage reel** et ne doit pas etre declaree fournie sans fichier video.


**Kit V2 :** Le déploiement cloud et Docker ne font pas partie des livrables nécessaires. Documenter le test de Streamlit exécuté localement, avec captures de l’interface, commandes réelles et storyboard pour la vidéo de 15–20 minutes.

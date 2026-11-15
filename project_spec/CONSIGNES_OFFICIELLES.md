# Consignes et livrables — capture « Projets ML_ECC » fournie

> Transcription du contenu visible dans la capture d'ecran transmise. Source : onglet « Consignes et livrables » du tableur `Projets ML_ECC`. Date limite visible : **30 novembre**. D'autres precisions orales ou dans d'autres onglets ne sont pas presumees connues.

## Consignes generales (source)

1. Chaque projet doit comporter une partie theorique presentant les fondements de tous les concepts, methodes et algorithmes utilises.
2. Une phase de pretraitement et d'analyse exploratoire des donnees est obligatoire.
3. Comparaison des differents modeles, dont un modele de reference (*baseline*) simple et d'autres plus avances.
4. Prevention des fuites de donnees : separer les jeux d'entrainement, de validation et de test **avant tout pretraitement**.
5. Interpretabilite des modeles : integrer obligatoirement une analyse de l'interpretabilite en utilisant au moins une methode adaptee : SHAP, importance des variables par permutation ou **analyse detaillee des erreurs**.
6. Donnees utilisees : privilegier les jeux de donnees ouverts (*open data*) ou, si necessaire, des donnees synthetiques generees par l'equipe. Preciser la source des donnees et decrire leur mode de preparation.
7. La solution finale doit etre automatisee et deployee, si possible (par exemple via Streamlit, Flask, une API, etc.).
8. Code et gestion du projet : chaque equipe doit disposer d'un depot Git contenant le code source, les donnees ou les scripts permettant de les obtenir, ainsi qu'un fichier README decrivant les etapes d'installation, d'execution et de reproduction des resultats.
9. Technologies et bibliotheques : utiliser Python et les bibliotheques adaptees au sujet, comme scikit-learn, LightGBM, XGBoost, PyTorch, Hugging Face, Gymnasium ou autres selon les besoins du projet.

## Livrables (source)

1. Rapport ecrit : contexte, problematique, objectifs, fondements theoriques, methodologie, resultats obtenus et discussion.
2. Presentation video du projet, accompagnee d'une demonstration des principales fonctionnalites et des resultats (**15–20 minutes**).
3. Presentation PowerPoint.
4. Code source et fichiers necessaires a l'execution du projet et a la reproduction des experiences.
5. Donnees utilisees, sources et description des traitements effectues.
6. Deploiement de la solution ou, a defaut, demonstration permettant de tester son fonctionnement.

**Echeance : 30 novembre 2026.**

## Traduction operationnelle POUR CE RAG (interpretation proposee, pas texte officiel)

- La « baseline simple » peut etre un BM25 sans reranking ; avancés = Dense, fusion hybride, puis rerankers ; comparaison a conditions egales.
- Pour la prevention des fuites : sauvegarder les splits des **questions** avant la selection des parametres, avant toute analyse exploratoire des performances et avant toute construction de jeux d'entrainement/apprentissage. Dans un corpus RAG fixe, l'indexation non supervisee des 93 PDF peut concerner le corpus entier, mais les requetes/references du test ne doivent jamais servir a regler le pipeline ; justifier explicitement cette difference dans le rapport. Si un modele est fine-tune, isoler strictement les donnees apprises, de validation et de test.
- Pour l'interpretabilite : analyse detaillee des erreurs, obligatoire et plus appropriee au classement de passages que SHAP ajoute artificiellement. Ajouter audits de contributions BM25, cosine et RRF, ainsi qu'exemples de faux positifs/negatifs.
- Pour les donnees publiques : identifier les documents FOMC fournis, leurs dates, type, nombre de pages, provenance; ne pas inventer de source ou licence.
- Le sujet fourni dans notre echange : « Optimisation et deploiement d'un systeme de generation augmentee par recuperation (RAG) pour la question-reponse : etude comparative des strategies de recuperation et de reordonnancement (reranking) et proposition d'un cadre d'evaluation rigoureux. »

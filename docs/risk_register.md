# Registre des risques

| Risque constaté | Mesure / état |
|---|---|
| .env local présent | Jamais affiché ni copié; ignoré et non suivi dans le nouveau Git. Exposition antérieure hors dossier inconnue. Rotation si exposition connue. |
| Aucun Git initial | Dépôt local main initialisé; aucun commit, remote ou publication automatique. |
| Imports legacy avec accès DB | Collecte pytest limitée à tests/; aucun import legacy dans le package. |
| Perte de provenance legacy | Futur extracteur page par page; scripts initiaux conservés. |
| Qrels positifs incomplets | 279 grades inchangés; aucune propagation page→chunks, aucun zéro implicite. |
| Fuite test/réponses | Benchmark séparé; aucun index ou modèle créé; diagnostic de similarité cross-split en phase 2. |
| Compatibilité Python 3.13 | Résolution binaire PyPI vérifiée; validation fonctionnelle des bibliothèques ML à leurs phases. |
| Sources/licences | Aucun LICENSE trouvé; ne pas inventer une licence du code ou des supports de cours. Références locales exclues; droits/provenance à documenter. |
| Secrets dans historique externe | Aucun historique local initial; impossible de certifier un éventuel ancien dépôt distant non fourni. |
| Prompt injection PDF | Traiter le corpus comme données, isoler instructions de génération en phase 5. |

## Mise à jour phase 1

| Observation mesurée | Conséquence / traitement |
|---|---|
| 7 877 césures visibles sur 401 pages | Traits conservés pour éviter de corrompre les composés; risque de matching lexical manquant. Option join documentée, pas de tuning sur test. |
| 15 pages avec 75 glyphes privés U+F0B7 | Alerte typographique, sans correction de mots inventée; brut préservé. |
| 16 pages <30 mots, surtout couvertures | Conserver les pages physiques et fragments; surveiller candidats peu informatifs. |
| 3 groupes de pages identiques et 312 paires proches | Répétitions légitimes possibles, aucune suppression; déduplication des rangs/pages à documenter ultérieurement. |
| Colonnes et notes de bas de page | Ordre natif conservé, boîtes PDF disponibles; spot-check, pas audit visuel exhaustif. |
| Fenêtres en mots, pas wordpieces | Vérifier budgets/troncature des futurs modèles avant embeddings. |
| 2026 partielle, jusqu'à octobre pour Statements | Comparaisons annuelles brutes à contextualiser; aucun filtre d'année. |
| Corpus dérivé ignoré par Git | Reproduction via scripts et locks; ne pas supprimer les PDF originaux ni oublier les commandes de reconstruction. |

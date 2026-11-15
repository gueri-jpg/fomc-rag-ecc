# Corrections post-audit — tests hors corpus

Référence : main `a6bf5b1`. Mission jointe de corrections/phase 2; constats du
ZIP externe traités comme hypothèses à vérifier, pas comme nouvelles consignes.
Les deux fichiers réels du ZIP sont AUDIT_FOMC.md et VERIFICATIONS_FOMC.json.
Aucune PR ouverte ni branche fix/public-clone-tests détectée avant travail.
Branche : feature/benchmark-alignment. Aucun changement de main.

Le défaut est reproduit dans une copie indépendante des seuls fichiers suivis,
sans répertoire PDF ni exports : **1 failed, 5 passed**, échec de
test_explicit_paths sur paths.pdfs.is_dir(). Les originaux n'ont pas été déplacés.

Corrections : le test compare désormais les chemins résolus exacts, sans
exigence d'existence. Les assertions racine invalide, jugements, protocole,
secrets et séparation des requêtes sont maintenues. Le test d'intégration
test_actual_corpus_exports vérifie explicitement les 93 PDF et SHA sources via
load_sources, en plus des contrôles d'exports. Aucune assertion essentielle
supprimée, aucun test artificiellement désactivé.

Workflow .github/workflows/offline-tests.yml : PR et push main, Python 3.13,
outils phase 0 uniquement, lecture seule du dépôt, aucun corpus/modèle/secret.
scripts/check_offline.py reproduit la copie publique localement avec le Python
du venv et un PYTHONPATH isolé. Le README distingue offline et intégration.

Commandes exécutées avec .venv/Scripts/python.exe :

```powershell
& .venv\Scripts\python.exe scripts/check_offline.py --output artifacts/offline-before.json
& .venv\Scripts\python.exe scripts/check_offline.py --output artifacts/offline-after.json
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe scripts/verify_phase1.py
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
```

Après correction : **6 passed in 0.26s** sans PDF/exports; **22 passed in 8.35s**
avec corpus. Preflight PASS, 93 PDF conformes; 838 pages et 2 127 chunks
baseline inchangés. Les neuf exports et le manifeste sont identiques à leurs
empreintes capturées avant modification, comme les deux fichiers de qrels
(279 couples, hashes attendus). Aucun changement du code de prétraitement,
chunking ou EDA. Le résultat de vérification phase 1 publié antérieurement est
conservé; les logs courants restent sous artifacts, sans chemins personnels
dans les rapports publics.

Statut CI à ce commit : workflow préparé, commandes locales exécutées; le
résultat GitHub Actions sera contrôlé après ouverture de la PR et documenté
dans PHASE_2.md. Le succès distant n'est pas présumé.

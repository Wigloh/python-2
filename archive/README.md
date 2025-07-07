# 📁 Archive des Fichiers Obsolètes - PROJET MSPR

Ce dossier contient tous les fichiers qui ont été développés pendant le projet mais qui ne sont plus nécessaires pour la version finale de production.

## 📂 Structure de l'Archive

### 🗂️ `old_apps/`
**Applications Flask obsolètes remplacées par `app_complete.py`**
- `mspr912.py` - Version originale avec appels externes OpenFaaS
- `app.py` - Version basique pour tests handlers (si existait)
- `app_simple.py` - Version intermédiaire sans templates externes (si existait)

### 🧪 `old_tests/`
**Tests de développement remplacés par les tests finaux**
- `simple_test.py` - Test basique des handlers
- `test_2fa_complete.py` - Doublon de validation_finale.py
- `test_login_complete.py` - Tests login intégrés ailleurs
- `test_simple.py` - Tests création utilisateur de base
- `test_simple_fixed.py` - Version corrigée des tests simples
- `test_login_simple.py` - Tests login basiques
- `test_login_fixed.py` - Version corrigée des tests login
- `test_login_handler.py` - Tests spécifiques handler login
- `test_quick.py` - Tests rapides de développement
- `test_working.py` - Tests fonctionnels temporaires
- `test_login_complete.py` (du dossier tests/) - Doublon

### 🚀 `old_deployment/`
**Scripts de déploiement remplacés par les versions finales**
- `deploy_openfaas.sh/.bat` - Remplacés par `deploy_full.sh` et `finalisation_complete.bat`
- `prepare_openfaas.sh/.bat` - Intégrés dans les scripts finaux
- `test_deployment.sh` - Intégré dans la validation finale
- `test_full_deployment.sh/.bat` - Remplacés par les scripts consolidés

### ⚙️ `old_configs/`
**Configurations intermédiaires remplacées par les versions production**
- `openfaas-minimal.yaml` - Remplacé par `kubernetes-production.yaml`
- `kubernetes-example.yaml` - Version exemple, remplacée par production

## ✅ Fichiers de Production Conservés

### 🎯 **Application Finale**
- `app_complete.py` - Application Flask complète avec tous les handlers
- `templates/` et `static/` - Interface utilisateur

### 🔧 **Handlers Core**
- `handler.py`, `login_handler.py`, `generate_2fa_handler.py`
- Dossiers OpenFaaS : `create-user/`, `login-user/`, `generate-2fa/`

### 🧪 **Tests Finaux**
- `validation_finale.py` - Test de validation complet
- `test_complete_system.py` - Tests système intégrés
- `tests/test_final.py` - Tests finalisés
- `tests/verification_complete.py` - Vérification complète

### 🚀 **Déploiement Final**
- `finalisation_complete.bat` - Script de déploiement complet Windows
- `deploy_full.sh` - Script de déploiement complet Linux
- `kubernetes-production.yaml` - Manifeste Kubernetes production

### 📚 **Documentation**
- `README.md`, `PROJET_TERMINÉ.md`, `RESUME_FINAL.md`
- `STEP_BY_STEP_GUIDE.md`, `DEPLOYMENT_CONFIG.md`

---

## 📝 Note

Ces fichiers archivés peuvent être consultés pour référence ou récupérés si nécessaire, mais ils ne sont plus utilisés dans la version finale du projet MSPR.

**Date d'archivage :** 7 juillet 2025
**Statut du projet :** COMPLET ET FONCTIONNEL ✅

@echo off
REM Script de préparation pour OpenFaaS (Windows)
REM 🔧 Exécuter ce script pour préparer le déploiement

echo 🚀 Préparation du déploiement OpenFaaS...

REM 1. Créer les répertoires pour les fonctions
echo 📁 Création des répertoires...
mkdir create-user 2>nul
mkdir login-user 2>nul
mkdir generate-2fa 2>nul

REM 2. Copier les handlers
echo 📄 Copie des handlers...
copy handler.py create-user\handler.py >nul
copy login_handler.py login-user\handler.py >nul
copy generate_2fa_handler.py generate-2fa\handler.py >nul

REM 3. Copier les requirements
echo 📦 Copie des requirements...
copy openfaas_requirements.txt create-user\requirements.txt >nul
copy openfaas_requirements.txt login-user\requirements.txt >nul
copy openfaas_requirements.txt generate-2fa\requirements.txt >nul

echo ✅ Préparation terminée !
echo.
echo 🔧 Prochaines étapes :
echo 1. Modifier les URLs dans stack.yml selon votre environnement
echo 2. Créer les secrets Kubernetes
echo 3. Déployer avec faas-cli deploy -f stack.yml
echo.
echo 📝 Fichiers créés :
echo - create-user\ (avec handler.py et requirements.txt)
echo - login-user\ (avec handler.py et requirements.txt)
echo - generate-2fa\ (avec handler.py et requirements.txt)

pause

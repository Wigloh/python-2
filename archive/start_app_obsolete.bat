@echo off
echo ===========================================
echo    Application MSPR - Frontend Flask
echo ===========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Créer l'environnement virtuel s'il n'existe pas
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
    echo Environnement virtuel créé avec succès !
    echo.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dépendances...
echo - Flask et requests pour le frontend
echo - Cryptography pour le chiffrement
echo - PostgreSQL pour la base de données
echo - QRCode et Pillow pour les QR codes
echo.
pip install -r requirements.txt

REM Vérifier les dépendances critiques
echo.
echo Vérification des dépendances critiques...
python -c "import flask; print('✓ Flask installé')"
python -c "import requests; print('✓ Requests installé')"
python -c "import cryptography; print('✓ Cryptography installé')"
python -c "import psycopg2; print('✓ PostgreSQL installé')"
python -c "import qrcode; print('✓ QRCode installé')"
python -c "from PIL import Image; print('✓ Pillow installé')"

REM Démarrer l'application
echo.
echo ===========================================
echo    Démarrage de l'application Flask
echo ===========================================
echo.
echo L'application sera accessible à l'adresse :
echo http://127.0.0.1:5000
echo.
echo ATTENTION: Assurez-vous qu'OpenFaaS est démarré sur :
echo http://localhost:8080/function/
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

python mspr912.py

pause

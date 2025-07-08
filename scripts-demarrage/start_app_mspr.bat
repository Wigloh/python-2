@echo off
echo 🔐 MSPR - Demarrage avec PostgreSQL
echo ====================================

echo 📍 Verification de l'environnement...

REM Verification Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installe ou pas dans le PATH
    echo 💡 Installez Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python detecte

REM Verification PostgreSQL
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL n'est pas installe ou pas dans le PATH
    echo 💡 Installez PostgreSQL depuis https://www.postgresql.org/download/windows/
    echo 💡 Ajoutez C:\Program Files\PostgreSQL\15\bin au PATH
    pause
    exit /b 1
)
echo ✅ PostgreSQL detecte

REM Demarrage du service PostgreSQL
echo �️ Demarrage du service PostgreSQL...
net start postgresql-x64-15 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Impossible de demarrer PostgreSQL (peut-etre deja demarre)
) else (
    echo ✅ Service PostgreSQL demarre
)

REM Installation des dependances
echo �📦 Installation des dependances Python...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Probleme avec l'installation des dependances
    echo 💡 Essayez : pip install flask psycopg2-binary cryptography qrcode[pil] pyotp
    pause
)
echo ✅ Dependances Python installees

REM Configuration base de donnees PostgreSQL
echo 🗄️ Configuration de la base PostgreSQL...
psql -U postgres -c "CREATE DATABASE cofrap;" >nul 2>&1
psql -U postgres -d cofrap -f database_setup.sql >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Base peut-etre deja configuree ou erreur de connexion
    echo 💡 Verifiez votre mot de passe PostgreSQL
) else (
    echo ✅ Base PostgreSQL configuree
)

REM Configuration variables d'environnement pour PostgreSQL
echo 🔧 Configuration des variables PostgreSQL...
set DB_HOST=localhost
set DB_NAME=cofrap
set DB_USER=postgres
set DB_PASSWORD=password
set FERNET_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=
set SECRET_KEY=dev-secret-key-mspr-2025
echo ✅ Variables PostgreSQL configurees

echo.
echo 🚀 Demarrage de l'application MSPR avec PostgreSQL...
echo 📱 Interface disponible sur : http://localhost:5000
echo.
echo 🎯 Pages disponibles :
echo    • http://localhost:5000/        (Accueil)
echo    • http://localhost:5000/create  (Creation compte)
echo    • http://localhost:5000/login   (Connexion 2FA)
echo    • http://localhost:5000/test    (Tests API)
echo.
echo 🗄️ Base de donnees : PostgreSQL (cofrap)
echo.

REM Demarrage de l'application Flask
python app_complete.py

pause

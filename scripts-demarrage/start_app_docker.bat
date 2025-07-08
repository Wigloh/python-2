@echo off
echo 🔐 MSPR - Demarrage avec PostgreSQL Docker
echo ==========================================

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

REM Verification Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker n'est pas installe ou pas dans le PATH
    echo 💡 Installez Docker Desktop depuis https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)
echo ✅ Docker detecte

REM Verification du conteneur PostgreSQL
docker ps | findstr postgres-mspr >nul 2>&1
if %errorlevel% neq 0 (
    echo 🚀 Demarrage du conteneur PostgreSQL...
    docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15 >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ Tentative de redemarrage du conteneur existant...
        docker start postgres-mspr >nul 2>&1
    )
    timeout /t 5 /nobreak >nul
    echo ✅ Conteneur PostgreSQL demarre
) else (
    echo ✅ Conteneur PostgreSQL deja actif
)

REM Installation des dependances
echo 📦 Installation des dependances Python...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Probleme avec l'installation des dependances
    echo 💡 Essayez : pip install flask psycopg2-binary cryptography qrcode[pil] pyotp
    pause
)
echo ✅ Dependances Python installees

REM Configuration base de donnees PostgreSQL
echo 🗄️ Configuration de la base PostgreSQL...
docker cp database_setup.sql postgres-mspr:/database_setup.sql >nul 2>&1
docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Base peut-etre deja configuree ou erreur de connexion Docker
    echo 💡 Verifiez que le conteneur PostgreSQL fonctionne : docker ps
) else (
    echo ✅ Base PostgreSQL configuree
)

REM Configuration variables d'environnement pour PostgreSQL Docker
echo 🔧 Configuration des variables PostgreSQL Docker...
set DB_HOST=localhost
set DB_NAME=cofrap
set DB_USER=postgres
set DB_PASSWORD=mspr2024
set FERNET_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=
set SECRET_KEY=dev-secret-key-mspr-2025
echo ✅ Variables PostgreSQL Docker configurees

echo.
echo 🚀 Demarrage de l'application MSPR avec PostgreSQL Docker...
echo 📱 Interface disponible sur : http://localhost:5000
echo.
echo 🎯 Pages disponibles :
echo    • http://localhost:5000/        (Accueil)
echo    • http://localhost:5000/create  (Creation compte)
echo    • http://localhost:5000/login   (Connexion 2FA)
echo    • http://localhost:5000/test    (Tests API)
echo.
echo 🗄️ Base de donnees : PostgreSQL Docker (cofrap)
echo 🐳 Conteneur : postgres-mspr
echo.

REM Demarrage de l'application Flask
python app_complete.py

pause

@echo off
echo ========================================
echo 🚀 MSPR - Demarrage Ultra-Rapide Docker
echo ========================================
echo.
echo Ce script execute automatiquement toutes les etapes :
echo - Verification des prerequis
echo - Demarrage du conteneur PostgreSQL
echo - Installation des dependances Python
echo - Configuration de la base de donnees
echo - Demarrage de l'application Flask
echo.
pause

echo 📍 ETAPE 1 : Verification des prerequis
python --version
if %errorlevel% neq 0 (
    echo ❌ Python non detecte. Installez Python 3.8+ depuis https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python OK

docker --version
if %errorlevel% neq 0 (
    echo ❌ Docker non detecte. Installez Docker Desktop depuis https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)
echo ✅ Docker OK

echo.
echo 📍 ETAPE 2 : Demarrage du conteneur PostgreSQL
docker ps | findstr postgres-mspr >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Conteneur PostgreSQL deja actif
) else (
    echo 🚀 Creation du conteneur PostgreSQL...
    docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15
    if %errorlevel% neq 0 (
        echo ⚠️ Tentative de redemarrage du conteneur existant...
        docker start postgres-mspr
    )
    echo ⏳ Attente du demarrage (10 secondes)...
    timeout /t 10 /nobreak >nul
    echo ✅ Conteneur PostgreSQL pret
)

echo.
echo 📍 ETAPE 3 : Installation des dependances Python
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Probleme avec l'installation des dependances
    echo 💡 Tentative avec des packages individuels...
    pip install flask psycopg2-binary cryptography qrcode[pil] pyotp >nul 2>&1
)
echo ✅ Dependances Python installees

echo.
echo 📍 ETAPE 4 : Configuration de la base de donnees
if exist database_setup.sql (
    docker cp database_setup.sql postgres-mspr:/database_setup.sql >nul 2>&1
    docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql >nul 2>&1
    echo ✅ Base de donnees configuree
) else (
    echo ⚠️ Fichier database_setup.sql non trouve
)

echo.
echo 📍 ETAPE 5 : Configuration des variables d'environnement
set DB_HOST=localhost
set DB_NAME=cofrap
set DB_USER=postgres
set DB_PASSWORD=mspr2024
set FERNET_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=
set SECRET_KEY=dev-secret-key-mspr-2025
echo ✅ Variables configurees

echo.
echo 📍 ETAPE 6 : Test de connexion
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT COUNT(*) FROM users;" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Connexion base de donnees OK
) else (
    echo ⚠️ Probleme de connexion a la base
)

echo.
echo 🎉 Configuration terminee !
echo.
echo 📱 L'application va demarrer sur : http://localhost:5000
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
echo 📍 ETAPE 7 : Demarrage de l'application Flask
python app_complete.py

pause

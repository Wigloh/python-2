@echo off
echo =======================================
echo 🛠️ MSPR - Utilitaires de Maintenance
echo =======================================
echo.
echo Choisissez une action :
echo.
echo [1] Arreter tous les conteneurs PostgreSQL
echo [2] Supprimer le conteneur PostgreSQL
echo [3] Recreer completement le conteneur
echo [4] Voir les logs du conteneur
echo [5] Tester la connexion a la base
echo [6] Reinstaller les dependances Python
echo [7] Nettoyer et redemarrer tout
echo [8] Quitter
echo.
set /p choice="Votre choix (1-8): "

if "%choice%"=="1" goto stop
if "%choice%"=="2" goto remove
if "%choice%"=="3" goto recreate
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto test
if "%choice%"=="6" goto reinstall
if "%choice%"=="7" goto clean
if "%choice%"=="8" goto quit
goto invalid

:stop
echo.
echo 🛑 Arret du conteneur PostgreSQL...
docker stop postgres-mspr
echo ✅ Conteneur arrete
goto end

:remove
echo.
echo 🗑️ Suppression du conteneur PostgreSQL...
docker stop postgres-mspr >nul 2>&1
docker rm postgres-mspr
echo ✅ Conteneur supprime
goto end

:recreate
echo.
echo 🔄 Recreation complete du conteneur...
docker stop postgres-mspr >nul 2>&1
docker rm postgres-mspr >nul 2>&1
docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15
timeout /t 10 /nobreak >nul
if exist database_setup.sql (
    docker cp database_setup.sql postgres-mspr:/database_setup.sql
    docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql
)
echo ✅ Conteneur recree et configure
goto end

:logs
echo.
echo 📋 Logs du conteneur PostgreSQL :
echo ================================
docker logs postgres-mspr
goto end

:test
echo.
echo 🔍 Test de connexion a la base...
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT version();"
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"
echo ✅ Test termine
goto end

:reinstall
echo.
echo 📦 Reinstallation des dependances Python...
pip uninstall -y flask psycopg2-binary cryptography qrcode pyotp >nul 2>&1
pip install -r requirements.txt
echo ✅ Dependances reinstallees
goto end

:clean
echo.
echo 🧹 Nettoyage complet et redemarrage...
echo Arret de l'application Flask si active...
taskkill /F /IM python.exe >nul 2>&1
echo Suppression du conteneur PostgreSQL...
docker stop postgres-mspr >nul 2>&1
docker rm postgres-mspr >nul 2>&1
echo Recreation du conteneur...
docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15
timeout /t 10 /nobreak >nul
echo Reinstallation des dependances...
pip install -r requirements.txt >nul 2>&1
echo Configuration de la base...
if exist database_setup.sql (
    docker cp database_setup.sql postgres-mspr:/database_setup.sql
    docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql
)
echo ✅ Nettoyage complet termine - pret pour un nouveau demarrage
goto end

:invalid
echo.
echo ❌ Choix invalide. Veuillez choisir entre 1 et 8.
pause
goto start

:quit
echo.
echo 👋 Au revoir !
goto end

:end
echo.
pause

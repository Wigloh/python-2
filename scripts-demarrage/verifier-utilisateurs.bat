@echo off
echo =======================================
echo 🔍 MSPR - Verification Base PostgreSQL
echo =======================================
echo.

REM Verification que le conteneur PostgreSQL fonctionne
docker ps | findstr postgres-mspr >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Conteneur PostgreSQL non actif
    echo 💡 Demarrez le conteneur avec : docker start postgres-mspr
    pause
    exit /b 1
)
echo ✅ Conteneur PostgreSQL actif

echo.
echo 📊 Liste des utilisateurs crees :
echo =======================================
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT id, username, gendate, expired FROM users ORDER BY gendate DESC;"

echo.
echo 📈 Statistiques de la base :
echo =======================================
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT COUNT(*) as total_users, COUNT(CASE WHEN expired = false THEN 1 END) as active_users, COUNT(CASE WHEN expired = true THEN 1 END) as expired_users FROM users;"

echo.
echo 🔍 Commandes utiles :
echo =======================================
echo 1. Voir tous les utilisateurs :
echo    docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT * FROM users;"
echo.
echo 2. Voir un utilisateur specifique :
echo    docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT * FROM users WHERE username='nom_utilisateur';"
echo.
echo 3. Compter les utilisateurs :
echo    docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT COUNT(*) FROM users;"
echo.
echo 4. Supprimer un utilisateur (test) :
echo    docker exec -it postgres-mspr psql -U postgres -d cofrap -c "DELETE FROM users WHERE username='nom_utilisateur';"
echo.
echo 5. Se connecter manuellement a PostgreSQL :
echo    docker exec -it postgres-mspr psql -U postgres -d cofrap
echo.

pause

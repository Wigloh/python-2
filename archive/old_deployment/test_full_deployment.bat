@echo off
REM Script de déploiement et test complet pour Windows

echo 🚀 MSPR - Déploiement et Tests Complets
echo ========================================

REM 1. Vérifier que PostgreSQL est en cours d'exécution
echo 📊 1. Vérification de PostgreSQL...
docker ps | findstr "mspr-postgres" >nul
if %ERRORLEVEL% == 0 (
    echo ✅ PostgreSQL est actif
) else (
    echo ❌ PostgreSQL n'est pas actif. Démarrage...
    docker run --name mspr-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=cofrap -p 5432:5432 -d postgres:13
    timeout /t 5 /nobreak >nul
    
    REM Créer la table users
    echo 📝 Création de la table users...
    docker exec mspr-postgres psql -U postgres -d cofrap -c "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password TEXT NOT NULL, secret_2fa TEXT, gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expired BOOLEAN DEFAULT FALSE, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
)

REM 2. Installer les dépendances Python
echo 📦 2. Installation des dépendances Python...
pip install -r requirements.txt

REM 3. Démarrer l'application Flask en arrière-plan
echo 🌐 3. Démarrage de l'application Flask...
start /B python app.py

REM Attendre que Flask soit prêt
echo ⏳ Attente du démarrage de Flask...
timeout /t 5 /nobreak >nul

REM 4. Tests des endpoints
echo 🧪 4. Tests des endpoints...

REM Test 1: Santé du service
echo 🏥 Test 1: Santé du service
curl -s http://localhost:5000/health

echo.

REM Test 2: Créer un utilisateur
echo 👤 Test 2: Création d'un utilisateur
curl -s -X POST http://localhost:5000/api/create-user -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"TestPassword123!\"}"

echo.

REM Test 3: Connexion
echo 🔐 Test 3: Connexion
curl -s -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"TestPassword123!\"}"

echo.

REM Test 4: Générer 2FA
echo 🔑 Test 4: Génération du 2FA
curl -s -X POST http://localhost:5000/api/generate-2fa -H "Content-Type: application/json" -d "{\"username\": \"testuser\"}"

echo.
echo.
echo ✅ Tests terminés !
echo 🌐 Pour utiliser l'application manuellement:
echo    python app.py
echo 🔗 URL: http://localhost:5000
echo.
echo 🛑 Appuyez sur Ctrl+C pour arrêter Flask quand vous avez terminé
pause

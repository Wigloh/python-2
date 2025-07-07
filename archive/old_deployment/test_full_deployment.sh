#!/bin/bash
# Script de déploiement et test complet

set -e

echo "🚀 MSPR - Déploiement et Tests Complets"
echo "========================================"

# 1. Vérifier que PostgreSQL est en cours d'exécution
echo "📊 1. Vérification de PostgreSQL..."
if docker ps | grep -q "mspr-postgres"; then
    echo "✅ PostgreSQL est actif"
else
    echo "❌ PostgreSQL n'est pas actif. Démarrage..."
    docker run --name mspr-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=cofrap -p 5432:5432 -d postgres:13
    sleep 5
    
    # Créer la table users
    echo "📝 Création de la table users..."
    docker exec mspr-postgres psql -U postgres -d cofrap -c "
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password TEXT NOT NULL,
        secret_2fa TEXT,
        gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expired BOOLEAN DEFAULT FALSE,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"
fi

# 2. Installer les dépendances Python
echo "📦 2. Installation des dépendances Python..."
pip install -r requirements.txt

# 3. Démarrer l'application Flask en arrière-plan
echo "🌐 3. Démarrage de l'application Flask..."
python app.py &
FLASK_PID=$!

# Attendre que Flask soit prêt
echo "⏳ Attente du démarrage de Flask..."
sleep 5

# 4. Tests des endpoints
echo "🧪 4. Tests des endpoints..."

# Test 1: Santé du service
echo "🏥 Test 1: Santé du service"
curl -s http://localhost:5000/health | jq '.'

# Test 2: Créer un utilisateur
echo "👤 Test 2: Création d'un utilisateur"
curl -s -X POST http://localhost:5000/api/create-user \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123!"
  }' | jq '.'

# Test 3: Connexion
echo "🔐 Test 3: Connexion"
curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123!"
  }' | jq '.'

# Test 4: Générer 2FA
echo "🔑 Test 4: Génération du 2FA"
GENERATE_2FA_RESPONSE=$(curl -s -X POST http://localhost:5000/api/generate-2fa \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser"
  }')

echo "$GENERATE_2FA_RESPONSE" | jq '.'

# Extraire le code de test
TEST_CODE=$(echo "$GENERATE_2FA_RESPONSE" | jq -r '.test_code')

if [ "$TEST_CODE" != "null" ] && [ "$TEST_CODE" != "" ]; then
    echo "🔍 Test 5: Vérification du 2FA avec le code: $TEST_CODE"
    curl -s -X POST http://localhost:5000/api/verify-2fa \
      -H "Content-Type: application/json" \
      -d "{
        \"username\": \"testuser\",
        \"code_2fa\": \"$TEST_CODE\"
      }" | jq '.'
else
    echo "❌ Impossible d'extraire le code de test du 2FA"
fi

# 5. Nettoyer
echo "🧹 5. Nettoyage..."
kill $FLASK_PID 2>/dev/null || true

echo ""
echo "✅ Tests terminés !"
echo "🌐 Pour utiliser l'application manuellement:"
echo "   python app.py"
echo "🔗 URL: http://localhost:5000"

#!/bin/bash
# 🧪 Script de test complet du déploiement MSPR
# 📝 Teste toutes les fonctions déployées

echo "🧪 Tests du déploiement MSPR..."

# Configuration
OPENFAAS_URL="http://localhost:8080"  # 📝 MODIFIER selon votre setup
FLASK_URL="http://localhost:5000"    # 📝 MODIFIER selon votre setup

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
print_test() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

echo "📋 Configuration des tests :"
echo "- OpenFaaS URL: $OPENFAAS_URL"
echo "- Flask URL: $FLASK_URL"
echo ""

# Test 1 : Vérifier que les pods sont en cours d'exécution
echo "1️⃣ Test des pods Kubernetes..."
kubectl get pods -n mspr-system
kubectl get pods -n openfaas-fn | grep -E "(create-user|login-user|generate-2fa)"

# Test 2 : Test de création d'utilisateur
echo ""
echo "2️⃣ Test de création d'utilisateur..."
RESPONSE=$(curl -s -X POST $OPENFAAS_URL/function/create-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser123"}')

if echo "$RESPONSE" | grep -q "success"; then
    print_test 0 "Création d'utilisateur"
    echo "Réponse: $RESPONSE"
else
    print_test 1 "Création d'utilisateur"
    echo "Erreur: $RESPONSE"
fi

# Test 3 : Test de génération 2FA
echo ""
echo "3️⃣ Test de génération 2FA..."
RESPONSE=$(curl -s -X POST $OPENFAAS_URL/function/generate-2fa \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser123"}')

if echo "$RESPONSE" | grep -q "success"; then
    print_test 0 "Génération 2FA"
    echo "QR Code généré avec succès"
else
    print_test 1 "Génération 2FA"
    echo "Erreur: $RESPONSE"
fi

# Test 4 : Test de connexion à l'application Flask
echo ""
echo "4️⃣ Test de l'application Flask..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $FLASK_URL)

if [ "$HTTP_STATUS" -eq 200 ]; then
    print_test 0 "Application Flask accessible"
else
    print_test 1 "Application Flask (HTTP $HTTP_STATUS)"
fi

# Test 5 : Test de la base de données
echo ""
echo "5️⃣ Test de la base de données..."
DB_TEST=$(kubectl exec -it deployment/postgresql -n mspr-system -- psql -U postgres -d cofrap -c "SELECT COUNT(*) FROM users;" 2>/dev/null)

if [ $? -eq 0 ]; then
    print_test 0 "Base de données accessible"
    echo "Nombre d'utilisateurs: $DB_TEST"
else
    print_test 1 "Base de données"
fi

# Test 6 : Test des secrets Kubernetes
echo ""
echo "6️⃣ Test des secrets Kubernetes..."
SECRETS_COUNT=$(kubectl get secrets -n mspr-system | grep -c -E "(postgresql-secret|encryption-secret|flask-secret)")

if [ "$SECRETS_COUNT" -eq 3 ]; then
    print_test 0 "Secrets Kubernetes ($SECRETS_COUNT/3)"
else
    print_test 1 "Secrets Kubernetes ($SECRETS_COUNT/3)"
fi

# Test 7 : Test des fonctions OpenFaaS
echo ""
echo "7️⃣ Test des fonctions OpenFaaS..."
FUNCTIONS=$(faas-cli list 2>/dev/null | grep -c -E "(create-user|login-user|generate-2fa)")

if [ "$FUNCTIONS" -eq 3 ]; then
    print_test 0 "Fonctions OpenFaaS ($FUNCTIONS/3)"
else
    print_test 1 "Fonctions OpenFaaS ($FUNCTIONS/3)"
fi

# Résumé
echo ""
echo "📊 Résumé des tests :"
echo "- Pods Kubernetes : Vérifiés"
echo "- Création d'utilisateur : Testé"
echo "- Génération 2FA : Testé"
echo "- Application Flask : Testé"
echo "- Base de données : Testé"
echo "- Secrets : Testé"
echo "- Fonctions OpenFaaS : Testé"

echo ""
echo "🔧 Commandes utiles pour le debug :"
echo "- kubectl logs deployment/postgresql -n mspr-system"
echo "- kubectl get pods -n mspr-system"
echo "- kubectl get pods -n openfaas-fn"
echo "- faas-cli list"
echo "- curl -X POST $OPENFAAS_URL/function/create-user -d '{\"username\":\"test\"}'"

echo ""
echo "✅ Tests terminés !"

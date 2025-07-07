#!/bin/bash
# Script de préparation pour OpenFaaS
# 🔧 Exécuter ce script pour préparer le déploiement

echo "🚀 Préparation du déploiement OpenFaaS..."

# 1. Créer les répertoires pour les fonctions
echo "📁 Création des répertoires..."
mkdir -p create-user
mkdir -p login-user
mkdir -p generate-2fa

# 2. Copier les handlers
echo "📄 Copie des handlers..."
cp handler.py create-user/handler.py
cp login_handler.py login-user/handler.py
cp generate_2fa_handler.py generate-2fa/handler.py

# 3. Copier les requirements
echo "📦 Copie des requirements..."
cp openfaas_requirements.txt create-user/requirements.txt
cp openfaas_requirements.txt login-user/requirements.txt
cp openfaas_requirements.txt generate-2fa/requirements.txt

# 4. Créer les fichiers .yml individuels
echo "⚙️ Création des fichiers de configuration..."

# create-user.yml
cat > create-user.yml << 'EOF'
version: 1.0
provider:
  name: openfaas
  gateway: http://localhost:8080

functions:
  create-user:
    lang: python3
    handler: ./create-user
    image: create-user:latest
    environment:
      DB_HOST: postgres
      DB_NAME: cofrap
      APP_NAME: "MSPR App"
      ISSUER_NAME: "MSPR Security"
EOF

# login-user.yml
cat > login-user.yml << 'EOF'
version: 1.0
provider:
  name: openfaas
  gateway: http://localhost:8080

functions:
  login-user:
    lang: python3
    handler: ./login-user
    image: login-user:latest
    environment:
      DB_HOST: postgres
      DB_NAME: cofrap
EOF

# generate-2fa.yml
cat > generate-2fa.yml << 'EOF'
version: 1.0
provider:
  name: openfaas
  gateway: http://localhost:8080

functions:
  generate-2fa:
    lang: python3
    handler: ./generate-2fa
    image: generate-2fa:latest
    environment:
      DB_HOST: postgres
      DB_NAME: cofrap
      APP_NAME: "MSPR App"
      ISSUER_NAME: "MSPR Security"
EOF

echo "✅ Préparation terminée !"
echo ""
echo "🔧 Prochaines étapes :"
echo "1. Modifier les URLs dans stack.yml selon votre environnement"
echo "2. Créer les secrets : kubectl create secret generic..."
echo "3. Déployer : faas-cli deploy -f stack.yml"
echo ""
echo "📝 Fichiers créés :"
echo "- create-user/ (avec handler.py et requirements.txt)"
echo "- login-user/ (avec handler.py et requirements.txt)"
echo "- generate-2fa/ (avec handler.py et requirements.txt)"
echo "- create-user.yml, login-user.yml, generate-2fa.yml"

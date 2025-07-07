#!/bin/bash
# 🔐 Script de création des secrets Kubernetes pour MSPR
# 📝 Modifier les valeurs selon votre environnement

echo "🔐 Création des secrets Kubernetes..."

# 1. Créer le namespace (si nécessaire)
echo "📁 Création du namespace mspr-system..."
kubectl create namespace mspr-system --dry-run=client -o yaml | kubectl apply -f -

# 2. Secret PostgreSQL
echo "🗃️ Création du secret PostgreSQL..."
kubectl create secret generic postgresql-secret \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=POSTGRES_PASSWORD=your_secure_password_here \
  --from-literal=POSTGRES_DB=cofrap \
  --from-literal=DB_HOST=postgresql-service \
  --namespace=mspr-system

# 3. Secret de chiffrement
echo "🔒 Création du secret de chiffrement..."
kubectl create secret generic encryption-secret \
  --from-literal=FERNET_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg= \
  --namespace=mspr-system

# 4. Secret Flask
echo "🌐 Création du secret Flask..."
kubectl create secret generic flask-secret \
  --from-literal=SECRET_KEY=your_flask_secret_key_here \
  --namespace=mspr-system

# 5. Secrets pour OpenFaaS (namespace openfaas-fn)
echo "⚡ Création des secrets OpenFaaS..."
kubectl create secret generic postgresql-secret \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=POSTGRES_PASSWORD=your_secure_password_here \
  --from-literal=POSTGRES_DB=cofrap \
  --from-literal=DB_HOST=postgresql-service \
  --namespace=openfaas-fn

kubectl create secret generic encryption-secret \
  --from-literal=FERNET_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg= \
  --namespace=openfaas-fn

# 6. Vérifier les secrets créés
echo "✅ Vérification des secrets créés..."
echo "Secrets dans mspr-system:"
kubectl get secrets -n mspr-system

echo "Secrets dans openfaas-fn:"
kubectl get secrets -n openfaas-fn

echo ""
echo "🔧 IMPORTANT : Modifier les valeurs suivantes avant la production :"
echo "- POSTGRES_PASSWORD : Utiliser un mot de passe sécurisé"
echo "- FERNET_KEY : Générer une nouvelle clé avec python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
echo "- SECRET_KEY : Générer une clé Flask sécurisée"
echo ""
echo "✅ Secrets créés avec succès !"

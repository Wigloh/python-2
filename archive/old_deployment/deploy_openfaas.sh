#!/bin/bash
# 🚀 Script de déploiement OpenFaaS complet pour MSPR

echo "🚀 Déploiement OpenFaaS pour MSPR..."

# 1. Installation d'OpenFaaS avec Helm
echo "📦 Installation d'OpenFaaS..."
kubectl create namespace openfaas
kubectl create namespace openfaas-fn

# Créer les secrets d'authentification
echo "🔐 Configuration des secrets..."
kubectl -n openfaas create secret generic basic-auth \
  --from-literal=basic-auth-user=admin \
  --from-literal=basic-auth-password=MSPR2025

# Installation avec manifestes
echo "📥 Téléchargement des manifestes OpenFaaS..."
curl -sSL https://raw.githubusercontent.com/openfaas/faas-netes/master/artifacts/install/openfaas.yaml | kubectl apply -f -

# Attendre que les pods soient prêts
echo "⏳ Attente du démarrage d'OpenFaaS..."
kubectl -n openfaas rollout status deployment/gateway

# Port-forward pour accès local
echo "🌐 Configuration de l'accès local..."
kubectl port-forward -n openfaas svc/gateway 8080:8080 &

echo "✅ OpenFaaS déployé !"
echo "🔗 Gateway: http://localhost:8080"
echo "👤 User: admin"
echo "🔑 Password: MSPR2025"

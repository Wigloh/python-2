@echo off
REM 🚀 Script de déploiement OpenFaaS complet pour MSPR (Windows)

echo 🚀 Déploiement OpenFaaS pour MSPR...

REM 1. Installation d'OpenFaaS
echo 📦 Installation d'OpenFaaS...
kubectl create namespace openfaas
kubectl create namespace openfaas-fn

REM Créer les secrets d'authentification
echo 🔐 Configuration des secrets...
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password=MSPR2025

REM Installation rapide avec les composants essentiels
echo 📥 Déploiement des composants OpenFaaS...

REM Gateway
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway
  namespace: openfaas
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gateway
  template:
    metadata:
      labels:
        app: gateway
    spec:
      containers:
      - name: gateway
        image: openfaas/gateway:0.25.4
        env:
        - name: functions_provider_url
          value: "http://127.0.0.1:8081/"
        - name: direct_functions
          value: "true"
        - name: direct_functions_suffix
          value: "openfaas-fn.svc.cluster.local"
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: gateway
  namespace: openfaas
spec:
  type: NodePort
  ports:
  - port: 8080
    targetPort: 8080
    nodePort: 31112
  selector:
    app: gateway
EOF

echo ⏳ Attente du démarrage...
timeout /t 10 /nobreak >nul

echo ✅ OpenFaaS déployé !
echo 🔗 Gateway: http://localhost:31112
echo 👤 User: admin
echo 🔑 Password: MSPR2025

echo.
echo 📋 Commandes suivantes :
echo   kubectl get pods -n openfaas
echo   kubectl get svc -n openfaas

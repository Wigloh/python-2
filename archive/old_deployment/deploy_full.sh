#!/bin/bash
# 🚀 Script de déploiement complet MSPR
# 📝 Ce script déploie toute l'infrastructure

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement complet du système MSPR..."

# Variables de configuration
NAMESPACE="mspr-system"
POSTGRES_PASSWORD="your_secure_password_here"  # 📝 MODIFIER
FERNET_KEY="ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="  # 📝 MODIFIER
FLASK_SECRET="your_flask_secret_key_here"  # 📝 MODIFIER
DOMAIN="mspr.your-domain.com"  # 📝 MODIFIER

echo "📋 Configuration :"
echo "- Namespace: $NAMESPACE"
echo "- Domain: $DOMAIN"
echo ""

# Étape 1 : Créer le namespace
echo "1️⃣ Création du namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Étape 2 : Créer les secrets
echo "2️⃣ Création des secrets..."
kubectl create secret generic postgresql-secret \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  --from-literal=POSTGRES_DB=cofrap \
  --from-literal=DB_HOST=postgresql-service \
  --namespace=$NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic encryption-secret \
  --from-literal=FERNET_KEY=$FERNET_KEY \
  --namespace=$NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic flask-secret \
  --from-literal=SECRET_KEY=$FLASK_SECRET \
  --namespace=$NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

# Étape 3 : Déployer PostgreSQL
echo "3️⃣ Déploiement de PostgreSQL..."
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgresql-pvc
  namespace: $NAMESPACE
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  namespace: $NAMESPACE
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:13
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgresql-secret
              key: POSTGRES_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgresql-secret
              key: POSTGRES_PASSWORD
        - name: POSTGRES_DB
          valueFrom:
            secretKeyRef:
              name: postgresql-secret
              key: POSTGRES_DB
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgresql-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgresql-storage
        persistentVolumeClaim:
          claimName: postgresql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql-service
  namespace: $NAMESPACE
spec:
  selector:
    app: postgresql
  ports:
    - port: 5432
      targetPort: 5432
EOF

# Étape 4 : Attendre que PostgreSQL soit prêt
echo "4️⃣ Attente que PostgreSQL soit prêt..."
kubectl wait --for=condition=available --timeout=300s deployment/postgresql -n $NAMESPACE

# Étape 5 : Initialiser la base de données
echo "5️⃣ Initialisation de la base de données..."
kubectl exec -it deployment/postgresql -n $NAMESPACE -- psql -U postgres -d cofrap -c "
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    secret_2fa TEXT,
    gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_expired ON users(expired);
"

# Étape 6 : Préparer OpenFaaS
echo "6️⃣ Préparation des secrets OpenFaaS..."
kubectl create secret generic postgresql-secret \
  --from-literal=POSTGRES_USER=postgres \
  --from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  --from-literal=POSTGRES_DB=cofrap \
  --from-literal=DB_HOST=postgresql-service.$NAMESPACE.svc.cluster.local \
  --namespace=openfaas-fn \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic encryption-secret \
  --from-literal=FERNET_KEY=$FERNET_KEY \
  --namespace=openfaas-fn \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Déploiement terminé !"
echo ""
echo "🔧 Prochaines étapes :"
echo "1. Préparer les fonctions OpenFaaS : ./prepare_openfaas.sh"
echo "2. Déployer les fonctions : faas-cli deploy -f stack.yml"
echo "3. Déployer l'application Flask"
echo "4. Configurer l'Ingress pour $DOMAIN"
echo ""
echo "🧪 Tests :"
echo "kubectl get pods -n $NAMESPACE"
echo "kubectl logs deployment/postgresql -n $NAMESPACE"

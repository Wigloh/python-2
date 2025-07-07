# 🚀 Guide de Déploiement Étape par Étape

Ce guide vous accompagne dans le déploiement complet du système MSPR.

## 📋 Prérequis

### Outils nécessaires :
- [x] **kubectl** - Client Kubernetes
- [x] **faas-cli** - Client OpenFaaS
- [x] **Docker** - Pour construire les images
- [x] **Cluster Kubernetes** - Minikube, Docker Desktop, ou cluster cloud
- [x] **OpenFaaS** - Installé sur le cluster

### Vérification des prérequis :
```bash
kubectl version --client
faas-cli version
docker version
```

## 🔧 Étape 1 : Configuration

### 1.1 Modifier les variables dans les scripts

**Dans `deploy_full.sh` :**
```bash
POSTGRES_PASSWORD="your_secure_password_here"  # 📝 MODIFIER
FERNET_KEY="ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="  # 📝 MODIFIER
FLASK_SECRET="your_flask_secret_key_here"  # 📝 MODIFIER
DOMAIN="mspr.your-domain.com"  # 📝 MODIFIER
```

**Dans `stack.yml` :**
```yaml
provider:
  gateway: http://your-openfaas-gateway:8080  # 📝 MODIFIER
```

### 1.2 Générer des clés sécurisées

```bash
# Générer une nouvelle clé Fernet
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Générer une clé Flask
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Étape 2 : Déploiement de l'Infrastructure

### 2.1 Déploiement automatique complet
```bash
chmod +x deploy_full.sh
./deploy_full.sh
```

### 2.2 Déploiement manuel (si vous préférez)

**Créer le namespace :**
```bash
kubectl create namespace mspr-system
```

**Créer les secrets :**
```bash
chmod +x create_secrets.sh
./create_secrets.sh
```

**Déployer PostgreSQL :**
```bash
kubectl apply -f kubernetes-example.yaml
```

**Attendre que PostgreSQL soit prêt :**
```bash
kubectl wait --for=condition=available --timeout=300s deployment/postgresql -n mspr-system
```

**Initialiser la base de données :**
```bash
kubectl exec -it deployment/postgresql -n mspr-system -- psql -U postgres -d cofrap -f /tmp/database_setup.sql
```

## ⚡ Étape 3 : Déploiement OpenFaaS

### 3.1 Préparer les fonctions
```bash
chmod +x prepare_openfaas.sh
./prepare_openfaas.sh
```

### 3.2 Construire et déployer les fonctions
```bash
# Construire les images
faas-cli build -f stack.yml

# Déployer les fonctions
faas-cli deploy -f stack.yml
```

### 3.3 Vérifier le déploiement
```bash
faas-cli list
```

## 🌐 Étape 4 : Déploiement de l'Application Flask

### 4.1 Modifier la configuration Flask

**Dans `mspr912.py` :**
```python
# Modifier l'URL OpenFaaS
BASE_URL = os.environ.get('OPENFAAS_URL', 'http://gateway.openfaas:8080/function/')

# Utiliser les variables d'environnement
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'changeme')
```

### 4.2 Créer un Dockerfile pour Flask
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "mspr912.py"]
```

### 4.3 Déployer l'application Flask
```bash
# Construire l'image
docker build -t mspr-flask:latest .

# Déployer dans Kubernetes
kubectl apply -f kubernetes-example.yaml
```

## 🧪 Étape 5 : Tests et Validation

### 5.1 Test automatique complet
```bash
chmod +x test_deployment.sh
./test_deployment.sh
```

### 5.2 Tests manuels

**Test de création d'utilisateur :**
```bash
curl -X POST http://localhost:8080/function/create-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser"}'
```

**Test de génération 2FA :**
```bash
curl -X POST http://localhost:8080/function/generate-2fa \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser"}'
```

**Test de login :**
```bash
curl -X POST http://localhost:8080/function/login-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password", "totp_code": "123456"}'
```

### 5.3 Tests de nos scripts Python
```bash
cd tests
python run_all_tests.py
```

## 🔧 Étape 6 : Configuration de Production

### 6.1 Configurer l'Ingress (accès externe)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mspr-ingress
  namespace: mspr-system
spec:
  rules:
  - host: mspr.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mspr-flask-service
            port:
              number: 80
```

### 6.2 Configurer HTTPS (Let's Encrypt)
```yaml
metadata:
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - mspr.your-domain.com
    secretName: mspr-tls
```

### 6.3 Sécuriser les paramètres
- [ ] Changer tous les mots de passe par défaut
- [ ] Générer de nouvelles clés de chiffrement
- [ ] Configurer les limites de ressources
- [ ] Configurer les health checks
- [ ] Configurer les logs et monitoring

## 📊 Étape 7 : Monitoring et Maintenance

### 7.1 Commandes utiles
```bash
# Vérifier les pods
kubectl get pods -n mspr-system

# Voir les logs
kubectl logs deployment/postgresql -n mspr-system
kubectl logs deployment/mspr-flask-app -n mspr-system

# Vérifier les fonctions OpenFaaS
faas-cli list

# Vérifier les secrets
kubectl get secrets -n mspr-system
```

### 7.2 Maintenance de la base de données
```bash
# Se connecter à PostgreSQL
kubectl exec -it deployment/postgresql -n mspr-system -- psql -U postgres -d cofrap

# Voir les utilisateurs
SELECT id, username, gendate, expired FROM users;

# Nettoyer les utilisateurs expirés
DELETE FROM users WHERE expired = TRUE;
```

## 🚨 Dépannage

### Problèmes courants :

**OpenFaaS ne trouve pas les fonctions :**
```bash
faas-cli list
kubectl get pods -n openfaas-fn
```

**Erreur de connexion à la base de données :**
```bash
kubectl logs deployment/postgresql -n mspr-system
kubectl exec -it deployment/postgresql -n mspr-system -- psql -U postgres -l
```

**Secrets manquants :**
```bash
kubectl get secrets -n mspr-system
kubectl get secrets -n openfaas-fn
```

**Application Flask ne démarre pas :**
```bash
kubectl logs deployment/mspr-flask-app -n mspr-system
```

## ✅ Checklist de Déploiement

- [ ] Prérequis installés (kubectl, faas-cli, docker)
- [ ] Cluster Kubernetes accessible
- [ ] OpenFaaS installé et accessible
- [ ] Variables de configuration modifiées
- [ ] Clés de sécurité générées
- [ ] Infrastructure déployée (PostgreSQL, secrets)
- [ ] Base de données initialisée
- [ ] Fonctions OpenFaaS déployées
- [ ] Application Flask déployée
- [ ] Tests passés avec succès
- [ ] Ingress configuré (pour production)
- [ ] HTTPS configuré (pour production)
- [ ] Monitoring configuré

## 🎉 Félicitations !

Votre système MSPR est maintenant déployé et opérationnel ! 🚀

**Accès :**
- Application Flask : http://your-domain.com
- Fonctions OpenFaaS : http://your-openfaas-gateway:8080/function/
- Base de données : Accessible via les pods Kubernetes

**Fonctionnalités disponibles :**
- ✅ Création d'utilisateurs sécurisée
- ✅ Authentification 2FA avec Google Authenticator
- ✅ Chiffrement des données sensibles
- ✅ Expiration automatique des mots de passe
- ✅ Interface web intuitive
- ✅ API REST complète

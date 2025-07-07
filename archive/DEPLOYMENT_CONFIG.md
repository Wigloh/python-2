# 🚀 Guide de Déploiement - Configuration

Ce document liste toutes les modifications nécessaires pour déployer le système en production.

## 📋 Checklist de Déploiement

### 1. Configuration Base de Données

#### Dans tous les handlers (`handler.py`, `login_handler.py`, `generate_2fa_handler.py`)

```python
# 🔧 MODIFIER CES VALEURS :
DB_HOST = "postgres"  # 📝 KUBERNETES: Nom du service PostgreSQL
DB_NAME = "cofrap"    # 📝 Nom de votre base de données
DB_USER = "postgres"  # 📝 Utilisateur (utiliser les secrets K8s)
DB_PASSWORD = "password"  # 📝 Mot de passe (utiliser les secrets K8s)
```

**Recommandation Kubernetes :**
```yaml
# postgresql-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
type: Opaque
stringData:
  POSTGRES_USER: "votre_utilisateur"
  POSTGRES_PASSWORD: "votre_mot_de_passe_securise"
  POSTGRES_DB: "cofrap"
```

### 2. Configuration de Chiffrement

#### Dans tous les handlers - Fonction `get_encryption_key()`

```python
# 🔧 PRODUCTION: Supprimer la clé par défaut
def get_encryption_key():
    env_key = os.environ.get('FERNET_KEY')
    if env_key:
        return env_key.encode()
    else:
        # 📝 SUPPRIMER cette ligne en production :
        # return b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
        
        # 📝 AJOUTER cette ligne en production :
        raise ValueError("FERNET_KEY environment variable is required")
```

**Recommandation Kubernetes :**
```yaml
# encryption-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: encryption-secret
type: Opaque
stringData:
  FERNET_KEY: "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="  # Générer une nouvelle clé !
```

### 3. Application Flask (`mspr912.py`)

```python
# 🔧 MODIFIER CES VALEURS :
BASE_URL = 'http://localhost:8080/function/'  # 📝 URL de vos fonctions OpenFaaS
app.secret_key = 'supersecretkey'  # 📝 Clé secrète forte pour la production

# 📝 PRODUCTION: Utiliser les variables d'environnement
BASE_URL = os.environ.get('OPENFAAS_URL', 'http://gateway.openfaas:8080/function/')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'changeme')
```

### 4. Configuration 2FA (`generate_2fa_handler.py`)

```python
# 🔧 PERSONNALISER CES VALEURS :
APP_NAME = "MSPR App"  # 📝 Nom affiché dans Google Authenticator
ISSUER_NAME = "MSPR Security"  # 📝 Nom de votre organisation

# 📝 PRODUCTION: Supprimer les informations de debug
response = {
    "message": "2FA setup successful",
    "username": username,
    "qr_code_base64": qr_code_b64,
    # "secret": totp_secret,  # 📝 SUPPRIMER cette ligne !
    # "test_code": current_code,  # 📝 SUPPRIMER cette ligne !
    "instructions": {...},
    "verification_url": f"https://your-domain.com/function/verify-2fa",  # 📝 MODIFIER l'URL
    "status": "success"
}
```

### 5. Structure Base de Données

```sql
-- 📝 CRÉER cette table dans PostgreSQL :
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    secret_2fa TEXT,
    gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 📝 AJOUTER cette colonne
);

-- 📝 CRÉER un index pour les performances :
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_expired ON users(expired);
```

## 🐳 Configuration Docker/Kubernetes

### 1. Variables d'Environnement

```yaml
# deployment.yaml
env:
  - name: DB_HOST
    value: "postgresql-service"
  - name: DB_NAME
    valueFrom:
      secretKeyRef:
        name: postgresql-secret
        key: POSTGRES_DB
  - name: DB_USER
    valueFrom:
      secretKeyRef:
        name: postgresql-secret
        key: POSTGRES_USER
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: postgresql-secret
        key: POSTGRES_PASSWORD
  - name: FERNET_KEY
    valueFrom:
      secretKeyRef:
        name: encryption-secret
        key: FERNET_KEY
  - name: OPENFAAS_URL
    value: "http://gateway.openfaas:8080/function/"
  - name: FLASK_SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: flask-secret
        key: SECRET_KEY
```

### 2. Services Kubernetes

```yaml
# postgresql-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgresql-service
spec:
  selector:
    app: postgresql
  ports:
    - port: 5432
      targetPort: 5432
```

### 3. OpenFaaS Functions

```yaml
# stack.yml
version: 1.0
provider:
  name: openfaas
  gateway: http://gateway.openfaas:8080

functions:
  create-user:
    lang: python3
    handler: ./create-user
    image: your-registry/create-user:latest
    environment:
      DB_HOST: postgresql-service
    secrets:
      - postgresql-secret
      - encryption-secret

  login-user:
    lang: python3
    handler: ./login-user
    image: your-registry/login-user:latest
    environment:
      DB_HOST: postgresql-service
    secrets:
      - postgresql-secret
      - encryption-secret

  generate-2fa:
    lang: python3
    handler: ./generate-2fa
    image: your-registry/generate-2fa:latest
    environment:
      DB_HOST: postgresql-service
    secrets:
      - postgresql-secret
      - encryption-secret
```

## 🔒 Sécurité - Points Critiques

### 1. À Supprimer en Production

- [ ] Clé de chiffrement par défaut dans `get_encryption_key()`
- [ ] Champ `"secret"` dans la réponse de `generate_2fa_handler.py`
- [ ] Champ `"test_code"` dans la réponse de `generate_2fa_handler.py`
- [ ] Clé secrète Flask par défaut dans `mspr912.py`

### 2. À Ajouter en Production

- [ ] Gestion des erreurs de connexion DB
- [ ] Pools de connexions PostgreSQL
- [ ] Logging et monitoring
- [ ] Rotation des clés de chiffrement
- [ ] Validation des entrées utilisateur
- [ ] Rate limiting sur les API

### 3. Variables d'Environnement Requises

```bash
# 📝 OBLIGATOIRES en production :
FERNET_KEY=your_base64_encryption_key
DB_HOST=postgresql-service
DB_NAME=cofrap
DB_USER=postgres
DB_PASSWORD=secure_password
OPENFAAS_URL=http://gateway.openfaas:8080/function/
FLASK_SECRET_KEY=your_flask_secret_key
```

## 🧪 Tests de Déploiement

Après déploiement, tester :

1. **Création d'utilisateur** :
```bash
curl -X POST https://your-domain.com/function/create-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser"}'
```

2. **Login** :
```bash
curl -X POST https://your-domain.com/function/login-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password", "totp_code": "123456"}'
```

3. **Génération 2FA** :
```bash
curl -X POST https://your-domain.com/function/generate-2fa \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser"}'
```

---

**🚨 IMPORTANT :** Ne jamais exposer les secrets ou clés de chiffrement dans le code source !

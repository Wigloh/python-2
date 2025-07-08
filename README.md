# 🔐 MSPR - Système d'Authentification Sécurisé

**Application Flask complète** avec authentification 2FA, chiffrement avancé et interface utilisateur intuitive.

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/votre-repo/mspr)
[![Flask](https://img.shields.io/badge/Flask-2.3+-red.svg)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Security-2FA%20%2B%20Fernet-green.svg)](https://cryptography.io/)
[![Docker](https://img.shields.io/badge/Docker-PostgreSQL-blue.svg)](https://www.docker.com/)
[![OpenFaaS](https://img.shields.io/badge/OpenFaaS-Ready-orange.svg)](https://www.openfaas.com/)

> **🐳 Configuration requise :** PostgreSQL exclusivement via conteneur Docker (aucune installation locale nécessaire)

---

## 📋 **Table des matières**

- [🧩 Objectifs fonctionnels](#-objectifs-fonctionnels)
- [🎯 Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [🚀 Démarrage rapide](#-démarrage-rapide)
- [💻 Interface utilisateur](#-interface-utilisateur)
- [🔧 Configuration](#-configuration)
- [🗄️ Base de données](#️-base-de-données)
- [☁️ Déploiement OpenFaaS](#️-déploiement-openfaas)
- [🔒 Sécurité](#-sécurité)
- [🛠️ Développement](#️-développement)

---

## 🎯 **Fonctionnalités - Vue d'ensemble**

### ✅ **Système complet d'authentification (Objectifs 1-4)**
- **Création automatisée de comptes** avec mots de passe complexes (24 caractères) → **Objectif 1**
- **Authentification 2FA** compatible Google Authenticator → **Objectif 2**  
- **QR Codes sécurisés** pour mot de passe et configuration 2FA → **Objectifs 1 & 2**
- **Gestion d'expiration** des comptes (6 mois) → **Objectif 4**
- **Chiffrement complet** des données (Fernet) → **Objectifs 1 & 2**

### ✅ **Interface utilisateur intuitive (Objectif 5)**
- **Page d'accueil** avec navigation claire
- **Formulaires simples** pour création et connexion
- **Messages d'erreur** contextuels et user-friendly
- **Design responsive** compatible mobile
- **Interface de test** pour développeurs

### ✅ **Architecture sécurisée (Support des 5 objectifs)**
- **Handlers OpenFaaS** pour architecture serverless
- **Base PostgreSQL** avec chiffrement des données sensibles
- **Sessions sécurisées** avec protection CSRF
- **Validation en temps réel** des codes 2FA → **Objectif 3**

### 🔄 **Cycle de vie complet des comptes**
```
Création → Configuration 2FA → Authentification → Expiration (6 mois) → Renouvellement
   ↓             ↓                    ↓                    ↓               ↓
Obj. 1        Obj. 2              Obj. 3              Obj. 4         Obj. 1+2
```

---

## 🏗️ **Architecture - Mapping des objectifs**

```
┌─────────────────────────────────────────────────────────────┐
│                🌐 Interface Web Flask (Objectif 5)          │
├─────────────────────────────────────────────────────────────┤
│  📱 Pages et leurs objectifs :                             │
│  • /           → Page d'accueil (navigation globale)        │
│  • /create     → Création compte (Objectif 1)              │
│  • /login      → Authentification 2FA (Objectif 3)         │
│  • /test       → Interface API (développeurs)               │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│            🔧 Handlers Business Logic par objectif          │
├─────────────────────────────────────────────────────────────┤
│  • handler.py           → Objectifs 1 & 2 (Création + 2FA) │
│  • login_handler.py     → Objectifs 3 & 4 (Auth + Expir.)  │
│  • generate_2fa_handler → Objectif 2 (Gestion 2FA dédiée)  │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│         🗄️ Base PostgreSQL (Support tous objectifs)        │
├─────────────────────────────────────────────────────────────┤
│  Table: users                                               │
│  • username (unique)              → Objectifs 1, 3         │
│  • password (chiffré Fernet)      → Objectifs 1, 3         │
│  • secret_2fa (chiffré Fernet)    → Objectifs 2, 3         │
│  • gendate (timestamp)            → Objectifs 1, 4         │
│  • expired (boolean)              → Objectif 4             │
└─────────────────────────────────────────────────────────────┘
```

### 🔗 **Flux fonctionnels par objectif**

#### **Flux Objectif 1 (Création):**
```
Template create.html → POST /create-account → handler.py → 
Génération mot de passe → QR Code → Chiffrement → 
Base PostgreSQL → Template create_success.html
```

#### **Flux Objectif 2 (2FA):**
```
handler.py → Génération secret TOTP → QR Code 2FA → 
Chiffrement → Base PostgreSQL → Affichage QR Code
```

#### **Flux Objectif 3 (Authentification):**
```
Template login.html → POST /authenticate → login_handler.py → 
Déchiffrement → Validation TOTP → Contrôle expiration → 
Réponse succès/échec
```

#### **Flux Objectif 4 (Expiration):**
```
login_handler.py → Check gendate → Si > 6 mois → 
expired = TRUE → Redirection vers /create
```

#### **Flux Objectif 5 (Interface):**
```
Navigation Flask → Templates responsives → 
JavaScript validation → Messages flash → 
UX guidée complète
```

---

## 🚀 **Démarrage rapide**

### **⚠️ Prérequis obligatoires à installer/démarrer**

#### **1. Python 3.8+ (obligatoire)**
```powershell
# Vérifiez si Python est installé
python --version

# Si pas installé, téléchargez depuis :
# https://www.python.org/downloads/
```

#### **2. Docker (obligatoire)**
```powershell
# Installation Docker Desktop pour Windows
# Téléchargez : https://www.docker.com/products/docker-desktop/

# Vérification de l'installation
docker --version
docker-compose --version

# OU via package managers :
# Chocolatey : choco install docker-desktop
# Winget : winget install Docker.DockerDesktop
```

#### **3. PostgreSQL via Docker (obligatoire)**
```powershell
# Démarrage du conteneur PostgreSQL
docker run -d `
  --name postgres-mspr `
  -e POSTGRES_DB=cofrap `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=mspr2024 `
  -p 5432:5432 `
  postgres:15

# Vérification que le conteneur fonctionne
docker ps

# Test de connexion à PostgreSQL
docker exec -it postgres-mspr psql -U postgres -d cofrap
```

#### **3. Dépendances Python (obligatoire)**
```powershell
# Dans le dossier du projet
cd "C:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\python-2"

# Installation des dépendances
pip install -r requirements.txt
```

### **🔧 Configuration étape par étape**

> **💡 Alternative rapide :** Vous pouvez utiliser le script automatique dans `scripts-demarrage\demarrage-ultra-rapide.bat` qui exécute toutes ces étapes automatiquement.

#### **Étape 1 : Configuration PostgreSQL via Docker**
```powershell
# 1. Démarrez le conteneur PostgreSQL (si pas déjà fait)
docker run -d `
  --name postgres-mspr `
  -e POSTGRES_DB=cofrap `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=mspr2024 `
  -p 5432:5432 `
  postgres:15

# 2. Vérifiez que le conteneur fonctionne
docker ps

# 3. Connectez-vous au conteneur PostgreSQL
docker exec -it postgres-mspr psql -U postgres -d cofrap

# 4. Dans psql, vérifiez la base (elle existe déjà)
\l

# 5. Exécutez le script de création des tables depuis Windows :
# Copiez d'abord le script dans le conteneur
docker cp database_setup.sql postgres-mspr:/database_setup.sql

# Puis exécutez-le
docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql

# 6. Vérifiez que la table est créée :
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"

# 7. Arrêter le conteneur si besoin :
# docker stop postgres-mspr
```

#### **Étape 2 : Installation des dépendances Python**
```powershell
# Dans le dossier du projet
cd "C:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\python-2"

# Installation des dépendances
pip install -r requirements.txt

# Vérification que les packages sont installés
pip list | findstr flask
pip list | findstr psycopg2
pip list | findstr cryptography
```

#### **Étape 3 : Configuration des variables d'environnement**
```powershell
# Configuration des variables d'environnement pour PostgreSQL Docker
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="
$env:SECRET_KEY = "dev-secret-key-mspr-2025"
```

#### **Étape 4 : Démarrage de l'application**
```powershell
# Démarrage de l'application Flask
python app_complete.py

# L'application sera disponible sur :
# http://localhost:5000
```

### **🎯 Workflow de démarrage complet PostgreSQL via Docker**

#### **Étapes détaillées à suivre dans l'ordre :**

#### **1. Vérification des prérequis**
```powershell
# Vérifiez Python et Docker
python --version
# Résultat attendu : Python 3.8+ (ex: Python 3.11.5)

docker --version
# Résultat attendu : Docker version 20.10+ (ex: Docker version 20.10.17)

# Si Docker Desktop n'est pas démarré, lancez-le depuis le menu Démarrer
```

#### **2. Préparation du dossier de travail**
```powershell
# Allez dans le dossier du projet
cd "C:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\python-2"

# Vérifiez que les fichiers importants sont présents
dir app_complete.py
dir database_setup.sql
dir requirements.txt
```

#### **3. Démarrage du conteneur PostgreSQL**
```powershell
# Démarrez le conteneur PostgreSQL avec la base cofrap
docker run -d `
  --name postgres-mspr `
  -e POSTGRES_DB=cofrap `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=mspr2024 `
  -p 5432:5432 `
  postgres:15

# Attendez quelques secondes que le conteneur démarre
timeout /t 10

# Vérifiez que le conteneur fonctionne
docker ps
# Vous devez voir une ligne avec "postgres-mspr"
```

#### **4. Installation des dépendances Python**
```powershell
# Installation des packages Python requis
pip install -r requirements.txt

# Vérification des packages installés
pip show flask
pip show psycopg2-binary
pip show cryptography
pip show qrcode
pip show pyotp
```

#### **5. Configuration de la base de données**
```powershell
# Copiez le script de création des tables dans le conteneur
docker cp database_setup.sql postgres-mspr:/database_setup.sql

# Exécutez le script pour créer les tables
docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql

# Vérifiez que la table users a été créée
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"
# Vous devez voir la table "users" dans la liste
```

#### **6. Configuration des variables d'environnement**
```powershell
# Configurez les variables pour la session PowerShell
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="
$env:SECRET_KEY = "dev-secret-key-mspr-2025"

# Vérifiez que les variables sont définies
echo $env:DB_HOST
echo $env:DB_NAME
```

#### **7. Test de connexion à la base de données**
```powershell
# Testez manuellement la connexion à PostgreSQL
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT version();"
# Doit afficher la version de PostgreSQL

# Testez que la table est accessible
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT COUNT(*) FROM users;"
# Doit retourner "0" (table vide)
```

#### **8. Démarrage de l'application Flask**
```powershell
# Lancez l'application Flask
python app_complete.py

# Vous devriez voir :
# * Running on http://localhost:5000
# * Debug mode: on
```

#### **9. Test de l'application dans le navigateur**
```powershell
# Dans un autre terminal PowerShell, testez l'application
curl http://localhost:5000/health
# Ou ouvrez directement dans le navigateur

# Ouvrez l'interface complète
start http://localhost:5000
```

### **🎯 Avantages des scripts automatiques :**
- ✅ **Zéro configuration manuelle** requise
- ✅ **Vérifications automatiques** des prérequis
- ✅ **Gestion d'erreurs** intégrée
- ✅ **Messages informatifs** à chaque étape
- ✅ **Démarrage en 2 minutes** au lieu de 10
- ✅ **Point d'entrée unique** : `DEMARRER-MSPR.bat`

> **💡 Conseil :** Si vous débutez avec le projet, utilisez `DEMARRER-MSPR.bat` puis option 1 pour une première configuration sans effort !

---

## 💻 **Interface utilisateur**

### 🏠 **Page d'accueil** (`/`)
- Navigation claire vers toutes les fonctionnalités
- Statut du système en temps réel
- Documentation des fonctionnalités de sécurité

### 👤 **Création de compte** (`/create`)
- **Formulaire simple** : Saisie du nom d'utilisateur uniquement
- **Génération automatique** :
  - Mot de passe complexe 24 caractères
  - Secret 2FA compatible Google Authenticator
  - QR Codes pour sauvegarde et configuration
- **Affichage sécurisé** : QR Codes en base64, pas de stockage d'images

### 🔑 **Connexion** (`/login`)
- **Triple authentification** :
  - Nom d'utilisateur
  - Mot de passe généré
  - Code 2FA (6 chiffres)
- **Validation temps réel** du code TOTP
- **Gestion expiration** : Redirection automatique si compte expiré

### 🔧 **Interface de test** (`/test`)
- **Pour développeurs** : Test des APIs et endpoints
- **Fonctions interactives** : Création, login, 2FA en direct
- **Debugging** : Affichage des réponses JSON complètes

---

## 🔧 **Configuration**

### **Variables d'environnement PostgreSQL Docker**
```powershell
# Configuration PostgreSQL Docker (Windows PowerShell)
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"

# Clé de chiffrement (IMPORTANT: même clé pour tous les handlers!)
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="

# Clé secrète Flask
$env:SECRET_KEY = "votre-cle-secrete-production"
```

### **Configuration PostgreSQL Docker dans le code**
```python
# Dans app_complete.py
import os

# Configuration PostgreSQL Docker
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'mspr2024'

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
```

---

## 🗄️ **Base de données**

### **Structure table `users`**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,           -- Chiffré Fernet
    secret_2fa TEXT,                  -- Chiffré Fernet
    gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Index pour performance**
```sql
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_expired ON users(expired);
CREATE INDEX idx_users_gendate ON users(gendate);
```

### **Setup PostgreSQL Docker automatique**
```powershell
# Méthode 1: Script complet
docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15
docker cp database_setup.sql postgres-mspr:/database_setup.sql
docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql

# Méthode 2: Étape par étape via Docker
docker exec -it postgres-mspr psql -U postgres -d cofrap
# Dans psql :
# \i /database_setup.sql
# \q

# Vérification de la configuration
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"
```

---

## ☁️ **Déploiement OpenFaaS**

### **Handlers disponibles**
- **`create-user/`** - Fonction de création d'utilisateurs
- **`login-user/`** - Fonction d'authentification
- **`generate-2fa/`** - Fonction de gestion 2FA

### **Configuration stack.yml**
```yaml
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  create-user:
    lang: python3
    handler: ./create-user
    image: create-user:latest
  
  login-user:
    lang: python3
    handler: ./login-user
    image: login-user:latest
  
  generate-2fa:
    lang: python3
    handler: ./generate-2fa
    image: generate-2fa:latest
```

### **Déploiement**
```bash
# Build et déploiement
faas-cli build -f stack.yml
faas-cli deploy -f stack.yml

# Test des fonctions
curl -X POST http://localhost:8080/function/create-user \
     -d '{"username": "testuser"}'
```

---

## 🔒 **Sécurité**

### **Chiffrement**
- **Algorithme** : Fernet (cryptographically strong)
- **Données chiffrées** : Mots de passe + secrets 2FA
- **Clé unique** : Même clé pour tous les handlers

### **2FA (TOTP)**
- **Compatible** : Google Authenticator, Authy, etc.
- **Standard** : RFC 6238 (Time-based OTP)
- **Fenêtre** : 30 secondes avec tolérance ±1

### **Gestion session**
- **Protection CSRF** intégrée
- **Flash messages** sécurisés
- **Expiration** : 6 mois automatique

### **Validation**
- **Input** : Sanitisation complète
- **SQL** : Requêtes préparées (protection injection)
- **XSS** : Templates échappés automatiquement

---

## 🛠️ **Développement**

### **Structure du projet**
```
script python/
├── 🎯 APPLICATION PRINCIPALE
│   ├── app_complete.py         # Application Flask complète
│   ├── templates/              # Interface utilisateur
│   │   ├── index.html         # Interface de test
│   │   ├── home.html          # Page d'accueil
│   │   ├── create.html        # Création de compte
│   │   ├── login.html         # Connexion
│   │   ├── create_success.html # Succès création
│   │   └── login_success.html  # Succès connexion
│   ├── static/                # Ressources statiques
│   │   ├── css/main.css       # Styles principaux
│   │   └── js/main.js         # JavaScript interactif
│   └── requirements.txt       # Dépendances Python
│
├── 🔧 HANDLERS CORE
│   ├── handler.py             # Création utilisateurs + 2FA
│   ├── login_handler.py       # Authentification sécurisée
│   └── generate_2fa_handler.py # Génération 2FA dédiée
│
├── 🚀 OPENFAAS (SERVERLESS)
│   ├── create-user/           # Handler packagé création
│   ├── login-user/            # Handler packagé login
│   ├── generate-2fa/          # Handler packagé 2FA
│   ├── stack.yml              # Configuration OpenFaaS
│   └── openfaas_requirements.txt
│
├── 🗄️ BASE DE DONNÉES
│   └── database_setup.sql     # Structure PostgreSQL
│
└── 📁 UTILITAIRES
    ├── DEMARRER-MSPR.bat          # 🚀 LANCEUR PRINCIPAL - Point d'entrée unique
    ├── scripts-demarrage/         # Scripts automatiques (menu + ultra-rapide)
    │   ├── menu-demarrage.bat    # Menu principal de démarrage
    │   ├── demarrage-ultra-rapide.bat  # Script automatique complet
    │   ├── utilitaires-maintenance.bat # Outils de maintenance
    │   ├── start_app_docker.bat  # Script Docker détaillé
    │   ├── start_app_mspr.bat    # Script PostgreSQL local (déprécié)
    │   └── README-SCRIPTS.md     # Documentation des scripts
    ├── database_setup.sql         # Structure PostgreSQL
    └── PROJET_ESSENTIEL.md        # Documentation structure
```

### **Tests en local**
```bash
# Test de santé
curl http://localhost:5000/health

# Test API création
curl -X POST http://localhost:5000/api/create-user \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser"}'

# Test API login
curl -X POST http://localhost:5000/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "...", "totp_code": "123456"}'
```

### **Debug mode**
```python
# Dans app_complete.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 📞 **Support**

### **URLs importantes**
- **Page d'accueil** : `http://localhost:5000/` - Navigation principale
- **Création compte** : `http://localhost:5000/create` - Formulaire utilisateur → POST vers `/create-account`
- **Connexion** : `http://localhost:5000/login` - Triple authentification → POST vers `/authenticate`
- **Test développeurs** : `http://localhost:5000/test` - Interface API interactive
- **Santé système** : `http://localhost:5000/health` - Status monitoring

### **Logs et debugging**
```python
# Logs Flask en debug mode
app.run(debug=True)

# Logs personnalisés dans les handlers
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📜 **Licence**

Projet éducatif MSPR - Tous droits réservés.

---

**🎉 Votre système d'authentification sécurisé est prêt !**

Testez dès maintenant sur `http://localhost:5000/` 🚀

---

## 🧩 **Objectifs fonctionnels détaillés et liens entre eux**

### 🔹 **Objectif 1 : Création sécurisée de comptes utilisateurs**

#### **Actions :**
- ✅ **Générer automatiquement un mot de passe sécurisé** (24 caractères)
- ✅ **Générer un QR Code** contenant ce mot de passe  
- ✅ **Chiffrer le mot de passe** (algorithme Fernet)
- ✅ **Stocker en base** : `username`, `password` (chiffré), `gendate`

#### **Résultat :**
- ✅ Nouvel utilisateur inscrit avec identifiants forts
- ✅ QR Code facilite la transmission sécurisée du mot de passe

#### **Liens avec les autres objectifs :**
- **→ Objectif 2** : La création d'un compte déclenche immédiatement la génération du secret 2FA
- **→ Objectif 3** : Les données stockées seront utilisées lors de l'authentification  
- **→ Objectif 4** : La date de création servira à vérifier l'expiration
- **→ Objectif 5** : Interface `/create` pour déclencher cette action

**📄 Implémentation :** `handler.py` + Template `create.html` + `create_success.html`

---

### 🔹 **Objectif 2 : Mise en place du 2FA obligatoire**

#### **Actions :**
- ✅ **Générer un secret TOTP** (Time-based One-Time Password)
- ✅ **Générer un QR Code** pour configurer Google Authenticator
- ✅ **Chiffrer le secret TOTP** (Fernet)
- ✅ **Stocker le secret en base** (lié à l'utilisateur : `secret_2fa`)

#### **Résultat :**
- ✅ Compte activé uniquement avec double authentification
- ✅ Sécurité renforcée contre les compromissions de mots de passe

#### **Liens avec les autres objectifs :**
- **← Objectif 1** : Dépend de la création du compte
- **→ Objectif 3** : Le secret 2FA sera vérifié à chaque connexion
- **→ Objectif 5** : QR Code affiché dans la frontend

**📄 Implémentation :** `generate_2fa_handler.py` + intégré dans `handler.py`

---

### 🔹 **Objectif 3 : Authentification avec vérification complète**

#### **Actions utilisateur :**
- 📝 Saisit son **login**
- 📝 Saisit son **mot de passe** 
- 📝 Saisit son **code 2FA** (6 chiffres)

#### **Actions système :**
- 🔓 **Déchiffre et vérifie** le mot de passe
- 🔐 **Valide le code TOTP** (2FA) en temps réel
- ⏰ **Vérifie si le compte est expiré** (> 6 mois)
- ✅ **Retourne une réponse** (succès ou échec)

#### **Résultat :**
- ✅ Accès accordé uniquement si les 3 éléments sont valides
- ⚠️ Si compte expiré → déclenchement du renouvellement automatique

#### **Liens avec les autres objectifs :**
- **← Objectif 1** : Utilise le mot de passe stocké
- **← Objectif 2** : Utilise le secret TOTP stocké  
- **→ Objectif 4** : Déclenche la relance du cycle si expiré
- **→ Objectif 5** : Interface `/login` pour l'utilisateur

**📄 Implémentation :** `login_handler.py` + Template `login.html` + `login_success.html`

---

### 🔹 **Objectif 4 : Gestion de l'expiration automatique (6 mois)**

#### **Actions à chaque authentification :**
- 📅 **Vérifier la date de création** stockée en base (`gendate`)
- ⏰ **Si > 6 mois** :
  - Marquer le compte comme expiré (`expired = TRUE`)
  - Refuser l'authentification
  - Proposer via la frontend une relance du processus

#### **Résultat :**
- 🔄 Identifiants automatiquement renouvelés
- 🛡️ Rotation sécurisée des mots de passe et secrets 2FA tous les 6 mois

#### **Liens avec les autres objectifs :**
- **← Objectif 1** : Utilise la date enregistrée à la création
- **→ Objectif 1 + 2** : Déclenche nouvelle création mot de passe + 2FA si expiré  
- **→ Objectif 5** : Communique le statut au frontend

**📄 Implémentation :** Logique dans `login_handler.py` + Messages flash + Redirection

---

### 🔹 **Objectif 5 : Interface utilisateur simple et fonctionnelle**

#### **Actions utilisateur disponibles :**
- 👤 **Créer un compte** → `/create`
- 📱 **Scanner les QR Codes** (mot de passe + 2FA)
- 🔑 **Se connecter** avec mot de passe + 2FA → `/login`
- ⚠️ **Être informé** si le compte est expiré
- 🔄 **Relancer le processus** si nécessaire

#### **Résultat :**
- 🎯 Projet démontrable visuellement
- 🖱️ Utilisateur peut interagir avec toutes les fonctions via interface simple

#### **Liens avec tous les objectifs :**
- **Interface pour Objectif 1** : Page création de compte
- **Interface pour Objectif 2** : Affichage QR Codes 2FA
- **Interface pour Objectif 3** : Page connexion sécurisée
- **Interface pour Objectif 4** : Messages expiration + renouvellement

**📄 Implémentation :** Templates Flask + CSS responsive + JavaScript validation

---

### 🔗 **Schéma des liens entre objectifs**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Objectif 1    │───▶│   Objectif 2    │───▶│   Objectif 3    │
│ Création compte │    │   Setup 2FA     │    │ Authentification│
└─────────────────┘    └─────────────────┘    └─────────┬───────┘
         ▲                       ▲                       │
         │                       │                       ▼
         │               ┌─────────────────┐    ┌─────────────────┐
         │               │   Objectif 5    │    │   Objectif 4    │
         └───────────────│ Interface Web   │◀───│   Expiration    │
                         └─────────────────┘    └─────────────────┘
```

**🎯 Cycle complet :** Création → 2FA → Authentification → Vérification expiration → (Si expiré) Recréation

---

### **🛠️ Dépannage des problèmes courants - Étapes manuelles**

#### **❌ "Docker n'est pas reconnu" ou conteneur PostgreSQL ne démarre pas**
```powershell
# ÉTAPE 1: Vérifiez que Docker Desktop est installé et démarré
docker --version
# Si erreur, installez Docker Desktop : https://docs.docker.com/desktop/install/windows-install/

# ÉTAPE 2: Démarrez Docker Desktop manuellement
# Ouvrez Docker Desktop depuis le menu Démarrer Windows
# Attendez que l'icône Docker devienne verte dans la barre des tâches

# ÉTAPE 3: Vérifiez l'état des conteneurs
docker ps -a
# Recherchez postgres-mspr dans la liste

# ÉTAPE 4: Si le conteneur existe mais est arrêté
docker start postgres-mspr

# ÉTAPE 5: Si problème persistant, supprimez et recréez le conteneur
docker stop postgres-mspr
docker rm postgres-mspr
docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15
```

#### **❌ "Connection refused" PostgreSQL**
```powershell
# ÉTAPE 1: Vérifiez que le conteneur PostgreSQL fonctionne
docker ps | findstr postgres-mspr
# Doit montrer un conteneur "Up" avec le port 5432

# ÉTAPE 2: Vérifiez les logs du conteneur
docker logs postgres-mspr
# Recherchez des erreurs dans les logs

# ÉTAPE 3: Testez la connexion directe au conteneur
docker exec -it postgres-mspr psql -U postgres -d cofrap
# Si ça fonctionne, tapez \q pour quitter

# ÉTAPE 4: Vérifiez que le port 5432 n'est pas utilisé par un autre service
netstat -an | findstr 5432
# Ne devrait montrer que Docker

# ÉTAPE 5: Redémarrez le conteneur si nécessaire
docker restart postgres-mspr
timeout /t 10
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT version();"
```

#### **❌ "Module 'psycopg2' not found"**
```powershell
# ÉTAPE 1: Installez le driver PostgreSQL pour Python
pip install psycopg2-binary

# ÉTAPE 2: Vérifiez l'installation
pip show psycopg2-binary

# ÉTAPE 3: Si problème persistant, réinstallez toutes les dépendances
pip uninstall -y psycopg2-binary flask cryptography qrcode pyotp
pip install -r requirements.txt

# ÉTAPE 4: Testez l'import en Python
python -c "import psycopg2; print('psycopg2 OK')"
```

#### **❌ "Table users does not exist"**
```powershell
# ÉTAPE 1: Vérifiez que le script de base de données a été exécuté
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"
# Doit montrer la table "users"

# ÉTAPE 2: Si la table n'existe pas, re-exécutez le script
docker cp database_setup.sql postgres-mspr:/database_setup.sql
docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql

# ÉTAPE 3: Vérifiez que le fichier database_setup.sql existe
dir database_setup.sql

# ÉTAPE 4: Vérifiez le contenu du script
type database_setup.sql

# ÉTAPE 5: Re-vérifiez que la table est créée
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
```

#### **❌ "Port 5000 already in use"**
```powershell
# ÉTAPE 1: Identifiez le processus utilisant le port 5000
netstat -ano | findstr :5000

# ÉTAPE 2: Arrêtez le processus si possible
# Notez le PID de la dernière colonne et arrêtez-le
taskkill /PID [numéro_PID] /F

# ÉTAPE 3: Ou modifiez le port dans app_complete.py
# Changez la ligne : app.run(host='0.0.0.0', port=5001, debug=True)

# ÉTAPE 4: Utilisez le nouveau port
# http://localhost:5001
```

#### **❌ Variables d'environnement non reconnues**
```powershell
# ÉTAPE 1: Re-configurez les variables dans la session PowerShell
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="

# ÉTAPE 2: Vérifiez que les variables sont définies
Get-ChildItem Env: | Where-Object {$_.Name -like "DB_*"}

# ÉTAPE 3: Si problème persistant, modifiez directement app_complete.py
# Ajoutez au début du fichier après les imports :
# os.environ['DB_HOST'] = 'localhost'
# os.environ['DB_NAME'] = 'cofrap'
# etc.
```

#### **❌ "Module 'psycopg2' not found"**
```powershell
# Installez le driver PostgreSQL pour Python
pip install psycopg2-binary

# Ou réinstallez toutes les dépendances
pip install -r requirements.txt
```

#### **❌ "Connection refused" PostgreSQL**
```powershell
# Vérifiez que le conteneur PostgreSQL fonctionne
docker ps | findstr postgres-mspr

# Vérifiez les logs du conteneur
docker logs postgres-mspr

# Redémarrez le conteneur si nécessaire
docker stop postgres-mspr
docker start postgres-mspr
```

#### **❌ "Authentication failed" PostgreSQL**
```powershell
# Vérifiez la connexion au conteneur PostgreSQL
docker exec -it postgres-mspr psql -U postgres -d cofrap

# Réinitialisez le mot de passe si nécessaire
# (nécessite des droits administrateur)
```

#### **❌ "Port 5000 already in use"**
```powershell
# Modifiez le port dans app_complete.py
# app.run(host='0.0.0.0', port=5001, debug=True)
```

#### **❌ Variables d'environnement non définies**
```powershell
# Redéfinissez les variables dans la session PowerShell
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="

# Vérifiez qu'elles sont bien définies
echo $env:DB_HOST
echo $env:DB_NAME
```

### **📋 Checklist complète avant démarrage - PostgreSQL Docker**

Cochez chaque étape après l'avoir réalisée :

- [ ] ✅ **Python 3.8+ installé** (`python --version`)
- [ ] ✅ **Docker Desktop installé et démarré** (`docker --version`)
- [ ] ✅ **Dossier de projet ouvert** (`cd "C:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\python-2"`)
- [ ] ✅ **Conteneur PostgreSQL créé et démarré** (`docker run -d --name postgres-mspr...`)
- [ ] ✅ **Conteneur visible dans la liste** (`docker ps | findstr postgres-mspr`)
- [ ] ✅ **Dépendances Python installées** (`pip install -r requirements.txt`)
- [ ] ✅ **Script de base copié dans le conteneur** (`docker cp database_setup.sql postgres-mspr:/database_setup.sql`)
- [ ] ✅ **Tables créées dans la base** (`docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql`)
- [ ] ✅ **Table users visible** (`docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"`)
- [ ] ✅ **Variables d'environnement configurées** (`$env:DB_HOST = "localhost"`, etc.)
- [ ] ✅ **Connexion à la base testée** (`docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT COUNT(*) FROM users;"`)
- [ ] ✅ **Application Flask démarrée** (`python app_complete.py`)
- [ ] ✅ **Interface accessible** (Ouvrir `http://localhost:5000`)

### **🚀 Guide de démarrage étape par étape (10 minutes maximum)**

> **⚡ Démarrage ultra-rapide :** Utilisez `scripts-demarrage\demarrage-ultra-rapide.bat` pour automatiser toutes ces étapes en 2 minutes !

**Suivez ces étapes exactement dans l'ordre :**

```powershell
# ÉTAPE 1 : Préparatifs
cd "C:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\python-2"
python --version
docker --version

# ÉTAPE 2 : Démarrage PostgreSQL
docker run -d --name postgres-mspr -e POSTGRES_DB=cofrap -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mspr2024 -p 5432:5432 postgres:15
timeout /t 10
docker ps

# ÉTAPE 3 : Installation Python
pip install -r requirements.txt

# ÉTAPE 4 : Configuration base de données
docker cp database_setup.sql postgres-mspr:/database_setup.sql
docker exec -i postgres-mspr psql -U postgres -d cofrap -f /database_setup.sql
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "\dt"

# ÉTAPE 5 : Variables d'environnement
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="

# ÉTAPE 6 : Test et démarrage
docker exec -it postgres-mspr psql -U postgres -d cofrap -c "SELECT COUNT(*) FROM users;"
python app_complete.py

# ÉTAPE 7 : Ouverture navigateur
# Dans un autre terminal ou navigateur : http://localhost:5000
```

**🎉 Votre application sera prête en 5 minutes !**

---

## 🚀 **Scripts de démarrage automatiques**

Pour simplifier la configuration, des scripts automatiques sont disponibles dans le dossier `scripts-demarrage/` :

### **⚡ Option 1 : Démarrage ultra-rapide (Recommandé)**
```powershell
# NOUVELLE MÉTHODE : Lanceur principal depuis la racine
.\DEMARRER-MSPR.bat

# Puis choisissez l'option 1 : Démarrage ultra-rapide
```

### **📋 Option 2 : Menu interactif**
```powershell
# Via le lanceur principal (recommandé)
.\DEMARRER-MSPR.bat

# Puis choisissez l'option 2 : Menu de démarrage
```

### **🛠️ Option 3 : Utilitaires de maintenance**
```powershell
# Via le lanceur principal (recommandé)
.\DEMARRER-MSPR.bat

# Puis choisissez l'option 3 : Utilitaires de maintenance
```

### **⚡ GUIDE DE DÉPANNAGE RAPIDE**

#### **❌ Problème : "start_app_docker.bat n'est pas reconnu"**

**✅ Solution :**
```powershell
# NOUVELLE MÉTHODE (recommandée) :
# Utilisez le lanceur principal depuis le dossier python-2
cd "C:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\python-2"
.\DEMARRER-MSPR.bat

# Puis choisissez l'option 1 : Démarrage ultra-rapide
```

**📋 Explication :**
Les scripts ont été réorganisés dans le dossier `scripts-demarrage/`. Le nouveau lanceur `DEMARRER-MSPR.bat` gère automatiquement les chemins corrects.

---

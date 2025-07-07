# Application MSPR - Frontend Flask

Cette application Flask sert de frontend pour un système d'authentification utilisant OpenFaaS avec authentification à deux facteurs (2FA).

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [OpenFaaS Setup](#openfaas-setup)
- [Exécution](#exécution)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Dépannage](#dépannage)

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.7+** - [Télécharger Python](https://www.python.org/downloads/)
- **pip** - Gestionnaire de paquets Python (inclus avec Python)
- **OpenFaaS** - Service backend pour l'authentification
- **Git** (optionnel) - Pour cloner le projet

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
# Si vous utilisez Git
git clone <votre-repo-url>
cd "script python"

# Ou téléchargez et décompressez le dossier
```

### 2. Créer un environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate

# Sur macOS/Linux :
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install flask requests
```

Ou créez un fichier `requirements.txt` avec :

```txt
Flask==2.3.3
requests==2.31.0
```

Et installez avec :

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Configuration OpenFaaS

Modifiez l'URL de base dans `mspr912.py` :

```python
# URL de vos fonctions OpenFaaS (à adapter)
BASE_URL = 'http://localhost:8080/function/'  # Remplacez par votre URL OpenFaaS
```

### 2. Configuration de la clé secrète

Pour la production, changez la clé secrète dans `mspr912.py` :

```python
app.secret_key = 'votre-cle-secrete-super-forte'  # Changez cette valeur !
```

## 🔧 OpenFaaS Setup

### Handlers OpenFaaS fournis

Le projet inclut deux handlers OpenFaaS :

1. **`handler.py`** - Création d'utilisateurs (`create-user`)
2. **`login_handler.py`** - Authentification (`login-user`)

### Installation des dépendances OpenFaaS

```bash
pip install -r openfaas_requirements.txt
```

### Configuration des handlers

#### 1. Clé de chiffrement

Les handlers utilisent une clé de chiffrement fixe. **IMPORTANT** : 

```python
# Dans les deux handlers, la clé doit être identique !
FERNET_KEY = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
```

Pour la production, définissez la variable d'environnement :
```bash
export FERNET_KEY="votre-cle-secrete-base64"
```

#### 2. Configuration de la base de données

Modifiez les paramètres de connexion dans les handlers :

```python
DB_HOST = "localhost"  # ou votre serveur PostgreSQL
DB_NAME = "cofrap"
DB_USER = "postgres"
DB_PASSWORD = "password"
```

#### 3. Structure de la base de données

Créez la table utilisateurs :

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    secret_2fa TEXT,
    gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired BOOLEAN DEFAULT FALSE
);
```

### Déploiement OpenFaaS

1. **Créer les fonctions OpenFaaS** :
   ```bash
   faas-cli new --lang python3 create-user
   faas-cli new --lang python3 login-user
   ```

2. **Copier les handlers** :
   ```bash
   cp handler.py create-user/handler.py
   cp login_handler.py login-user/handler.py
   ```

3. **Configurer requirements.txt** :
   ```bash
   cp openfaas_requirements.txt create-user/requirements.txt
   cp openfaas_requirements.txt login-user/requirements.txt
   ```

4. **Déployer** :
   ```bash
   faas-cli up -f create-user.yml
   faas-cli up -f login-user.yml
   ```

### Test des fonctions

```bash
# Test création d'utilisateur
curl -X POST http://localhost:8080/function/create-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser"}'

# Test connexion
curl -X POST http://localhost:8080/function/login-user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "motdepasse", "code_2fa": "123456"}'
```

## 🎯 Exécution

### 1. Démarrer l'application

```bash
# Assurez-vous d'être dans le bon répertoire
cd "c:\Users\louis.fievet\OneDrive - Ifag Paris\EPSI\MSPR\TPRE912\script python"

# Activer l'environnement virtuel si ce n'est pas déjà fait
venv\Scripts\activate

# Lancer l'application
python mspr912.py
```

### 2. Accéder à l'application

Ouvrez votre navigateur et allez à :
```
http://127.0.0.1:5000
```

## 📁 Structure du projet

```
script python/
├── 📄 Application Flask
│   ├── mspr912.py              # Application Flask principale
│   ├── static/                 # Fichiers statiques
│   │   └── css/
│   │       ├── style.css       # Styles généraux
│   │       └── forms.css       # Styles des formulaires
│   └── templates/              # Templates HTML
│       ├── home.html           # Page d'accueil
│       ├── create.html         # Création de compte
│       └── login.html          # Connexion
├── 📄 Handlers OpenFaaS
│   ├── handler.py              # Handler - création d'utilisateurs ✨
│   ├── login_handler.py        # Handler - authentification ✨
│   └── generate_2fa_handler.py # Handler - génération 2FA ✨
├── 📄 Tests
│   ├── tests/                  # Dossier des tests
│   │   ├── __init__.py         # Module Python
│   │   ├── README.md           # Documentation des tests
│   │   ├── run_all_tests.py    # Script pour lancer tous les tests
│   │   ├── test_simple.py      # Tests création utilisateur
│   │   ├── test_2fa.py         # Tests authentification 2FA
│   │   ├── test_login_simple.py # Tests login basiques
│   │   ├── test_login_complete.py # Tests login complets
│   │   ├── test_handlers.py    # Tests handlers OpenFaaS
│   │   ├── test_login_handler.py # Tests spécifiques login
│   │   ├── test_password_expiration.py # Tests expiration
│   │   └── verification_complete.py # Vérification complète
├── 📄 Configuration
│   ├── requirements.txt        # Dépendances Python
│   ├── openfaas_requirements.txt # Dépendances OpenFaaS
│   ├── start_app.bat          # Script démarrage Windows
│   └── README.md              # Ce fichier
├── 📄 Documentation
│   └── PROJET_TERMINÉ.md      # Résumé du projet
└── venv/                      # Environnement virtuel
```

## 🎨 Fonctionnalités

### Pages disponibles

1. **Page d'accueil** (`/`)
   - Liens vers création de compte et connexion
   - Affichage des messages flash

2. **Création de compte** (`/create`)
   - Formulaire de création d'utilisateur
   - Intégration avec OpenFaaS `create-user`

3. **Connexion** (`/login`)
   - Formulaire de connexion avec 2FA
   - Intégration avec OpenFaaS `login-user`
   - Gestion des mots de passe expirés

### Fonctionnalités techniques

- **Messages flash** : Affichage des messages de succès/erreur
- **Responsive design** : Interface adaptée aux mobiles
- **Validation des formulaires** : Champs obligatoires
- **Gestion des erreurs** : Messages d'erreur explicites

## 🔧 Dépannage

### Problèmes courants

#### 1. Erreur "Template not found"
```bash
# Vérifiez que les templates sont dans le bon dossier
ls templates/
# Doit afficher : create.html  home.html  login.html
```

#### 2. Erreur "Module not found"
```bash
# Assurez-vous que l'environnement virtuel est activé
venv\Scripts\activate
# Puis installez les dépendances
pip install flask requests
```

#### 3. Erreur de connexion OpenFaaS
```bash
# Vérifiez que OpenFaaS est démarré
curl http://localhost:8080/system/functions
# Ou adaptez l'URL dans mspr912.py
```

#### 4. CSS ne se charge pas
```bash
# Vérifiez la structure des fichiers statiques
ls static/css/
# Doit afficher : forms.css  style.css
```

### Logs de débogage

Pour activer les logs détaillés, modifiez `mspr912.py` :

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🚀 Déploiement

### Pour le développement
```bash
python mspr912.py
```

### Pour la production
Utilisez un serveur WSGI comme Gunicorn :

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 mspr912:app
```

## 📝 Variables d'environnement

Vous pouvez utiliser des variables d'environnement pour la configuration :

```python
import os

BASE_URL = os.environ.get('OPENFAAS_URL', 'http://localhost:8080/function/')
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')
```

## 🤝 Contribution

Pour contribuer au projet :

1. Créez une branche pour votre fonctionnalité
2. Effectuez vos modifications
3. Testez l'application
4. Soumettez une pull request

## 📞 Support

En cas de problème :

1. Vérifiez les logs dans le terminal
2. Consultez la section [Dépannage](#dépannage)
3. Vérifiez que OpenFaaS est accessible
4. Contactez l'équipe de développement

---

**Dernière mise à jour :** Juillet 2025
**Version :** 1.0.0

## 📡 Documentation API

### Endpoints

#### 1. Créer un utilisateur avec 2FA
```bash
POST /function/create-user
Content-Type: application/json

{
  "username": "monuser"
}
```

**Réponse:**
```json
{
  "message": "User created successfully",
  "username": "monuser",
  "password": "motdepasse-généré",
  "password_qr_code": "qrcode-base64-motdepasse",
  "totp_secret": "secret-2fa-base32",
  "totp_qr_code": "qrcode-base64-2fa",
  "instructions": {
    "step1": "Save your password securely",
    "step2": "Scan the TOTP QR code with Google Authenticator",
    "step3": "Use both password and 2FA code to login"
  },
  "status": "success"
}
```

#### 2. Se connecter avec 2FA
```bash
POST /function/login-user
Content-Type: application/json

{
  "username": "monuser",
  "password": "motdepasse",
  "code_2fa": "123456"
}
```

## 🔐 Fonctionnalités de Login

### login_handler.py - Authentification sécurisée

Le handler de login implémente toutes les vérifications de sécurité requises :

#### Vérifications effectuées :

1. **Récupération utilisateur** - Recherche dans la base de données
2. **Vérification mot de passe** - Déchiffrement et comparaison
3. **Vérification code 2FA** - Validation TOTP avec Google Authenticator
4. **Vérification expiration** - Contrôle de la date de création (6 mois maximum)
5. **Marquage d'expiration** - Mise à jour automatique si expiré

#### Réponses possibles :

**Succès :**
```json
{
  "message": "Login successful",
  "username": "testuser",
  "login_time": "2025-07-07T13:06:14.283489",
  "password_expires_in_days": 124,
  "status": "success"
}
```

**Mot de passe expiré :**
```json
{
  "error": "Password has expired (6 months). Please contact administrator for renewal.",
  "status": "error",
  "expired": true
}
```

**Erreurs possibles :**
- `Username, password, and TOTP code are required`
- `Invalid credentials`
- `User account has expired. Please contact administrator.`
- `Invalid TOTP code`

### Paramètres d'entrée :

```json
{
  "username": "nom_utilisateur",
  "password": "mot_de_passe",
  "totp_code": "123456"
}
```
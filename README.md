# 🔐 MSPR - Système d'Authentification Sécurisé

**Application Flask complète** avec authentification 2FA, chiffrement avancé et interface utilisateur intuitive.

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/votre-repo/mspr)
[![Flask](https://img.shields.io/badge/Flask-2.3+-red.svg)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Security-2FA%20%2B%20Fernet-green.svg)](https://cryptography.io/)
[![OpenFaaS](https://img.shields.io/badge/OpenFaaS-Ready-orange.svg)](https://www.openfaas.com/)

---

## 📋 **Table des matières**

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

## 🎯 **Fonctionnalités**

### ✅ **Système complet d'authentification**
- **Création automatisée de comptes** avec mots de passe complexes (24 caractères)
- **Authentification 2FA** compatible Google Authenticator
- **QR Codes sécurisés** pour mot de passe et configuration 2FA
- **Gestion d'expiration** des comptes (6 mois)
- **Chiffrement complet** des données (Fernet)

### ✅ **Interface utilisateur intuitive**
- **Page d'accueil** avec navigation claire
- **Formulaires simples** pour création et connexion
- **Messages d'erreur** contextuels et user-friendly
- **Design responsive** compatible mobile
- **Interface de test** pour développeurs

### ✅ **Architecture sécurisée**
- **Handlers OpenFaaS** pour architecture serverless
- **Base PostgreSQL** avec chiffrement des données sensibles
- **Sessions sécurisées** avec protection CSRF
- **Validation en temps réel** des codes 2FA

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 Interface Web Flask                    │
├─────────────────────────────────────────────────────────────┤
│  📱 Pages:                                                  │
│  • /           → Page d'accueil                             │
│  • /create     → Création de compte                         │
│  • /login      → Connexion sécurisée                        │
│  • /test       → Interface API (développeurs)               │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                 🔧 Handlers Business Logic                  │
├─────────────────────────────────────────────────────────────┤
│  • handler.py           → Création utilisateurs + 2FA       │
│  • login_handler.py     → Authentification complète         │
│  • generate_2fa_handler → Gestion 2FA dédiée               │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              🗄️ Base de données PostgreSQL                  │
├─────────────────────────────────────────────────────────────┤
│  Table: users                                               │
│  • username (unique)                                        │
│  • password (chiffré Fernet)                               │
│  • secret_2fa (chiffré Fernet)                             │
│  • gendate (timestamp)                                     │
│  • expired (boolean)                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 **Démarrage rapide**

### **1. Prérequis**
```bash
# Installez Python 3.8+ et PostgreSQL
python --version  # Vérifiez la version
```

### **2. Installation**
```bash
# Clonez le projet
git clone <votre-repo>
cd "script python"

# Installez les dépendances
pip install -r requirements.txt
```

### **3. Configuration base de données**
```bash
# Connectez-vous à PostgreSQL
psql -U postgres

# Créez la base et la table
CREATE DATABASE cofrap;
\c cofrap;
\i database_setup.sql
```

### **4. Démarrage**
```bash
# Démarrez l'application
python app_complete.py

# Ouvrez votre navigateur sur :
# http://localhost:5000
```

---

## 💻 **Interface utilisateur**

### 🏠 **Page d'accueil** (`/`)
- Navigation claire vers toutes les fonctionnalités
- Statut du système en temps réel
- Documentation des fonctionnalités de sécurité

### 👤 **Création de compte** (`/create`)
- **Interface intuitive** : Template `create.html` avec formulaire guidé
- **Validation frontend** : Contrôles JavaScript temps réel
- **Formulaire simple** : Saisie du nom d'utilisateur uniquement
- **Génération automatique** :
  - Mot de passe complexe 24 caractères
  - Secret 2FA compatible Google Authenticator
  - QR Codes pour sauvegarde et configuration
- **Affichage sécurisé** : QR Codes en base64, pas de stockage d'images
- **Page de succès** : Template `create_success.html` avec QR Codes et instructions

### 🔑 **Connexion** (`/login`)
- **Interface sécurisée** : Template `login.html` avec triple authentification
- **Champs optimisés** :
  - Nom d'utilisateur (auto-complétion sécurisée)
  - Mot de passe (24 caractères, masqué)
  - Code 2FA (formatage automatique 6 chiffres)
- **Validation temps réel** :
  - Formatage automatique du code 2FA
  - Contrôles JavaScript avant envoi
  - Vérification TOTP côté serveur
- **Gestion expiration** : Détection automatique + redirection vers création
- **Messages d'aide** : Guide Google Authenticator intégré
- **Page de succès** : Template `login_success.html` après authentification

### 🔧 **Interface de test** (`/test`)
- **Pour développeurs** : Test des APIs et endpoints
- **Fonctions interactives** : Création, login, 2FA en direct
- **Debugging** : Affichage des réponses JSON complètes

---

## 🔧 **Configuration**

### **Variables d'environnement**
```bash
# Configuration base de données
export DB_HOST=localhost
export DB_NAME=cofrap
export DB_USER=postgres
export DB_PASSWORD=password

# Clé de chiffrement (IMPORTANT: même clé pour tous les handlers!)
export FERNET_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=

# Clé secrète Flask
export SECRET_KEY=votre-cle-secrete-production
```

### **Configuration personnalisée**
```python
# Dans app_complete.py
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configuration DB
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'password'
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

### **Setup automatique**
```bash
# Exécutez le script de setup
psql -U postgres -d cofrap -f database_setup.sql
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
│   ├── templates/              # Interface utilisateur complète
│   │   ├── home.html          # Page d'accueil navigation
│   │   ├── create.html        # ✨ Formulaire création compte
│   │   ├── login.html         # ✨ Interface connexion 2FA
│   │   ├── create_success.html # Succès création + QR Codes
│   │   ├── login_success.html  # Succès connexion
│   │   └── index.html         # Interface de test (développeurs)
│   ├── static/                # Ressources statiques
│   │   ├── css/main.css       # Styles principaux + responsive
│   │   └── js/main.js         # JavaScript validation temps réel
│   └── requirements.txt       # Dépendances Python complètes
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
    ├── start_app.bat          # Script démarrage Windows
    └── PROJET_ESSENTIEL.md    # Documentation structure
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
- **Création compte** : `http://localhost:5000/create` - Formulaire utilisateur
- **Connexion** : `http://localhost:5000/login` - Triple authentification
- **Test développeurs** : `http://localhost:5000/test` - Interface API interactive
- **Santé système** : `http://localhost:5000/health` - Status monitoring

### **Tests fonctionnels complets**
```bash
# 1. Test création compte complet
curl -X POST http://localhost:5000/api/create-user \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser2025"}'

# 2. Test login avec 2FA
curl -X POST http://localhost:5000/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser2025", "password": "mot-de-passe-généré", "totp_code": "123456"}'

# 3. Test gestion expiration (compte > 6 mois)
curl -X POST http://localhost:5000/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "ancien_compte", "password": "...", "totp_code": "123456"}'
```

### **Interface web complète**
```bash
# Navigation recommandée pour tests
1. http://localhost:5000/           # Page d'accueil
2. http://localhost:5000/create     # Créer un compte
3. Configurer Google Authenticator  # Scanner QR Code 2FA
4. http://localhost:5000/login      # Tester connexion
5. http://localhost:5000/test       # Tests développeurs
```

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

### 🚀 **Prochaines étapes recommandées :**

1. **Démarrez l'application** : `python app_complete.py`
2. **Testez la création** : http://localhost:5000/create
3. **Configurez le 2FA** : Scannez les QR Codes avec Google Authenticator
4. **Testez la connexion** : http://localhost:5000/login
5. **Explorez l'interface** : http://localhost:5000/test (pour développeurs)

### 📱 **Configuration Google Authenticator :**
1. Téléchargez l'app Google Authenticator
2. Scannez le QR Code 2FA généré lors de la création
3. Utilisez les codes à 6 chiffres pour vous connecter

**✅ Tous vos templates sont prêts et fonctionnels !**

Testez dès maintenant sur `http://localhost:5000/` �

---

## 🎯 **Workflow utilisateur complet**

### **1. Création d'un nouveau compte** 
```
👤 Utilisateur → /create → Template create.html
   ↓
📝 Saisie nom d'utilisateur (validation JS)
   ↓
🚀 POST /create → handler.py
   ↓
✅ Génération automatique :
   • Mot de passe 24 caractères
   • Secret 2FA (TOTP)
   • QR Code mot de passe
   • QR Code 2FA
   ↓
📱 Template create_success.html :
   • Affichage des QR Codes
   • Instructions Google Authenticator
   • Bouton test connexion
```

### **2. Configuration 2FA**
```
📱 Google Authenticator
   ↓
📲 Scanner QR Code 2FA
   ↓
🔑 Codes 6 chiffres générés (30s)
   ↓
✅ Application configurée
```

### **3. Connexion sécurisée**
```
🔑 Utilisateur → /login → Template login.html
   ↓
📝 Triple authentification :
   • Nom d'utilisateur
   • Mot de passe (24 caractères)
   • Code 2FA (formatage auto)
   ↓
🔒 POST /login → login_handler.py
   ↓
✅ Vérifications :
   • Login existe en DB
   • Déchiffrement mot de passe
   • Validation TOTP temps réel
   • Contrôle expiration (6 mois)
   ↓
🎉 Template login_success.html
```

### **4. Gestion des erreurs**
```
❌ Erreurs possibles :
   • Nom d'utilisateur inexistant
   • Mot de passe incorrect
   • Code 2FA invalide/expiré
   • Compte expiré (> 6 mois)
   ↓
⚠️ Messages flash contextuels
   ↓
🔄 Redirection appropriée :
   • Compte expiré → /create
   • Autres erreurs → /login avec aide
```

---

## 🎨 **Fonctionnalités Frontend avancées**

### **Templates interactifs**

#### **`create.html`**
- **Validation live** : Nom d'utilisateur (lettres, chiffres, - et _)
- **Messages d'aide** : Explications détaillées génération auto
- **Design sécurisé** : Icônes et couleurs pour guider l'utilisateur
- **Responsive** : Compatible mobile et desktop

#### **`login.html`** 
- **Formatage automatique** : Code 2FA (6 chiffres numériques uniquement)
- **Auto-focus** : Navigation clavier optimisée
- **Validation pré-envoi** : Contrôles JavaScript avant POST
- **Guide intégré** : Instructions Google Authenticator
- **Gestion d'erreurs** : Messages contextuels selon le problème

#### **`create_success.html`**
- **QR Codes sécurisés** : Affichage base64 direct (pas de fichiers)
- **Instructions complètes** : Guide pas-à-pas configuration 2FA
- **Actions rapides** : Boutons test connexion et retour accueil
- **Mise en garde** : Importance sauvegarde et expiration 6 mois

### **JavaScript avancé**
```javascript
// Formatage temps réel code 2FA
document.getElementById('totp_code').addEventListener('input', function(e) {
    let value = e.target.value.replace(/[^0-9]/g, '');
    if (value.length > 6) value = value.substring(0, 6);
    e.target.value = value;
});

// Validation formulaire avant envoi
form.addEventListener('submit', function(e) {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const totp = document.getElementById('totp_code').value;
    
    if (!username || !password || totp.length !== 6) {
        e.preventDefault();
        alert('⚠️ Veuillez remplir tous les champs correctement.');
        return false;
    }
});
```

### **CSS responsive et sécurisé**
```css
/* Mise en évidence des champs selon validation */
.valid { border-color: #28a745; }
.invalid { border-color: #dc3545; }

/* QR Codes optimisés */
.qr-code { 
    max-width: 200px; 
    border: 2px solid #007bff; 
    border-radius: 8px; 
}

/* Messages flash contextuels */
.flash-messages .success { background: #d4edda; border-left: 4px solid #28a745; }
.flash-messages .error { background: #f8d7da; border-left: 4px solid #dc3545; }
.flash-messages .warning { background: #fff3cd; border-left: 4px solid #ffc107; }
```

---

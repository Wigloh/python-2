# 🚀 Scripts de Démarrage MSPR

Ce dossier contient tous les scripts de démarrage et utilitaires pour le projet MSPR.

## 📂 **Fichiers disponibles**

### **🎯 Scripts principaux**

#### **`menu-demarrage.bat`** - Menu principal
- Point d'entrée unique pour tous les scripts
- Choix entre Docker ou PostgreSQL local
- Interface utilisateur simple

#### **`demarrage-ultra-rapide.bat`** - Démarrage automatique complet
- **Recommandé pour la plupart des utilisateurs**
- Exécute automatiquement toutes les étapes :
  - Vérification des prérequis (Python + Docker)
  - Création/démarrage du conteneur PostgreSQL
  - Installation des dépendances Python
  - Configuration de la base de données
  - Démarrage de l'application Flask
- **Temps : ~2 minutes**

### **🛠️ Utilitaires**

#### **`utilitaires-maintenance.bat`** - Outils de maintenance
- Arrêt/suppression/recréation des conteneurs
- Visualisation des logs
- Tests de connexion
- Réinstallation des dépendances
- Nettoyage complet

### **📜 Scripts hérités**

#### **`start_app_docker.bat`** - Démarrage Docker détaillé
- Version détaillée avec vérifications étape par étape
- Affichage des résultats de chaque étape
- Recommandé pour le débogage

#### **`start_app_mspr.bat`** - Démarrage PostgreSQL local
- **Déprécié** - utilise PostgreSQL local au lieu de Docker
- Conservé pour compatibilité

## 🚀 **Utilisation recommandée**

### **Pour débuter rapidement :**
```cmd
# Lancez simplement :
scripts-demarrage\demarrage-ultra-rapide.bat
```

### **Pour choisir la méthode :**
```cmd
# Menu avec options :
scripts-demarrage\menu-demarrage.bat
```

### **Pour maintenance/dépannage :**
```cmd
# Outils de maintenance :
scripts-demarrage\utilitaires-maintenance.bat
```

## 🔧 **Prérequis**

- **Python 3.8+** installé et dans le PATH
- **Docker Desktop** installé et démarré
- **Connexion Internet** pour télécharger l'image PostgreSQL

## 📁 **Structure recommandée**

```
python-2/
├── scripts-demarrage/          # ← Ce dossier
│   ├── menu-demarrage.bat
│   ├── demarrage-ultra-rapide.bat
│   ├── utilitaires-maintenance.bat
│   ├── start_app_docker.bat
│   └── start_app_mspr.bat
├── app_complete.py
├── database_setup.sql
├── requirements.txt
└── ...autres fichiers du projet
```

## ⚡ **Guide rapide**

1. **Première utilisation :**
   ```cmd
   cd "chemin\vers\python-2"
   scripts-demarrage\demarrage-ultra-rapide.bat
   ```

2. **Utilisations suivantes :**
   ```cmd
   scripts-demarrage\menu-demarrage.bat
   ```

3. **En cas de problème :**
   ```cmd
   scripts-demarrage\utilitaires-maintenance.bat
   # Choisir option 7 : "Nettoyer et redemarrer tout"
   ```

## 🎯 **Pages de l'application**

Une fois démarrée, l'application est disponible sur :

- **Page d'accueil** : http://localhost:5000/
- **Création de compte** : http://localhost:5000/create
- **Connexion 2FA** : http://localhost:5000/login
- **Interface de test** : http://localhost:5000/test

## 📞 **Support**

Si vous rencontrez des problèmes :

1. Utilisez `utilitaires-maintenance.bat` option 4 pour voir les logs
2. Utilisez l'option 7 pour un nettoyage complet
3. Consultez le README principal du projet

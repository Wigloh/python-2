#!/usr/bin/env python3
"""
Configuration SQLite automatique pour MSPR
Créez ce fichier si PostgreSQL pose problème
"""

import sqlite3
import os
from datetime import datetime

def setup_sqlite_database():
    """Configure une base SQLite comme alternative à PostgreSQL"""
    db_path = 'cofrap.db'
    
    print("🔧 Configuration SQLite pour MSPR...")
    
    # Supprimer l'ancienne base si elle existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Ancienne base {db_path} supprimée")
    
    # Créer la nouvelle base
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Créer la table users (équivalent PostgreSQL)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            secret_2fa TEXT,
            gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expired BOOLEAN DEFAULT FALSE,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Créer les index pour performance
    cursor.execute('CREATE INDEX idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX idx_users_expired ON users(expired)')
    cursor.execute('CREATE INDEX idx_users_gendate ON users(gendate)')
    
    conn.commit()
    
    print(f"✅ Base SQLite créée : {db_path}")
    print("✅ Table 'users' créée avec tous les champs")
    print("✅ Index créés pour les performances")
    
    # Test d'insertion
    try:
        cursor.execute(
            "INSERT INTO users (username, password, secret_2fa) VALUES (?, ?, ?)",
            ('test_user', 'encrypted_password', 'encrypted_2fa_secret')
        )
        conn.commit()
        
        # Test de lecture
        cursor.execute("SELECT * FROM users WHERE username = ?", ('test_user',))
        result = cursor.fetchone()
        
        if result:
            print("✅ Test d'insertion/lecture réussi")
            
            # Nettoyer le test
            cursor.execute("DELETE FROM users WHERE username = ?", ('test_user',))
            conn.commit()
            print("✅ Données de test nettoyées")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
    
    finally:
        conn.close()
    
    # Configurer les variables d'environnement pour SQLite
    print("\n🔧 Configuration des variables d'environnement...")
    os.environ['DB_TYPE'] = 'sqlite'
    os.environ['DB_PATH'] = db_path
    os.environ['DB_HOST'] = ''  # Non utilisé avec SQLite
    os.environ['DB_NAME'] = db_path
    os.environ['DB_USER'] = ''  # Non utilisé avec SQLite
    os.environ['DB_PASSWORD'] = ''  # Non utilisé avec SQLite
    
    print("✅ Variables configurées pour SQLite")
    print(f"✅ Fichier de base : {os.path.abspath(db_path)}")
    
    return db_path

def test_database_connection():
    """Test que la base SQLite fonctionne"""
    try:
        conn = sqlite3.connect('cofrap.db')
        cursor = conn.cursor()
        
        # Test simple
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        print(f"✅ Connexion base OK - {count} utilisateurs")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion base : {e}")
        return False

if __name__ == '__main__':
    print("🔐 MSPR - Configuration SQLite automatique")
    print("=" * 50)
    
    # Configuration de la base
    db_path = setup_sqlite_database()
    
    # Test de connexion
    if test_database_connection():
        print("\n🎉 Configuration SQLite terminée avec succès !")
        print("\nProchaines étapes :")
        print("1. Démarrez l'application : python app_complete.py")
        print("2. Ouvrez votre navigateur : http://localhost:5000")
        print("3. Testez la création de compte : http://localhost:5000/create")
    else:
        print("\n❌ Problème avec la configuration SQLite")
    
    print("\n💡 Cette configuration SQLite remplace PostgreSQL")
    print("💡 Vos données seront stockées dans :", os.path.abspath('cofrap.db'))

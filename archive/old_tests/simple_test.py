#!/usr/bin/env python3
"""
Test simple des handlers sans Flask
"""

import json
import os
import sys

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration pour utiliser localhost (Docker PostgreSQL)
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'password'

def test_create_user():
    """Test de création d'utilisateur"""
    try:
        from handler import handle as create_user_handler
        
        # Données de test
        test_data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        
        # Appeler le handler
        result = create_user_handler(json.dumps(test_data))
        print("✅ Test création utilisateur:")
        print(result)
        return True
        
    except Exception as e:
        print(f"❌ Erreur création utilisateur: {e}")
        return False

def test_login():
    """Test de connexion"""
    try:
        from login_handler import handle as login_handler
        
        # Données de test
        test_data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        
        # Appeler le handler
        result = login_handler(json.dumps(test_data))
        print("✅ Test connexion:")
        print(result)
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

def test_generate_2fa():
    """Test de génération 2FA"""
    try:
        from generate_2fa_handler import handle as generate_2fa_handler
        
        # Données de test
        test_data = {
            "username": "testuser"
        }
        
        # Appeler le handler
        result = generate_2fa_handler(json.dumps(test_data))
        print("✅ Test génération 2FA:")
        print(result)
        return True
        
    except Exception as e:
        print(f"❌ Erreur génération 2FA: {e}")
        return False

def main():
    print("🧪 Test des handlers MSPR")
    print("=" * 40)
    
    # Vérifier PostgreSQL
    print("📊 Vérification PostgreSQL...")
    import subprocess
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if "mspr-postgres" in result.stdout:
            print("✅ PostgreSQL est actif")
        else:
            print("❌ PostgreSQL n'est pas actif")
            return
    except Exception as e:
        print(f"❌ Erreur vérification Docker: {e}")
        return
    
    # Tests des handlers
    print("\n🧪 Tests des handlers...")
    
    # Test 1: Création utilisateur
    print("\n1. Test création utilisateur:")
    test_create_user()
    
    # Test 2: Connexion
    print("\n2. Test connexion:")
    test_login()
    
    # Test 3: Génération 2FA
    print("\n3. Test génération 2FA:")
    test_generate_2fa()
    
    print("\n✅ Tests terminés !")

if __name__ == '__main__':
    main()

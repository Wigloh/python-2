#!/usr/bin/env python3
"""
Test de vérification 2FA avec le code généré
"""

import json
import os
import sys

# Configuration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'password'

def test_verify_2fa():
    """Test de vérification 2FA"""
    try:
        from generate_2fa_handler import handle as generate_2fa_handler
        
        # D'abord générer un nouveau 2FA pour obtenir le code
        print("🔑 Génération d'un nouveau 2FA...")
        generate_data = {
            "username": "testuser"
        }
        
        generate_result = generate_2fa_handler(json.dumps(generate_data))
        generate_response = json.loads(generate_result)
        
        if generate_response.get("status") == "success":
            test_code = generate_response.get("test_code")
            print(f"✅ Code 2FA généré: {test_code}")
            
            # Maintenant vérifier le code
            print("🔍 Vérification du code 2FA...")
            verify_data = {
                "username": "testuser",
                "code_2fa": test_code
            }
            
            verify_result = generate_2fa_handler(json.dumps(verify_data))
            verify_response = json.loads(verify_result)
            
            print("✅ Résultat de la vérification:")
            print(json.dumps(verify_response, indent=2))
            
            return verify_response.get("verified", False)
        else:
            print(f"❌ Erreur génération 2FA: {generate_response}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification 2FA: {e}")
        return False

def test_login_with_2fa():
    """Test de connexion avec 2FA"""
    try:
        from login_handler import handle as login_handler
        from generate_2fa_handler import handle as generate_2fa_handler
        
        # Générer un code 2FA valide
        generate_data = {"username": "testuser"}
        generate_result = generate_2fa_handler(json.dumps(generate_data))
        generate_response = json.loads(generate_result)
        
        if generate_response.get("status") == "success":
            test_code = generate_response.get("test_code")
            
            # Tenter la connexion avec le code 2FA
            print("🔐 Test de connexion avec 2FA...")
            login_data = {
                "username": "testuser",
                "password": "TestPassword123!",
                "totp_code": test_code
            }
            
            login_result = login_handler(json.dumps(login_data))
            login_response = json.loads(login_result)
            
            print("✅ Résultat de la connexion:")
            print(json.dumps(login_response, indent=2))
            
            return login_response.get("status") == "success"
        else:
            print(f"❌ Erreur génération 2FA: {generate_response}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion avec 2FA: {e}")
        return False

def main():
    print("🧪 Test complet du système 2FA")
    print("=" * 40)
    
    # Test 1: Vérification 2FA
    print("\n1. Test de vérification 2FA:")
    verify_success = test_verify_2fa()
    
    # Test 2: Connexion avec 2FA
    print("\n2. Test de connexion avec 2FA:")
    login_success = test_login_with_2fa()
    
    # Résumé
    print("\n📊 Résumé des tests:")
    print(f"   - Vérification 2FA: {'✅ Succès' if verify_success else '❌ Échec'}")
    print(f"   - Connexion avec 2FA: {'✅ Succès' if login_success else '❌ Échec'}")
    
    if verify_success and login_success:
        print("\n🎉 Tous les tests 2FA passent ! Le système est fonctionnel.")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez la configuration.")

if __name__ == '__main__':
    main()

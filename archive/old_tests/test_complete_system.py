#!/usr/bin/env python3
"""
🧪 Tests automatisés complets du système MSPR
Teste tous les composants : Flask, PostgreSQL, handlers, 2FA
"""

import requests
import json
import time
import subprocess
import sys

# Configuration
FLASK_URL = "http://localhost:5000"
POSTGRES_CONTAINER = "mspr-postgres"

def colored_print(message, color="white"):
    """Affiche un message coloré"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{message}\033[0m")

def test_infrastructure():
    """Teste l'infrastructure (PostgreSQL, Flask)"""
    colored_print("🔧 Test de l'infrastructure...", "blue")
    
    # Test PostgreSQL
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={POSTGRES_CONTAINER}", "--format", "{{.Names}}"],
            capture_output=True, text=True, check=True
        )
        if POSTGRES_CONTAINER in result.stdout:
            colored_print("✅ PostgreSQL est actif", "green")
        else:
            colored_print("❌ PostgreSQL n'est pas actif", "red")
            return False
    except Exception as e:
        colored_print(f"❌ Erreur vérification PostgreSQL: {e}", "red")
        return False
    
    # Test Flask
    try:
        response = requests.get(f"{FLASK_URL}/health", timeout=5)
        if response.status_code == 200:
            colored_print("✅ Flask API est accessible", "green")
            data = response.json()
            colored_print(f"   Service: {data.get('service')}", "white")
            colored_print(f"   Database: {data.get('database')}", "white")
            return True
        else:
            colored_print(f"❌ Flask API retourne {response.status_code}", "red")
            return False
    except Exception as e:
        colored_print(f"❌ Erreur connexion Flask: {e}", "red")
        return False

def test_create_user():
    """Teste la création d'utilisateur"""
    colored_print("👤 Test de création d'utilisateur...", "blue")
    
    username = f"testuser_{int(time.time())}"
    password = "TestPassword123!"
    
    try:
        response = requests.post(
            f"{FLASK_URL}/api/create-user",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            colored_print("✅ Utilisateur créé avec succès", "green")
            colored_print(f"   Username: {data.get('username')}", "white")
            colored_print(f"   Password généré: {data.get('password', 'Non affiché')}", "white")
            return username, data.get('password', password)
        else:
            colored_print(f"❌ Erreur création utilisateur: {response.text}", "red")
            return None, None
            
    except Exception as e:
        colored_print(f"❌ Erreur requête création: {e}", "red")
        return None, None

def test_generate_2fa(username):
    """Teste la génération 2FA"""
    colored_print("🔑 Test de génération 2FA...", "blue")
    
    try:
        response = requests.post(
            f"{FLASK_URL}/api/generate-2fa",
            json={"username": username},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                colored_print("✅ 2FA généré avec succès", "green")
                colored_print(f"   Secret: {data.get('secret', 'Non affiché')[:8]}...", "white")
                colored_print(f"   Code test: {data.get('test_code')}", "white")
                colored_print("   QR Code généré ✓", "white")
                return data.get('test_code')
            else:
                colored_print(f"❌ Erreur dans la réponse 2FA: {data}", "red")
                return None
        else:
            colored_print(f"❌ Erreur génération 2FA: {response.text}", "red")
            return None
            
    except Exception as e:
        colored_print(f"❌ Erreur requête 2FA: {e}", "red")
        return None

def test_verify_2fa(username, code):
    """Teste la vérification 2FA"""
    colored_print("🔍 Test de vérification 2FA...", "blue")
    
    try:
        response = requests.post(
            f"{FLASK_URL}/api/verify-2fa",
            json={"username": username, "code_2fa": code},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('verified'):
                colored_print("✅ Code 2FA vérifié avec succès", "green")
                return True
            else:
                colored_print(f"❌ Code 2FA invalide: {data}", "red")
                return False
        else:
            colored_print(f"❌ Erreur vérification 2FA: {response.text}", "red")
            return False
            
    except Exception as e:
        colored_print(f"❌ Erreur requête vérification: {e}", "red")
        return False

def test_database_content():
    """Teste le contenu de la base de données"""
    colored_print("🗄️ Test du contenu de la base de données...", "blue")
    
    try:
        # Compter les utilisateurs
        result = subprocess.run([
            "docker", "exec", POSTGRES_CONTAINER, 
            "psql", "-U", "postgres", "-d", "cofrap", 
            "-c", "SELECT COUNT(*) FROM users;"
        ], capture_output=True, text=True, check=True)
        
        lines = result.stdout.strip().split('\n')
        count_line = [line for line in lines if line.strip().isdigit()]
        if count_line:
            user_count = int(count_line[0].strip())
            colored_print(f"✅ Base de données accessible", "green")
            colored_print(f"   Nombre d'utilisateurs: {user_count}", "white")
            return True
        else:
            colored_print("❌ Impossible de compter les utilisateurs", "red")
            return False
            
    except Exception as e:
        colored_print(f"❌ Erreur accès base de données: {e}", "red")
        return False

def main():
    """Fonction principale de test"""
    colored_print("🧪 MSPR - Tests Automatisés Complets", "blue")
    colored_print("=" * 50, "white")
    
    # Résultats des tests
    results = {}
    
    # Test 1: Infrastructure
    colored_print("\n1️⃣ Tests d'infrastructure", "yellow")
    results['infrastructure'] = test_infrastructure()
    
    if not results['infrastructure']:
        colored_print("\n❌ Infrastructure non disponible. Arrêt des tests.", "red")
        return False
    
    # Test 2: Base de données
    colored_print("\n2️⃣ Test de la base de données", "yellow")
    results['database'] = test_database_content()
    
    # Test 3: Création d'utilisateur
    colored_print("\n3️⃣ Test de création d'utilisateur", "yellow")
    username, password = test_create_user()
    results['create_user'] = username is not None
    
    if not username:
        colored_print("\n❌ Impossible de créer un utilisateur. Tests 2FA annulés.", "red")
        results['2fa'] = False
        results['verify_2fa'] = False
    else:
        # Test 4: Génération 2FA
        colored_print("\n4️⃣ Test de génération 2FA", "yellow")
        test_code = test_generate_2fa(username)
        results['2fa'] = test_code is not None
        
        if test_code:
            # Test 5: Vérification 2FA
            colored_print("\n5️⃣ Test de vérification 2FA", "yellow")
            results['verify_2fa'] = test_verify_2fa(username, test_code)
        else:
            results['verify_2fa'] = False
    
    # Résumé
    colored_print("\n📊 RÉSUMÉ DES TESTS", "blue")
    colored_print("=" * 30, "white")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        color = "green" if passed else "red"
        colored_print(f"   {test_name.replace('_', ' ').title()}: {status}", color)
    
    colored_print(f"\nScore: {passed_tests}/{total_tests} tests passés", "blue")
    
    if passed_tests == total_tests:
        colored_print("\n🎉 TOUS LES TESTS PASSENT ! Le système MSPR est fonctionnel.", "green")
        colored_print("\n🔗 Accédez à l'interface web: http://localhost:5000", "blue")
        return True
    else:
        colored_print(f"\n⚠️  {total_tests - passed_tests} test(s) ont échoué.", "yellow")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

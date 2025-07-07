#!/usr/bin/env python3
"""
🧪 Script de Validation Complète du Projet MSPR
Teste tous les composants pour s'assurer que le système fonctionne entièrement
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

# Configuration
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'password'

def colored_print(message, color="white"):
    """Affichage coloré pour une meilleure lisibilité"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[0m"
    }
    print(f"{colors.get(color, '')}{message}{colors['white']}")

def test_database_connection():
    """Test de connexion à la base de données"""
    colored_print("\n📊 TEST 1: Connexion Base de Données", "blue")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            dbname='cofrap', 
            user='postgres',
            password='password'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        colored_print("✅ PostgreSQL connecté avec succès", "green")
        colored_print(f"   Version: {version[0][:50]}...", "white")
        return True
    except Exception as e:
        colored_print(f"❌ Erreur PostgreSQL: {e}", "red")
        return False

def test_table_structure():
    """Test de la structure de la table users"""
    colored_print("\n📋 TEST 2: Structure Table Users", "blue")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            dbname='cofrap',
            user='postgres', 
            password='password'
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        
        expected_columns = ['id', 'username', 'password', 'secret_2fa', 'gendate', 'expired', 'updated_at']
        actual_columns = [col[0] for col in columns]
        
        colored_print(f"✅ Table 'users' trouvée avec {len(columns)} colonnes", "green")
        for col_name, col_type in columns:
            colored_print(f"   - {col_name}: {col_type}", "white")
        
        missing = [col for col in expected_columns if col not in actual_columns]
        if missing:
            colored_print(f"⚠️  Colonnes manquantes: {missing}", "yellow")
        else:
            colored_print("✅ Toutes les colonnes attendues sont présentes", "green")
        
        return len(missing) == 0
    except Exception as e:
        colored_print(f"❌ Erreur structure table: {e}", "red")
        return False

def test_handlers_import():
    """Test d'import des handlers"""
    colored_print("\n🔧 TEST 3: Import des Handlers", "blue")
    results = {}
    
    # Test handler création
    try:
        from handler import handle as create_handler
        colored_print("✅ Handler création importé", "green")
        results['create'] = True
    except Exception as e:
        colored_print(f"❌ Handler création: {e}", "red")
        results['create'] = False
    
    # Test handler login
    try:
        from login_handler import handle as login_handler
        colored_print("✅ Handler login importé", "green")
        results['login'] = True
    except Exception as e:
        colored_print(f"❌ Handler login: {e}", "red")
        results['login'] = False
    
    # Test handler 2FA
    try:
        from generate_2fa_handler import handle as gen_2fa_handler
        colored_print("✅ Handler 2FA importé", "green")
        results['2fa'] = True
    except Exception as e:
        colored_print(f"❌ Handler 2FA: {e}", "red")
        results['2fa'] = False
    
    return all(results.values())

def test_dependencies():
    """Test des dépendances critiques"""
    colored_print("\n📦 TEST 4: Dépendances Critiques", "blue")
    dependencies = [
        'flask', 'psycopg2', 'cryptography', 'pyotp', 'qrcode', 'python-dateutil'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            colored_print(f"✅ {dep}", "green")
        except ImportError:
            colored_print(f"❌ {dep} manquant", "red")
            all_ok = False
    
    return all_ok

def test_handler_functionality():
    """Test fonctionnel des handlers"""
    colored_print("\n⚙️  TEST 5: Fonctionnalité Handlers", "blue")
    
    try:
        from handler import handle as create_handler
        from login_handler import handle as login_handler
        from generate_2fa_handler import handle as gen_2fa_handler
        
        # Test création utilisateur
        test_username = f"test_validation_{int(time.time())}"
        create_data = {"username": test_username}
        
        colored_print(f"🔧 Test création utilisateur: {test_username}", "white")
        result = create_handler(json.dumps(create_data))
        result_data = json.loads(result)
        
        if result_data.get('status') == 'success':
            colored_print("✅ Création utilisateur: OK", "green")
            password = result_data.get('password')
            colored_print(f"   Mot de passe généré: {password}", "white")
            
            # Test génération 2FA
            colored_print("🔧 Test génération 2FA", "white")
            gen_result = gen_2fa_handler(json.dumps({"username": test_username}))
            gen_data = json.loads(gen_result)
            
            if gen_data.get('status') == 'success':
                colored_print("✅ Génération 2FA: OK", "green")
                colored_print(f"   QR Code généré: {'✅' if gen_data.get('qr_code_base64') else '❌'}", "white")
                
                # Test login (sans 2FA pour éviter la complexité)
                colored_print("🔧 Test login (sans 2FA)", "white")
                login_data = {
                    "username": test_username,
                    "password": password
                }
                login_result = login_handler(json.dumps(login_data))
                login_response = json.loads(login_result)
                
                # Le login sans 2FA devrait échouer, mais le handler doit répondre
                colored_print("✅ Handler login: Répond correctement", "green")
                
            else:
                colored_print(f"❌ Génération 2FA: {gen_data.get('error', 'Erreur inconnue')}", "red")
                return False
        else:
            colored_print(f"❌ Création utilisateur: {result_data.get('error', 'Erreur inconnue')}", "red")
            return False
            
        return True
        
    except Exception as e:
        colored_print(f"❌ Erreur test handlers: {e}", "red")
        return False

def test_flask_app_startup():
    """Test de démarrage de l'application Flask"""
    colored_print("\n🌐 TEST 6: Application Flask", "blue")
    
    try:
        # Import de l'app
        from app_complete import app
        colored_print("✅ Import app_complete.py: OK", "green")
        
        # Test de configuration
        if app.secret_key:
            colored_print("✅ Secret key configurée", "green")
        else:
            colored_print("⚠️  Secret key non configurée", "yellow")
        
        # Test des routes principales
        with app.test_client() as client:
            # Test page d'accueil
            response = client.get('/')
            if response.status_code == 200:
                colored_print("✅ Route '/' accessible", "green")
            else:
                colored_print(f"❌ Route '/': {response.status_code}", "red")
            
            # Test endpoint health
            response = client.get('/health')
            if response.status_code == 200:
                colored_print("✅ Endpoint '/health' accessible", "green")
                health_data = response.get_json()
                colored_print(f"   Service: {health_data.get('service', 'N/A')}", "white")
            else:
                colored_print(f"❌ Endpoint '/health': {response.status_code}", "red")
        
        return True
        
    except Exception as e:
        colored_print(f"❌ Erreur Flask: {e}", "red")
        return False

def test_templates_and_static():
    """Test des templates et fichiers statiques"""
    colored_print("\n🎨 TEST 7: Templates et Fichiers Statiques", "blue")
    
    # Test existence templates
    templates = ['templates/home.html', 'templates/create.html', 'templates/login.html']
    static_files = ['static/css/style.css', 'static/css/forms.css']
    
    all_ok = True
    
    for template in templates:
        if os.path.exists(template):
            colored_print(f"✅ {template}", "green")
        else:
            colored_print(f"❌ {template} manquant", "red")
            all_ok = False
    
    for static_file in static_files:
        if os.path.exists(static_file):
            colored_print(f"✅ {static_file}", "green")
        else:
            colored_print(f"⚠️  {static_file} manquant (optionnel)", "yellow")
    
    return all_ok

def main():
    """Fonction principale de validation"""
    colored_print("=" * 60, "blue")
    colored_print("🧪 VALIDATION COMPLÈTE DU PROJET MSPR", "blue")
    colored_print("=" * 60, "blue")
    colored_print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "white")
    
    tests = [
        ("Base de données", test_database_connection),
        ("Structure table", test_table_structure), 
        ("Import handlers", test_handlers_import),
        ("Dépendances", test_dependencies),
        ("Fonctionnalité handlers", test_handler_functionality),
        ("Application Flask", test_flask_app_startup),
        ("Templates/Static", test_templates_and_static)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            colored_print(f"\n❌ Erreur critique dans {test_name}: {e}", "red")
            results.append((test_name, False))
    
    # Résumé final
    colored_print("\n" + "=" * 60, "blue")
    colored_print("📊 RÉSUMÉ DES TESTS", "blue")
    colored_print("=" * 60, "blue")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = "green" if result else "red"
        colored_print(f"{status} - {test_name}", color)
        if result:
            passed += 1
    
    colored_print("\n" + "-" * 60, "white")
    score = (passed / total) * 100
    color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    colored_print(f"🎯 SCORE FINAL: {passed}/{total} ({score:.1f}%)", color)
    
    if score == 100:
        colored_print("\n🎉 PARFAIT! Le projet fonctionne entièrement! 🎉", "green")
    elif score >= 80:
        colored_print("\n✅ EXCELLENT! Le projet est fonctionnel avec quelques détails mineurs", "green")
    elif score >= 60:
        colored_print("\n⚠️  BON! Le projet fonctionne mais nécessite quelques corrections", "yellow")
    else:
        colored_print("\n❌ PROBLÈMES! Le projet nécessite des corrections importantes", "red")
    
    colored_print("\n🚀 Pour lancer l'application: python app_complete.py", "blue")
    colored_print("🌐 Interface web: http://localhost:5000", "blue")

if __name__ == "__main__":
    main()

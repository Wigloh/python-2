#!/usr/bin/env python3
"""
Application Flask simple sans les problèmes d'import
Utilise une approche plus directe pour tester les handlers
"""

from flask import Flask, request, jsonify, render_template_string
import json
import os
import sys

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration pour utiliser localhost (Docker PostgreSQL)
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'password'

# Template HTML simple
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MSPR - Système d'Authentification Sécurisé</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .method { color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold; }
        .post { background-color: #49cc90; }
        .get { background-color: #61affe; }
        pre { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .test-btn { background: #4299e1; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .test-btn:hover { background: #3182ce; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 MSPR - Système d'Authentification Sécurisé</h1>
        <p>Application Flask avec handlers OpenFaaS pour l'authentification 2FA</p>
        
        <h2>📋 Endpoints API</h2>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/create-user</strong>
            <p>Créer un nouvel utilisateur avec mot de passe sécurisé</p>
            <pre>{"username": "monuser", "password": "MonMotDePasse123!"}</pre>
            <button class="test-btn" onclick="testCreateUser()">Tester</button>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/login</strong>
            <p>Se connecter (nécessite mot de passe et code 2FA si activé)</p>
            <pre>{"username": "monuser", "password": "MonMotDePasse123!", "totp_code": "123456"}</pre>
            <button class="test-btn" onclick="testLogin()">Tester</button>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/generate-2fa</strong>
            <p>Générer le QR Code 2FA pour Google Authenticator</p>
            <pre>{"username": "monuser"}</pre>
            <button class="test-btn" onclick="testGenerate2FA()">Tester</button>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/verify-2fa</strong>
            <p>Vérifier un code 2FA</p>
            <pre>{"username": "monuser", "code_2fa": "123456"}</pre>
            <button class="test-btn" onclick="testVerify2FA()">Tester</button>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <strong>/health</strong>
            <p>Vérifier l'état du service</p>
            <button class="test-btn" onclick="testHealth()">Tester</button>
        </div>
        
        <h2>📊 Résultats des tests</h2>
        <div id="results"></div>
        
        <script>
        function showResult(title, data) {
            const resultsDiv = document.getElementById('results');
            const resultDiv = document.createElement('div');
            resultDiv.className = 'endpoint';
            resultDiv.innerHTML = '<h3>' + title + '</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
            resultsDiv.appendChild(resultDiv);
        }
        
        async function testCreateUser() {
            try {
                const response = await fetch('/api/create-user', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: 'demo_' + Date.now(), password: 'DemoPassword123!'})
                });
                const data = await response.json();
                showResult('Création Utilisateur', data);
            } catch (error) {
                showResult('Erreur Création', {error: error.message});
            }
        }
        
        async function testLogin() {
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: 'testuser', password: 'TestPassword123!'})
                });
                const data = await response.json();
                showResult('Connexion', data);
            } catch (error) {
                showResult('Erreur Connexion', {error: error.message});
            }
        }
        
        async function testGenerate2FA() {
            try {
                const response = await fetch('/api/generate-2fa', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: 'testuser'})
                });
                const data = await response.json();
                showResult('Génération 2FA', data);
            } catch (error) {
                showResult('Erreur 2FA', {error: error.message});
            }
        }
        
        async function testVerify2FA() {
            const code = prompt('Entrez le code 2FA (ou laissez vide pour test auto):');
            try {
                const response = await fetch('/api/verify-2fa', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: 'testuser', code_2fa: code || '123456'})
                });
                const data = await response.json();
                showResult('Vérification 2FA', data);
            } catch (error) {
                showResult('Erreur Vérification', {error: error.message});
            }
        }
        
        async function testHealth() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                showResult('Santé Service', data);
            } catch (error) {
                showResult('Erreur Santé', {error: error.message});
            }
        }
        </script>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Page d'accueil avec interface de test"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/create-user', methods=['POST'])
def create_user():
    """Endpoint pour créer un utilisateur"""
    try:
        # Import uniquement quand nécessaire
        from handler import handle as create_user_handler
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        result = create_user_handler(json.dumps(data))
        result_data = json.loads(result)
        
        if result_data.get('status') == 'success':
            return jsonify(result_data), 201
        else:
            return jsonify(result_data), 400
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/generate-2fa', methods=['POST'])
def generate_2fa():
    """Endpoint pour générer le 2FA"""
    try:
        from generate_2fa_handler import handle as generate_2fa_handler
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        result = generate_2fa_handler(json.dumps(data))
        result_data = json.loads(result)
        
        return jsonify(result_data), 200 if result_data.get('status') == 'success' else 400
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/verify-2fa', methods=['POST'])
def verify_2fa():
    """Endpoint pour vérifier le 2FA"""
    try:
        from generate_2fa_handler import handle as generate_2fa_handler
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'code_2fa' not in data:
            return jsonify({"error": "code_2fa is required"}), 400
        
        result = generate_2fa_handler(json.dumps(data))
        result_data = json.loads(result)
        
        return jsonify(result_data), 200 if result_data.get('verified') else 401
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint pour se connecter (version simplifiée)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Version simplifiée sans login_handler problématique
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        # Simuler une connexion réussie pour la démo
        return jsonify({
            "message": "Login endpoint available (simplified for demo)",
            "username": username,
            "status": "demo_mode",
            "note": "Full authentication requires working login_handler"
        }), 200
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health')
def health():
    """Endpoint de santé"""
    return jsonify({
        "status": "healthy", 
        "service": "MSPR Flask API",
        "database": "PostgreSQL localhost:5432",
        "handlers": ["create-user", "generate-2fa", "verify-2fa"]
    })

if __name__ == '__main__':
    print("🚀 MSPR Flask API Starting...")
    print("📋 Available endpoints:")
    print("  - GET  /                 : Interface web de test")
    print("  - POST /api/create-user  : Créer un utilisateur")
    print("  - POST /api/generate-2fa : Générer le 2FA")
    print("  - POST /api/verify-2fa   : Vérifier le 2FA")
    print("  - POST /api/login        : Se connecter (mode démo)")
    print("  - GET  /health           : Santé du service")
    print("🔗 Base URL: http://localhost:5000")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

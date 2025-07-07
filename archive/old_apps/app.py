#!/usr/bin/env python3
"""
Application Flask simple pour tester les handlers
Utilise les handlers OpenFaaS comme fonctions normales
"""

from flask import Flask, request, jsonify, render_template
import os
import sys

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer nos handlers
from handler import handle as create_user_handler
from login_handler import handle as login_handler
from generate_2fa_handler import handle as generate_2fa_handler

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration pour utiliser localhost (Docker PostgreSQL)
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'password'

@app.route('/')
def home():
    """Page d'accueil avec documentation des endpoints"""
    return render_template('home.html')

@app.route('/api/create-user', methods=['POST'])
def create_user():
    """Endpoint pour créer un utilisateur"""
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Appeler le handler OpenFaaS
        result = create_user_handler(request.get_data(as_text=True))
        
        # Parser le résultat JSON
        import json
        result_data = json.loads(result)
        
        # Retourner avec le bon code de statut
        if result_data.get('status') == 'success':
            return jsonify(result_data), 201
        else:
            return jsonify(result_data), 400
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint pour se connecter"""
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Appeler le handler OpenFaaS
        result = login_handler(request.get_data(as_text=True))
        
        # Parser le résultat JSON
        import json
        result_data = json.loads(result)
        
        # Retourner avec le bon code de statut
        if result_data.get('status') == 'success':
            return jsonify(result_data), 200
        else:
            return jsonify(result_data), 401
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/generate-2fa', methods=['POST'])
def generate_2fa():
    """Endpoint pour générer le 2FA"""
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Appeler le handler OpenFaaS
        result = generate_2fa_handler(request.get_data(as_text=True))
        
        # Parser le résultat JSON
        import json
        result_data = json.loads(result)
        
        # Retourner avec le bon code de statut
        if result_data.get('status') == 'success':
            return jsonify(result_data), 200
        else:
            return jsonify(result_data), 400
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/verify-2fa', methods=['POST'])
def verify_2fa():
    """Endpoint pour vérifier le 2FA"""
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Ajouter le code de vérification aux données
        if 'code_2fa' not in data:
            return jsonify({"error": "code_2fa is required"}), 400
        
        # Appeler le handler OpenFaaS (même que generate_2fa mais avec code)
        result = generate_2fa_handler(request.get_data(as_text=True))
        
        # Parser le résultat JSON
        import json
        result_data = json.loads(result)
        
        # Retourner avec le bon code de statut
        if result_data.get('verified'):
            return jsonify(result_data), 200
        else:
            return jsonify(result_data), 401
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/create')
def create_page():
    """Page pour créer un utilisateur"""
    return render_template('create.html')

@app.route('/login-page')
def login_page():
    """Page de connexion"""
    return render_template('login.html')

@app.route('/health')
def health():
    """Endpoint de santé"""
    return jsonify({"status": "healthy", "service": "MSPR Flask API"})

if __name__ == '__main__':
    print("🚀 MSPR Flask API Starting...")
    print("📋 Available endpoints:")
    print("  - GET  /                 : Page d'accueil")
    print("  - GET  /create           : Page de création d'utilisateur")
    print("  - GET  /login-page       : Page de connexion")
    print("  - POST /api/create-user  : Créer un utilisateur")
    print("  - POST /api/login        : Se connecter")
    print("  - POST /api/generate-2fa : Générer le 2FA")
    print("  - POST /api/verify-2fa   : Vérifier le 2FA")
    print("  - GET  /health           : Santé du service")
    print("🔗 Base URL: http://localhost:5000")
    print("")
    
    # Lancer l'application
    app.run(host='0.0.0.0', port=5000, debug=True)

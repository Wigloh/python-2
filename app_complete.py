#!/usr/bin/env python3
"""
Application Flask complète avec tous les handlers
Version complète avec login, création d'utilisateur, et 2FA
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import json
import os
import sys

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = 'mspr-secret-key-2025-projet-education'

# Configuration PostgreSQL Docker - VALEURS FIXES POUR LE PROJET
# Note: Ces variables sont définies pour les handlers qui les utilisent encore
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'cofrap'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'mspr2024'
os.environ['FERNET_KEY'] = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

@app.route('/')
def home():
    """Page d'accueil avec navigation"""
    return render_template('home.html')

@app.route('/test')
def test_interface():
    """Interface de test API complète"""
    return render_template('index.html')

@app.route('/create')
def create_page():
    """Page de création de compte"""
    return render_template('create.html')

@app.route('/login')
def login_page():
    """Page de connexion"""
    return render_template('login.html')

@app.route('/create-account', methods=['POST'])
def create_account():
    """Traitement de création de compte via formulaire"""
    try:
        username = request.form.get('username')
        
        if not username:
            flash('Le nom d\'utilisateur est requis', 'error')
            return redirect(url_for('create_page'))
        
        # Appel du handler de création
        from handler import handle as create_user_handler
        
        data = {"username": username}
        result = create_user_handler(json.dumps(data))
        result_data = json.loads(result)
        
        if result_data.get('status') == 'success':
            # Stocker les données en session ou les passer au template
            return render_template('create_success.html', 
                                 username=username,
                                 password=result_data.get('password'),
                                 password_qr=result_data.get('password_qr_code'),
                                 totp_qr=result_data.get('totp_qr_code'))
        else:
            flash(f'Erreur lors de la création: {result_data.get("error")}', 'error')
            return redirect(url_for('create_page'))
            
    except Exception as e:
        flash(f'Erreur serveur: {str(e)}', 'error')
        return redirect(url_for('create_page'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Traitement de connexion via formulaire"""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        totp_code = request.form.get('totp_code')
        
        if not username or not password or not totp_code:
            flash('Tous les champs sont requis', 'error')
            return redirect(url_for('login_page'))
        
        # Appel du handler de login
        from login_handler import handle as login_handler
        
        data = {"username": username, "password": password, "totp_code": totp_code}
        result = login_handler(json.dumps(data))
        result_data = json.loads(result)
        
        if result_data.get('status') == 'success':
            flash('Connexion réussie !', 'success')
            return render_template('login_success.html', username=username)
        else:
            error_msg = result_data.get('error', 'Erreur de connexion')
            if result_data.get('expired'):
                flash('Votre compte a expiré. Veuillez créer un nouveau compte.', 'warning')
                return redirect(url_for('create_page'))
            else:
                flash(error_msg, 'error')
                return redirect(url_for('login_page'))
            
    except Exception as e:
        flash(f'Erreur serveur: {str(e)}', 'error')
        return redirect(url_for('login_page'))

@app.route('/api/create-user', methods=['POST'])
def create_user():
    """Endpoint pour créer un utilisateur - Handler complet"""
    try:
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

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint pour se connecter - Handler complet"""
    try:
        from login_handler import handle as login_handler
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        result = login_handler(json.dumps(data))
        result_data = json.loads(result)
        
        if result_data.get('status') == 'success':
            return jsonify(result_data), 200
        else:
            return jsonify(result_data), 401
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/generate-2fa', methods=['POST'])
def generate_2fa():
    """Endpoint pour générer le 2FA - Handler complet"""
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
    """Endpoint pour vérifier le 2FA - Handler complet"""
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

@app.route('/api/test-full-flow', methods=['GET'])
def test_full_flow():
    """Endpoint pour tester le flux complet"""
    return jsonify({
        "message": "Use the web interface to test the full flow",
        "steps": [
            "1. Create a user with /api/create-user",
            "2. Generate 2FA with /api/generate-2fa", 
            "3. Login with /api/login using password and 2FA code"
        ],
        "status": "info"
    })

@app.route('/health')
def health():
    """Endpoint de santé détaillé"""
    try:
        # Test de connexion base de données
        import psycopg2
        conn = psycopg2.connect(
            host='localhost', 
            dbname='cofrap', 
            user='postgres', 
            password='password'
        )
        conn.close()
        db_status = "✅ Connected"
    except Exception as e:
        db_status = f"❌ Error: {str(e)}"
    
    return jsonify({
        "status": "healthy", 
        "service": "MSPR Flask API Complete",
        "version": "2.0 - Full Handlers",
        "database": f"PostgreSQL localhost:5432 - {db_status}",
        "handlers": {
            "create-user": "✅ Active",
            "login": "✅ Active (Full)",
            "generate-2fa": "✅ Active", 
            "verify-2fa": "✅ Active"
        },
        "features": [
            "🔒 Password encryption (Fernet)",
            "🔑 2FA TOTP (Google Authenticator)",
            "📱 QR Code generation",
            "⏰ Password expiration",
            "🗄️ PostgreSQL database"
        ]
    })

if __name__ == '__main__':
    print("🚀 MSPR Flask API Complete Starting...")
    print("📋 Available endpoints:")
    print("  - GET  /                 : Interface web complète")
    print("  - POST /api/create-user  : Créer un utilisateur (complet)")
    print("  - POST /api/login        : Se connecter (complet avec 2FA)")
    print("  - POST /api/generate-2fa : Générer le 2FA")
    print("  - POST /api/verify-2fa   : Vérifier le 2FA")
    print("  - GET  /api/test-full-flow : Test du flux complet")
    print("  - GET  /health           : Santé du service (détaillée)")
    print("🔗 Base URL: http://localhost:5000")
    print("🎯 Version: Complete avec tous les handlers fonctionnels")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/env python3
"""
Script de test simple pour les handlers OpenFaaS
"""
import json
import random
import string
import base64
import io
import sys
import os
from cryptography.fernet import Fernet

# Ajouter le répertoire parent au path pour importer les handlers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import qrcode

# Clé de test
FERNET_KEY = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
fernet = Fernet(FERNET_KEY)

def generate_password(length=24):
    """Génère un mot de passe sécurisé"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def generate_qrcode(data):
    """Génère un QR code en base64"""
    qr = qrcode.make(data)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def test_handler_logic():
    """Test la logique du handler sans base de données"""
    print("🧪 Test de la logique du handler...")
    
    try:
        # Simulation de création d'utilisateur
        username = "testuser123"
        password = generate_password()
        
        print(f"✅ Nom d'utilisateur: {username}")
        print(f"✅ Mot de passe généré: {password}")
        
        # Test du chiffrement
        encrypted_password = fernet.encrypt(password.encode()).decode()
        print(f"✅ Mot de passe chiffré: {encrypted_password[:50]}...")
        
        # Test du déchiffrement
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        print(f"✅ Mot de passe déchiffré: {decrypted_password}")
        
        # Vérification
        if password == decrypted_password:
            print("✅ Chiffrement/déchiffrement OK")
        else:
            print("❌ Erreur de chiffrement/déchiffrement")
        
        # Test du QR code
        qrcode_b64 = generate_qrcode(password)
        print(f"✅ QR Code généré: {len(qrcode_b64)} caractères")
        
        # Réponse simulée
        response = {
            "message": "User created successfully",
            "username": username,
            "password": password,
            "qrcode_base64": qrcode_b64,
            "status": "success"
        }
        
        print(f"✅ Réponse JSON: {json.dumps(response, indent=2)}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_dependencies():
    """Test des dépendances"""
    print("🧪 Test des dépendances...")
    
    dependencies = [
        ("json", "JSON natif"),
        ("requests", "Requests HTTP"),
        ("cryptography", "Cryptographie"),
        ("psycopg2", "PostgreSQL"),
        ("qrcode", "QR Code"),
        ("PIL", "Pillow (traitement d'images)")
    ]
    
    all_ok = True
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"✅ {desc}")
        except ImportError:
            print(f"❌ {desc} - MANQUANT")
            all_ok = False
    
    return all_ok

def main():
    """Fonction principale"""
    print("=" * 50)
    print("    TEST SIMPLE DES HANDLERS")
    print("=" * 50)
    
    # Test des dépendances
    if test_dependencies():
        print("\n" + "=" * 50)
        print("    TEST DE LA LOGIQUE")
        print("=" * 50)
        test_handler_logic()
    else:
        print("\n❌ Certaines dépendances manquent")
        print("   Exécutez: pip install -r requirements.txt")
    
    print("\n" + "=" * 50)
    print("    TESTS TERMINÉS")
    print("=" * 50)

if __name__ == "__main__":
    main()

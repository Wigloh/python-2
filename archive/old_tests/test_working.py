#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simplifié qui fonctionne vraiment - sans emojis
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test des imports"""
    print("=== Test des imports ===")
    
    try:
        import handler
        print("OK Import handler.py")
        
        import login_handler
        print("OK Import login_handler.py")
        
        import generate_2fa_handler
        print("OK Import generate_2fa_handler.py")
        
        return True
    except Exception as e:
        print(f"ERREUR Import: {e}")
        return False

def test_dependencies():
    """Test des dépendances"""
    print("\n=== Test des dépendances ===")
    
    dependencies = [
        ("JSON", "json"),
        ("Cryptographie", "cryptography"),
        ("QR Code", "qrcode"),
        ("PyOTP", "pyotp"),
        ("PostgreSQL", "psycopg2"),
        ("Pillow", "PIL")
    ]
    
    all_good = True
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"OK {name}")
        except ImportError as e:
            print(f"ERREUR {name}: {e}")
            all_good = False
    
    return all_good

def test_crypto():
    """Test du chiffrement"""
    print("\n=== Test du chiffrement ===")
    
    try:
        from cryptography.fernet import Fernet
        
        # Clé de test
        key = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
        fernet = Fernet(key)
        
        # Test chiffrement/déchiffrement
        data = "test_password"
        encrypted = fernet.encrypt(data.encode())
        decrypted = fernet.decrypt(encrypted).decode()
        
        if data == decrypted:
            print("OK Chiffrement/Déchiffrement")
            return True
        else:
            print("ERREUR Chiffrement/Déchiffrement")
            return False
            
    except Exception as e:
        print(f"ERREUR Crypto: {e}")
        return False

def test_totp():
    """Test TOTP"""
    print("\n=== Test TOTP ===")
    
    try:
        import pyotp
        
        # Générer un secret
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        
        # Générer un code
        code = totp.now()
        
        if code and len(code) == 6:
            print("OK TOTP généré")
            return True
        else:
            print("ERREUR TOTP")
            return False
            
    except Exception as e:
        print(f"ERREUR TOTP: {e}")
        return False

def test_qrcode():
    """Test QR Code"""
    print("\n=== Test QR Code ===")
    
    try:
        import qrcode
        import io
        import base64
        
        # Générer un QR code
        qr = qrcode.make("test_data")
        buffered = io.BytesIO()
        qr.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        if qr_base64 and len(qr_base64) > 100:
            print("OK QR Code généré")
            return True
        else:
            print("ERREUR QR Code")
            return False
            
    except Exception as e:
        print(f"ERREUR QR Code: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("    TEST SYSTÈME MSPR - VERSION SIMPLIFIÉE")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Dépendances", test_dependencies),
        ("Chiffrement", test_crypto),
        ("TOTP", test_totp),
        ("QR Code", test_qrcode)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
    
    # Résultats
    print("\n" + "=" * 60)
    print(f"RÉSULTATS: {passed}/{total} tests réussis ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("STATUT: TOUS LES TESTS RÉUSSIS [OK]")
        return True
    else:
        print("STATUT: CORRECTIONS NÉCESSAIRES")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

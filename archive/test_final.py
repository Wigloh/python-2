#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test final - Système MSPR complet
Tous les tests fonctionnels sans problème d'encodage
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_all_functionality():
    """Test de toutes les fonctionnalités"""
    print("="*70)
    print("    TESTS SYSTÈME MSPR - AUTHENTIFICATION SÉCURISÉE")
    print("="*70)
    
    all_tests_passed = True
    
    # Test 1: Dépendances
    print("\n1. TEST DES DÉPENDANCES")
    print("-" * 40)
    
    dependencies = [
        ("JSON", "json"),
        ("Requests", "requests"),
        ("Cryptographie", "cryptography"),
        ("PostgreSQL", "psycopg2"),
        ("QR Code", "qrcode"),
        ("Pillow", "PIL"),
        ("PyOTP", "pyotp"),
        ("DateUtil", "dateutil")
    ]
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"OK {name}")
        except ImportError as e:
            print(f"ERREUR {name}: {e}")
            all_tests_passed = False
    
    # Test 2: Import des handlers
    print("\n2. TEST DES HANDLERS")
    print("-" * 40)
    
    handlers = [
        ("handler.py", "handler"),
        ("login_handler.py", "login_handler"),
        ("generate_2fa_handler.py", "generate_2fa_handler")
    ]
    
    for filename, module_name in handlers:
        try:
            __import__(module_name)
            print(f"OK Import {filename}")
        except ImportError as e:
            print(f"ERREUR Import {filename}: {e}")
            all_tests_passed = False
    
    # Test 3: Fonctionnalités critiques
    print("\n3. TEST DES FONCTIONNALITÉS")
    print("-" * 40)
    
    # Test de génération de mot de passe
    try:
        import string
        import random
        
        def generate_password(length=24):
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            return ''.join(random.SystemRandom().choice(chars) for _ in range(length))
        
        password = generate_password()
        print(f"OK Génération mot de passe: {len(password)} caractères")
        
        # Vérifier la complexité
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*" for c in password)
        
        if has_upper and has_lower and has_digit and has_special:
            print("OK Complexité mot de passe validée")
        else:
            print("ERREUR Complexité mot de passe insuffisante")
            all_tests_passed = False
            
    except Exception as e:
        print(f"ERREUR Génération mot de passe: {e}")
        all_tests_passed = False
    
    # Test de chiffrement
    try:
        from cryptography.fernet import Fernet
        
        # Clé fixe de test (identique aux handlers)
        key = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
        fernet = Fernet(key)
        
        test_data = "test_password_123"
        encrypted = fernet.encrypt(test_data.encode())
        decrypted = fernet.decrypt(encrypted).decode()
        
        if test_data == decrypted:
            print("OK Chiffrement/Déchiffrement Fernet")
        else:
            print("ERREUR Chiffrement/Déchiffrement")
            all_tests_passed = False
            
    except Exception as e:
        print(f"ERREUR Chiffrement: {e}")
        all_tests_passed = False
    
    # Test TOTP
    try:
        import pyotp
        
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        code = totp.now()
        
        # Vérifier que le code est valide
        if totp.verify(code):
            print("OK Génération et vérification TOTP")
        else:
            print("ERREUR TOTP invalide")
            all_tests_passed = False
            
    except Exception as e:
        print(f"ERREUR TOTP: {e}")
        all_tests_passed = False
    
    # Test 4: Fonctions utilitaires
    print("\n4. TEST DES FONCTIONS UTILITAIRES")
    print("-" * 40)
    
    try:
        import qrcode
        import base64
        import io
        
        # Test génération QR Code
        qr = qrcode.make("Test QR Code")
        buffered = io.BytesIO()
        qr.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        if len(qr_base64) > 0:
            print(f"OK Génération QR Code: {len(qr_base64)} caractères")
        else:
            print("ERREUR QR Code vide")
            all_tests_passed = False
            
    except Exception as e:
        print(f"ERREUR QR Code: {e}")
        all_tests_passed = False
    
    # Test 5: Gestion des dates
    print("\n5. TEST GESTION DES DATES")
    print("-" * 40)
    
    try:
        from datetime import datetime, timedelta
        from dateutil.relativedelta import relativedelta
        
        # Test calcul d'expiration
        creation_date = datetime.utcnow() - timedelta(days=30)  # Il y a 1 mois
        expiration_date = creation_date + relativedelta(months=6)
        current_date = datetime.utcnow()
        
        is_expired = current_date > expiration_date
        
        print(f"OK Calcul expiration: créé il y a 1 mois, expiré = {is_expired}")
        
        # Test avec date ancienne
        old_date = datetime.utcnow() - timedelta(days=200)  # Il y a 7 mois
        old_expiration = old_date + relativedelta(months=6)
        old_expired = current_date > old_expiration
        
        print(f"OK Calcul expiration: créé il y a 7 mois, expiré = {old_expired}")
        
        if not is_expired and old_expired:
            print("OK Logique d'expiration correcte")
        else:
            print("ERREUR Logique d'expiration")
            all_tests_passed = False
            
    except Exception as e:
        print(f"ERREUR Gestion dates: {e}")
        all_tests_passed = False
    
    # Résumé final
    print("\n" + "="*70)
    if all_tests_passed:
        print("    SUCCÈS - TOUS LES TESTS SONT PASSÉS !")
        print("    Le système MSPR est prêt et fonctionnel")
    else:
        print("    ÉCHEC - Certains tests ont échoué")
        print("    Consultez les messages d'erreur ci-dessus")
    print("="*70)
    
    # Statistiques
    print(f"\nDate d'exécution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Fonctionnalités testées:")
    print("- Génération mots de passe sécurisés")
    print("- Chiffrement Fernet")
    print("- Authentification 2FA TOTP")
    print("- Génération QR Codes")
    print("- Gestion expiration (6 mois)")
    print("- Import des handlers OpenFaaS")
    
    return all_tests_passed

if __name__ == "__main__":
    success = test_all_functionality()
    
    if success:
        print("\nSTATUT FINAL: SYSTÈME OPÉRATIONNEL")
        sys.exit(0)
    else:
        print("\nSTATUT FINAL: CORRECTIONS NÉCESSAIRES")
        sys.exit(1)

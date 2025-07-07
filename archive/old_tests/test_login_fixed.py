#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de login simple et fonctionnel sans emojis pour Windows
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock des dépendances pour les tests
import unittest.mock as mock
from datetime import datetime, timedelta

def test_login_handler_simple():
    """Test simplifié du handler de login"""
    print("=== Test simplifié du handler de login ===")
    
    # Mock des dépendances
    with mock.patch('psycopg2.connect') as mock_connect:
        with mock.patch('pyotp.TOTP') as mock_totp:
            with mock.patch('cryptography.fernet.Fernet') as mock_fernet:
                
                # Configuration des mocks
                mock_conn = mock.Mock()
                mock_cur = mock.Mock()
                mock_connect.return_value = mock_conn
                mock_conn.cursor.return_value = mock_cur
                
                # Mock d'un utilisateur valide
                mock_user_data = (
                    'testuser',
                    'encrypted_password',
                    'encrypted_2fa_secret',
                    datetime.utcnow(),
                    False
                )
                mock_cur.fetchone.return_value = mock_user_data
                
                # Mock du déchiffrement
                mock_fernet_instance = mock.Mock()
                mock_fernet.return_value = mock_fernet_instance
                mock_fernet_instance.decrypt.side_effect = [
                    b'testpassword',  # Mot de passe déchiffré
                    b'JBSWY3DPEHPK3PXP'  # Secret 2FA déchiffré
                ]
                
                # Mock de la vérification TOTP
                mock_totp_instance = mock.Mock()
                mock_totp.return_value = mock_totp_instance
                mock_totp_instance.verify.return_value = True
                
                # Import du handler après avoir configuré les mocks
                try:
                    import login_handler
                except ImportError:
                    print("ERREUR: Impossible d'importer login_handler")
                    return False
                
                # Test 1: Login réussi
                print("Test 1: Login réussi")
                request_data = {
                    'username': 'testuser',
                    'password': 'testpassword',
                    'totp_code': '123456'
                }
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'success'
                assert 'Login successful' in result['message']
                print("OK Test 1 réussi")
                
                # Test 2: Paramètres manquants
                print("\nTest 2: Paramètres manquants")
                request_data = {
                    'username': 'testuser',
                    'password': 'testpassword'
                    # totp_code manquant
                }
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'error'
                assert 'required' in result['error']
                print("OK Test 2 réussi")
                
                # Test 3: Utilisateur inexistant
                print("\nTest 3: Utilisateur inexistant")
                mock_cur.fetchone.return_value = None
                
                request_data = {
                    'username': 'nonexistent',
                    'password': 'testpassword',
                    'totp_code': '123456'
                }
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'error'
                assert 'Invalid credentials' in result['error']
                print("OK Test 3 réussi")
                
                # Test 4: Utilisateur déjà expiré
                print("\nTest 4: Utilisateur déjà expiré")
                mock_user_data_expired = (
                    'testuser',
                    'encrypted_password',
                    'encrypted_2fa_secret',
                    datetime.utcnow(),
                    True  # expired = True
                )
                mock_cur.fetchone.return_value = mock_user_data_expired
                
                request_data = {
                    'username': 'testuser',
                    'password': 'testpassword',
                    'totp_code': '123456'
                }
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'error'
                assert 'expired' in result['error']
                print("OK Test 4 réussi")
                
                # Test 5: Mauvais mot de passe
                print("\nTest 5: Mauvais mot de passe")
                mock_cur.fetchone.return_value = mock_user_data  # Utilisateur valide
                
                request_data = {
                    'username': 'testuser',
                    'password': 'wrongpassword',
                    'totp_code': '123456'
                }
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'error'
                assert 'Invalid credentials' in result['error']
                print("OK Test 5 réussi")
                
                # Test 6: Mauvais code TOTP
                print("\nTest 6: Mauvais code TOTP")
                mock_totp_instance.verify.return_value = False
                
                request_data = {
                    'username': 'testuser',
                    'password': 'testpassword',
                    'totp_code': '000000'
                }
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'error'
                assert 'Invalid TOTP code' in result['error']
                print("OK Test 6 réussi")
                
                # Test 7: JSON invalide
                print("\nTest 7: JSON invalide")
                response = login_handler.handle("invalid json")
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'error'
                assert 'Invalid JSON format' in result['error']
                print("OK Test 7 réussi")
                
                print("\n=== Tous les tests du handler de login sont réussis ! ===")
                return True

def test_password_expiration_function():
    """Test de la fonction check_password_expiration"""
    print("=== Test de la fonction check_password_expiration ===")
    
    try:
        import login_handler
    except ImportError:
        print("ERREUR: Impossible d'importer login_handler")
        return False
    
    # Test 1: Date récente (30 jours)
    print("Test 1: Date récente (30 jours)")
    recent_date = datetime.utcnow() - timedelta(days=30)
    is_expired = login_handler.check_password_expiration(recent_date)
    print(f"Date de création: {recent_date}")
    print(f"Expiré attendu: False, obtenu: {is_expired}")
    
    # Test 2: Date ancienne (200 jours)
    print("Test 2: Date ancienne (200 jours)")
    old_date = datetime.utcnow() - timedelta(days=200)
    is_expired = login_handler.check_password_expiration(old_date)
    print(f"Date de création: {old_date}")
    print(f"Expiré attendu: True, obtenu: {is_expired}")
    
    # Test 3: Date None
    print("Test 3: Date None")
    is_expired = login_handler.check_password_expiration(None)
    print(f"Date None: expiré = {is_expired}")
    assert is_expired == True
    print("OK Test 3 réussi")
    
    print("=== Tests d'expiration terminés ===")
    return True

if __name__ == "__main__":
    print("Début des tests de login...")
    
    try:
        success1 = test_login_handler_simple()
        success2 = test_password_expiration_function()
        
        if success1 and success2:
            print("\nTOUS LES TESTS RÉUSSIS !")
            sys.exit(0)
        else:
            print("\nCERTAINS TESTS ONT ÉCHOUÉ")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nERREUR pendant les tests: {e}")
        sys.exit(1)

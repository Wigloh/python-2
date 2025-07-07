import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock des dépendances pour les tests
import unittest.mock as mock

# Test du handler de login
def test_login_handler():
    print("=== Test du handler de login ===")
    
    # Mock des dépendances
    with mock.patch('psycopg2.connect') as mock_connect:
        with mock.patch('pyotp.TOTP') as mock_totp:
            with mock.patch('cryptography.fernet.Fernet') as mock_fernet:
                with mock.patch('dateutil.relativedelta.relativedelta') as mock_relativedelta:
                    
                    # Configuration des mocks
                    mock_conn = mock.Mock()
                    mock_cur = mock.Mock()
                    mock_connect.return_value = mock_conn
                    mock_conn.cursor.return_value = mock_cur
                    
                    # Mock d'un utilisateur valide
                    from datetime import datetime
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
                    
                    # Mock de relativedelta pour calculer l'expiration
                    mock_relativedelta.return_value = mock.Mock()
                    
                    # Import du handler après avoir configuré les mocks
                    import login_handler
                    
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
                    print("✓ Test 1 réussi")
                    
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
                    print("✓ Test 2 réussi")
                    
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
                    print("✓ Test 3 réussi")
                    
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
                    print("✓ Test 4 réussi")
                    
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
                    print("✓ Test 5 réussi")
                    
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
                    print("✓ Test 6 réussi")
                    
                    # Test 7: JSON invalide
                    print("\nTest 7: JSON invalide")
                    response = login_handler.handle("invalid json")
                    result = json.loads(response)
                    
                    print(f"Résultat: {result}")
                    assert result['status'] == 'error'
                    assert 'Invalid JSON format' in result['error']
                    print("✓ Test 7 réussi")
                    
                    print("\n=== Tous les tests du handler de login sont réussis ! ===")

if __name__ == "__main__":
    test_login_handler()

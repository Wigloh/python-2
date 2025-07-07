#!/usr/bin/env python3
"""
Script de test complet pour la fonction login-user avec gestion d'expiration
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock des dépendances pour les tests
import unittest.mock as mock
from datetime import datetime, timedelta

# Test complet avec gestion d'expiration
def test_login_with_expiration():
    print("=== Test complet avec gestion d'expiration ===")
    
    # Mock des dépendances
    with mock.patch('psycopg2.connect') as mock_connect:
        with mock.patch('pyotp.TOTP') as mock_totp:
            with mock.patch('cryptography.fernet.Fernet') as mock_fernet:
                
                # Configuration des mocks
                mock_conn = mock.Mock()
                mock_cur = mock.Mock()
                mock_connect.return_value = mock_conn
                mock_conn.cursor.return_value = mock_cur
                
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
                import login_handler
                
                # Test 1: Mot de passe expiré (7 mois)
                print("Test 1: Mot de passe expiré (7 mois)")
                
                # Simuler un utilisateur avec un mot de passe créé il y a 7 mois
                old_date = datetime.utcnow() - timedelta(days=210)  # 7 mois
                mock_user_data_expired = (
                    'testuser',
                    'encrypted_password',
                    'encrypted_2fa_secret',
                    old_date,
                    False  # pas encore marqué comme expiré
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
                assert result.get('expired') == True
                print("✓ Test 1 réussi - Mot de passe expiré détecté")
                
                # Vérifier que l'utilisateur a été marqué comme expiré
                # La méthode execute devrait avoir été appelée pour faire l'UPDATE
                update_calls = [call for call in mock_cur.execute.call_args_list if 'UPDATE' in str(call)]
                assert len(update_calls) > 0
                print("✓ Utilisateur marqué comme expiré en base")
                
                # Test 2: Mot de passe récent (2 mois)
                print("\nTest 2: Mot de passe récent (2 mois)")
                
                # Reset des mocks
                mock_cur.reset_mock()
                mock_fernet_instance.decrypt.side_effect = [
                    b'testpassword',  # Mot de passe déchiffré
                    b'JBSWY3DPEHPK3PXP'  # Secret 2FA déchiffré
                ]
                
                # Simuler un utilisateur avec un mot de passe créé il y a 2 mois
                recent_date = datetime.utcnow() - timedelta(days=60)  # 2 mois
                mock_user_data_recent = (
                    'testuser',
                    'encrypted_password',
                    'encrypted_2fa_secret',
                    recent_date,
                    False
                )
                mock_cur.fetchone.return_value = mock_user_data_recent
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                assert result['status'] == 'success'
                assert 'Login successful' in result['message']
                assert 'password_expires_in_days' in result
                assert result['password_expires_in_days'] > 0
                print("✓ Test 2 réussi - Login autorisé pour mot de passe récent")
                
                # Test 3: Mot de passe à la limite (exactement 6 mois)
                print("\nTest 3: Mot de passe à la limite (exactement 6 mois)")
                
                # Reset des mocks
                mock_cur.reset_mock()
                mock_fernet_instance.decrypt.side_effect = [
                    b'testpassword',  # Mot de passe déchiffré
                    b'JBSWY3DPEHPK3PXP'  # Secret 2FA déchiffré
                ]
                
                # Simuler un utilisateur avec un mot de passe créé il y a exactement 6 mois
                limit_date = datetime.utcnow() - timedelta(days=180)  # 6 mois
                mock_user_data_limit = (
                    'testuser',
                    'encrypted_password',
                    'encrypted_2fa_secret',
                    limit_date,
                    False
                )
                mock_cur.fetchone.return_value = mock_user_data_limit
                
                response = login_handler.handle(json.dumps(request_data))
                result = json.loads(response)
                
                print(f"Résultat: {result}")
                # À la limite, cela dépend de l'implémentation exacte
                # Mais généralement, 6 mois exacts pourraient être considérés comme expirés
                if result['status'] == 'error':
                    assert 'expired' in result['error']
                    print("✓ Test 3 réussi - Mot de passe à la limite considéré comme expiré")
                else:
                    assert result['status'] == 'success'
                    assert result['password_expires_in_days'] <= 1
                    print("✓ Test 3 réussi - Mot de passe à la limite encore valide")
                
                print("\n=== Test complet d'expiration terminé avec succès ! ===")

if __name__ == "__main__":
    test_login_with_expiration()

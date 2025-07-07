import json
import psycopg2
import pyotp
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dateutil.relativedelta import relativedelta

# Fonction pour obtenir la clé de chiffrement
def get_encryption_key():
    """
    Récupère la clé de chiffrement depuis les variables d'environnement
    ou utilise une clé par défaut pour le développement
    """
    env_key = os.environ.get('FERNET_KEY')
    if env_key:
        return env_key.encode()
    else:
        # Clé par défaut pour le développement - CHANGEZ EN PRODUCTION !
        return b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

# Clé de chiffrement FIXE (à sécuriser via un secret Kubernetes en production)
# ATTENTION : Cette clé doit être la même pour tous les appels !
FERNET_KEY = get_encryption_key()
fernet = Fernet(FERNET_KEY)

# Configuration base de données
DB_HOST = "postgres"  # nom du service dans le cluster ou "localhost"
DB_NAME = "cofrap"
DB_USER = "postgres"
DB_PASSWORD = "password"

def get_user_by_username(username):
    """Récupère un utilisateur par son nom d'utilisateur"""
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT username, password, secret_2fa, gendate, expired
        FROM users
        WHERE username = %s
    """, (username,))
    
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        return {
            'username': user[0],
            'password': user[1],
            'secret_2fa': user[2],
            'gendate': user[3],
            'expired': user[4]
        }
    return None

def check_password_expiration(gendate):
    """Vérifie si le mot de passe a expiré (6 mois)"""
    if not gendate:
        return True  # Considérer comme expiré si pas de date
    
    # Calculer la date d'expiration (6 mois après la génération)
    expiration_date = gendate + relativedelta(months=6)
    current_date = datetime.utcnow()
    
    return current_date > expiration_date

def verify_totp_code(secret, code):
    """Vérifie un code TOTP"""
    try:
        totp = pyotp.TOTP(secret)
        # Vérifier le code avec une tolérance de 30 secondes
        return totp.verify(code, valid_window=1)
    except Exception:
        return False

def mark_user_as_expired(username):
    """Marque un utilisateur comme expiré dans la base de données"""
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        UPDATE users 
        SET expired = %s
        WHERE username = %s
    """, (True, username))
    conn.commit()
    cur.close()
    conn.close()

def handle(req):
    try:
        # Extraction des paramètres
        body = json.loads(req)
        username = body.get('username')
        password = body.get('password')
        totp_code = body.get('totp_code')

        # Vérification des paramètres requis
        if not username or not password or not totp_code:
            return json.dumps({
                "error": "Username, password, and TOTP code are required",
                "status": "error"
            })

        # Récupération de l'utilisateur
        user = get_user_by_username(username)
        if not user:
            return json.dumps({
                "error": "Invalid credentials",
                "status": "error"
            })

        # Vérification si l'utilisateur est déjà marqué comme expiré
        if user['expired']:
            return json.dumps({
                "error": "User account has expired. Please contact administrator.",
                "status": "error"
            })

        # Vérification de l'expiration du mot de passe
        if check_password_expiration(user['gendate']):
            # Marquer l'utilisateur comme expiré
            mark_user_as_expired(username)
            return json.dumps({
                "error": "Password has expired (6 months). Please contact administrator for renewal.",
                "status": "error",
                "expired": True
            })

        # Déchiffrement du mot de passe stocké
        try:
            decrypted_password = fernet.decrypt(user['password'].encode()).decode()
        except Exception:
            return json.dumps({
                "error": "Error decrypting password",
                "status": "error"
            })

        # Vérification du mot de passe
        if password != decrypted_password:
            return json.dumps({
                "error": "Invalid credentials",
                "status": "error"
            })

        # Déchiffrement du secret 2FA
        try:
            decrypted_2fa_secret = fernet.decrypt(user['secret_2fa'].encode()).decode()
        except Exception:
            return json.dumps({
                "error": "Error decrypting 2FA secret",
                "status": "error"
            })

        # Vérification du code TOTP
        if not verify_totp_code(decrypted_2fa_secret, totp_code):
            return json.dumps({
                "error": "Invalid TOTP code",
                "status": "error"
            })

        # Authentification réussie
        days_until_expiry = (user['gendate'] + relativedelta(months=6) - datetime.utcnow()).days
        
        response = {
            "message": "Login successful",
            "username": username,
            "login_time": datetime.utcnow().isoformat(),
            "password_expires_in_days": max(0, days_until_expiry),
            "status": "success"
        }

        return json.dumps(response)

    except psycopg2.Error as db_error:
        # Erreur de base de données
        error_response = {
            "error": f"Database error: {str(db_error)}",
            "status": "error"
        }
        return json.dumps(error_response)
    
    except json.JSONDecodeError:
        # Erreur de parsing JSON
        error_response = {
            "error": "Invalid JSON format",
            "status": "error"
        }
        return json.dumps(error_response)
    
    except Exception as e:
        # Autres erreurs
        error_response = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }
        return json.dumps(error_response)

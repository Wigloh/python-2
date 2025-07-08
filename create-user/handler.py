import json
import random
import string
import psycopg2
import qrcode
import base64
import io
import os
import pyotp
from datetime import datetime
from cryptography.fernet import Fernet

# Fonction pour obtenir la clé de chiffrement
def get_encryption_key():
    """
    Clé de chiffrement fixe pour le projet MSPR
    """
    # Clé fixe pour le projet - MÊME CLÉ POUR TOUS LES HANDLERS !
    return b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

# Clé de chiffrement FIXE (identique pour tous les handlers)
FERNET_KEY = get_encryption_key()
fernet = Fernet(FERNET_KEY)

# Configuration base de données - VALEURS FIXES POUR LE PROJET
DB_HOST = 'localhost'        # PostgreSQL Docker sur localhost
DB_NAME = 'cofrap'          # Nom de la base de données
DB_USER = 'postgres'        # Utilisateur PostgreSQL
DB_PASSWORD = 'mspr2024'    # Mot de passe PostgreSQL Docker

def generate_password(length=24):
    # Utiliser seulement des caractères ASCII sûrs
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def generate_qrcode(data):
    qr = qrcode.make(data)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def insert_user(username, encrypted_password, encrypted_2fa_secret, gendate):
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, password, secret_2fa, gendate, expired)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, encrypted_password, encrypted_2fa_secret, gendate, False))
    conn.commit()
    cur.close()
    conn.close()

# Configuration 2FA
APP_NAME = "MSPR App"  # Nom de votre application
ISSUER_NAME = "MSPR Security"  # Nom de votre organisation

def generate_totp_secret():
    """Génère un secret TOTP aléatoire"""
    return pyotp.random_base32()

def generate_totp_qr_code(username, secret):
    """Génère un QR Code pour TOTP (Google Authenticator)"""
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name=ISSUER_NAME
    )
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    qr_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def handle(req):
    try:
        # Extraction des paramètres
        body = json.loads(req)
        username = body.get('username')

        if not username:
            return json.dumps({
                "error": "Username is required",
                "status": "error"
            })

        # Génération du mot de passe
        password = generate_password()
        encrypted_password = fernet.encrypt(password.encode()).decode()

        # Génération du secret 2FA
        totp_secret = generate_totp_secret()
        encrypted_2fa_secret = fernet.encrypt(totp_secret.encode()).decode()

        # Génération du QR Code pour le mot de passe (pour info)
        password_qr = generate_qrcode(f"Password: {password}")
        
        # Génération du QR Code pour le 2FA (Google Authenticator)
        totp_qr = generate_totp_qr_code(username, totp_secret)

        # Insertion en base de données
        gendate = datetime.utcnow()
        insert_user(username, encrypted_password, encrypted_2fa_secret, gendate)

        response = {
            "message": "User created successfully",
            "username": username,
            "password": password,
            "password_qr_code": password_qr,
            "totp_secret": totp_secret,  # À supprimer en production
            "totp_qr_code": totp_qr,
            "instructions": {
                "step1": "Save your password securely",
                "step2": "Scan the TOTP QR code with Google Authenticator",
                "step3": "Use both password and 2FA code to login"
            },
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

import json
import pyotp
import qrcode
import base64
import io
import os
import psycopg2
from datetime import datetime
from cryptography.fernet import Fernet

# Fonction pour obtenir la clé de chiffrement (identique aux autres handlers)
def get_encryption_key():
    """
    Récupère la clé de chiffrement depuis les variables d'environnement
    ou utilise une clé par défaut pour le développement
    
    🔧 DÉPLOIEMENT: Configuration de la clé de chiffrement
    """
    env_key = os.environ.get('FERNET_KEY')
    if env_key:
        return env_key.encode()
    else:
        # 📝 DÉVELOPPEMENT: Clé par défaut - DOIT ÊTRE LA MÊME dans tous les handlers !
        # 📝 PRODUCTION: Supprimer cette ligne et utiliser UNIQUEMENT la variable d'environnement
        # 📝 KUBERNETES: Définir FERNET_KEY comme Secret dans le cluster
        return b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

# Clé de chiffrement FIXE (identique aux autres handlers)
FERNET_KEY = get_encryption_key()
fernet = Fernet(FERNET_KEY)

# Configuration base de données (identique aux autres handlers)
# 🔧 DÉPLOIEMENT: Modifier ces valeurs pour votre environnement
DB_HOST = "localhost"  # 📝 Pour tests avec Docker PostgreSQL local
DB_NAME = "cofrap"    # 📝 PRODUCTION: Nom de votre base de données
DB_USER = "postgres"  # 📝 PRODUCTION: Utilisateur PostgreSQL (utiliser les secrets K8s)
DB_PASSWORD = "password"  # 📝 PRODUCTION: Mot de passe PostgreSQL (utiliser les secrets K8s)

# Configuration 2FA
# 🔧 DÉPLOIEMENT: Personnaliser ces valeurs pour votre organisation
APP_NAME = "MSPR App"  # 📝 PRODUCTION: Nom de votre application (affiché dans Google Authenticator)
ISSUER_NAME = "MSPR Security"  # 📝 PRODUCTION: Nom de votre organisation (affiché dans Google Authenticator)

def generate_totp_secret():
    """
    Génère un secret TOTP aléatoire
    """
    return pyotp.random_base32()

def generate_totp_qr_code(username, secret):
    """
    Génère un QR Code pour TOTP (Google Authenticator)
    """
    # Créer l'URI TOTP selon les spécifications
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name=ISSUER_NAME
    )
    
    # Générer le QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    # Convertir en image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir en base64
    buffered = io.BytesIO()
    qr_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def verify_totp_code(secret, code):
    """
    Vérifie un code TOTP
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

def get_user_from_db(username):
    """
    Récupère un utilisateur depuis la base de données
    
    🔧 DÉPLOIEMENT: Configuration de la connexion base de données
    """
    # 📝 KUBERNETES: Utiliser les services et secrets du cluster
    # 📝 PRODUCTION: Ajouter la gestion des pools de connexions
    conn = psycopg2.connect(
        host=DB_HOST, 
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, password, secret_2fa, gendate, expired
        FROM users WHERE username = %s
    """, (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def update_user_2fa(username, encrypted_secret):
    """
    Met à jour le secret 2FA d'un utilisateur
    
    🔧 DÉPLOIEMENT: Configuration de la connexion base de données
    """
    # 📝 KUBERNETES: Utiliser les services et secrets du cluster
    # 📝 PRODUCTION: Ajouter la gestion des pools de connexions
    conn = psycopg2.connect(
        host=DB_HOST, 
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        UPDATE users 
        SET secret_2fa = %s, updated_at = %s
        WHERE username = %s
    """, (encrypted_secret, datetime.utcnow(), username))
    conn.commit()
    cur.close()
    conn.close()

def handle(req):
    """
    Handler pour la génération de 2FA
    
    Paramètres attendus:
    - username: nom d'utilisateur
    - code_2fa (optionnel): code pour vérification
    """
    try:
        # Extraction des paramètres
        body = json.loads(req)
        username = body.get('username')
        verification_code = body.get('code_2fa')  # Optionnel pour vérification

        if not username:
            return json.dumps({
                "error": "Username is required",
                "status": "error"
            })

        # Vérifier que l'utilisateur existe
        user_data = get_user_from_db(username)
        if not user_data:
            return json.dumps({
                "error": "User not found",
                "status": "error"
            })

        user_id, db_username, password, existing_secret, gendate, expired = user_data

        # Si un code de vérification est fourni, vérifier le 2FA existant
        if verification_code:
            if not existing_secret:
                return json.dumps({
                    "error": "No 2FA secret found for this user",
                    "status": "error"
                })
            
            try:
                # Déchiffrer le secret existant
                decrypted_secret = fernet.decrypt(existing_secret.encode()).decode()
                
                # Vérifier le code
                if verify_totp_code(decrypted_secret, verification_code):
                    return json.dumps({
                        "message": "2FA code verified successfully",
                        "verified": True,
                        "status": "success"
                    })
                else:
                    return json.dumps({
                        "error": "Invalid 2FA code",
                        "verified": False,
                        "status": "error"
                    })
            except Exception as decrypt_error:
                return json.dumps({
                    "error": "Failed to decrypt 2FA secret",
                    "status": "error"
                })

        # Générer un nouveau secret 2FA
        totp_secret = generate_totp_secret()
        
        # Chiffrer le secret
        encrypted_secret = fernet.encrypt(totp_secret.encode()).decode()
        
        # Générer le QR Code
        qr_code_b64 = generate_totp_qr_code(username, totp_secret)
        
        # Mettre à jour la base de données
        update_user_2fa(username, encrypted_secret)
        
        # Générer un code de test pour vérification
        totp = pyotp.TOTP(totp_secret)
        current_code = totp.now()
        
        response = {
            "message": "2FA setup successful",
            "username": username,
            "qr_code_base64": qr_code_b64,
            "secret": totp_secret,  # 📝 PRODUCTION: SUPPRIMER cette ligne pour la sécurité !
            "test_code": current_code,  # 📝 PRODUCTION: SUPPRIMER cette ligne pour la sécurité !
            "instructions": {
                "step1": "Scan the QR code with Google Authenticator or similar app",
                "step2": "Enter the 6-digit code from your app to verify setup",
                "step3": "Use the verification endpoint with your code"
            },
            # 📝 OPENFAAS: Modifier l'URL selon votre déploiement
            # 📝 KUBERNETES: Utiliser l'URL du service ou ingress
            "verification_url": f"/function/verify-2fa",  # ou "https://your-domain.com/function/verify-2fa"
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

-- 🗃️ Script de création de la base de données MSPR
-- 📝 Exécuter ce script dans PostgreSQL

-- 1. Créer la base de données (si elle n'existe pas)
-- CREATE DATABASE cofrap;

-- 2. Se connecter à la base de données cofrap
-- \c cofrap;

-- 3. Créer la table users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    secret_2fa TEXT,
    gendate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Créer les index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_expired ON users(expired);
CREATE INDEX IF NOT EXISTS idx_users_gendate ON users(gendate);

-- 5. Créer une fonction pour mettre à jour automatiquement updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 6. Créer un trigger pour mettre à jour updated_at automatiquement
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 7. Afficher la structure de la table
\d users;

-- 8. Vérifier que la table est créée
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- 9. Créer un utilisateur de test (optionnel pour les tests)
-- INSERT INTO users (username, password, secret_2fa, expired) 
-- VALUES ('testuser', 'encrypted_password_here', 'encrypted_secret_here', FALSE);

COMMIT;

-- 📝 Commandes utiles pour la maintenance :

-- Voir tous les utilisateurs :
-- SELECT id, username, gendate, expired FROM users;

-- Nettoyer les utilisateurs expirés :
-- DELETE FROM users WHERE expired = TRUE;

-- Mettre à jour un utilisateur comme expiré :
-- UPDATE users SET expired = TRUE WHERE gendate < NOW() - INTERVAL '6 months';

-- Vérifier l'expiration des mots de passe :
-- SELECT 
--     username, 
--     gendate, 
--     (gendate + INTERVAL '6 months') as expires_at,
--     (gendate + INTERVAL '6 months') < NOW() as is_expired
-- FROM users;

COMMIT;

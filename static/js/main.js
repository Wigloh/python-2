/* MSPR - JavaScript pour l'interface d'authentification sécurisée */

let lastGeneratedUser = null;
let lastGeneratedCode = null;

function showResult(title, data, type = 'info') {
    const resultsDiv = document.getElementById('results');
    const resultDiv = document.createElement('div');
    resultDiv.className = 'endpoint ' + (type === 'success' ? 'success' : type === 'error' ? 'error' : '');
    
    let content = '<h3>' + title + '</h3>';
    
    // Affichage spécial pour les QR codes
    if (data.qr_code_base64) {
        content += '<p><strong>QR Code 2FA :</strong></p>';
        content += '<img src="data:image/png;base64,' + data.qr_code_base64 + '" class="qr-code" alt="QR Code 2FA">';
    }
    if (data.password_qr_code) {
        content += '<p><strong>QR Code Mot de passe :</strong></p>';
        content += '<img src="data:image/png;base64,' + data.password_qr_code + '" class="qr-code" alt="QR Code Password">';
    }
    
    content += '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    resultDiv.innerHTML = content;
    resultsDiv.appendChild(resultDiv);
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function testCreateUser() {
    try {
        const username = 'user_' + Date.now();
        const password = 'TestPassword123!';
        lastGeneratedUser = {username, password};
        
        const response = await fetch('/api/create-user', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            lastGeneratedUser.generatedPassword = data.password;
            showResult('✅ Création Utilisateur', data, 'success');
        } else {
            showResult('❌ Erreur Création', data, 'error');
        }
    } catch (error) {
        showResult('❌ Erreur Réseau', {error: error.message}, 'error');
    }
}

async function testLogin() {
    try {
        if (!lastGeneratedUser) {
            alert('Créez d\'abord un utilisateur ou utilisez un utilisateur existant');
            return;
        }
        
        const username = lastGeneratedUser.username;
        const password = lastGeneratedUser.generatedPassword || lastGeneratedUser.password;
        const totp_code = lastGeneratedCode || prompt('Entrez le code 2FA (6 chiffres) ou laissez vide pour test sans 2FA :');
        
        const payload = {username, password};
        if (totp_code && totp_code.trim()) {
            payload.totp_code = totp_code.trim();
        }
        
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            showResult('✅ Connexion Réussie', data, 'success');
        } else {
            showResult('❌ Échec Connexion', data, 'error');
        }
    } catch (error) {
        showResult('❌ Erreur Connexion', {error: error.message}, 'error');
    }
}

async function testGenerate2FA() {
    try {
        if (!lastGeneratedUser) {
            alert('Créez d\'abord un utilisateur');
            return;
        }
        
        const response = await fetch('/api/generate-2fa', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: lastGeneratedUser.username})
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            lastGeneratedCode = data.test_code;
            showResult('✅ 2FA Généré', data, 'success');
        } else {
            showResult('❌ Erreur 2FA', data, 'error');
        }
    } catch (error) {
        showResult('❌ Erreur 2FA', {error: error.message}, 'error');
    }
}

async function testVerify2FA() {
    try {
        if (!lastGeneratedUser) {
            alert('Créez d\'abord un utilisateur et générez un 2FA');
            return;
        }
        
        const code = lastGeneratedCode || prompt('Entrez le code 2FA (6 chiffres) :');
        if (!code) return;
        
        const response = await fetch('/api/verify-2fa', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: lastGeneratedUser.username, code_2fa: code})
        });
        const data = await response.json();
        
        if (data.verified) {
            showResult('✅ 2FA Vérifié', data, 'success');
        } else {
            showResult('❌ 2FA Invalide', data, 'error');
        }
    } catch (error) {
        showResult('❌ Erreur Vérification', {error: error.message}, 'error');
    }
}

async function testHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        showResult('🏥 Santé Service', data, 'success');
    } catch (error) {
        showResult('❌ Erreur Santé', {error: error.message}, 'error');
    }
}

async function testFullFlow() {
    showResult('🚀 Démarrage du test complet...', {message: 'Création utilisateur → 2FA → Connexion'});
    
    // 1. Créer utilisateur
    await testCreateUser();
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 2. Générer 2FA
    await testGenerate2FA();
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 3. Test connexion
    await testLogin();
    
    showResult('🎉 Test complet terminé !', {message: 'Vérifiez les résultats ci-dessus'}, 'success');
}

from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash
import requests

# Alternative : si vous voulez garder le dossier 'page'
# app = Flask(__name__, template_folder='page')

# Configuration actuelle (recommandée)
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # pour gérer les messages flash

# URL de vos fonctions OpenFaaS (à adapter)
BASE_URL = 'http://localhost:8080/function/'  # Remplace par l'adresse de ton OpenFaaS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']

        # Appel de la fonction OpenFaaS de création
        response = requests.post(f'{BASE_URL}create-user', json={'username': username})

        if response.status_code == 200:
            flash('Compte créé avec succès ! Vérifiez votre QR Code et 2FA.', 'success')
        else:
            flash('Erreur lors de la création du compte.', 'danger')

        return redirect(url_for('home'))

    return render_template('create.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        code_2fa = request.form['code_2fa']

        # Appel de la fonction OpenFaaS d’authentification
        response = requests.post(f'{BASE_URL}login-user', json={
            'username': username,
            'password': password,
            'code_2fa': code_2fa
        })

        if response.status_code == 200:
            result = response.json()
            if result.get('expired'):
                flash('Votre mot de passe est expiré, veuillez recréer vos identifiants.', 'warning')
                return redirect(url_for('create'))
            else:
                flash('Connexion réussie !', 'success')
                return redirect(url_for('home'))
        else:
            flash('Échec de la connexion. Vérifiez vos identifiants.', 'danger')

        return redirect(url_for('home'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

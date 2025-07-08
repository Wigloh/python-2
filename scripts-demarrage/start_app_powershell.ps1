# MSPR - Script PowerShell pour demarrage avec PostgreSQL Docker
Write-Host "MSPR - Demarrage avec PostgreSQL Docker" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Changement vers le dossier parent (python-2)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$parentDir = Split-Path -Parent $scriptDir
Set-Location $parentDir
Write-Host "Repertoire de travail: $parentDir" -ForegroundColor Gray

# Configuration des variables d'environnement
Write-Host "Configuration des variables d'environnement..." -ForegroundColor Yellow
$env:DB_HOST = "localhost"
$env:DB_NAME = "cofrap"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "mspr2024"
$env:FERNET_KEY = "ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg="
$env:SECRET_KEY = "dev-secret-key-mspr-2025"

Write-Host "Variables configurees:" -ForegroundColor Green
Write-Host "   DB_HOST: $env:DB_HOST" -ForegroundColor Gray
Write-Host "   DB_NAME: $env:DB_NAME" -ForegroundColor Gray
Write-Host "   DB_USER: $env:DB_USER" -ForegroundColor Gray

# Verification que app_complete.py existe
if (Test-Path "app_complete.py") {
    Write-Host "Fichier app_complete.py trouve" -ForegroundColor Green
} else {
    Write-Host "ERREUR: Fichier app_complete.py non trouve" -ForegroundColor Red
    Write-Host "Repertoire actuel: $(Get-Location)" -ForegroundColor Red
    exit 1
}

# Demarrage de l'application
Write-Host ""
Write-Host "Demarrage de l'application Flask..." -ForegroundColor Green
Write-Host "L'application sera accessible sur: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pages disponibles:" -ForegroundColor Yellow
Write-Host "   - http://localhost:5000/        (Accueil)" -ForegroundColor Gray
Write-Host "   - http://localhost:5000/create  (Creation compte)" -ForegroundColor Gray
Write-Host "   - http://localhost:5000/login   (Connexion 2FA)" -ForegroundColor Gray
Write-Host "   - http://localhost:5000/test    (Tests API)" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter l'application" -ForegroundColor Yellow
Write-Host ""

# Lancement de l'application avec les variables d environnement
python app_complete.py

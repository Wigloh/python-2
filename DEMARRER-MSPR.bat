@echo off
echo ===============================
echo 🚀 MSPR - Lanceur Principal
echo ===============================
echo.
echo Bienvenue dans le systeme d'authentification securise MSPR !
echo.
echo Ce lanceur vous donne acces a tous les scripts de demarrage.
echo.
echo Choisissez votre option :
echo.
echo [1] 🚀 Demarrage ultra-rapide (Recommande)
echo [2] 📋 Menu de demarrage complet  
echo [3] 🛠️ Utilitaires de maintenance
echo [4] 📖 Aide et documentation
echo [5] ❌ Quitter
echo.
set /p choice="Votre choix (1-5): "

if "%choice%"=="1" goto ultra
if "%choice%"=="2" goto menu
if "%choice%"=="3" goto maintenance
if "%choice%"=="4" goto aide
if "%choice%"=="5" goto quit
goto invalid

:ultra
echo.
echo 🚀 Lancement du demarrage ultra-rapide...
call scripts-demarrage\demarrage-ultra-rapide.bat
goto end

:menu
echo.
echo 📋 Ouverture du menu de demarrage...
call scripts-demarrage\menu-demarrage.bat
goto end

:maintenance
echo.
echo 🛠️ Ouverture des utilitaires de maintenance...
call scripts-demarrage\utilitaires-maintenance.bat
goto end

:aide
echo.
echo 📖 Documentation disponible :
echo.
echo • README_NEW.md - Documentation complete du projet
echo • scripts-demarrage\README-SCRIPTS.md - Guide des scripts
echo.
echo 🌐 URLs importantes une fois l'application demarree :
echo • http://localhost:5000/        - Page d'accueil
echo • http://localhost:5000/create  - Creation de compte
echo • http://localhost:5000/login   - Connexion 2FA
echo • http://localhost:5000/test    - Interface de test
echo.
echo 📋 Prerequis necessaires :
echo • Python 3.8+ installe
echo • Docker Desktop installe et demarre
echo • Connexion Internet (pour telecharger PostgreSQL)
echo.
pause
goto start

:invalid
echo.
echo ❌ Choix invalide. Veuillez choisir entre 1 et 5.
pause
goto start

:quit
echo.
echo 👋 Au revoir !
echo Merci d'avoir utilise le systeme MSPR !
goto end

:start
cls
goto :eof

:end
echo.
pause

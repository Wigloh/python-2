@echo off
echo ================================
echo 🔐 MSPR - Scripts de Demarrage
echo ================================
echo.

REM Changement vers le dossier parent (python-2)
cd /d "%~dp0.."

echo Choisissez votre methode de demarrage :
echo.
echo [1] Demarrage complet automatique (Docker + PostgreSQL)
echo [2] Demarrage PostgreSQL local (ancien)
echo [3] Quitter
echo.
set /p choice="Votre choix (1-3): "

if "%choice%"=="1" goto docker
if "%choice%"=="2" goto local
if "%choice%"=="3" goto quit
goto invalid

:docker
echo.
echo 🐳 Lancement du script Docker...
call "%~dp0start_app_docker.bat"
goto end

:local
echo.
echo 🗄️ Lancement du script PostgreSQL local...
call "%~dp0start_app_mspr.bat"
goto end

:invalid
echo.
echo ❌ Choix invalide. Veuillez choisir 1, 2 ou 3.
pause
goto start

:quit
echo.
echo 👋 Au revoir !
goto end

:end
pause

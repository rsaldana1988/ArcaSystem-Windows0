@echo off
setlocal
cd /d "%~dp0"
title ArcaSystem - Inicio automatico
if not exist ".venv\Scripts\python.exe" (
  echo [ArcaSystem] Preparando el entorno por primera vez...
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>nul
    if errorlevel 1 goto NO_PYTHON
    python -m venv .venv
  )
  if errorlevel 1 goto ERROR
)
if not exist ".venv\arca_integral_v1.txt" (
  echo [ArcaSystem] Instalando componentes. Esto puede tardar unos minutos...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto ERROR
  echo instalado>".venv\arca_integral_v1.txt"
)
echo [ArcaSystem] Preparando la base de datos...
if exist db.sqlite3 if not exist db_antes_actualizacion.sqlite3 copy /y db.sqlite3 db_antes_actualizacion.sqlite3 >nul
".venv\Scripts\python.exe" manage.py migrate --noinput
if errorlevel 1 goto ERROR
".venv\Scripts\python.exe" manage.py import_arcasystem_logo
if errorlevel 1 goto ERROR
start "" "http://127.0.0.1:8000/"
echo.
echo ArcaSystem esta iniciando. No cierres esta ventana mientras lo uses.
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000 --noreload
pause
exit /b
:NO_PYTHON
echo Necesitas instalar Python desde https://www.python.org/downloads/windows/
echo Marca la opcion Add Python to PATH y vuelve a abrir este archivo.
pause
exit /b 1
:ERROR
echo No se pudo iniciar ArcaSystem. Revisa el mensaje anterior.
pause
exit /b 1

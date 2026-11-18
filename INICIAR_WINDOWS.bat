@echo off
cd /d "%~dp0"
if not exist .venv (py -m venv .venv)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
start http://127.0.0.1:8000/
python manage.py runserver
pause

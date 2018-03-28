@echo off
python3 -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python3 manage.py makemigrations dondapp
python3 manage.py makemigrations
python3 manage.py migrate
python3 populate_script.py
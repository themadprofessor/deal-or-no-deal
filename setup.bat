@echo off
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py makemigrations dondapp
python manage.py makemigrations
python manage.py migrate
python populate_script.py
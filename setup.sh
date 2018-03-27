#!/bin/sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations dondapp
python manage.py makemigrations
python manage.py migrate
python populate_script.py

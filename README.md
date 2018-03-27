# Deal or No Deal
## Student deal voting site

### Requirements
- Python 3
- PiP

### Automatic Setup

Run either `setup.bat` or `setup.sh` to setup environment and database

### Manual Setup

Create and activate a virtual environment:

```
python -m venv venv_name

venv_name\Scripts\activate.bat` or `source venv_name/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Setup and populate database

```
python manage.py makemigrations dondapp

python manage.py makemigrations

python manage.py

python populate_script.py
```

### Running server

Ensure your virtual environment is activated

```
python manage.py runserver
```

Then the server can be accessed at [http://127.0.0.1:8080](http://127.0.0.1:8080)
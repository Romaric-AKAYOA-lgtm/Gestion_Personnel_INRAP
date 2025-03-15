@echo off
echo Setting up Django project...

REM Crée un environnement virtuel
python -m venv venv

REM Active l'environnement virtuel
venv\Scripts\activate

REM Installe les dépendances
pip install -r requirements.txt

REM Crée un projet Django
django-admin startproject gestion_personnel

REM Démarre le serveur
cd gestion_personnel
python manage.py runserver

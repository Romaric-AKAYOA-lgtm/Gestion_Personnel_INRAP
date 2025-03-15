import os
import sys
import webbrowser  # Ajout du module pour ouvrir le navigateur

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestion_Personnel_INRAP.settings')

    # Simuler la commande 'runserver' pour démarrer le serveur Django sans auto-rechargement
    sys.argv = ['manage.py', 'runserver', '--noreload']  # Désactive l'auto-rechargement

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

    # Ouvrir automatiquement le navigateur après avoir démarré le serveur Django
    webbrowser.open('http://127.0.011:8000/')  # Adresse locale du serveur Django

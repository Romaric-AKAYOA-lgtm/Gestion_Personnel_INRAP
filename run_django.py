import os
import sys
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle  # Assurez-vous que l'import est correct
import webbrowser
import django.db.backends
import threading  # Importation du module threading

# Pour vérifier si reportlab est bien installé et faire une réinstallation si nécessaire
try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
except ImportError:
    print("Le module reportlab n'est pas installé ou mal installé. Installation en cours...")
    os.system('pip install reportlab')

def run_django_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestion_Personnel_INRAP.settings')
    
    # Simuler la commande 'runserver' pour démarrer le serveur Django sans auto-rechargement
    sys.argv = ['manage.py', 'runserver', '--noreload']
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    # Démarrer le serveur Django dans un thread séparé
    server_thread = threading.Thread(target=run_django_server)
    server_thread.start()

    # Ouvrir automatiquement le navigateur après un délai pour être sûr que le serveur est lancé
    import time
    time.sleep(2)  # Attendre 2 secondes pour être sûr que le serveur est bien démarré
    webbrowser.open('http://127.0.0.1:8000/')

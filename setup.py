from setuptools import setup, find_packages
import os

# Lire le fichier requirements.txt s'il existe
requirements_file = 'requirements.txt'
if os.path.exists(requirements_file):
    with open(requirements_file, encoding='utf-8') as f:
        required = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]  # Ignore les commentaires
else:
    required = []

setup(
    name='Gestion_Personnel_INRAP',  # Nom de l'application
    version='1.0',  # Version de l'application
    packages=find_packages(),  # Recherche automatique des packages
    install_requires=required,  # Ajout des dépendances
    entry_points={  # Point d'entrée de la commande CLI
        'console_scripts': [
            'start-personnel-inrap=Gestion_Personnel_INRAP.start_server:main',  # Commande personnalisée
        ],
    },
    url="https://github.com/TonRepo/Gestion_Personnel_INRAP",  # L'URL de ton projet
    author="Ton Nom",  # À modifier avec ton nom
    author_email="ton.email@example.com",  # À modifier avec ton email
    description="Application de gestion du personnel INRAP",  # Description de l'application
    classifiers=[  # Catégories pour PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Version minimale de Python
)

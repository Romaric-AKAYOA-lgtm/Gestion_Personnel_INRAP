from setuptools import setup, find_packages

setup(
    name='Gestion_Personnel_INRAP',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2.8',  # Assure-toi que tu as la version correcte de Django
        'gunicorn',        # Ajoute Gunicorn pour démarrer le serveur
        'pytz',
        'sqlparse',
        'django-environ',  # Pour la gestion des variables d'environnement
    ],
    entry_points={
        'console_scripts': [
            'startproject=django.core.management:execute_from_command_line',
        ],
    },
    python_requires='>=3.9',
)

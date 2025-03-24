from setuptools import setup, find_packages
import os

# Charger les dépendances depuis requirements.txt
requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
if os.path.exists(requirements_file):
    with open(requirements_file, encoding='utf-8') as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    required = []

# Charger la description depuis README.md
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.exists(readme_file):
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Application de gestion du personnel INRAP"

setup(
    name='Gestion_Personnel_INRAP',
    version='1.0',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'start-personnel-inrap=Gestion_Personnel_INRAP.start_server:main',
        ],
    },
    url="https://github.com/TonRepo/Gestion_Personnel_INRAP",
    author="Ton Nom",
    author_email="ton.email@example.com",
    description="Application de gestion du personnel INRAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

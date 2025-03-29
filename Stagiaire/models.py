from django.db import models
from datetime import date

from django.forms import ValidationError

from RespensableOrganisationUnite.models import ResponsableOrganisationUnite


class Stagiaire(models.Model):
    # Informations personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    
    # Informations académiques
    universite = models.CharField(max_length=255)
    formation = models.CharField(max_length=255)

    # Informations sur le stage
    date_debut_stage = models.DateField()
    date_fin_stage = models.DateField()
    
    # Le tuteur doit être un responsable dont la date de fin est <= aujourd'hui
    tuteur_entreprise = models.ForeignKey(
        ResponsableOrganisationUnite, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    evaluation_stage = models.TextField(blank=True, null=True)

    # Statut du stage (En cours, Terminé, etc.)
    STATUT_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('SUSPENDU', 'Suspendu'),
    ]
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='EN_COURS',
    )

    # Compétences
    competences = models.TextField(blank=True)

    # Date d'inscription
    date_inscription = models.DateTimeField(auto_now_add=True)

    # Commentaires
    commentaires = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Stagiaire"
        verbose_name_plural = "Stagiaires"

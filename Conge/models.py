from django.db import models
from django.core.exceptions import ValidationError
from Employee.models import Employee

class Conge(models.Model):
    TYPE_CONGE = [
        ('annuel', 'Annuel'),
        ('maladie', 'Maladie'),
        ('maternité', 'Maternité'),
    ]
    
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type = models.CharField(max_length=20, choices=TYPE_CONGE)
    statut = models.BooleanField(default=False)  # Approuvé ou non
    
    def clean(self):
        # Récupération des dates de début de service, fin de service et retraite de l'employé
        date_debut_service = self.employe.start_date
        date_fin_service = self.employe.retirement_date
        date_retraite = self.employe.retirement_date
        
        # Vérifier si la date de fin de service est définie, sinon utiliser la date de retraite
        if date_fin_service is None:
            date_fin_service = date_retraite
        
        # Vérifier que les dates sont valides
        if date_debut_service is None or date_fin_service is None:
            raise ValidationError("Les dates de service et de retraite de l'employé doivent être définies.")
        
        # Vérifier que les dates de congé sont comprises entre la date de début et la date de fin de service
        if not (date_debut_service <= self.date_debut <= date_fin_service):
            raise ValidationError(f"La date de début du congé doit être entre {date_debut_service} et {date_fin_service}.")
        
        if not (date_debut_service <= self.date_fin <= date_fin_service):
            raise ValidationError(f"La date de fin du congé doit être entre {date_debut_service} et {date_fin_service}.")
        
        if self.date_debut > self.date_fin:
            raise ValidationError("La date de début du congé ne peut pas être après la date de fin.")

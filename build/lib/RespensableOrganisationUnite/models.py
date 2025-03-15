from django.db import models
from Employee.models import Employee
from OrganizationalUnit.models import OrganizationalUnit
from fonction.models import Fonction  # Assurez-vous que c'est bien 'Fonction' et non 'Function'

class ResponsableOrganisationUnite(models.Model):
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Employee, on_delete=models.CASCADE)
    function = models.ForeignKey(Fonction, on_delete=models.CASCADE)  # Ajout de la fonction
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.responsable} - {self.organizational_unit}"

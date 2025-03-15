from django import forms

from fonction.models import Fonction
from .models import ResponsableOrganisationUnite
from Employee.models import Employee
from fonction.models import Fonction
from OrganizationalUnit.models import OrganizationalUnit
from django.core.exceptions import ValidationError

class ResponsableOrganisationUniteForm(forms.ModelForm):
    class Meta:
        model = ResponsableOrganisationUnite
        fields = ['organizational_unit', 'responsable', 'function', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_debut(self):
        responsable = self.cleaned_data.get('responsable')
        date_debut = self.cleaned_data.get('date_debut')

        if responsable and responsable.start_date:
            if date_debut < responsable.start_date:
                raise ValidationError(f"La date de début doit être supérieure ou égale à la date de début de l'employé ({responsable.start_date}).")

        return date_debut

    def __init__(self, *args, **kwargs):
        super(ResponsableOrganisationUniteForm, self).__init__(*args, **kwargs)
        self.fields['organizational_unit'].queryset = OrganizationalUnit.objects.all()
        self.fields['responsable'].queryset = Employee.objects.all()
        self.fields['function'].queryset = Fonction.objects.all()  # Remplir le champ fonction avec toutes les fonctions disponibles

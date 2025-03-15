from django import forms
from .models import Specialite
import re
from django.core.exceptions import ValidationError

class SpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialite
        fields = ['designation' ]

    def clean_nom(self):
        nom = self.cleaned_data['designation']
        
        # Vérification que le nom ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in nom) :
            raise ValidationError("La designation ne doit contenir que des lettres, sans chiffres ni caractères spéciaux.")
        
        # Vérification que le nom n'est pas vide
        if not nom:
            raise ValidationError("La designation est obligatoire.")
        
        return nom

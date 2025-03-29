from datetime import date
from django import forms
from django.db.models import Q
from .models import Stagiaire
from RespensableOrganisationUnite.models import ResponsableOrganisationUnite

class StagiaireForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'date_naissance', 'email', 'telephone', 'adresse', 'universite', 'formation', 
                  'date_debut_stage', 'date_fin_stage', 'tuteur_entreprise', 'evaluation_stage', 'statut', 
                  'competences', 'commentaires']
        
        widgets = {
            'date_debut_stage': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_stage': forms.DateInput(attrs={'type': 'date'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Récupérer les dates de naissance et de début de stage
        date_naissance = cleaned_data.get('date_naissance')
        date_debut_stage = cleaned_data.get('date_debut_stage')

        # Vérifier que l'écart entre la date de naissance et la date de début de stage est >= 16 ans
        if date_naissance and date_debut_stage:
            # Calcul de l'écart en années
            age_at_start = date_debut_stage.year - date_naissance.year
            if (date_debut_stage.month, date_debut_stage.day) < (date_naissance.month, date_naissance.day):
                age_at_start -= 1  # Si la date de naissance n'est pas encore passée dans l'année en cours

            # Vérifier si l'âge à la date de début du stage est inférieur à 16 ans
            if age_at_start < 16:
                self.add_error('date_naissance', "Le stagiaire doit avoir au moins 16 ans lors de la date de début du stage.")

        # Vérification pour le tuteur
        tuteur_entreprise = cleaned_data.get('tuteur_entreprise')
        if tuteur_entreprise:
            if not tuteur_entreprise.date_fin or tuteur_entreprise.date_fin <= date.today():
                self.add_error('tuteur_entreprise', "Le tuteur sélectionné doit avoir une date de fin après aujourd'hui.")

        return cleaned_data

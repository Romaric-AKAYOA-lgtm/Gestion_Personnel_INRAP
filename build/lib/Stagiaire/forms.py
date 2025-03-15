from datetime import date
from django import forms
from .models import Stagiaire

class StagiaireForm(forms.ModelForm):
    # Définition des champs du modèle
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'date_naissance', 'email', 'telephone', 'adresse', 'universite', 'formation', 
                  'date_debut_stage', 'date_fin_stage', 'tuteur_entreprise', 'evaluation_stage', 'statut', 
                  'competences', 'commentaires']
        
        # Widgets pour les champs de date (facilite la saisie sous forme de date)
        widgets = {
            'date_debut_stage': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_stage': forms.DateInput(attrs={'type': 'date'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    # Optionnel : Ajoutez des validations personnalisées au formulaire si nécessaire
    def clean(self):
        cleaned_data = super().clean()

        # Validation personnalisée pour le tuteur
        tuteur_entreprise = cleaned_data.get('tuteur_entreprise')
        
        if tuteur_entreprise:
            # Vérification que la date_fin du responsable soit <= à la date actuelle
            if tuteur_entreprise.date_fin and tuteur_entreprise.date_fin > date.today():
                self.add_error('tuteur_entreprise', "Le tuteur sélectionné a une date de fin après aujourd'hui.")

        return cleaned_data


from django import forms
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'start_date', 
            'grade', 'echelon', 'matricule', 'specialty', 
             'observation', 'status', 
            'sexe', 'image', 'adresse', 'num_tel', 'email'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'retirement_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("Le prénom est obligatoire.")
        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError("Le prénom ne doit pas contenir de chiffres.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Le nom est obligatoire.")
        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError("Le nom ne doit pas contenir de chiffres.")
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        start_date = cleaned_data.get('start_date')
        retirement_date = cleaned_data.get('retirement_date')

        # Vérifier que la date de service est au moins 18 ans après la date de naissance
        if dob and start_date and start_date < (dob + relativedelta(years=18)):
            self.add_error('start_date', "La date de service doit être au moins 18 ans après la date de naissance.")

        # Vérifier que la date de service est inférieure à la date de retraite
        if start_date and retirement_date and start_date >= retirement_date:
            self.add_error('start_date', "La date de service doit être inférieure à la date de retraite.")

        return cleaned_data
    def clean_retirement_date(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        retirement_date = date_of_birth+ timedelta(days=60*365)  # Ajout de 60 ans à la date de naissance
        
        return retirement_date
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Mise à jour automatique du statut si l'agent est à la retraite
        if instance.retirement_date and instance.retirement_date <= date.today():
            instance.status = 'retired'

        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):  # Remplace AuthenticationForm par forms.Form
    username = forms.CharField(
        label="Nom d'utilisateur", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        label="Mot de passe", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

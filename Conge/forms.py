from django import forms
from .models import Conge

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = '__all__'

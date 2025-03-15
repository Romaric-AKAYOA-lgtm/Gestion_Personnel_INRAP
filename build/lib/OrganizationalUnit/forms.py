from django import forms
from .models import OrganizationalUnit
from django.core.exceptions import ValidationError
 
class OrganizationalUnitForm(forms.ModelForm):
    class Meta:
        model = OrganizationalUnit
        fields = ['name', 'parent',"unite", 'designation', 'unite', 'parent']
        """   
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Nom de l'unité"}),
            'parent': forms.Select(),
            'responsable': forms.Select(),
        }
        """
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Le nom de l'unité est obligatoire.")
        return name

    def clean_unit_type(self):
        unit_type = self.cleaned_data.get('unit_type')
        if unit_type not in dict(OrganizationalUnit.UNIT_TYPES).keys():
            raise ValidationError("Type d'unité invalide.")
        return unit_type

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')

        if parent and self.instance.pk and parent.pk == self.instance.pk:
            raise ValidationError("Une unité ne peut pas être son propre parent.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

from django.db import models

class Administration(models.Model):
    nom = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    devise = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    devise_pays = models.CharField(max_length=50)
    drapeau = models.ImageField(upload_to='drapeaux/')  # Champ pour le drapeau du pays

    def __str__(self):
        return self.nom
    class Meta:
        app_label = 'administration'

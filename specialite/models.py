from django.db import models

# Create your models here.
class  Specialite(models.Model):
    designation = models.CharField(max_length=50, unique=True,)
    def __str__(self):
        return f"{self.designation}"
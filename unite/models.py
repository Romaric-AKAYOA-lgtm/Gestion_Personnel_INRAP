from django.db import models

# Create your models here.
class  Unite(models.Model):
    designation = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.designation}"

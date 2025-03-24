from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password, check_password
from specialite.models import Specialite

class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)

    STATUS_CHOICES = [
        ('Actif', 'Actif'),
        ('Non Actif', 'Non Actif'),
    ]
    
    first_name = models.CharField(
        blank=True, null=True,
        max_length=50,
        help_text="Prénom de l'agent"
    )
    last_name = models.CharField(
        max_length=50,
        help_text="Nom de l'agent"
    )
    date_of_birth = models.DateField(help_text="Date de naissance")
    place_of_birth = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        help_text="Lieu de naissance"
    )
    start_date = models.DateField(
        verbose_name="Prise de service",
        help_text="Date de prise de service à l'INRAP"
    )
    retirement_date = models.DateField(
        verbose_name="Départ à la retraite",
        help_text="Date de départ à la retraite",
        blank=True,
        null=True
    )
    grade = models.CharField(max_length=50, help_text="Grade", blank=True, null=True)
    echelon = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Échelon"
    )
    matricule = models.CharField(max_length=7, help_text="Matricule solde")
    specialty = models.ForeignKey(Specialite, on_delete=models.CASCADE, blank=True, null=True)
    observation = models.TextField(
        blank=True,
        null=True,
        help_text="Observations éventuelles"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
          blank=True,
        null=True,
        default='Actif',
        help_text="Statut de l'agent"
    )
    sexe = models.CharField(
        max_length=20, 
        choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')]
    )
    image = models.ImageField(
        default="1.png", 
        upload_to='employe/', 
        blank=True, 
        null=True
    )
    adresse = models.CharField(max_length=60, blank=True, null=True,)
    num_tel = models.CharField(
        blank=True, null=True,
        max_length=15, 
        unique=True, 
        error_messages={"unique": "Ce numéro est déjà utilisé."}
    )
    email = models.EmailField(
        blank=True, null=True,
        unique=True, 
        error_messages={"unique": "Cet email est déjà utilisé."}
    )
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['last_name', 'first_name']

    def set_password(self, raw_password):
        """Hache le mot de passe avant de l'enregistrer."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Vérifie si le mot de passe saisi correspond au mot de passe haché."""
        return check_password(raw_password, self.password)

    @classmethod
    def authenticate(cls, username, password):
        """Vérifie les identifiants de l'utilisateur."""
        try:
            secretaire = cls.objects.get(username=username)
            if secretaire.check_password(password):
                return secretaire
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        """Retourne le nom complet de l'employé."""
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.retirement_date and self.date_of_birth:
            self.retirement_date = self.date_of_birth + relativedelta(years=65)
        super().save(*args, **kwargs)

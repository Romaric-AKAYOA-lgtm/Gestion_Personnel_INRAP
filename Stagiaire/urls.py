from django.urls import path
from . import views

app_name = 'stagiaire'  # Définir l'espace de noms pour l'application

urlpatterns = [
    # URL pour la création d'un stagiaire
    path('create/', views.create_stagiaire, name='create_stagiaire'),
    
    # URL pour la liste des stagiaires
    path('list/', views.stagiaire_list, name='stagiaire_list'),
    
    # URL pour la modification d'un stagiaire
    path('modify/<int:id>/', views.modify_stagiaire, name='modify_stagiaire'),  # Modification du stagiaire par son ID
     path('recherche/', views.stagiaire_search, name='recherche'),  # Ajout de la route de recherche
]

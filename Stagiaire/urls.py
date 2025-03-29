from django.urls import path
from . import views

app_name = 'stagiaire'

urlpatterns = [
    # URL pour la création d'un stagiaire
    path('create/', views.create_stagiaire, name='create_stagiaire'),
    
    # URL pour la liste des stagiaires
    path('list/', views.stagiaire_list, name='stagiaire_list'),
    
    # URL pour la modification d'un stagiaire
    path('modify/<int:id>/', views.modify_stagiaire, name='modify_stagiaire'),
    
    # URL pour la recherche des stagiaires
    path('recherche/', views.stagiaire_search, name='recherche'),
    
    # URL pour la suppression d'un stagiaire
    path('delete/<int:id>/', views.delete_stagiaire, name='delete_stagiaire'),  # Suppression du stagiaire par son ID
]

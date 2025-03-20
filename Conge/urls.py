from django.urls import path
from . import views

app_name='conge'

urlpatterns = [ 
    # Gestion des congés
    path('conges/', views.liste_conges, name='liste_conges'),
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
    path('conges/modifier/<int:conge_id>/', views.modifier_conge, name='modifier_conge'),
    path('conges/supprimer/<int:conge_id>/', views.supprimer_conge, name='supprimer_conge'),
     path('recherche/', views.conge_search, name='recherche'),
]

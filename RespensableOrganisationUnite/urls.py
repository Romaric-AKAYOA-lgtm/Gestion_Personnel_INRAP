from django.urls import path
from . import views

app_name = "RespensableOrganisationUnite"

urlpatterns = [
    # Liste de toutes les unités organisationnelles
    path('', views.liste_RespensableOrganisationUnite, name='list'),
    # Création d'une nouvelle unité organisationnelle
    path('create/', views.ajouter_RespensableOrganisationUnite, name='create'),
    # Modification d'une unité organisationnelle
    path('<int:id>/update/', views.modifier_RespensableOrganisationUnitet, name='update'),
    # Suppression d'une unité organisationnelle
    path('<int:id>/delete/', views.supprimer_RespensableOrganisationUnite, name='delete'),
    path('search/', views.search_responsable_unite, name='search_responsable_unite'),
]

from django.urls import path
from . import views

app_name = 'stagiaire'

urlpatterns = [
   path('', views.create_stagiaire, name='create_stagiaire'),
    path('list/', views.stagiaire_list, name='stagiaire_list'),
    path('modify/<int:id>/', views.modify_stagiaire, name='modify_stagiaire'),
    path('recherche/', views.stagiaire_search, name='recherche'),
    path('delete/<int:id>/', views.delete_stagiaire, name='delete_stagiaire'),
]

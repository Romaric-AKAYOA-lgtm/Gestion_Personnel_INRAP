from django.urls import path
from . import views

app_name = 'unite'

urlpatterns = [
    path('', views.unite_list, name='unite'),
    path('creer/', views.unite_create, name='creer'),
   path('<int:id>/modifier/', views.modifier_unite, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_unite,  name='supprimer'),
    path('recherche/', views.unite_search, name='recherche'),  # Ajout de la route de recherche
]

from django.urls import path
from . import views

app_name = 'specialite'

urlpatterns = [
    path('', views.specialite_list, name='specialite'),
    path('creer/', views.specialite_create, name='creer'),
    path('<int:id>/', views.specialite_detail, name='information'),
   path('<int:id>/modifier/', views.modifier_specialite, name='modifier'),
   path('<int:id>/supprimer/', views.supprimer_specialite , name='supprimer'),
]

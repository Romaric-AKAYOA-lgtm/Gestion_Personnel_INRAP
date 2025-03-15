from django.urls import path
from . import views

app_name = 'fonction'

urlpatterns = [
    path('', views.fonction_list, name='fonction'),
    path('creer/', views.fonction_create, name='creer'),
    path('<int:id>/', views.fonction_detail, name='information'),
   path('<int:id>/modifier/', views.modifier_fonction, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_fonction,  name='supprimer'),
]

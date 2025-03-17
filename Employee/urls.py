from django.urls import path
from . import views

app_name = "Employee"

urlpatterns = [
  
    # Liste de tous les employés
    path('Employee', views.liste_employes ,name='list'),
    # Création d'un nouvel employé
    path('create/', views.ajouter_employe, name='create'),
    # Modification d'un employé
    path('<int:id>/update/', views.modifier_employe, name='update'),
    # Suppression d'un employé
    path('<int:id>/delete/', views.supprimer_employe, name='delete'),
     path('employee/pdf/', views.generate_employee_pdf, name='generate_employee_pdf'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

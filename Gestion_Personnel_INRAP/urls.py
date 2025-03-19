from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Employee.views import login_view
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', login_view, name='login'),
    path('home', views.home_view, name='home'),  
     path('imprimer/options/', views.print_options, name='print_options'),
    path('imprimer/rapports/', views.print_results, name='print_results'),
     path('unite/', include('unite.urls')),
    path('OrganizationalUnit/', include('OrganizationalUnit.urls')),
    path('Employee/', include('Employee.urls')),
    path('Activation/', include('Activation.urls')),  # Ajoutez cette ligne  path('fiche_employe/<int:employe_id>/', views.fiche_employe_view, name='fiche_employe'),
    path('fonction/', include('fonction.urls')),
    path('specialite/', include('specialite.urls')),  # Ajoutez cette ligne  path('fiche_employe/<int:employe_id>/', views.fiche_employe_view, name='fiche_employe'),
    path('conge/', include('Conge.urls')),
    path('RespensableOrganisationUnite/', include('RespensableOrganisationUnite.urls')),
    path ('stagiaire', include('Stagiaire.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
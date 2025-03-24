from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from Employee.models import Employee
from Employee.views import get_username_from_session
from OrganizationalUnit.models import OrganizationalUnit
from fonction.models import Fonction
from .models import ResponsableOrganisationUnite
from .forms import ResponsableOrganisationUniteForm
# Liste des Responsables
def liste_RespensableOrganisationUnite(request):
    username = get_username_from_session(request)
    # Vérification de l'authentification de l'utilisateur
    if not username:
        return redirect('OrganizationalUnit:login')  #
    responsables = ResponsableOrganisationUnite.objects.all()  # Récupérer tous les responsables
    return render(request, 'respensableorganisationunite/list.html', {'responsables': responsables, 'username':username })

# Ajouter un Responsable
def ajouter_RespensableOrganisationUnite(request):
    username = get_username_from_session(request)

    # Vérification de l'authentification de l'utilisateur
    if not username:
        return redirect('OrganizationalUnit:login')  #
    organizational_units = OrganizationalUnit.objects.all().order_by('name')
    employees = Employee.objects.filter(status='Actif')
    functions = Fonction.objects.all().order_by('designation')
    
    if request.method == 'POST':
        form = ResponsableOrganisationUniteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Responsable ajouté avec succès.")
            return redirect('RespensableOrganisationUnite:list')
    else:
        form = ResponsableOrganisationUniteForm()
    
    return render(request, 'respensableorganisationunite/create.html', {
        'organizational_units': organizational_units,
        'employees': employees,
        'functions': functions,
        'username':username , 
        'form': form
    })

# Modifier un Responsable
def modifier_RespensableOrganisationUnitet(request, id):
    username = get_username_from_session(request)

    # Vérification de l'authentification de l'utilisateur
    if not username:
        return redirect('OrganizationalUnit:login')  #
    organizational_units = OrganizationalUnit.objects.all()
    employees = Employee.objects.filter(status='Actif')
    functions = Fonction.objects.all()
    
    responsable = get_object_or_404(ResponsableOrganisationUnite, id=id)
    
    if request.method == 'POST':
        form = ResponsableOrganisationUniteForm(request.POST, instance=responsable)
        if form.is_valid():
            form.save()
            messages.success(request, "Responsable modifié avec succès.")
            return redirect('RespensableOrganisationUnite:list')
    else:
        form = ResponsableOrganisationUniteForm(instance=responsable)
    
    return render(request, 'respensableorganisationunite/modifier.html', {
        'organizational_units': organizational_units,
        'employee': employees,
        'functions': functions, 
        'username':username , 
        'form': form,})

# Supprimer un Responsable
def supprimer_RespensableOrganisationUnite(request, id):
    username = get_username_from_session(request)

    # Vérification de l'authentification de l'utilisateur
    if not username:
        return redirect('OrganizationalUnit:login')  #
    responsable = get_object_or_404(ResponsableOrganisationUnite, id=id)  # Récupérer le responsable existant par son ID
    
    if request.method == 'POST':
        responsable.delete()  # Supprimer le responsable
        messages.success(request, "Responsable supprimé avec succès.")  # Message de succès
        return redirect('RespensableOrganisationUnite:list')  # Rediriger vers la liste des responsables

    return render(request, 'respensableorganisationunite/supprimer.html', {'responsable': responsable, 'username':username })


def search_responsable_unite(request):
    username = get_username_from_session(request)

    # Vérification de l'authentification de l'utilisateur
    if not username:
        return redirect('OrganizationalUnit:login')  #
    query = request.GET.get("query", "")
    filter_by = request.GET.get("filter", "")

    results = ResponsableOrganisationUnite.objects.all()

    if query:
        if filter_by == "organizational_unit":
            results = results.filter(organizational_unit__name__icontains=query)
        elif filter_by == "responsable":
            results = results.filter(responsable__first_name__icontains=query) | results.filter(responsable__last_name__icontains=query)
        elif filter_by == "function":
            results = results.filter(function__titre__icontains=query)
        elif filter_by == "date_debut":
            results = results.filter(date_debut__icontains=query)
        elif filter_by == "date_fin":
            results = results.filter(date_fin__icontains=query)

    return render(request, "RespensableOrganisationUnite/search.html", {"results": results, "query": query, "filter": filter_by, 
                                                                        'username':username  })

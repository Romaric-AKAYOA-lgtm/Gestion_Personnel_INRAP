from django.shortcuts import render, redirect, get_object_or_404
from Activation.models import Activation
from Employee.models import Employee
from Employee.views import get_username_from_session
from unite.models import Unite
from .models import OrganizationalUnit
from .forms import OrganizationalUnitForm

# Vue pour afficher toutes les unités organisationnelles
def liste_OrganizationalUnit(request):
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Vérification de l'activation
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    organizational_units = OrganizationalUnit.objects.all().order_by('name') # Changement de nom ici
    return render(request, 'OrganizationalUnit/liste_unites.html', {
       'username' : username, 'organizational_units': organizational_units})

# Vue pour ajouter une unité organisationnelle
def ajouter_OrganizationalUnit(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    form = OrganizationalUnitForm()

    # Récupération des données associées
    unite_dict = {unite.id: unite.designation for unite in Unite.objects.all().order_by('designation')}
    organizational_units_dict = {org_unit.id: org_unit.name for org_unit in OrganizationalUnit.objects.all().order_by('name')}
    
    if request.method == 'POST':
        form = OrganizationalUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('OrganizationalUnit:list')

    return render(request, 'OrganizationalUnit/ajouter_unite.html', {
        'username':username, 
        'form': form,
        'unite_dict': unite_dict,
        'organizational_units_dict': organizational_units_dict,
    })

def modifier_OrganizationalUnit(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    unite = get_object_or_404(OrganizationalUnit, id=id)
    unite_dict = {unite.id: unite.designation for unite in Unite.objects.all().order_by('designation')}
    organizational_units_dict = {org_unit.id: org_unit.name for org_unit in OrganizationalUnit.objects.all().order_by('name')}
    
    if request.method == 'POST':
        form = OrganizationalUnitForm(request.POST, instance=unite)
        if form.is_valid():
            form.save()
            return redirect('OrganizationalUnit:list')  # Rediriger vers la liste après modification
    else:
        form = OrganizationalUnitForm(instance=unite)  # Initialisation du formulaire avec les données de l'unité

    return render(request, 'OrganizationalUnit/modifier_unite.html', {
        'username':username,
        'username':username, 
        'form': form, 'unite': unite,
         'unite_dict': unite_dict,
        'organizational_units_dict': organizational_units_dict,
        })

# Vue pour supprimer une unité organisationnelle
def supprimer_OrganizationalUnit(request, id):
    organizational_unit = get_object_or_404(OrganizationalUnit, id=id)  # Changement de nom ici
    organizational_unit.delete()
    return redirect('OrganizationalUnit:list')

from django.db.models import Q

def search_organizational_units(request):
    username = get_username_from_session(request)

    # Vérification de l'authentification de l'utilisateur
    if not username:
        return redirect('OrganizationalUnit:login')  # Redirection avec espace de noms

    """
    Vue permettant de rechercher des unités organisationnelles
    en fonction du critère sélectionné dans le formulaire.
    """
    query_value = request.GET.get('query', '').strip()
    filter_criteria = request.GET.get('filter', '')  # Récupérer le critère sélectionné

    # Vérifier si une valeur de recherche est fournie
    if not query_value or not filter_criteria:
        results = []  # Aucun résultat si pas de valeur entrée
    else:
        # Création dynamique du filtre en fonction du critère sélectionné
        filters = Q()
        if filter_criteria == "name":
            filters = Q(name__icontains=query_value)
        elif filter_criteria == "designation":
            filters = Q(designation__icontains=query_value)
        elif filter_criteria == "unite":
            filters = Q(unite__name__icontains=query_value)  # Recherche par unité associée
        elif filter_criteria == "parent":
            filters = Q(parent__name__icontains=query_value)  # Recherche par unité parente

        try:
            # Application des filtres et tri par nom
            results = OrganizationalUnit.objects.filter(filters).order_by('name')
        except Exception as e:
            results = []
            print(f"Erreur lors de la récupération des résultats : {e}")  # Log d'erreur

    return render(request, 'OrganizationalUnit/search.html', {
        'username': username,
        'results': results,
        'query_value': query_value,  # Valeur saisie par l'utilisateur
        'filter_criteria': filter_criteria,  # Critère de filtrage sélectionné
    })

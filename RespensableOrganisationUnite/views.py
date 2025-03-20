from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ResponsableOrganisationUnite
from .forms import ResponsableOrganisationUniteForm
# Liste des Responsables
def liste_RespensableOrganisationUnite(request):
    responsables = ResponsableOrganisationUnite.objects.all()  # Récupérer tous les responsables
    return render(request, 'respensableorganisationunite/list.html', {'responsables': responsables})

# Ajouter un Responsable
def ajouter_RespensableOrganisationUnite(request):
    if request.method == 'POST':
        form = ResponsableOrganisationUniteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Responsable ajouté avec succès.")
            return redirect('RespensableOrganisationUnite:list')
    else:
        form = ResponsableOrganisationUniteForm()
    return render(request, 'respensableorganisationunite/create.html', {'form': form})

# Modifier un Responsable
def modifier_RespensableOrganisationUnitet(request, id):
    responsable = get_object_or_404(ResponsableOrganisationUnite, id=id)
    
    if request.method == 'POST':
        form = ResponsableOrganisationUniteForm(request.POST, instance=responsable)
        if form.is_valid():
            form.save()
            messages.success(request, "Responsable modifié avec succès.")
            return redirect('RespensableOrganisationUnite:list')
    else:
        form = ResponsableOrganisationUniteForm(instance=responsable)
    
    return render(request, 'respensableorganisationunite/modifier.html', {'form': form})

# Supprimer un Responsable
def supprimer_RespensableOrganisationUnite(request, id):
    responsable = get_object_or_404(ResponsableOrganisationUnite, id=id)  # Récupérer le responsable existant par son ID
    
    if request.method == 'POST':
        responsable.delete()  # Supprimer le responsable
        messages.success(request, "Responsable supprimé avec succès.")  # Message de succès
        return redirect('RespensableOrganisationUnite:list')  # Rediriger vers la liste des responsables

    return render(request, 'respensableorganisationunite/supprimer.html', {'responsable': responsable})


def search_responsable_unite(request):
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

    return render(request, "RespensableOrganisationUnite/search.html", {"results": results, "query": query, "filter": filter_by})

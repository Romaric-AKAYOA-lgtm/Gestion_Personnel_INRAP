from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from Activation.models import Activation
from Employee.views import get_username_from_session
from .models import Fonction
from .forms import  FonctionForm
 
def fonction_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    fonction = Fonction.objects.all().order_by('designation')
    return render(request, 'fonction/fonction_list.html', {
       'username':username,  'fonction': fonction})

def fonction_create(request):
    if request.method == "POST":
        form = FonctionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fonction:fonction')
    else:
        form = FonctionForm()
    return render(request, 'fonction/fonction_form.html', {'form': form})

def fonction_detail(request, id):
    fonction= get_object_or_404(Fonction, id=id)
    return render(request, 'fonction/fonction_detail.html', {'directeur': fonction})

def modifier_fonction(request, id):
    fonction = get_object_or_404(Fonction, id=id)

    if request.method == "POST":
        form =FonctionForm(request.POST, instance=fonction)
        if form.is_valid():
            form.save()
            return redirect('fonction:fonction')  # Redirigez vers la liste des fonction après la sauvegarde
    else:
        form =FonctionForm (instance=fonction)  # Remplir le formulaire avec les données existantes

    return render(request, 'fonction/fonction_form_edit.html', {'form': form, 'fonction': fonction})

def supprimer_fonction(request, id):
    fonction = get_object_or_404(Fonction , id=id)
    fonction.delete()
    return redirect('fonction:fonction')


def fonction_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    query = request.GET.get('query', '').strip()  # Récupérer la requête de recherche et supprimer les espaces inutiles
    
    # Récupérer les spécialités en fonction de la recherche
    fonction = Fonction.objects.all().order_by('designation')
    
    if query:
        fonction = fonction.filter(designation__icontains=query)

    return render(request, 'specialite/search.html', {
        'username':username, 
        'fonction': fonction,
        'query': query,
    })

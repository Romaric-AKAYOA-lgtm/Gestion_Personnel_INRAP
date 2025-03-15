from django.shortcuts import get_object_or_404, redirect, render
from Activation.models import Activation
from Employee.views import get_username_from_session
from .models import Stagiaire
from .forms import StagiaireForm

def stagiaire_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    stagiaires = Stagiaire.objects.all()  # Récupérer tous les stagiaires
    return render(request, 'stagiaire/stagiaire_list.html', {
       'username': username, 'stagiaires': stagiaires})


def create_stagiaire(request):
    if request.method == 'POST':
        form = StagiaireForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarder le stagiaire dans la base de données
            return redirect('stagiaire:stagiaire_list')  # Rediriger vers la liste des stagiaires après la création
    else:
        form = StagiaireForm()  # Afficher un formulaire vide pour un nouveau stagiaire

    return render(request, 'stagiaire/create_stagiaire.html', {'form': form})


def modify_stagiaire(request, id):
    """Permet de modifier un stagiaire et de récupérer son tuteur."""
    stagiaire = get_object_or_404(Stagiaire, id=id)  # Récupérer le stagiaire avec l'ID donné

    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    if request.method == 'POST':
        form = StagiaireForm(request.POST, instance=stagiaire)  # Pré-remplir le formulaire avec les données existantes
        if form.is_valid():
            form.save()  # Sauvegarder les modifications
            return redirect('stagiaire:stagiaire_list')  # Rediriger vers la liste des stagiaires après modification
    else:
        form = StagiaireForm(instance=stagiaire)  # Afficher le formulaire avec les données existantes

    return render(request, 'stagiaire/modify_stagiaire.html', {
        'form': form,
        'stagiaire': stagiaire,  # Passer les données du stagiaire
        'username': username
    })

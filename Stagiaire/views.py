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

def stagiaire_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (nom, prénom, email, etc.)
    
    # Initialisation de la queryset avec tous les stagiaires
    stagiaires = Stagiaire.objects.all().order_by('nom')

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'username':
            stagiaires = stagiaires.filter(username__icontains=query)
        elif critere == 'prenom':
            stagiaires = stagiaires.filter(prenom__icontains=query)
        elif critere == 'nom':
            stagiaires = stagiaires.filter(nom__icontains=query)
        elif critere == 'email':
            stagiaires = stagiaires.filter(email__icontains=query)
        elif critere == 'telephone':
            stagiaires = stagiaires.filter(telephone__icontains=query)
        elif critere == 'matricule':
            stagiaires = stagiaires.filter(matricule__icontains=query)
        elif critere == 'status':
            stagiaires = stagiaires.filter(status__icontains=query)
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale
        stagiaires = stagiaires.filter(username__icontains=query) | stagiaires.filter(prenom__icontains=query) | stagiaires.filter(nom__icontains=query) | stagiaires.filter(email__icontains=query)

    # Ajouter d'autres filtres si nécessaire, par exemple date_debut, date_fin, etc.
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Appliquer les filtres supplémentaires uniquement si les champs sont remplis
    if date_debut:
        stagiaires = stagiaires.filter(date_debut__gte=date_debut)
    if date_fin:
        stagiaires = stagiaires.filter(date_fin__lte=date_fin)

    # Si aucune condition n'est remplie, on retourne un message disant qu'il n'y a pas de résultats
    if not stagiaires.exists():
        stagiaires = None  # Pas de stagiaires trouvés

    return render(request, 'stagiaire/search.html', {
        'stagiaires': stagiaires,
        'username': username,
        'query': query,
        'criteres': critere,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })

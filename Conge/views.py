from django.shortcuts import get_object_or_404, redirect, render

from Activation.models import Activation
from Employee.views import get_username_from_session
from .forms import CongeForm
from .models import Conge

# Vue pour afficher les congés
def liste_conges(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    conges = Conge.objects.all()
    return render(request, 'conge/liste_conges.html', {
       'username':username,  'conges': conges})

# Create your views here.
def ajouter_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('conge:liste_conges')
    else:
        form = CongeForm()
    return render(request, 'conge/ajouter_conge.html', {'form': form})

# Vue pour modifier un congé
def modifier_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)
    if request.method == 'POST':
        form = CongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            return redirect('conge:liste_conges')
    else:
        form = CongeForm(instance=conge)
    return render(request, 'conge/modifier_conge.html', {'form': form})

# Vue pour supprimer un congé
def supprimer_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)
    if request.method == 'POST':
        conge.delete()
        return redirect('conge:liste_conges')
    return render(request, 'conge/supprimer_conge.html', {'conge': conge})


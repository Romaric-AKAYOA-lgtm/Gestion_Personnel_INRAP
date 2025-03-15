from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from Activation.models import Activation
from Employee.views import get_username_from_session
from .models import Unite
from .forms import UniteForm
 
def unite_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    unite = Unite.objects.all().order_by('designation')
    return render(request, 'unite/unite_list.html', {
       'username':username, 'unite': unite})

def unite_create(request):
    if request.method == "POST":
        form = UniteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unite:unite')
    else:
        form = UniteForm()
    return render(request, 'unite/unite_form.html', {'form': form})


def modifier_unite(request, id):
    unite = get_object_or_404(Unite, id=id)

    if request.method == "POST":
        form =UniteForm(request.POST, instance=unite)
        if form.is_valid():
            form.save()
            return redirect('unite:unite')  # Redirigez vers la liste des fonction après la sauvegarde
    else:
        form = UniteForm (instance=unite)  # Remplir le formulaire avec les données existantes

    return render(request, 'unite/unite_form_edit.html', {'form': form, 'unite': unite})

def supprimer_unite(request, id):
    unite = get_object_or_404(Unite , id=id)
    unite.delete()
    return redirect('unite:unite')

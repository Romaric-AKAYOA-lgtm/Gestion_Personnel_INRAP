from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User  # Import du modèle User de Django
from .forms import LoginForm
from Activation.models import Activation
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from Activation.models import Activation
from fonction.models import Fonction
from specialite.models import Specialite
from .models import Employee
from .forms import EmployeeForm
from Activation.views import activation_view

def get_username_from_session(request):
    """Récupère le nom d'utilisateur depuis la session et redirige vers la page de connexion si aucun utilisateur n'est trouvé."""
    username = request.session.get('username', None)
    
    if not username:
        return None  # Aucun nom d'utilisateur trouvé dans la session
    return username
# Vue pour afficher tous les employés
def liste_employes(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    response = activation_view(request)
    if response.status_code == 302:  # Redirection si la clé est invalide
        return response
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Vérifier l'activation en appelant la fonction
    employes = Employee.objects.all()
    return render(request, 'Employee/liste_employes.html', {
       'username':username,  'employes': employes})

# Vue pour ajouter un employé
def ajouter_employe(request):
    form = EmployeeForm()
    specialite= Specialite.objects.all().order_by('designation')
    fonction=Fonction.objects.all().order_by('designation')
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Employee:lists')
    else:
        form = EmployeeForm()
    return render(request, 'Employee/ajouter_employe.html', {
        'form': form,
        'specialite':specialite, 
        'fonction':fonction
        })

# Vue pour modifier un employé
def modifier_employe(request, id):
    employe = get_object_or_404(Employee, id=id)
    specialite= Specialite.objects.all().order_by('designation')
    fonction=Fonction.objects.all().order_by('designation')
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('Employee:list')
    else:
        form = EmployeeForm(instance=employe)
    return render(request, 'Employee/modifier_employe.html', {
        'form': form,
         'specialite':specialite, 
        'fonction':fonction
        })

# Vue pour supprimer un employé
def supprimer_employe(request, id):
    employe = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employe.delete()
        return redirect('Employee:list')
    return render(request, 'Employee/supprimer_employe.html', {'employe': employe})


def secretaire_detail2(request, username, password):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """
    Vérifie si un secrétaire avec username et password existe,
    puis affiche ses détails.
    """
    secretaire = Employee.objects.filter(username=username).first()
    
    if not secretaire or not secretaire.check_password(password):
        return render(request, "secretaire/login.html", {"error": "Nom d'utilisateur ou mot de passe incorrect."})

    if secretaire.date_fin and secretaire.date_fin < now().date():
        return render(request, "Employee/login.html", {"error": "Votre accès est expiré."})

    return render(request, "Employee/detail.html", {"secretaire": secretaire})



def login_view(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""

    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """
    Gère l'authentification du secrétaire et du superutilisateur en utilisant une session.
    """
    try:
        activation = Activation.objects.latest("activated_on")
        if not activation.is_valid():
            print("Activation est invalide, redirection vers la page d'activation.")
            return redirect("Activation:activation_page")
    except Activation.DoesNotExist:
        print("Aucune activation trouvée, redirection vers la page d'activation.")
        return redirect("Activation:activation_page")

    error_message = None
    print("Formulaire de connexion reçu.")

    if request.method == "POST":
        print("Méthode POST détectée.")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(f"Nom d'utilisateur : {username}")
            print(f"Mot de passe : {password}")

            # Vérifier d'abord si l'utilisateur est un superuser
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password) and user.is_superuser:
                print(f"Connexion réussie pour le superutilisateur {username}.")
                request.session['superuser_id'] = user.id  # Stocker l'ID du superutilisateur
                return redirect("admin:index")  # Rediriger vers l'interface d'administration

            # Vérifier si le secrétaire existe avec ce username
            secretaire = Employee.objects.filter(username=username).first()

            if not secretaire:
                print("Aucun secrétaire trouvé avec ce nom d'utilisateur.")
                error_message = "Nom d'utilisateur incorrect."
            elif not secretaire.password:
                print("Mot de passe incorrect.", secretaire.password)
                error_message = "Mot de passe incorrect."
            elif secretaire.retirement_date and secretaire.retirement_date < now().date():
                print(f"L'accès est expiré pour {username}, date_fin : {secretaire.retirement_date}")
                error_message = "Votre accès est expiré."
            else:
                print(f"Connexion réussie pour {username}. Enregistrement de l'ID dans la session.")
                # Si toutes les vérifications sont réussies, on enregistre l'utilisateur dans la session
                request.session['secretaire_id'] = secretaire.id  # Stocker l'ID dans la session
                # Enregistrer également le username pour l'utiliser sur la page d'accueil
                request.session['username'] = username  # Ajouter le username à la session
                print("Redirection vers la page d'accueil.")
                return redirect("home")  # Rediriger vers l'accueil
        else:
            print("Le formulaire n'est pas valide.")
    else:
        print("Méthode GET détectée. Affichage du formulaire.")
        form = LoginForm()

    return render(request, "Employee/login.html", {"form": form, "error": error_message})

def logout_view(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """
    Déconnecte le secrétaire ou le superuser en supprimant la session.
    """
    request.session.flush()  # Supprime toutes les données de session
    return redirect("Employee:login")  # Rediriger vers la page de connexion



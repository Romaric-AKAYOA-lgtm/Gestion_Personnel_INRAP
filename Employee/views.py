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

    return render(request, 'Employee/login.html', {'form': form, 'error': error_message})


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


from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch  # Assurez-vous que 'inch' est bien importé ici
from .models import Employee
from datetime import datetime

def generate_employee_pdf(request):
    # Filtrage des employés : ceux qui sont actifs, et ceux qui sont en retraite et dont la date n'est pas atteinte
    current_date = datetime.today().date()

    active_employees = Employee.objects.filter(status='active')
    retired_employees = Employee.objects.filter(status='retired', retirement_date__gt=current_date)

    # Création du document PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees_report.pdf"'

    buffer = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Ajouter l'entête INRAP et République du Congo
    header = Paragraph("<b>INRAP</b>", style=getSampleStyleSheet()['Title'])
    header2 = Paragraph("<b>République du Congo</b>", style=getSampleStyleSheet()['Title'])
    elements.append(header)
    elements.append(header2)

    # Ajouter un espace avant le tableau
    elements.append(Spacer(1, 0.25 * inch))  # Utilisation de 'inch' ici

    # Définir les données du tableau : entêtes + données
    data = [
        ['Nom', 'Prénom', 'Matricule', 'Grade', 'Spécialité', 'Date de Prise de Service', 'Date de Retraite']
    ]

    # Ajout des employés actifs
    for employee in active_employees:
        data.append([ 
            employee.last_name, 
            employee.first_name, 
            employee.matricule, 
            employee.grade, 
            employee.specialty, 
            employee.start_date, 
            'Non applicable'
        ])

    # Ajout des employés en retraite
    for employee in retired_employees:
        data.append([ 
            employee.last_name, 
            employee.first_name, 
            employee.matricule, 
            employee.grade, 
            employee.specialty, 
            employee.start_date, 
            employee.retirement_date
        ])

    # Création du tableau
    table = Table(data)

    # Style du tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    # Ajouter le tableau au PDF
    elements.append(table)

    # Ajouter la concaténation de Brazzaville et de la date système en bas à droite
    footer_text = f"Brazzaville - {datetime.now().strftime('%d/%m/%Y')}"
    footer = Paragraph(footer_text, style=getSampleStyleSheet()['Normal'])
    elements.append(Spacer(1, 0.5 * inch))  # Ajouter de l'espace avant le footer

    # Alignement du footer à droite
    footer_table = Table([[footer]], colWidths=[400])
    footer_table.setStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT')])
    
    # Ajouter le footer
    elements.append(footer_table)

    # Générer le PDF
    buffer.build(elements)
    return response

def employee_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (username, first_name, email, etc.)
    
    # Initialisation de la queryset avec tous les employés
    employees = Employee.objects.all()

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'username':
            employees = employees.filter(username__icontains=query)
        elif critere == 'first_name':
            employees = employees.filter(first_name__icontains=query)
        elif critere == 'last_name':
            employees = employees.filter(last_name__icontains=query)
        elif critere == 'email':
            employees = employees.filter(email__icontains=query)
        elif critere == 'num_tel':
            employees = employees.filter(num_tel__icontains=query)
        elif critere == 'matricule':
            employees = employees.filter(matricule__icontains=query)
        elif critere == 'status':
            employees = employees.filter(status__icontains=query)
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale
        employees = employees.filter(username__icontains=query) | employees.filter(first_name__icontains=query) | employees.filter(last_name__icontains=query) | employees.filter(email__icontains=query)

    # Ajouter d'autres filtres si nécessaire, par exemple date_debut, date_fin, etc.
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Appliquer les filtres supplémentaires uniquement si les champs sont remplis
    if date_debut:
        employees = employees.filter(start_date__gte=date_debut)
    if date_fin:
        employees = employees.filter(retirement_date__lte=date_fin)

    # Si aucune condition n'est remplie, on retourne un message disant qu'il n'y a pas de résultats
    if not employees:
        employees = None  # Pas d'employés trouvés

    return render(request, 'employee/search.html', {
        'employees': employees,
        'username': username,
        'query': query,
        'criteres': critere,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })

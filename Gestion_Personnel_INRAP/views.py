from datetime import date, datetime, timedelta
from itertools import count
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.timezone import now
from django.http import HttpResponse
from django.template.loader import render_to_string
from Activation.models import Activation
from Conge.models import Conge
from Employee.models import Employee
from Employee.views import get_username_from_session
from OrganizationalUnit.models import OrganizationalUnit  # Si le modèle est dans le même fichier
# OU
from Activation.views import activation_view
from Stagiaire.models import Stagiaire

def home_view(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

     # Vérifier l'activation en appelant la fonction
    # Vérification de la validité de la clé d'activation via activation_view
    response = activation_view(request)
    if response.status_code == 302:  # Redirection si la clé est invalide
        return response
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session


    # 🔹 Gestion des employés récents (moins de 6 mois)
    today = now().date()
    six_mois_avant = today - timedelta(days=180)
    
    search_query = request.GET.get("search", "")
    employes = Employee.objects.all()
    
    if search_query:
        employes = employes.filter(Q(last_name__icontains=search_query) | Q(function__icontains=search_query))
    
    employes_recents = employes.filter(start_date__gte=six_mois_avant)

    # 🔹 Gestion des congés et affectations
    employes_retour_conge = Employee.objects.filter(conge__date_fin__lte=now()).distinct()

    # Calcul des âges
    employes_ages = [
        {
            "employe": emp,
            "age": today.year - emp.date_of_birth.year - ((today.month, today.day) < (emp.date_of_birth.month, emp.date_of_birth.day)),
        }
        for emp in employes
    ]

    tranche_30 = sum(1 for item in employes_ages if item["age"] < 30)
    tranche_50 = sum(1 for item in employes_ages if 30 <= item["age"] < 50)
    tranche_50_plus = sum(1 for item in employes_ages if 50 >= item["age"] >= 60)

    # 🔹 Récupérer les employés récents
    employes_recents = Employee.objects.order_by('-start_date')[:10]
    
    # 🔹 Récupérer les unités organisationnelles
    unites_organisationnelles = OrganizationalUnit.objects.all()[:10]

    # 🔹 Récupérer les employés dans chaque unité organisationnelle (basé sur l'organisation associée)
    #employes_par_unite = Employee.objects.values('start_date').annotate(nombre_employes=count('id')).order_by('id')[:10]
    #employe_en_conge = Conge.objects.all()
    employe_en_conge = Conge.objects.filter(date_debut__lte=today, date_fin__gte=today)
    return render(request, "home.html", {
         "username": username,  # Passer le nom d'utilisateur dans le contexte
       "employes": employes,
        "hommes": employes.filter(sexe="Homme").count(),
        "femmes": employes.filter(sexe="Femme").count(),
        "tranche_30": tranche_30,
        "tranche_50": tranche_50,
        "tranche_50_plus": tranche_50_plus,
         "employes_ages": employes_ages,
        'employes_recents': employes_recents,
         "employes_retour_conge": employes_retour_conge,
         "employes_en_conge": employe_en_conge, 
        'unites_organisationnelles': unites_organisationnelles,
       # 'employes_par_unite': employes_par_unite,
    })



from django.shortcuts import render
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from Employee.models import Employee

def fiche_employe_view(request, employe_id):
    """Affiche la fiche d'un employé sans les données de congé et de retraite."""
    
    employe = get_object_or_404(Employee, id=employe_id)
    
    return render(request, "fiche_employe.html", {
        'employe': employe,
    })


from django.shortcuts import render
from datetime import datetime

def print_options(request):
    # Récupérer les données nécessaires
    stagiaires = Stagiaire.objects.all()
    active_employees = Employee.objects.filter(status='active')
    on_leave_employees = Employee.objects.filter(status='on_leave')
    retiring_employees = Employee.objects.filter(retirement_date__year=datetime.now().year)

    return render(request, 'your_template.html', {
        'stagiaires': stagiaires,
        'active_employees': active_employees,
        'on_leave_employees': on_leave_employees,
        'retiring_employees': retiring_employees
    })
import io
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def print_results(request):
    # Récupérer les options sélectionnées
    print_options = request.GET.getlist('print_options')

    # Créer le buffer pour le PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Créer la liste des données à inclure dans le PDF
    data = []
    
    # Titre
    data.append(['', '', 'Rapport d\'Impression'])

    # Vérification des options et ajout des sections correspondantes
    if 'stagiaires' in print_options:
        stagiaires = Stagiaire.objects.all()
        data.append(['', '', 'Stagiaires'])
        data.append(['Nom', 'Prénom', 'Date de Naissance'])
        for stagiaire in stagiaires:
            data.append([stagiaire.nom, stagiaire.prenom, stagiaire.date_naissance.strftime("%d/%m/%Y")])

    if 'active_employees' in print_options:
        active_employees = Employee.objects.filter(status='active')
        data.append(['', '', 'Employés Actifs'])
        data.append(['Nom', 'Prénom', 'Statut'])
        for employee in active_employees:
            data.append([employee.first_name, employee.last_name, employee.status])

    if 'on_leave_employees' in print_options:
        on_leave_employees = Employee.objects.filter(status='on_leave')
        data.append(['', '', 'Employés en Congé'])
        data.append(['Nom', 'Prénom', 'Statut'])
        for employee in on_leave_employees:
            data.append([employee.first_name, employee.last_name, employee.status])

    if 'retiring_employees' in print_options:
        retiring_employees = Employee.objects.filter(retirement_date__year=datetime.now().year)
        data.append(['', '', 'Employés Partant à la Retraite'])
        data.append(['Nom', 'Prénom', 'Date de Retraite'])
        for employee in retiring_employees:
            data.append([employee.first_name, employee.last_name, employee.retirement_date.strftime("%d/%m/%Y")])

    # Créer le tableau
    table = Table(data)
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Ajouter le tableau au document
    doc.build([table])

    # Retourner la réponse HTTP avec le PDF généré
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_impression.pdf"'
    return response
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
from RespensableOrganisationUnite.models import ResponsableOrganisationUnite
from Stagiaire.models import Stagiaire
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.timezone import now
from Activation.models import Activation
from Conge.models import Conge
from Employee.models import Employee
from Employee.views import get_username_from_session

def home_view(request):
    """Affiche la page d'accueil avec gestion du personnel et vérification d'activation."""

    # Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")

    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    today = now().date()
    six_mois_avant = today - timedelta(days=180)

    search_query = request.GET.get("search", "")
    employes = Employee.objects.all()
    
    if search_query:
        employes = employes.filter(Q(last_name__icontains=search_query) | Q(function__icontains=search_query))
    
    # Employés récents (moins de 6 mois)
    employes_recents = employes.filter(start_date__gte=six_mois_avant)

    # Employés de retour de congé
    employes_retour_conge = Employee.objects.filter(conge__date_fin__lte=today).distinct()

    # Employés en congé actuellement
    employe_en_conge = Conge.objects.filter(date_debut__lte=today, date_fin__gte=today)

    # Calcul des âges pour identifier les employés en retraite
    employes_ages = [
        {
            "employe": emp,
            "age": today.year - emp.date_of_birth.year - ((today.month, today.day) < (emp.date_of_birth.month, emp.date_of_birth.day)),
        }
        for emp in employes
    ]
    tranche_30 = sum(1 for item in employes_ages if item["age"] < 30)
    tranche_50 = sum(1 for item in employes_ages if 30 <= item["age"] < 50)
    tranche_50_plus = sum(1 for item in employes_ages if 50 <= item["age"] < 60)

    # Employés partant à la retraite cette année
    employes_retraite_annee = [emp["employe"] for emp in employes_ages if emp["age"] == 60]

    # Employés déjà retraités
    employes_retraites = [emp["employe"] for emp in employes_ages if emp["age"] > 60]

    # Liste des responsables des unités
    responsables_unites = ResponsableOrganisationUnite.objects.all()

    return render(request, "home.html", {
        "username": username,
        "employes": employes,
        "hommes": employes.filter(sexe="Homme").count(),
        "femmes": employes.filter(sexe="Femme").count(),
        "tranche_30": tranche_30,
        "tranche_50": tranche_50,
        "tranche_50_plus": tranche_50_plus,
        "employes_ages": employes_ages,
        "employes_recents": employes_recents,
        "employes_retour_conge": employes_retour_conge,
        "employes_en_conge": employe_en_conge,
        "employes_retraite_annee": employes_retraite_annee,
        "employes_retraites": employes_retraites,
        "responsables_unites": responsables_unites,
    })

from django.http import HttpResponse
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import timedelta
from django.utils.timezone import now
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from django.shortcuts import redirect

def export_to_word(request):
    # Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")

    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    # Récupérer l'employé correspondant au username de l'utilisateur connecté
    try:
         employee = Employee.objects.get(username=username)
    except Employee.DoesNotExist:
        employee = None  # Si l'employé n'existe pas pour cet utilisateur, gérer le cas ici

    """
    Génère un document Word en fonction des choix de l'utilisateur.
    """
    selected_sections = request.GET.getlist('sections')  # Récupérer les sections choisies
    
    doc = Document()
    section_titles = {
        'employes': 'Liste des Employés',
        'employes_recents': 'Employés récents (moins de 6 mois)',
        'employes_en_conge': 'Employés en congé',
        'employes_revenant_de_conge': 'Employés revenant de congé',
        'employes_depart_retraite': 'Employés en départ pour la retraite (cette année)',
        'employes_retraites': 'Employés déjà retraités',
        'stagiaires': 'Liste des Stagiaires'
    }
    
    # Changer l'orientation du document en paysage
    section = doc.sections[0]
    new_width = section.page_width
    new_height = section.page_height
    section.page_width = new_height
    section.page_height = new_width
    
    doc.add_heading('Rapport de Gestion du Personnel', level=1)
    
    # Liste des employés
    if 'employes' in selected_sections:
        doc.add_heading(section_titles['employes'], level=2)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Spécialité'
        hdr_cells[2].text = 'Date de début'
        for emp in Employee.objects.all():
            row_cells = table.add_row().cells
            row_cells[0].text = f"{emp.first_name} {emp.last_name}"
            row_cells[1].text = emp.specialty.designation
            row_cells[2].text = str(emp.start_date)
    
    # Liste des employés récents (moins de 6 mois)
    if 'employes_recents' in selected_sections:
        doc.add_heading(section_titles['employes_recents'], level=2)
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Date de début'
        six_mois_avant = now().date() - timedelta(days=180)
        employes_recents = Employee.objects.filter(start_date__gte=six_mois_avant)
        for emp in employes_recents:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{emp.first_name} {emp.last_name}"
            row_cells[1].text = str(emp.start_date)
    
    # Liste des employés en congé
    if 'employes_en_conge' in selected_sections:
        doc.add_heading(section_titles['employes_en_conge'], level=2)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Date de début'
        hdr_cells[2].text = 'Date de fin'
        today = now().date()
        employes_conge = Conge.objects.filter(date_debut__lte=today, date_fin__gte=today)
        for conge in employes_conge:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{conge.employe.first_name} {conge.employe.last_name}"
            row_cells[1].text = str(conge.date_debut)
            row_cells[2].text = str(conge.date_fin)
    
    # Employés revenant de congé
    if 'employes_revenant_de_conge' in selected_sections:
        doc.add_heading(section_titles['employes_revenant_de_conge'], level=2)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Date de début'
        hdr_cells[2].text = 'Date de retour'
        today = now().date()
        employes_revenant = Conge.objects.filter(date_fin__gte=today)
        for conge in employes_revenant:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{conge.employe.last_name} {conge.employe.first_name}"
            row_cells[1].text = str(conge.date_debut)
            row_cells[2].text = str(conge.date_fin)
    
    # Employés en départ pour la retraite cette année
    if 'employes_depart_retraite' in selected_sections:
        doc.add_heading(section_titles['employes_depart_retraite'], level=2)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Date de naissance'
        hdr_cells[2].text = 'Date de départ'
        today = now().date()
        start_of_year = today.replace(month=1, day=1)
        end_of_year = today.replace(month=12, day=31)
        employes_depart_retraite = Employee.objects.filter(retirement_date__gte=start_of_year, retirement_date__lte=end_of_year)
        for emp in employes_depart_retraite:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{emp.first_name} {emp.last_name}"
            row_cells[1].text = str(emp.date_of_birth)
            row_cells[2].text = str(emp.retirement_date)
    
    # Employés déjà retraités
    if 'employes_retraites' in selected_sections:
        doc.add_heading(section_titles['employes_retraites'], level=2)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Date de naissance'
        hdr_cells[2].text = 'Date de retraité'
        employes_retraites = Employee.objects.filter(retirement_date__lt=now().date())
        for emp in employes_retraites:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{emp.first_name} {emp.last_name}"
            row_cells[1].text = str(emp.date_of_birth)
            row_cells[2].text = str(emp.retirement_date)
    
    # Liste des stagiaires cette année et les années antérieures
    if 'stagiaires' in selected_sections:
        doc.add_heading(section_titles['stagiaires'], level=2)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nom Complet'
        hdr_cells[1].text = 'Prénom'
        hdr_cells[2].text = 'Année'
        this_year = now().year
        stagiaires = Stagiaire.objects.filter(date_debut_stage__year__lte=this_year)
        for stagiaire in stagiaires:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{stagiaire.nom} {stagiaire.prenom}"
            row_cells[1].text = stagiaire.prenom
            row_cells[2].text = str(stagiaire.date_debut_stage.year)

    # Ajout de "BRAZZAVILLE" + date système en bas à droite du document
    footer = doc.sections[-1].footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    paragraph.add_run("BRAZZAVILLE - " + now().strftime("%Y-%m-%d")).font.size = Pt(8)

    # Ajouter le nom et prénom de l'employé connecté si il existe
    if employee:
        paragraph.add_run(f"{employee.first_name} {employee.last_name}")  # Nom et prénom de l'employé connecté
    else:
        paragraph.add_run("Nom et prénom de l'employé connecté")  # Au cas où l'employé n'est pas trouvé
 
    # Enregistrement du document
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="rapport_personnel.docx"'
    doc.save(response)
    return response


def export_word_view(request):
    # Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")

    username = get_username_from_session(request)
    if not username:
        return redirect('login')
    """Page d'exportation"""
    return render(request, "export_to_word.html", {'username':username})
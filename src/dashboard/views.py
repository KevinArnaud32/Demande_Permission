from django.contrib.auth.decorators import login_required
from itertools import chain
from core.decorators import role_required
from demande.models.conges_model import Conges
from demande.models.permission_model import Permission
from demande.models.repos_maladie_model import ReposMaladie
from employe.models.departement_model import Departement
from employe.models.employe_model import Employe
from django.shortcuts import render, redirect
from employe.models.utilisateur_model import Utilisateur


# Create your views here.
@login_required
def dashboard(request):

    if request.user.role == "admin":
        return redirect('admin_dashboard')

    elif request.user.role == "rh":
        return redirect('rh_dashboard')

    elif request.user.role == "manager":
        return redirect('manager_dashboard')
    elif request.user.role == 'employe':
        return redirect('employe_dashboard')



@login_required
@role_required('admin')
def admin_dashboard(request):

    nombre_employe = Employe.objects.all().count()
    nombre_departement = Departement.objects.all().count()
    nombre_manager = Utilisateur.objects.filter(role='manager').count()
    nombre_rh = Utilisateur.objects.filter(role='rh').count()

    dernier_utilisateurs = Utilisateur.objects.order_by('-date_creation')[:5]
    dernier_employes = Employe.objects.select_related('departement', 'fonction').order_by('-id')[:5]


    context = {
        'nombre_employe': nombre_employe,
        'nombre_departement': nombre_departement,
        'nombre_manager': nombre_manager,
        'nombre_rh': nombre_rh,
        'derniers_utilisateurs': dernier_utilisateurs,
        'derniers_employes': dernier_employes,
    }

    return render(request,'dashboard/admin_dashboard.html', context)



@login_required
@role_required('rh')
def rh_dashboard(request):
    return render(request,'dashboard/rh_dashboard.html')



@login_required
@role_required('manager')
def manager_dashboard(request):
    return render( request,'dashboard/manager_dashboard.html')



@login_required
@role_required('employe')
def employe_dashboard(request):

    employe = request.user.employe

    # derniers demandes
    permissions = Permission.objects.filter(employe=employe)
    conges = Conges.objects.filter(employe=employe)
    repos_maladies = ReposMaladie.objects.filter(employe=employe)

    # Ajouter un attribut "type" pour l'affichage
    for p in permissions:
        p.type = "Permission"

    for c in conges:
        c.type = "Congé"

    for r in repos_maladies:
        r.type = "Repos maladie"

    # Fusionner et trier par date de création décroissante
    dernieres_demandes = sorted(
        chain(permissions, conges, repos_maladies),
        key=lambda demande: demande.date_creation,
        reverse=True
    )[:5]

    # total demandes
    total_permissions = Permission.objects.filter(employe=employe).count()
    total_repos_maladies = ReposMaladie.objects.filter(employe=employe).count()
    total_conges = Conges.objects.filter(employe=employe).count()

    total_demandes = total_conges + total_repos_maladies + total_permissions

    # demande en attente
    permission_attente = Permission.objects.filter(statut='en attente', employe=employe).count()
    repos_maladie_attente = ReposMaladie.objects.filter(statut='en attente', employe=employe).count()
    conges_attente = Conges.objects.filter(statut='en attente', employe=employe).count()

    demandes_attente = permission_attente + repos_maladie_attente + conges_attente

    # demande accpetée

    permission_accepte = Permission.objects.filter(statut='accepte', employe=employe).count()
    repos_maladie_accepte = ReposMaladie.objects.filter(statut='accepte', employe=employe).count()
    conges_accepte = Conges.objects.filter(statut='accepte', employe=employe).count()

    demande_accepte = permission_accepte + repos_maladie_accepte + conges_accepte

    context = {
        'total_demandes': total_demandes,
        'demandes_attente': demandes_attente,
        'total_conges': total_conges,
        'demande_accepte': demande_accepte,
        'dernieres_demandes': dernieres_demandes,
    }

    return render(request,'dashboard/employe_dashboard.html', context)
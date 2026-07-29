from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from demande.models.permission_model import Permission
from demande.models.conges_model import Conges
from demande.models.repos_maladie_model import ReposMaladie



@login_required
def suivi_demandes(request):

    user = request.user

    permissions = Permission.objects.none()
    conges = Conges.objects.none()
    repos = ReposMaladie.objects.none()

    # ================= EMPLOYE =================

    if user.role == "employe":

        employe = user.employe

        permissions = Permission.objects.filter(employe=employe)
        conges = Conges.objects.filter(employe=employe)
        repos = ReposMaladie.objects.filter(employe=employe)

    # ================= MANAGER =================

    elif user.role == "manager":

        departement = user.employe.departement

        permissions = Permission.objects.filter(
            employe__departement=departement
        ).exclude(
            employe=user.employe
        )

        # Les congés sont traités par les RH
        conges = Conges.objects.none()

        repos = ReposMaladie.objects.filter(
            employe__departement=departement
        ).exclude(
            employe=user.employe
        )

    # ================= RH =================

    elif user.role == "rh":

        departement = user.employe.departement

        # Toutes les demandes de congés
        conges = Conges.objects.all()

        # Permissions du département RH
        permissions = Permission.objects.filter(
            employe__departement=departement
        ).exclude(
            employe=user.employe
        )

        # Repos maladie du département RH
        repos = ReposMaladie.objects.filter(
            employe__departement=departement
        ).exclude(
            employe=user.employe
        )

    # ================= ADMIN =================

    elif user.role == "admin" or user.is_superuser:

        permissions = Permission.objects.all()
        conges = Conges.objects.all()
        repos = ReposMaladie.objects.all()

    else:

        return redirect("login")

    # ================= TYPE =================

    for permission in permissions:
        permission.type = "Permission"

    for conge in conges:
        conge.type = "Congé"

    for repos_maladie in repos:
        repos_maladie.type = "Repos maladie"

    # ================= FUSION =================

    demandes = sorted(
        chain(
            permissions,
            conges,
            repos,
        ),
        key=lambda x: x.date_creation,
        reverse=True
    )

    # ================= FILTRES =================

    type_demande = request.GET.get("type")
    statut = request.GET.get("statut")
    recherche = request.GET.get("search")

    if type_demande:
        demandes = [
            d for d in demandes
            if d.type.lower().startswith(type_demande.lower())
        ]

    if statut:
        demandes = [
            d for d in demandes
            if d.statut == statut
        ]

    if recherche:
        recherche = recherche.lower()

        demandes = [

            d for d in demandes

            if (
                    hasattr(d, "motif")
                    and recherche in d.motif.lower()
            )

        ]

    # ================= STATISTIQUES =================

    total_demandes = len(demandes)

    total_attente = len([
        d for d in demandes
        if d.statut == "en attente"
    ])

    total_acceptees = len([
        d for d in demandes
        if d.statut == "accepte"
    ])

    total_refusees = len([
        d for d in demandes
        if d.statut == "refuse"
    ])

    context = {

        "today": timezone.now(),

        "demandes": demandes,

        "total_demandes": total_demandes,

        "total_attente": total_attente,

        "total_acceptees": total_acceptees,

        "total_refusees": total_refusees,

    }

    return render(request,"demande/index.html",context)
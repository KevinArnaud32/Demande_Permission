from django.contrib.auth.decorators import login_required
from employe.models.employe_model import Employe
from demande.models.conges_model import Conges
from demande.models.permission_model import Permission
from demande.models.repos_maladie_model import ReposMaladie
from django.shortcuts import render

# Create your views here.
@login_required
def dashboard(request):

    user = request.user

    permissions = Permission.objects.none()

    conges = Conges.objects.none()

    repos = ReposMaladie.objects.none()

    # ================= EMPLOYE =================

    if user.role == 'employe':

        permissions = Permission.objects.filter(
            employe=user.employe
        )

        conges = Conges.objects.filter(
            employe=user.employe
        )

        repos = ReposMaladie.objects.filter(
            employe=user.employe
        )

    # ================= MANAGER =================

    elif user.role == 'manager':

        subordonnes = Employe.objects.filter(
            superieur=user.employe
        )

        permissions = Permission.objects.filter(
            employe__in=subordonnes
        )

        conges = Conges.objects.filter(
            employe__in=subordonnes
        )

        repos = ReposMaladie.objects.filter(
            employe__in=subordonnes
        )

    # ================= RH / ADMIN =================

    elif user.role in ['rh', 'admin']:

        permissions = Permission.objects.all()

        conges = Conges.objects.all()

        repos = ReposMaladie.objects.all()

    context = {

        'permissions_count': permissions.count(),

        'conges_count': conges.count(),

        'repos_count': repos.count(),

        'permissions_attente': permissions.filter(
            statut='en attente'
        ).count(),

        'conges_attente': conges.filter(
            statut='en attente'
        ).count(),

        'repos_attente': repos.filter(
            statut='en attente'
        ).count(),

        'latest_permissions': permissions.order_by(
            '-id'
        )[:5],

        'latest_conges': conges.order_by(
            '-id'
        )[:5],

        'latest_repos': repos.order_by(
            '-id'
        )[:5],

    }

    return render(request,'dashboard/index.html', context)




@login_required
def admin_dashboard(request):
    return render(request,'dashboard/admin_dashboard.html')



@login_required
def rh_dashboard(request):
    return render(request,'dashboard/rh_dashboard.html')



@login_required
def manager_dashboard(request):
    return render( request,'dashboard/manager_dashboard.html')



@login_required
def employe_dashboard(request):
    return render(request,'dashboard/employe_dashboard.html')
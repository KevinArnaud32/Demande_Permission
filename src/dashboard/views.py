from django.contrib.auth.decorators import login_required

from core.decorators import role_required
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
    return render(request,'dashboard/employe_dashboard.html')
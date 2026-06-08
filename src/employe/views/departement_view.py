from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.decorators import role_required
from employe.models.departement_model import Departement
from employe.forms.departement_form import DepartementForm


@login_required()
def departement_list(request):

    departements = Departement.objects.all()

    context = {
        'departements': departements,
    }

    return render(request, 'departement/index.html', context)



@login_required()
@role_required('admin')
def departement_create(request):

    if request.user.role != 'admin':
        return redirect('login')


    if request.method == 'POST':

        departement_form = DepartementForm(request.POST)

        if departement_form.is_valid():

            departement_form.save()
            return redirect('departement_list')

    else:
        departement_form = DepartementForm()

    context = {
        'departement_form': departement_form,
    }

    return render(request, 'departement/create.html', context)
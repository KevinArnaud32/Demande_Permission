from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import role_required
from employe.forms.utilisateur_form import UtilisateurForm
from employe.forms.employe_form import EmployeForm
from employe.forms.fonction_form import FonctionForm
from employe.models.utilisateur_model import Utilisateur
from employe.models.employe_model import Employe


@login_required()
def utilisateur_create(request):

    if request.user.role != 'admin':
        return redirect('login')


    form_utilisateur = UtilisateurForm()
    form_employe = EmployeForm()
    form_fonction = FonctionForm

    if request.method == 'POST':
        form_utilisateur = UtilisateurForm(request.POST)
        form_employe = EmployeForm(request.POST)
        form_fonction = FonctionForm(request.POST)

        if form_utilisateur.is_valid() and form_employe.is_valid() and form_fonction.is_valid():

            utilisateur = form_utilisateur.save(commit=False)
            utilisateur.set_password(form_utilisateur.cleaned_data['password'])
            utilisateur.save()

            fonction = form_fonction.save()

            superieur = None

            employe = form_employe.save(commit=False)
            employe.utilisateur = utilisateur
            employe.fonction = fonction

            if Utilisateur.role == 'employe':
                superieur = Employe.objects.filter(departement=employe.departement, utilisateur__role='manager')

            employe.superieur = superieur

            employe.save()

            return redirect('utilisateur_list')

    print(form_utilisateur.errors)
    print(form_employe.errors)
    print(form_fonction.errors)


    context = {
        'form_utilisateur': form_utilisateur,
        'form_employe': form_employe,
        'form_fonction': form_fonction,
    }

    return render(request, "utilisateur/create.html", context)



@login_required()
def utilisateur_list(request):

    if request.user.role != 'admin':
        return redirect('login')

    utilisateurs = Utilisateur.objects.all().order_by('-id')

    context = {
        'utilisateurs': utilisateurs,
    }

    return render(request, 'utilisateur/index.html', context)



@login_required()
@role_required('admin')
def utilisateur_detail(request, id):

     utilisateur = get_object_or_404(Utilisateur, id=id)

     context = {
         'utilisateur': utilisateur,
     }

     return render(request, 'utilisateur/detail.html', context)



@login_required()
@role_required('admin')
def utilisateur_update(request, id):

    if request.user.role != "admin":
        return redirect("login")

    utilisateur = get_object_or_404(Utilisateur, id=id)

    employe = Employe.objects.filter(utilisateur=utilisateur).first()

    if request.method == 'POST':

        utilisateur_form = UtilisateurForm(request, instance=utilisateur)
        employe_form = EmployeForm(request, instance=employe)

        if utilisateur_form.is_valid() and utilisateur_form.is_valid():
            utilisateur_form.save()
            employe_form.save()

            return redirect('utilisateur_list')
    else:

        utilisateur_form = UtilisateurForm(instance=utilisateur)
        employe_form = EmployeForm(instance=employe)

    context = {
        'utilisateur': utilisateur,
        'utilisateur_form': utilisateur_form,
        'employe_form': employe_form,
        'edit': True,
    }


    return render(request, 'utilisateur/update.html', context)



@login_required()
def utilisateur_detele(request, id):

    utilisateur = get_object_or_404(Utilisateur, pk=id)

    utilisateur.is_deleted = True
    utilisateur.save()

    return render(request, 'utilisateur/index.html')
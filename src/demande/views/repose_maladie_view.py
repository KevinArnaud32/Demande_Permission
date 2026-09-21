from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from demande.models.repos_maladie_model import ReposMaladie
from demande.forms.repos_maladie_form import ReposMaladieForm
from demande.models.validation_model import Validation
from utils.email import notifier_manager, envoyer_mail_repos_maladie


@login_required()
def repos_maladie_list(request):

    user = request.user

    employe = request.user.employe

    repos_maladies = None

    if user.role == 'employe':
        repos_maladies = ReposMaladie.objects.filter(statut='en attente', employe=employe).order_by('-date_creation')
    elif user.role == 'admin':
        repos_maladies = ReposMaladie.objects.all().order_by('-date_creation')
    elif user.role in ['manager', 'rh']:
        repos_maladies = ReposMaladie.objects.filter(employe__departement=user.employe.departement).exclude(employe=employe)

    context = {
        'repos_maladies': repos_maladies
    }

    return render(request,'repos_maladie/index.html', context)


@login_required()
def repos_maladie_create(request):

    employe = request.user.employe

    repos_maladie_form = ReposMaladieForm()

    if request.method == 'POST':

        repos_maladie_form = ReposMaladieForm(request.POST, request.FILES)

        if repos_maladie_form.is_valid():
            repos = repos_maladie_form.save(commit=False)
            repos.employe = employe
            repos.save()
            notifier_manager(repos)

            return redirect('repos_maladie_list')


    context = {
        'repos_maladie_form': repos_maladie_form
    }

    return render(request, 'repos_maladie/create.html', context)




@login_required()
def repos_maladie_detail(request, pk):

    repos_maladie = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    context = {
        'repos_maladie': repos_maladie
    }

    return render(
        request,
        'repos_maladie/detail.html',
        context
    )


@login_required()
def repos_maladie_update(request, pk):

    repos_maladie = get_object_or_404(ReposMaladie, pk=pk)

    repos_maladie_form = ReposMaladieForm(instance=repos_maladie)

    if request.method == 'POST':

        repos_maladie_form = ReposMaladieForm(request.POST, request.FILES, instance=repos_maladie)

        if repos_maladie_form.is_valid():
            repos_maladie_form.save()

            return redirect('repos_maladie_list')


    context = {
        'repos_maladie_form': repos_maladie_form
    }

    return render(request, 'repos_maladie/update.html', context)


@login_required()
def repos_maladie_delete(request, pk):

    repos_maladie = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    repos_maladie.delete()

    return redirect(
        'repos_maladie_list'
    )






@login_required()
def valider_repos_maladie(request, pk):

    repos_maladie = get_object_or_404(ReposMaladie, pk=pk)

    user = request.user

    # Empêcher de valider sa propre demande
    if repos_maladie.employe == user.employe:
        messages.error(
            request,
            "Vous ne pouvez pas valider votre propre demande."
        )
        return redirect("repos_maladie_detail", pk=pk)

    # Vérifier le statut
    if repos_maladie.statut != "en attente":
        messages.warning(
            request,
            "Cette demande a déjà été traitée."
        )
        return redirect("repos_maladie_detail", pk=pk)

    # Accepter la demande
    repos_maladie.statut = "accepte"
    repos_maladie.save()

    # Envoyer l'email
    envoyer_mail_repos_maladie(repos_maladie)

    # Notifier le responsable RH si cette fonction existe
    # notifier_rh_repos_maladie(repos_maladie)

    # Historique de la validation
    Validation.objects.create(
        demande_id=repos_maladie.id,
        validateur=user,
        type_demande="repos_maladie",
        decision="accepte",
        commentaire="Demande de repos maladie validée"
    )


    return redirect("repos_maladie_detail", pk=pk)



@login_required()
def refuser_repos_maladie(request, pk):

    repos_maladie = get_object_or_404(ReposMaladie, pk=pk)

    user = request.user

    # Empêcher de refuser sa propre demande
    if repos_maladie.employe == user.employe:
        messages.error(
            request,
            "Vous ne pouvez pas refuser votre propre demande."
        )
        return redirect("repos_maladie_detail", pk=pk)

    # Vérifier le statut
    if repos_maladie.statut != "en attente":
        messages.warning(
            request,
            "Cette demande a déjà été traitée."
        )
        return redirect("repos_maladie_detail", pk=pk)

    # Refuser la demande
    repos_maladie.statut = "refuse"
    repos_maladie.save()

    # Envoyer l'email de refus
    # envoyer_mail_refus_repos_maladie(repos_maladie)

    # Historique du refus
    Validation.objects.create(
        demande_id=repos_maladie.id,
        validateur=user,
        type_demande="repos_maladie",
        decision="refuse",
        commentaire="Demande de repos maladie refusée"
    )


    return redirect("repos_maladie_detail", pk=pk)

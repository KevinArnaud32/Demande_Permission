from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.decorators import role_required
from demande.models.conges_model import Conges
from demande.forms.conges_form import CongesForm
from demande.models.validation_model import Validation
from utils.email import notifier_manager


def conge_list(request):

    employe = request.user.employe

    user = request.user

    conges = None

    if user.role == 'employe':
        conges = Conges.objects.filter(employe=employe)
    elif user.role == 'rh':
        conges = Conges.objects.all().order_by('-date_creation')
    elif user.role == 'manager':
        conges = Conges.objects.filter(employe__departement=user.employe.departement)


    context = {
        'conges': conges
    }

    return render(request,'conge/index.html', context)


@login_required()
@role_required('employe')
def conge_create(request):

    employe = request.user.employe

    conges_form = CongesForm()

    if request.method == 'POST':

        conges_form = CongesForm(request.POST)

        if conges_form.is_valid():

            conges = conges_form.save(commit=False)
            conges.employe = employe
            conges.save()
            notifier_manager(conges)

            return redirect('conge_list')

    context = {
        'conges_form': conges_form,
    }


    return render(request,'conge/create.html', context)



def conge_detail(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    context = {
        'conge': conge
    }

    return render(
        request,
        'conge/detail.html',
        context
    )



@login_required
def conge_update(request, pk):

    conge = get_object_or_404(Conges, pk=pk)


    if request.user.role == "employe" and conge.employe.utilisateur != request.user:

        messages.error(
            request,
            "Vous n'êtes pas autorisé à modifier cette demande."
        )
        return redirect("conge_list")


    # Empêcher la modification si la demande n'est plus en attente
    if conge.statut != "en attente":
        messages.warning(request,"Cette demande ne peut plus être modifiée car elle a déjà été traitée.")
        return redirect("conges_list")


    if request.method == "POST":
        conges_form = CongesForm(request.POST, instance=conge)

        if conges_form.is_valid():
            conges_form.save()

            messages.success(request,"La demande de congé a été modifiée avec succès.")

            return redirect("conge_list")

    else:
        conges_form = CongesForm(instance=conge)

    context = {
        'conges_form': conges_form,
        'conge': conge,
    }

    return render(request,"conge/update.html", context)



def conge_delete(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    conge.delete()

    return redirect('conge_list')



@login_required()
def valider_conge(request, pk):

    conge = get_object_or_404(Conges, pk=pk)

    user = request.user

    # Empêcher de valider sa propre demande
    if conge.employe == user.employe:
        messages.error(request, "Vous ne pouvez pas valider votre propre demande.")
        return redirect("permission_detail", pk=pk)

    # Vérifier le statut
    if conge.statut != "en attente":
        messages.warning(request, "Cette demande a déjà été traitée.")
        return redirect("permission_detail", pk=pk)


    conge.statut = 'accepte'
    conge.save()

    # Historique
    Validation.objects.create(
        demande_id=conge.id,
        validateur=user,
        type_demande="conge",
        decision="accepte",
        commentaire="Demande validée"
    )


    return redirect('conge_detail', pk=pk)



@login_required()
def refuser_conge(request, pk):

    conge = get_object_or_404(Conges, pk=pk)

    user = request.user

    # Empêcher de valider sa propre demande
    if conge.employe == user.employe:
        messages.error(request, "Vous ne pouvez pas valider votre propre demande.")
        return redirect("permission_detail", pk=pk)

    # Vérifier le statut
    if conge.statut != "en attente":
        messages.warning(request, "Cette demande a déjà été traitée.")
        return redirect("permission_detail", pk=pk)


    conge.statut = 'refuse'
    conge.save()

    # Historique
    Validation.objects.create(
        demande_id=conge.id,
        validateur=user,
        type_demande="conge",
        decision="refuse",
        commentaire="Demande refusée"
    )


    return redirect('conge_detail', pk=pk)

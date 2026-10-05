from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.decorators import role_required
from demande.models.conges_model import Conges
from demande.forms.conges_form import CongesForm
from demande.models.validation_model import Validation
from demande.services.service_notification import creer_notification
from employe.models.utilisateur_model import Utilisateur
from utils.email import notifier_manager, envoyer_mail_conge, notifier_rh, envoyer_mail_refus_manager


def conge_list(request):

    user = request.user

    conges = None

    if user.role == 'employe':

        conges = Conges.objects.filter(
            employe=user.employe
        ).order_by('-id')

    elif user.role == 'rh':

        conges = Conges.objects.all().order_by('-date_creation')

    elif user.role == 'manager':

        conges = Conges.objects.filter(
            employe__departement=user.employe.departement
        ).order_by('-id')

    elif user.role == 'admin' or user.is_superuser:

        conges = Conges.objects.all().order_by('-date_creation')


    # Ajouter les informations de validation
    for conge in conges:

        # Vérifier si le supérieur a validé
        if conge.employe.superieur:

            conge.validation_superieur = Validation.objects.filter(
                demande_id=conge.id,
                type_demande="conge",
                decision="accepte",
                validateur=conge.employe.superieur.utilisateur
            ).exists()

        else:

            conge.validation_superieur = False


        # Vérifier si une RH a déjà traité la demande
        conge.validation_rh = Validation.objects.filter(
            demande_id=conge.id,
            type_demande="conge",
            validateur__role="rh"
        ).exists()


    context = {
        'conges': conges
    }

    return render(
        request,
        'conge/index.html',
        context
    )



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

            if employe.superieur:
                creer_notification(
                    destinataire=employe.superieur.utilisateur,
                    titre="Nouvelle demande de congé",
                    message=(
                        f"{employe.prenom} {employe.nom} "
                        f"a soumis une nouvelle demande de congé."
                    ),
                    type_notification="nouvelle_demande",
                    demande_id=conges.id,
                    type_demande="conge"
                )

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

    # ================= VALIDATION SUPERIEUR =================

    validation_superieur_obj = None

    if conge.employe.superieur:

        validation_superieur_obj = Validation.objects.filter(
            demande_id=conge.id,
            type_demande="conge",
            validateur=conge.employe.superieur.utilisateur
        ).order_by("-date_creation").first()

    validation_superieur = (
        validation_superieur_obj is not None
        and validation_superieur_obj.decision == "accepte"
    )


    # ================= VALIDATION RH =================

    validation_rh_obj = Validation.objects.filter(
        demande_id=conge.id,
        type_demande="conge",
        validateur__role="rh"
    ).order_by("-date_creation").first()

    validation_rh = (
        validation_rh_obj is not None
        and validation_rh_obj.decision == "accepte"
    )


    # ================= HISTORIQUE =================

    historique_validations = Validation.objects.filter(
        demande_id=conge.id,
        type_demande="conge"
    ).select_related(
        "validateur"
    ).order_by(
        "date_creation"
    )


    context = {
        'conge': conge,

        'validation_superieur': validation_superieur,
        'validation_superieur_obj': validation_superieur_obj,

        'validation_rh': validation_rh,
        'validation_rh_obj': validation_rh_obj,

        'historique_validations': historique_validations,
    }

    return render(request,'conge/detail.html',context)


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

    conge = get_object_or_404(Conges, pk=pk)

    conge.delete()

    return redirect('conge_list')



@login_required()
def valider_conge(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    user = request.user

    # Vérifier que seul le supérieur peut effectuer cette validation
    if not conge.employe.superieur:
        messages.error(
            request,
            "Cette demande ne possède pas de supérieur désigné."
        )
        return redirect(
            "conge_detail",
            pk=pk
        )

    if conge.employe.superieur.utilisateur != user:
        messages.error(
            request,
            "Vous n'êtes pas autorisé à valider cette demande."
        )
        return redirect(
            "conge_detail",
            pk=pk
        )

    # Empêcher de valider sa propre demande
    if conge.employe == user.employe:

        messages.error(
            request,
            "Vous ne pouvez pas valider votre propre demande."
        )

        return redirect(
            "conge_detail",
            pk=pk
        )

    # Vérifier le statut
    if conge.statut != "en attente":

        messages.warning(
            request,
            "Cette demande a déjà été traitée."
        )

        return redirect(
            "conge_detail",
            pk=pk
        )

    # Validation du supérieur
    conge.statut = "accepte"
    conge.save()

    # Notification à la RH
    rh_utilisateurs = Utilisateur.objects.filter(
        role="rh"
    )

    for rh in rh_utilisateurs:

        creer_notification(
            destinataire=rh,
            titre="Nouvelle validation de congé",
            message=(
                f"{conge.employe.prenom} {conge.employe.nom} "
                "a une demande de congé validée par son supérieur "
                "qui nécessite votre validation."
            ),
            type_notification="nouvelle_demande",
            demande_id=conge.id,
            type_demande="conge"
        )

    # Historique de validation du supérieur
    Validation.objects.create(
        demande_id=conge.id,
        validateur=user,
        type_demande="conge",
        decision="accepte",
        commentaire="Demande validée par le supérieur"
    )

    return redirect(
        "conge_detail",
        pk=pk
    )



@login_required()
def refuser_conge(request, pk):

    conge = get_object_or_404(Conges, pk=pk)

    user = request.user

    # Empêcher de valider sa propre demande
    if conge.employe == user.employe:
        messages.error(request, "Vous ne pouvez pas valider votre propre demande.")
        return redirect("conge_detail", pk=pk)

    # Vérifier le statut
    if conge.statut != "en attente":
        messages.warning(request, "Cette demande a déjà été traitée.")
        return redirect("conge_detail", pk=pk)


    conge.statut = 'refuse'
    conge.save()
    envoyer_mail_refus_manager(conge)

    creer_notification(
        destinataire=conge.employe.utilisateur,
        titre="Demande de congé refusée",
        message=(
            "Votre demande de congé a été refusée "
            "par votre responsable."
        ),
        type_notification="demande_refusee",
        demande_id=conge.id,
        type_demande="conge"
    )


    # Historique
    Validation.objects.create(
        demande_id=conge.id,
        validateur=user,
        type_demande="conge",
        decision="refuse",
        commentaire="Demande refusée"
    )


    return redirect('conge_detail', pk=pk)


@login_required()
@role_required('rh')
def valider_conge_rh(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    # Vérifier que le supérieur a déjà validé
    validation_superieur = Validation.objects.filter(
        demande_id=conge.id,
        type_demande="conge",
        decision="accepte"
    ).exclude(
        validateur=request.user
    ).exists()

    if not validation_superieur:

        messages.warning(
            request,
            "Cette demande doit d'abord être validée par le supérieur."
        )

        return redirect(
            "conge_detail",
            pk=pk
        )

    # Vérifier que la RH n'a pas déjà traité la demande
    validation_rh = Validation.objects.filter(
        demande_id=conge.id,
        type_demande="conge",
        validateur=request.user
    ).exists()

    if validation_rh:

        messages.warning(
            request,
            "Vous avez déjà traité cette demande."
        )

        return redirect(
            "conge_detail",
            pk=pk
        )

    # Validation finale par la RH
    conge.statut = "accepte"
    conge.save()

    # Notification finale à l'employé
    creer_notification(
        destinataire=conge.employe.utilisateur,
        titre="Demande de congé acceptée",
        message=(
            "Votre demande de congé a été définitivement "
            "acceptée par la RH."
        ),
        type_notification="demande_acceptee",
        demande_id=conge.id,
        type_demande="conge"
    )

    # Historique de validation RH
    Validation.objects.create(
        demande_id=conge.id,
        validateur=request.user,
        type_demande="conge",
        decision="accepte",
        commentaire="Demande définitivement validée par la RH"
    )

    return redirect(
        "conge_detail",
        pk=pk
    )


@login_required()
@role_required('rh')
def refuser_conge_rh(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    # Vérifier que le supérieur a déjà validé
    validation_superieur = Validation.objects.filter(
        demande_id=conge.id,
        type_demande="conge",
        decision="accepte"
    ).exclude(
        validateur=request.user
    ).exists()

    if not validation_superieur:

        messages.warning(
            request,
            "Cette demande doit d'abord être validée par le supérieur."
        )

        return redirect(
            "conge_detail",
            pk=pk
        )

    # Vérifier que la RH n'a pas déjà traité la demande
    validation_rh = Validation.objects.filter(
        demande_id=conge.id,
        type_demande="conge",
        validateur=request.user
    ).exists()

    if validation_rh:

        messages.warning(
            request,
            "Vous avez déjà traité cette demande."
        )

        return redirect(
            "conge_detail",
            pk=pk
        )

    # Refus final par la RH
    conge.statut = "refuse"
    conge.save()

    # Notification finale à l'employé
    creer_notification(
        destinataire=conge.employe.utilisateur,
        titre="Demande de congé refusée",
        message=(
            "Votre demande de congé a été refusée "
            "par la RH."
        ),
        type_notification="demande_refusee",
        demande_id=conge.id,
        type_demande="conge"
    )

    # Historique de validation RH
    Validation.objects.create(
        demande_id=conge.id,
        validateur=request.user,
        type_demande="conge",
        decision="refuse",
        commentaire="Demande refusée par la RH"
    )

    return redirect(
        "conge_detail",
        pk=pk
    )
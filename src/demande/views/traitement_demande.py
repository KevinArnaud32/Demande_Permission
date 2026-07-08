from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from demande.models.conges_model import Conges
from utils.email import envoyer_mail_conge
from demande.models.validation_model import Validation


@login_required
def traiter_conge(request, pk):

    conge = get_object_or_404(Conges, pk=pk)

    if request.user.role != "rh":
        return redirect("login")

    envoyer_mail_conge(conge)

    # conge.statut = "confirme"
    # conge.save()

    # Validation.objects.create(
    #     demande_id=conge.id,
    #     validateur=request.user,
    #     type_demande="conge",
    #     decision="accepte",
    #     commentaire="Congé confirmé et envoyé par email."
    # )

    return redirect("conge_list")
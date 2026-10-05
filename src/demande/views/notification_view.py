from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from demande.models.notification_model import Notification


@login_required()
def notification_list(request):

    notifications = Notification.objects.filter(
        destinataire=request.user
    ).order_by("-date_creation")

    context = {
        "notifications": notifications,
    }

    return render(
        request,
        "notification/list.html",
        context
    )



@login_required()
def notification_detail(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        destinataire=request.user
    )

    # Marquer la notification comme lue
    if not notification.lue:
        notification.lue = True
        notification.save(update_fields=["lue"])

    # Redirection selon le type de demande
    if notification.type_demande == "conge":
        return redirect("conge_detail", pk=notification.demande_id)

    elif notification.type_demande == "permission":
        return redirect("permission_detail", pk=notification.demande_id)

    elif notification.type_demande == "repos_maladie":
        return redirect(
            "repos_maladie_detail",
            pk=notification.demande_id
        )

    # Notification sans demande associée
    return redirect("dashboard")



@login_required()
def tout_marquer_comme_lue(request):

    Notification.objects.filter(
        destinataire=request.user,
        lue=False
    ).update(
        lue=True
    )

    return redirect("notification_list")
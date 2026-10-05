from .models.notification_model import Notification


def notifications_context(request):

    # Vérifier si l'utilisateur est connecté
    if not request.user.is_authenticated:
        return {
            "notifications": [],
            "notifications_non_lues": 0,
        }

    # Récupérer les 5 dernières notifications
    notifications = Notification.objects.filter(
        destinataire=request.user
    ).order_by("-date_creation")[:5]

    # Compter les notifications non lues
    notifications_non_lues = Notification.objects.filter(
        destinataire=request.user,
        lue=False
    ).count()

    return {
        "notifications": notifications,
        "notifications_non_lues": notifications_non_lues,
    }

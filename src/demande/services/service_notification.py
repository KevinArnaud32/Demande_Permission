from demande.models.notification_model import Notification


def creer_notification(
    destinataire,
    titre,
    message,
    type_notification="information",
    demande_id=None,
    type_demande=None
):
    """
    Crée une notification interne pour un utilisateur.
    """

    notification = Notification.objects.create(
        destinataire=destinataire,
        titre=titre,
        message=message,
        type_notification=type_notification,
        demande_id=demande_id,
        type_demande=type_demande,
    )

    return notification
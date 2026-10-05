from django.db import models
from employe.models.utilisateur_model import Utilisateur


class Notification(models.Model):

    TYPE_NOTIFICATION = [
        ("nouvelle_demande", "Nouvelle demande"),
        ("demande_acceptee", "Demande acceptée"),
        ("demande_refusee", "Demande refusée"),
        ("information", "Information"),
    ]

    destinataire = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    titre = models.CharField(
        max_length=255
    )

    message = models.TextField()

    type_notification = models.CharField(
        max_length=30,
        choices=TYPE_NOTIFICATION,
        default="information"
    )

    lue = models.BooleanField(
        default=False
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    demande_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    type_demande = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.titre} - {self.destinataire}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date_creation"]
from django.db import models
from base.helpers.date_time_model import DateTime
from employe.models.utilisateur_model import Utilisateur


class Validation(DateTime):
    ACTION_CHOICE = [
        ("accepte", "Accepté"),
        ("refuse", "Refusé")
    ]

    TYPE_DEMANDE = [
        ('permission', 'Permission'),
        ('conge', 'Congé'),
        ('repos_maladie', 'Repos maladie'),
    ]

    demande_id = models.PositiveIntegerField()
    validateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="validation_effectuees")
    type_demande = models.CharField(max_length=255, choices=TYPE_DEMANDE)
    decision = models.CharField(max_length=10, choices=ACTION_CHOICE)
    commentaire = models.CharField(max_length=255, default="")

    class Meta:
        verbose_name = "Validation"
        verbose_name_plural = "Validations"

    def __str__(self):
        return f"{self.demande_id} - {self.decision}"
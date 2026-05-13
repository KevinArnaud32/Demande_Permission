from django.db import models
from base.helpers.date_time_model import DateTime
from employe.models.utilisateur_model import Utilisateur


class Validation(DateTime):
    DECISION_CHOICE = [
        ("accepte", "Accepté"),
        ("refuse", "Refusé")
    ]

    TYPE_DEMANDE_CHOICES = [
        ('permission', 'Permission'),
        ('conge', 'Congé'),
        ('repos_maladie', 'Repos maladie'),
    ]

    validateur_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="validation_effectuees")
    type_demande = models.CharField(max_length=255, choices=TYPE_DEMANDE_CHOICES)
    demande_id = models.PositiveIntegerField()
    decision = models.CharField(max_length=10, choices=DECISION_CHOICE)
    commentaire = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Validation"
        verbose_name_plural = "Validations"

    def __str__(self):
        return f"{self.demande_id} - {self.decision}"
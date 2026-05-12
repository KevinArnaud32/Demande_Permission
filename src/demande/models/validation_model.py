from django.db import models
from base.helpers.date_time_model import DateTime
from demande.models.demande_model import Demande
from employe.models.employe_model import Employe


class Validation(DateTime):
    DECISION_CHOICE = [
        ("accepte", "Accepté"),
        ("refuse", "Refusé")
    ]

    demande_id = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="validation")
    validateur_id = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="validation_effectuees")
    decision = models.CharField(max_length=10, choices=DECISION_CHOICE)
    commentaire = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Validation"
        verbose_name_plural = "Validations"

    def __str__(self):
        return f"{self.demande_id} - {self.decision}"
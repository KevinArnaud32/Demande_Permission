from django.db import models
from base.helpers.date_time_model import DateTime
from employe.models.employe_model import Employe


class Demande(DateTime):
    STATUT_CHOICE = [
        ("en_attente", "En attente"),
        ("accepte", "Accepté"),
        ("refuse", "Refusé"),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    statut = models.CharField(max_length=255, choices=STATUT_CHOICE, default="en_attente")

    def __str__(self):
        return f"{self.employe} - {self.statut}"

    class Meta:
        verbose_name = "Demande"
        verbose_name_plural = "Demandes"
        abstract = True
from datetime import timedelta

from django.db import models

from demande.models.demande_model import Demande


class Conges(Demande):
    date_debut = models.DateField()
    nombre_jours = models.PositiveIntegerField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Congé - {self.employe}"

    def save(self, *args, **kwargs):
        self.date_fin = (self.date_debut + timedelta(days=self.nombre_jours))

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Conge"
        verbose_name_plural = "conges"
from datetime import timedelta

from django.db import models

from demande.models.demande_model import Demande


class ReposMaladie(Demande):
    date_debut = models.DateField()
    nombre_jours = models.PositiveIntegerField()
    date_fin = models.DateField(null=True, blank=True)
    justificatif = models.FileField(upload_to="justificatifs/")

    class Meta:
        verbose_name = "Repos Maladie"
        verbose_name_plural = "Repos maladies"

    def save(self,*args, **kwargs):
        self.date_fin = (self.date_debut + timedelta(days=self.nombre_jours))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Repos maladie - {self.employe}"
from django.db import models
from base.helpers.date_time_model import DateTime


class Departement(DateTime):
    nom_departement = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Departement"
        verbose_name_plural = "Departements"

    def __str__(self):
        return self.nom_departement
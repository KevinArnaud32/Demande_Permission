from django.db import models
from base.helpers.date_time_model import DateTime


class Fonction(DateTime):
    nom_fonction = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_fonction

    class Meta:
        verbose_name = "Fonction"
        verbose_name_plural = "Fonctions"
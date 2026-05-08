from  django.db import models

from employe.models.utilisateur_model import Utilisateur


class SoldesConges(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    total_jours = models.IntegerField()
    jours_utilise = models.IntegerField()
    jours_restant = models.IntegerField()

    class Meta:
        verbose_name = "Solde des conges"
        verbose_name_plural = "Solde des conges"

    def __str__(self):
        return f"{self.utilisateur}"
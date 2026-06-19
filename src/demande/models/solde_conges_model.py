from  django.db import models
from employe.models.employe_model import Employe


class SoldesConges(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, related_name="solde_conge")
    total_jours = models.PositiveIntegerField(default=30)
    jours_utilise = models.PositiveIntegerField(default=0)
    jours_restant = models.PositiveIntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):
        self.jours_restant = (self.total_jours - self.jours_utilise)

        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Solde des conges"
        verbose_name_plural = "Solde des conges"


    def __str__(self):
        return f"{self.employe} - {self.jours_restants} jours"
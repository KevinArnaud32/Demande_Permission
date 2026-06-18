from datetime import timedelta, datetime
from django.db import models
from demande.models.demande_model import Demande


class Permission(Demande):
    motif = models.TextField()
    heure_sortie = models.TimeField()
    nombre_minute = models.PositiveIntegerField()
    heure_retour = models.TimeField(null=True, blank=True)

    def save(self,*args, **kwargs):

        if self.heure_sortie and self.nombre_minute:

            heure_sortie = datetime.combine(
                datetime.today().date(),
                self.heure_sortie
            )

            heure_retour = heure_sortie + timedelta(minutes=self.nombre_minute)

            self.heure_retour = heure_retour.time()
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Permission - {self.employe}"


    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
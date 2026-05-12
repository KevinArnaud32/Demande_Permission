from datetime import timedelta
from django.db import models
from demande.models.demande_model import Demande


class Permission(Demande):
    motif = models.TextField()
    heure_sortie = models.DateTimeField()
    nombre_minute = models.PositiveIntegerField()
    heure_retour = models.DateTimeField(null=True, blank=True)

    def save(self,*args, **kwargs):
        self.heure_retour = (self.heure_sortie + timedelta(minutes=self.nombre_minute))
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Permission - {self.employe}"


    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
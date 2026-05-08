from django.db import models
from base.helpers.date_time_model import DateTime
from employe.models.departement_model import Departement
from employe.models.fonction_model import Fonction
from employe.models.utilisateur_model import Utilisateur


class Employe(DateTime):
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)
    fonction = models.ForeignKey(Fonction, on_delete=models.SET_NULL, null=True)
    superieur = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subordonnes")
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="employe")
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.nom} {self.prenom}"

    class Meta:
        verbose_name = "Employe"
        verbose_name_plural = "Employes"
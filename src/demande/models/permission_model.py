from django.db import models
from demande.models.demande_model import Demande
from demande.models.type_permission_model import TypePermission


class Permission(Demande):
    type_permission = models.ForeignKey(TypePermission, on_delete=models.PROTECT, related_name='permissions')
    motif = models.TextField(null=True)
    date_permission = models.DateField(null=True)
    date_retour = models.DateField(null=True)



    def __str__(self):
        return f"Permission - {self.employe}"


    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
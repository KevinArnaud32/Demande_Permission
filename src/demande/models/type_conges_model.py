from django.db import models
from base.helpers.date_time_model import DateTime


class TypeConge(DateTime):

    libelle = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )


    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Type de congé"
        verbose_name_plural = "Types de congés"
        ordering = ["libelle"]
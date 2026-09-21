from django.db import models


class TypePermission(models.Model):

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
        verbose_name = "Type de permission"
        verbose_name_plural = "Types de permissions"
        ordering = ["libelle"]
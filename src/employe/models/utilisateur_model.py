from django.contrib.auth.models import AbstractUser
from django.db import models
from base.helpers.date_time_model import DateTime


class Utilisateur(AbstractUser, DateTime):
    ROLE_CHOICES = [
        ('EMPLOYE', 'Employé'),
        ('MANAGER', 'Manager'),
        ('RH', 'RH'),
        ('ADMIN', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username

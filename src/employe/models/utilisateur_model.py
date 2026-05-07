from django.contrib.auth.models import AbstractUser
from django.db import models
from base.helpers.date_time_model import DateTime


class Utilisateur(AbstractUser, DateTime):
    ROLE_CHOICE = [
        ("employe", "Employé"),
        ("manager", "Manager"),
        ("rh", "RH"),
        ("admin", "Administrateur"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default='employe')

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username

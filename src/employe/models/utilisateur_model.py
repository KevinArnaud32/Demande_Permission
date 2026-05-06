from django.db import models


class Employe(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
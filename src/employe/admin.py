from django.contrib import admin

from employe.models.departement_model import Departement
from employe.models.employe_model import Employe
from employe.models.fonction_model import Fonction
from employe.models.utilisateur_model import Utilisateur

# Register your models here.
admin.site.register(Departement)
admin.site.register(Employe)
admin.site.register(Fonction)
admin.site.register(Utilisateur)
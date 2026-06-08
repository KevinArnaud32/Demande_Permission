from django.contrib import admin

from demande.models.conges_model import Conges
from demande.models.permission_model import Permission
from demande.models.repos_maladie_model import ReposMaladie
from demande.models.solde_conges_model import SoldesConges
from demande.models.validation_model import Validation

# Register your models here.
admin.site.register(Conges)
admin.site.register(Permission)
admin.site.register(ReposMaladie)
admin.site.register(SoldesConges)
admin.site.register(Validation)
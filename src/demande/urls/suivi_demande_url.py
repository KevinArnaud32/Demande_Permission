from django.urls import path
from demande.views.suivi_demande_view import suivi_demandes


urlpatterns = [
    path("suivi_demandes/", suivi_demandes ,name="suivi_demandes"),
]
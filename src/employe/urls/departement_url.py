from django.urls import path
from employe.views.departement_view import departement_list, departement_create


urlpatterns = [
    path('', departement_list, name='departement_list'),
    path('create/', departement_create, name='departement_create'),
]
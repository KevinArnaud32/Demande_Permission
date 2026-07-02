from django.urls import path
from demande.views.conge_view import *


urlpatterns = [

    path('', conge_list, name='conge_list'),
    path('create/', conge_create, name='conge_create'),
    path('details/<int:pk>/', conge_detail, name='conge_detail'),
    path('update/<int:pk>/', conge_update, name='conge_update'),
    path('delete/<int:pk>/', conge_delete, name='conge_delete'),
    path('valider/<int:pk>/', valider_conge, name='valider_conge'),
    path('refuser/<int:pk>/', refuser_conge, name='refuser_conge'),

]
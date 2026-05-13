from django.urls import path
from demande.views.conge_view import conge_list, conge_create, conge_delete, conge_detail, conge_update


urlpatterns = [
    path(
        '',
        conge_list,
        name='conge_list'
    ),

    path(
        'conges/create/',
        conge_create,
        name='conge_create'
    ),

    path(
        'conges/<int:pk>/',
        conge_detail,
        name='conge_detail'
    ),

    path(
        'conges/update/<int:pk>/',
        conge_update,
        name='conge_update'
    ),

    path(
        'conges/delete/<int:pk>/',
        conge_delete,
        name='conge_delete'
    ),
]
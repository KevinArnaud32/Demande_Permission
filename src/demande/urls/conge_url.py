from django.urls import path
from demande.views.conge_view import conge_list, conge_create, conge_delete, conge_detail, conge_update


urlpatterns = [
    path(
        '',
        conge_list,
        name='conge_list'
    ),

    path(
        'create/',
        conge_create,
        name='conge_create'
    ),

    path(
        'detail/<int:pk>/',
        conge_detail,
        name='conge_detail'
    ),

    path(
        'update/<int:pk>/',
        conge_update,
        name='conge_update'
    ),

    path(
        'delete/<int:pk>/',
        conge_delete,
        name='conge_delete'
    ),
]
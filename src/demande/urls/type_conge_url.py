from django.urls import path
from demande.views.type_conges_view import type_conge_create, type_conge_delete,type_conge_detail, type_conge_update, type_conge_list



urlpatterns = [
    path(
        "",
            type_conge_list,
        name="type_conge_list"
    ),

    path(
        "create/",
        type_conge_create,
        name="type_conge_create"
    ),

    path(
        "details/<int:pk>/",
        type_conge_detail,
        name="type_conge_detail"
    ),

    path(
        "update/<int:pk>/",
        type_conge_update,
        name="type_conge_update"
    ),

    path(
        "delete/<int:pk>/",
        type_conge_delete,
        name="type_conge_delete"
    ),

]
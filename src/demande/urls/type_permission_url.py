from django.urls import path
from demande.views.type_permissions_view import (type_permission_create, type_permission_delete, type_permission_detail,
        type_permission_update, type_permission_list)


urlpatterns = [
    path(
        "",
        type_permission_list,
        name="type_permission_list"
    ),

    path(
        "create/",
        type_permission_create,
        name="type_permission_create"
    ),

    path(
        "details/<int:pk>/",
        type_permission_detail,
        name="type_permission_detail"
    ),

    path(
        "update/<int:pk>/",
        type_permission_update,
        name="type_permission_update"
    ),

    path(
        "delete/<int:pk>/",
        type_permission_delete,
        name="type_permission_delete"
    ),
]
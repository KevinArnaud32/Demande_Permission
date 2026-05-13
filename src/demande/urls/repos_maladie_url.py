from django.urls import path
from demande.views.repose_maladie_view import repos_maladie_list, repos_maladie_create, repos_maladie_delete, repos_maladie_detail, repos_maladie_update


urlpatterns = [
    path(
        '',
        repos_maladie_list,
        name='repos_maladie_list'
    ),

    path(
        'repos-maladies/create/',
        repos_maladie_create,
        name='repos_maladie_create'
    ),

    path(
        'repos-maladies/<int:pk>/',
        repos_maladie_detail,
        name='repos_maladie_detail'
    ),

    path(
        'repos-maladies/update/<int:pk>/',
        repos_maladie_update,
        name='repos_maladie_update'
    ),

    path(
        'repos-maladies/delete/<int:pk>/',
        repos_maladie_delete,
        name='repos_maladie_delete'
    ),
]
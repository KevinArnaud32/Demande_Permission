from django.urls import path
from demande.views.validation_view import validation_list, validate_permission, validate_conge, validate_repos_maladie


urlpatterns = [
    path(
        'validations/',
        validation_list,
        name='validation_list'
    ),

    path(
        'validation/permission/<int:pk>/',
        validate_permission,
        name='validate_permission'
    ),

    path(
        'validation/conge/<int:pk>/',
        validate_conge,
        name='validate_conge'
    ),

    path(
        'validation/repos-maladie/<int:pk>/',
        validate_repos_maladie,
        name='validate_repos_maladie'
    ),
]
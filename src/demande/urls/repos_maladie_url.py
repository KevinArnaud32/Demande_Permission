from django.urls import path
from demande.views.repose_maladie_view import *


urlpatterns = [

    path('', repos_maladie_list, name='repos_maladie_list'),
    path('create/', repos_maladie_create, name='repos_maladie_create'),
    path('details/<int:pk>/', repos_maladie_detail, name='repos_maladie_detail'),
    path('update/<int:pk>/', repos_maladie_update, name='repos_maladie_update'),
    path('delete/<int:pk>/', repos_maladie_delete, name='repos_maladie_delete'),

]
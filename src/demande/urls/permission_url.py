from django.urls import path
from demande.views.permission_view import (permission_list, permission_create, permission_delete,
permission_detail, permission_update, valider_permission, refuser_permission)


urlpatterns = [

    path('', permission_list, name='permission_list'),
    path('create/', permission_create, name='permission_create'),
    path('details/<int:pk>/', permission_detail, name='permission_detail'),
    path('update/<int:pk>/', permission_update,name='permission_update'),
    path('delete/<int:pk>/', permission_delete, name='permission_delete'),
    path('valider/<int:pk>/', valider_permission, name='valider_permission'),
    path('refuser/<int:pk>/', refuser_permission, name='refuser_permission'),

]
from django.urls import path
from demande.views.permission_view import permission_list, permission_create, permission_delete, permission_detail, permission_update


urlpatterns = [

    path('', permission_list, name='permission_list'),
    path('create/', permission_create, name='permission_create'),
    path('<int:pk>/', permission_detail, name='permission_detail'),
    path('update/<int:pk>/', permission_update,name='permission_update'),
    path('delete/<int:pk>/',permission_delete, name='permission_delete'),

]
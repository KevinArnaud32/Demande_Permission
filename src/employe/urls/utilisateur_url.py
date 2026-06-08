from django.urls import path

from employe.views.utilisateur_view import utilisateur_list, utilisateur_create, utilisateur_detele, utilisateur_detail, utilisateur_update

urlpatterns = [
    path('', utilisateur_list, name='utilisateur_list'),
    path('create/', utilisateur_create, name='utilisateur_create'),
    path('detail/<int:id>/', utilisateur_detail, name='utilisateur_detail'),
    path('update/<int:id>/', utilisateur_update, name='utilisateur_update'),
    path('delete/<int:id>/', utilisateur_detele, name='utilisateur_delete'),
]
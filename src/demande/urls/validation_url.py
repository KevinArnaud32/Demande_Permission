from django.urls import path
from demande.views.validation_view import validation_list


urlpatterns = [
    path('', validation_list, name='validation_list'),
]
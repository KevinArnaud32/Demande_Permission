from django.urls import path
from demande.views.pdf_conge import conge_pdf_view, permission_pdf_view, repos_maladie_pdf_view


urlpatterns = [

    # PDF Congé
    path('conge/<int:pk>/', conge_pdf_view, name='conge_pdf'),

    # PDF Permission
    path('permission/<int:pk>/', permission_pdf_view, name='permission_pdf'),

    # PDF Repos maladie
    path('repos-maladie/<int:pk>/', repos_maladie_pdf_view, name='repos_maladie_pdf'),

]
"""
URL configuration for DemandeConges project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from demande.views.pdf_conge import conge_pdf_view
from demande.views.traitement_demande import traiter_conge


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('permission/', include('demande.urls.permission_url')),
    path('conges/', include('demande.urls.conge_url')),
    path('repos_maladie/',include('demande.urls.repos_maladie_url')),
    path('validaion/', include('demande.urls.validation_url')),
    path('auth/',include('authentification.urls')),
    path('utilisateur/', include('employe.urls.utilisateur_url')),
    path('departement/', include('employe.urls.departement_url')),
    path('envoi_pdf/<int:pk>/', traiter_conge, name='traiter_conge'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
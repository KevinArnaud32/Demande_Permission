from django.urls import path
from .views import dashboard, admin_dashboard, rh_dashboard, manager_dashboard, employe_dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('rh/', rh_dashboard, name='rh_dashboard'),
    path('manager/', manager_dashboard, name='manager_dashboard'),
    path('employe/', employe_dashboard, name='employe_dashboard'),
]
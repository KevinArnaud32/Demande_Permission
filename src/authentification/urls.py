from django.urls import path
from .views import logout_view, login_view, change_password_first


urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change_password_first/', change_password_first, name='change_password_first')
]
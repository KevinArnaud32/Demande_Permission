from django.urls import path
from demande.views.notification_view import notification_detail, notification_list, tout_marquer_comme_lue

urlpatterns = [
    path("list/", notification_list, name="notification_list"),
    path("detail/<int:pk>/", notification_detail, name="notification_detail"),
    path('tout_marquer_comme_lue/', tout_marquer_comme_lue, name="tout_marquer_comme_lue")
]
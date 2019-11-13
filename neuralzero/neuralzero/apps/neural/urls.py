from django.urls import path

from . import views

app_name = "neural"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:network_id>/", views.view_network, name="view"),
    path("<int:network_id>/edit/", views.view_network, name="edit"),
]

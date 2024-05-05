from django.urls import path
from routine import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create-routine/", views.create_routine, name="create-routine"),
    path("delete-routine/<int:routine_id>/", views.delete_routine, name="delete-routine"),
]

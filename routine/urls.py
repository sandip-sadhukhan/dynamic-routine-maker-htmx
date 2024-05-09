from django.urls import path
from routine import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("dashboard/", views.dashboard_page, name="dashboard"),
    path("create-routine/", views.create_routine, name="create-routine"),
    path("delete-routine/<int:routine_id>/", views.delete_routine, name="delete-routine"),
    path("routine/<int:routine_id>/", views.routine_page, name="routine-page"),
    path("routine/<int:routine_id>/<str:day>/", views.schedule_page, name="schedule-page"),
    path("create-schedule/<int:routine_id>/<str:day>/", views.create_schedule, name="create-schedule"),
    path("delete-schedule/<int:class_id>/", views.delete_schedule, name="delete-schedule"),
]

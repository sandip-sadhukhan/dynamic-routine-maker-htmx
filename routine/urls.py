from django.urls import path
from routine import views

urlpatterns = [
    path("", views.homePage, name="home"),
]
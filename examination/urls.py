from django.urls import path

from . import views

app_name = "examination"

urlpatterns = [
    path("halticket", views.Halticket.as_view(), name="halticket"),
]
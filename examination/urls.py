from django.urls import path

from . import views

app_name = "examination"

urlpatterns = [
    path("halticket", views.Halticket.as_view(), name="halticket"),
    path("GradeCard", views.GradeCard.as_view(), name="gradecard"),
    path("grademark/<str:pk>/", views.GradeMarkPdfView.as_view(), name="grademark"),
]
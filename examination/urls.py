from django.urls import path

from . import views

app_name = "examination"

urlpatterns = [
    path("halticket", views.Halticket.as_view(), name="halticket"),
    path("GradeCard", views.GradeCard.as_view(), name="gradecard"),
    path("exam_applied", views.ExamApplied.as_view(), name="exam_applied"),
    path("exam_applied_batch_based", views.ExamAppliedBatchBased.as_view(), name="exam_applied_batch_based"),
    path("grademark/<str:pk>/", views.GradeMarkPdfView.as_view(), name="grademark"),
    path("exam_appy/<str:pk>/", views.ExamApplyPdfView.as_view(), name="exam_apply"),
]
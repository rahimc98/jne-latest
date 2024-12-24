from django.urls import path

from . import views

app_name = "examination"

urlpatterns = [
    path('get_batch_filter/', views.get_batch_filter, name='get_batch_filter'),
    path("get/college_based_course", views.GetCourseView.as_view(), name="get_college_based_course"),
    path("get/course_based_batch", views.GetBatchView.as_view(), name="get_course_based_batch"),
    # college
    path("colleges/", views.CollegeListView.as_view(), name="college_list"),
    path("new/college/", views.CollegeCreateView.as_view(), name="college_create"),
    path("college/<str:pk>/", views.CollegeDetailView.as_view(), name="college_detail"),
    path("college/<str:pk>/update/", views.CollegeUpdateView.as_view(), name="college_update"),
    path("college/<str:pk>/delete/", views.CollegeDeleteView.as_view(), name="college_delete"),
    # Course
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("new/course/", views.CourseCreateView.as_view(), name="course_create"),
    path("course/<str:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("course/<str:pk>/update/", views.CourseUpdateView.as_view(), name="course_update"),
    path("course/<str:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    # Batch 
    path("batchs/", views.BatchListView.as_view(), name="batch_list"),
    path("new/batch/", views.BatchCreateView.as_view(), name="batch_create"),
    path("batch/<str:pk>/", views.BatchDetailView.as_view(), name="batch_detail"),
    path("batch/<str:pk>/update/", views.BatchUpdateView.as_view(), name="batch_update"),
    path("batch/<str:pk>/delete/", views.BatchDeleteView.as_view(), name="batch_delete"),
    # Examination  
    path("examinations/", views.ExaminationListView.as_view(), name="examination_list"),
    path("new/examination/", views.ExaminationCreateView.as_view(), name="examination_create"),
    path("examination/<str:pk>/", views.ExaminationDetailView.as_view(), name="examination_detail"),
    path("examination/<str:pk>/update/", views.ExaminationUpdateView.as_view(), name="examination_update"),
    path("examination/<str:pk>/delete/", views.ExaminationDeleteView.as_view(), name="examination_delete"),
    # Student  student
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("new/student/", views.StudentCreateView.as_view(), name="student_create"),
    path("student/<str:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("student/<str:pk>/update/", views.StudentUpdateView.as_view(), name="student_update"),
    path("student/<str:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    # subject
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("new/subject/", views.SubjectCreateView.as_view(), name="subject_create"),
    path("subject/<str:pk>/", views.SubjectDetailView.as_view(), name="subject_detail"),
    path("subject/<str:pk>/update/", views.SubjectUpdateView.as_view(), name="subject_update"),
    path("subject/<str:pk>/delete/", views.SubjectDeleteView.as_view(), name="subject_delete"),
    # ExamStudent
    path("examstudents/", views.ExamStudentListView.as_view(), name="examstudent_list"),
    path("new/examstudent/", views.ExamStudentCreateView.as_view(), name="examstudent_create"),
    path("examstudent/<str:pk>/", views.ExamStudentDetailView.as_view(), name="examstudent_detail"),
    path("examstudent/<str:pk>/update/", views.ExamStudentUpdateView.as_view(), name="examstudent_update"),
    path("examstudent/<str:pk>/delete/", views.ExamStudentDeleteView.as_view(), name="examstudent_delete"),     
    # ExamStudent Mark
    path("examstudentmarks/", views.ExamStudentMarkListView.as_view(), name="examstudentmark_list"),
    path("new/examstudentmark/", views.ExamStudentMarkCreateView.as_view(), name="examstudentmark_create"),
    path("examstudentmark/<str:pk>/", views.ExamStudentMarkDetailView.as_view(), name="examstudentmark_detail"),
    path("examstudentmark/<str:pk>/update/", views.ExamStudentMarkUpdateView.as_view(), name="examstudentmark_update"),
    path("examstudentmark/<str:pk>/delete/", views.ExamStudentMarkDeleteView.as_view(), name="examstudentmark_delete"),   

    path("batch_based_mark_list/<str:pk>/", views.BatchBasedMarkListView.as_view(), name="batch_based_mark_list"),  
    path("batch_based_mark_list_print/<str:pk>/", views.BatchBasedMarkListPrint.as_view(), name="batch_based_mark_list_print"),  

    path("halticket", views.Halticket.as_view(), name="halticket"), 
    path("GradeCard", views.GradeCard.as_view(), name="gradecard"),
    path("exam_applied", views.ExamApplied.as_view(), name="exam_applied"),
    path("exam_applied_batch_based", views.ExamAppliedBatchBased.as_view(), name="exam_applied_batch_based"),
    path("grademark/<str:pk>/", views.GradeMarkPdfView.as_view(), name="grademark"),
    path("exam_appy/<str:pk>/", views.ExamApplyPdfView.as_view(), name="exam_apply"),
]
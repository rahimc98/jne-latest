from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("gallery/", views.gallery, name="gallery"),
    path("institutions/", views.institution, name="institution"),
    path(
        "institution/<str:slug>/",
        views.institution_single,
        name="institution_single",
    ),
    path("department/<str:slug>/", views.department, name="department"),
    path("career/", views.career, name="career"),
    path("list-news/", views.news, name="news"),
    path("news/<str:pk>/", views.news_single, name="news_single"),
    path("contact/", views.contact, name="contact"),
    path("techies-park/", views.techies_park, name="techies_park"),
    path("jne-about/", views.jne_about, name="jne_about"),
    path("save-message/", views.save_message, name="save_message"),
    path("job-apply/<str:slug>/", views.job_apply, name="job_apply"),
    path("get-careers/", views.get_careers, name="get_careers"),
    path("get-gallery/", views.get_gallery, name="get_gallery"),
    path("exam-result/", views.exam_result, name="exam_result"),
    path("find-result/", views.find_result, name="find_result"),
    path("rank-list/", views.rank_list, name="rank_list"),
]

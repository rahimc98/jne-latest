from django.conf import settings as SETTINGS
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

app_name = "jne"

urlpatterns = (
    [
        re_path(r"^", include("web.urls", namespace="website")),
        re_path("admin/", admin.site.urls),
    ]
    + static(SETTINGS.STATIC_URL, document_root=SETTINGS.STATIC_ROOT)
    + static(SETTINGS.MEDIA_URL, document_root=SETTINGS.MEDIA_ROOT)
)

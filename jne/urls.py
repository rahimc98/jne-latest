from django.conf import settings as SETTINGS
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path,path

app_name = "jne"

urlpatterns = (
    [
        re_path(r"^", include("web.urls", namespace="website")),
        re_path("admin/", admin.site.urls),
        path("app/", include("core.urls", namespace="core")),
        path("accounts/", include("registration.backends.simple.urls")),
        path("accounts/", include("accounts.urls", namespace="accounts")),
        path("examination/", include("examination.urls", namespace="examination")),
    ]
    + static(SETTINGS.STATIC_URL, document_root=SETTINGS.STATIC_ROOT)
    + static(SETTINGS.MEDIA_URL, document_root=SETTINGS.MEDIA_ROOT)
)

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("admin/", include("core_apps.books.urls")),
            ]
        ),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "FRONTEND API"

admin.site.site_title = "FRONTEND API PORTAL"

admin.site.index_title = "Welcome to FRONTEND Api Portal"

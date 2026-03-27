from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.content.urls")),
    path("api/v1/", include("apps.activities.urls")),
    path("api/v1/", include("apps.community.urls")),
    path("api/v1/", include("apps.info.urls")),
]

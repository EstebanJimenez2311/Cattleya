from django.contrib import admin
from django.urls import path, include

from .views import healthcheck

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("api/", include("noticias.urls")),
]

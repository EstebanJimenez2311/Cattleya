from django.contrib import admin
from django.urls import path, include

from .views import healthcheck

admin.site.site_header = "Cattleya Admin"
admin.site.site_title = "Cattleya Dashboard"
admin.site.index_title = "Panel de gestion y monitoreo"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("api/", include("noticias.urls")),
    path("api/", include("analisis.urls")),
]

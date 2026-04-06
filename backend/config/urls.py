from django.contrib import admin
from django.urls import path, include

from .auth import CattleyaAdminAuthenticationForm
from .views import healthcheck

import config.admin  # noqa: F401

admin.site.site_header = "Cattleya Admin"
admin.site.site_title = "Cattleya Dashboard"
admin.site.index_title = "Panel de gestion y monitoreo"
admin.site.login_form = CattleyaAdminAuthenticationForm
admin.site.login_template = "admin/cattleya_login.html"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("api/", include("noticias.urls")),
    path("api/analisis/", include("analisis.urls")),
    path("api/estadisticas/", include("estadisticas.urls")),
]


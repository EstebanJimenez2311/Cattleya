from django.contrib import admin
from django.urls import path, include

from .auth import CattleyaAdminAuthenticationForm
from .views import chatbot_chat, chatbot_healthcheck, healthcheck

import config.admin  # noqa: F401

admin.site.site_header = "Cattleya Admin"
admin.site.site_title = "Cattleya Dashboard"
admin.site.index_title = "Panel de gestion y monitoreo"
admin.site.login_form = CattleyaAdminAuthenticationForm
admin.site.login_template = "admin/cattleya_login.html"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("api/chat", chatbot_chat, name="chatbot_chat"),
    path("api/chat/", chatbot_chat, name="chatbot_chat_slash"),
    path("api/chat/health", chatbot_healthcheck, name="chatbot_health"),
    path("api/chat/health/", chatbot_healthcheck, name="chatbot_health_slash"),
    path("api/", include("noticias.urls")),
    path("api/analisis/", include("analisis.urls")),
    path("api/estadisticas/", include("estadisticas.urls")),
]


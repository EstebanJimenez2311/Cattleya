from django.urls import path

from .views import (
    CargarAnalisisJsonView,
    DashboardAnalisisView,
    DetalleResultadoView,
    ListaResultadosView,
)

app_name = "analisis"

urlpatterns = [
    path("resultados/", ListaResultadosView.as_view(), name="lista-resultados"),
    path("resultados/<str:nombre>/", DetalleResultadoView.as_view(), name="detalle-resultado"),
    path("dashboard/", DashboardAnalisisView.as_view(), name="dashboard-frontend"),
    path("cargar-json/", CargarAnalisisJsonView.as_view(), name="cargar-json"),
]

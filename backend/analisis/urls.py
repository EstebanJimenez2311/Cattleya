from django.urls import path
from .views import ListaResultadosView, DetalleResultadoView

app_name = 'analisis'

urlpatterns = [
    path('resultados/', ListaResultadosView.as_view(), name='lista-resultados'),
    path('resultados/<str:nombre>/', DetalleResultadoView.as_view(), name='detalle-resultado'),
]

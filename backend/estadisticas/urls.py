from django.urls import path
from .views import ResumenView, TendenciaView, TiposViolenciaView

app_name = 'estadisticas'

urlpatterns = [
    path('resumen/', ResumenView.as_view(), name='resumen'),
    path('tendencia/', TendenciaView.as_view(), name='tendencia'),
    path('tipos/', TiposViolenciaView.as_view(), name='tipos'),
]

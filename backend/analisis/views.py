from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import ResultadoAnalisis
from .serializers import ResultadoAnalisisSerializer


class ListaResultadosView(ListAPIView):
    queryset = ResultadoAnalisis.objects.all().order_by('-actualizado')
    serializer_class = ResultadoAnalisisSerializer
    pagination_class = None


class DetalleResultadoView(RetrieveAPIView):
    queryset = ResultadoAnalisis.objects.all()
    serializer_class = ResultadoAnalisisSerializer
    lookup_field = 'nombre'
    lookup_url_kwarg = 'nombre'

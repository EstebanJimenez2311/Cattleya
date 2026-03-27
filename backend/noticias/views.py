from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Noticia
from .serializers import NoticiaSerializer

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer

    @action(detail=False, methods=['get'])
    def recientes(self, request):
        recientes = self.get_queryset().order_by('-fecha_publicacion')[:10]
        serializer = self.get_serializer(recientes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        tipo_violencia_count = Noticia.objects.values('tipo_violencia').annotate(count=Count('tipo_violencia'))
        ciudad_count = Noticia.objects.values('ciudad').annotate(count=Count('ciudad'))
        data = {
            'tipo_violencia': list(tipo_violencia_count),
            'ciudad': list(ciudad_count),
        }
        return Response(data)

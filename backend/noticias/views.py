from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Noticia
from .serializers import NoticiaSerializer


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer

    def get_queryset(self):
        return Noticia.objects.filter(es_prueba=False)

    @action(detail=False, methods=["get"])
    def recientes(self, request):
        recientes = self.get_queryset().order_by("-fecha_publicacion")[:10]
        serializer = self.get_serializer(recientes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def resumen(self, request):
        queryset = self.get_queryset()
        tipo_violencia_count = [
            {"tipo_violencia": "fisica", "count": queryset.filter(violencia_fisica=True).count()},
            {"tipo_violencia": "psicologica", "count": queryset.filter(violencia_psicologica=True).count()},
            {"tipo_violencia": "sexual", "count": queryset.filter(violencia_sexual=True).count()},
            {"tipo_violencia": "economica", "count": queryset.filter(violencia_economica=True).count()},
            {"tipo_violencia": "patrimonial", "count": queryset.filter(violencia_patrimonial=True).count()},
            {"tipo_violencia": "feminicidio", "count": queryset.filter(feminicidio=True).count()},
            {
                "tipo_violencia": "otros",
                "count": queryset.filter(
                    violencia_fisica=False,
                    violencia_psicologica=False,
                    violencia_sexual=False,
                    violencia_economica=False,
                    violencia_patrimonial=False,
                    feminicidio=False,
                ).count(),
            },
        ]
        ciudad_count = list(queryset.values("ciudad").annotate(count=Count("ciudad")))
        ambito_count = list(
            queryset.exclude(ambito_violencia="")
            .values("ambito_violencia")
            .annotate(count=Count("ambito_violencia"))
        )
        riesgo_count = list(
            queryset.exclude(nivel_riesgo="")
            .values("nivel_riesgo")
            .annotate(count=Count("nivel_riesgo"))
        )
        casos_criticos = queryset.filter(Q(nivel_riesgo="critico") | Q(feminicidio=True)).count()

        data = {
            "tipo_violencia": tipo_violencia_count,
            "ciudad": ciudad_count,
            "ambito_violencia": ambito_count,
            "nivel_riesgo": riesgo_count,
            "casos_criticos": casos_criticos,
        }
        return Response(data)

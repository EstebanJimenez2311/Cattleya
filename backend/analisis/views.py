from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ResultadoAnalisis
from .serializers import ResultadoAnalisisSerializer
from .services import build_frontend_payload, import_analysis_file


class ListaResultadosView(ListAPIView):
    queryset = ResultadoAnalisis.objects.all().order_by("-actualizado")
    serializer_class = ResultadoAnalisisSerializer
    pagination_class = None


class DetalleResultadoView(RetrieveAPIView):
    queryset = ResultadoAnalisis.objects.all()
    serializer_class = ResultadoAnalisisSerializer
    lookup_field = "nombre"
    lookup_url_kwarg = "nombre"


class DashboardAnalisisView(APIView):
    def get(self, request):
        nombre = request.query_params.get("nombre")
        if nombre:
            resultado = get_object_or_404(ResultadoAnalisis, nombre=nombre)
        else:
            resultado = ResultadoAnalisis.objects.order_by("-actualizado").first()

        if resultado is None:
            return Response(
                {"detail": "No hay análisis cargados todavía."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            payload = build_frontend_payload(resultado)
        except DjangoValidationError as exc:
            return Response(
                {"detail": "El análisis cargado no es compatible con el frontend.", "error": exc.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(payload)


class CargarAnalisisJsonView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        archivo = request.FILES.get("archivo")
        if not archivo:
            return Response(
                {"detail": "Debes adjuntar un archivo en el campo 'archivo'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        nombre = request.data.get("nombre") or None
        descripcion = request.data.get("descripcion") or None

        try:
            resultado, created = import_analysis_file(
                archivo,
                nombre=nombre,
                descripcion=descripcion,
            )
        except DjangoValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResultadoAnalisisSerializer(resultado)
        return Response(
            {
                "created": created,
                "message": "Análisis cargado correctamente.",
                "resultado": serializer.data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

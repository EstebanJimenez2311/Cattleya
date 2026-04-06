from rest_framework import serializers
from .models import ResultadoAnalisis


class ResultadoAnalisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoAnalisis
        fields = ['nombre', 'fuente', 'descripcion', 'datos', 'actualizado']
        read_only_fields = ['actualizado']

from rest_framework import serializers
from .models import ResultadoAnalisis


class ResultadoAnalisisSerializer(serializers.ModelSerializer):
    def validate_datos(self, value):
        ResultadoAnalisis.validate_datos_structure(value)
        return value

    class Meta:
        model = ResultadoAnalisis
        fields = ['nombre', 'fuente', 'descripcion', 'datos', 'actualizado']
        read_only_fields = ['actualizado']

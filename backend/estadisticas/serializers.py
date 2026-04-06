from rest_framework import serializers
from .models import EstadisticaResumen


class EstadisticaResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticaResumen
        fields = [
            'total_noticias',
            'total_verificadas',
            'violencia_fisica_count',
            'violencia_psicologica_count',
            'violencia_sexual_count',
            'violencia_economica_count',
            'violencia_patrimonial_count',
            'feminicidio_count',
            'ambito_familiar_count',
            'ambito_pareja_count',
            'ambito_comunitario_count',
            'ambito_institucional_count',
            'actualizado',
        ]


class ResumenViewSerializer(serializers.Serializer):
    """Serializer para la vista de resumen general"""
    total_noticias = serializers.IntegerField()
    total_verificadas = serializers.IntegerField()
    
    # Tipos de violencia
    tipos_violencia = serializers.DictField()
    
    # Ámbitos
    ambitos = serializers.DictField()
    
    # Ciudades top
    ciudades_top = serializers.ListField()


class TendenciaSerializer(serializers.Serializer):
    """Serializer para tendencias mensuales"""
    mes = serializers.CharField()
    total = serializers.IntegerField()
    verificadas = serializers.IntegerField()
    
    # Tipos de violencia por mes
    tipos_violencia = serializers.DictField()


class TiposViolenciaSerializer(serializers.Serializer):
    """Serializer para conteo de tipos de violencia"""
    tipo = serializers.CharField()
    cantidad = serializers.IntegerField()
    porcentaje = serializers.FloatField()

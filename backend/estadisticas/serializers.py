from rest_framework import serializers


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

from rest_framework import serializers

from .models import Noticia


class NoticiaSerializer(serializers.ModelSerializer):
    tipo_violencia = serializers.SerializerMethodField()

    class Meta:
        model = Noticia
        fields = "__all__"

    def get_tipo_violencia(self, obj):
        return obj.tipo_violencia

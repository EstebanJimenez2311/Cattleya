from django.contrib import admin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fuente', 'ciudad', 'tipo_violencia', 'nivel_riesgo', 'verificada', 'fecha_publicacion')
    list_filter = ('tipo_violencia', 'nivel_riesgo', 'verificada', 'ciudad', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion', 'fuente', 'ciudad')

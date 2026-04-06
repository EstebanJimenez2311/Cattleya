from django.contrib import admin
from .models import ResultadoAnalisis


@admin.register(ResultadoAnalisis)
class ResultadoAnalisisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fuente', 'actualizado')
    readonly_fields = ('actualizado',)
    search_fields = ('nombre', 'fuente')
    list_filter = ('actualizado',)

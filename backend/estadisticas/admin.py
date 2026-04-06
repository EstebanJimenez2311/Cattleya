from django.contrib import admin
from .models import EstadisticaResumen


@admin.register(EstadisticaResumen)
class EstadisticaResumenAdmin(admin.ModelAdmin):
    list_display = ('actualizado', 'total_noticias', 'total_verificadas')
    readonly_fields = ('actualizado',)
    fieldsets = (
        ('General', {
            'fields': ('total_noticias', 'total_verificadas', 'actualizado')
        }),
        ('Tipos de Violencia', {
            'fields': (
                'violencia_fisica_count',
                'violencia_psicologica_count',
                'violencia_sexual_count',
                'violencia_economica_count',
                'violencia_patrimonial_count',
                'feminicidio_count',
            )
        }),
        ('Ámbitos', {
            'fields': (
                'ambito_familiar_count',
                'ambito_pareja_count',
                'ambito_comunitario_count',
                'ambito_institucional_count',
            )
        }),
    )

from django.db import models


class EstadisticaResumen(models.Model):
    """Almacena estadísticas resumidas para acceso rápido"""
    total_noticias = models.IntegerField(default=0)
    total_verificadas = models.IntegerField(default=0)
    
    # Por tipo de violencia
    violencia_fisica_count = models.IntegerField(default=0)
    violencia_psicologica_count = models.IntegerField(default=0)
    violencia_sexual_count = models.IntegerField(default=0)
    violencia_economica_count = models.IntegerField(default=0)
    violencia_patrimonial_count = models.IntegerField(default=0)
    feminicidio_count = models.IntegerField(default=0)
    
    # Por ámbito
    ambito_familiar_count = models.IntegerField(default=0)
    ambito_pareja_count = models.IntegerField(default=0)
    ambito_comunitario_count = models.IntegerField(default=0)
    ambito_institucional_count = models.IntegerField(default=0)
    
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estadísticas actualizadas: {self.actualizado}"

    class Meta:
        verbose_name = "Estadística de Resumen"
        verbose_name_plural = "Estadísticas de Resumen"

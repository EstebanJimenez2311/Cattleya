from django.db import models
from django.utils import timezone


class ResultadoAnalisis(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fuente = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    datos = models.JSONField()
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Resultado de Análisis"
        verbose_name_plural = "Resultados de Análisis"
        ordering = ["-actualizado"]

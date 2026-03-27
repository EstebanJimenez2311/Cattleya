from django.db import models
import re

class Noticia(models.Model):
    TIPO_VIOLENCIA_CHOICES = [
        ('fisica', 'Violencia Física'),
        ('psicologica', 'Violencia Psicológica'),
        ('sexual', 'Violencia Sexual'),
        ('economica', 'Violencia Económica'),
        ('otros', 'Otros'),
    ]

    NIVEL_RIESGO_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField()
    fuente = models.CharField(max_length=100)
    url = models.URLField()
    ciudad = models.CharField(max_length=100)
    tipo_violencia = models.CharField(max_length=20, choices=TIPO_VIOLENCIA_CHOICES, blank=True)
    nivel_riesgo = models.CharField(max_length=10, choices=NIVEL_RIESGO_CHOICES, blank=True)
    verificada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Clasificar tipo_violencia basado en palabras clave
        texto = f"{self.titulo} {self.descripcion}".lower()
        if re.search(r'\b(física|golpe|agresión|violencia física)\b', texto):
            self.tipo_violencia = 'fisica'
        elif re.search(r'\b(psicológica|amenaza|insulto|violencia psicológica)\b', texto):
            self.tipo_violencia = 'psicologica'
        elif re.search(r'\b(sexual|abuso|violación|violencia sexual)\b', texto):
            self.tipo_violencia = 'sexual'
        elif re.search(r'\b(económica|dinero|control económico|violencia económica)\b', texto):
            self.tipo_violencia = 'economica'
        else:
            self.tipo_violencia = 'otros'

        # Calcular nivel_riesgo basado en tipo_violencia
        if self.tipo_violencia in ['fisica', 'sexual']:
            self.nivel_riesgo = 'alto'
        elif self.tipo_violencia == 'psicologica':
            self.nivel_riesgo = 'medio'
        else:
            self.nivel_riesgo = 'bajo'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_publicacion']

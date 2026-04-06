import re
import unicodedata

from django.db import models


class Noticia(models.Model):
    NIVEL_RIESGO_CHOICES = [
        ("bajo", "Bajo"),
        ("medio", "Medio"),
        ("alto", "Alto"),
        ("critico", "Critico"),
    ]

    AMBITO_CHOICES = [
        ("familiar", "Familiar"),
        ("pareja", "Pareja"),
        ("comunitario", "Comunitario"),
        ("institucional", "Institucional"),
        ("otro", "Otro"),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField()
    fuente = models.CharField(max_length=100)
    url = models.URLField(max_length=1000)
    ciudad = models.CharField(max_length=100)

    violencia_fisica = models.BooleanField(default=False)
    violencia_psicologica = models.BooleanField(default=False)
    violencia_sexual = models.BooleanField(default=False)
    violencia_economica = models.BooleanField(default=False)
    violencia_patrimonial = models.BooleanField(default=False)
    feminicidio = models.BooleanField(default=False)

    ambito_violencia = models.CharField(max_length=20, choices=AMBITO_CHOICES, blank=True)
    nivel_riesgo = models.CharField(max_length=10, choices=NIVEL_RIESGO_CHOICES, blank=True)

    verificada = models.BooleanField(default=False)
    es_prueba = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def reset_clasificacion(self):
        self.violencia_fisica = False
        self.violencia_psicologica = False
        self.violencia_sexual = False
        self.violencia_economica = False
        self.violencia_patrimonial = False
        self.feminicidio = False

    def normalizar_texto(self, texto):
        texto = unicodedata.normalize("NFD", texto.lower())
        return "".join(char for char in texto if unicodedata.category(char) != "Mn")

    def clasificar_violencia(self, texto):
        texto = self.normalizar_texto(texto)
        self.reset_clasificacion()

        if re.search(r"\b(golpe|agresion|agresion fisica|herida|lesion|maltrato fisico|arma blanca)\b", texto):
            self.violencia_fisica = True

        if re.search(r"\b(amenaza|amenazas|insulto|intimidacion|humillacion|control|hostigamiento|manipulacion)\b", texto):
            self.violencia_psicologica = True

        if re.search(r"\b(abuso sexual|violacion|acoso sexual)\b", texto):
            self.violencia_sexual = True

        if re.search(r"\b(control economico|dinero|dependencia economica|ingresos|recursos)\b", texto):
            self.violencia_economica = True

        if re.search(r"\b(destruccion de bienes|retencion de documentos|dano patrimonial)\b", texto):
            self.violencia_patrimonial = True

        if re.search(r"\b(feminicidio|asesinada|hallada sin vida)\b", texto):
            self.feminicidio = True

    def inferir_ambito(self, texto):
        texto = self.normalizar_texto(texto)

        if re.search(r"\b(pareja|expareja|novio|novia|esposo|esposa)\b", texto):
            return "pareja"
        if re.search(r"\b(familia|familiar|hogar|padre|madre|hermano|hermana)\b", texto):
            return "familiar"
        if re.search(r"\b(jefe|empresa|laboral|trabajo|institucion|ministerio)\b", texto):
            return "institucional"
        if re.search(r"\b(calle|via publica|transporte publico|bus|vecinos|comunidad|barrio)\b", texto):
            return "comunitario"

        return "otro"

    def calcular_riesgo(self):
        if self.feminicidio:
            return "critico"
        if self.violencia_fisica or self.violencia_sexual:
            return "alto"
        if self.violencia_psicologica:
            return "medio"
        return "bajo"

    @property
    def tipo_violencia(self):
        tipos = []

        if self.feminicidio:
            tipos.append("feminicidio")
        if self.violencia_fisica:
            tipos.append("fisica")
        if self.violencia_psicologica:
            tipos.append("psicologica")
        if self.violencia_sexual:
            tipos.append("sexual")
        if self.violencia_economica:
            tipos.append("economica")
        if self.violencia_patrimonial:
            tipos.append("patrimonial")

        return ", ".join(tipos) if tipos else "otros"

    def save(self, *args, **kwargs):
        texto = f"{self.titulo} {self.descripcion} {self.contenido or ''}"
        self.clasificar_violencia(texto)
        self.ambito_violencia = self.inferir_ambito(texto)
        self.nivel_riesgo = self.calcular_riesgo()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ["-fecha_publicacion"]

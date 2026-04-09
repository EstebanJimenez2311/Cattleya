from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import ResultadoAnalisis
from .services import (
    build_frontend_payload,
    get_analysis_description,
    get_analysis_name,
    get_analysis_source,
    parse_analysis_json,
)


class ResultadoAnalisisAdminForm(forms.ModelForm):
    archivo_json = forms.FileField(
        required=False,
        label="Archivo JSON",
        help_text="Puedes seleccionar o arrastrar aquí un archivo .json exportado desde el notebook.",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".json,application/json",
                "class": "cattleya-drop-input",
                "data-dropzone-label": "Suelta aquí tu archivo JSON o haz clic para seleccionarlo",
            }
        ),
    )

    class Meta:
        model = ResultadoAnalisis
        fields = ("nombre", "fuente", "descripcion")
        help_texts = {
            "nombre": "Identificador único del análisis. Si cargas desde JSON puede salir de metadata.nombre.",
        }

    def clean(self):
        cleaned_data = super().clean()
        archivo_json = cleaned_data.get("archivo_json")
        if not archivo_json:
            return cleaned_data

        raw_text = archivo_json.read().decode("utf-8", errors="replace")
        payload = parse_analysis_json(raw_text)
        cleaned_data["datos"] = payload

        if not cleaned_data.get("nombre"):
            cleaned_data["nombre"] = get_analysis_name(payload)
        if not cleaned_data.get("fuente"):
            cleaned_data["fuente"] = get_analysis_source(
                payload,
                fallback=getattr(archivo_json, "name", "json"),
            )
        if not cleaned_data.get("descripcion"):
            cleaned_data["descripcion"] = get_analysis_description(
                payload,
                fallback="Carga desde admin",
            )

        self.instance.datos = cleaned_data["datos"]
        self.instance.nombre = cleaned_data["nombre"]
        self.instance.fuente = cleaned_data["fuente"]
        self.instance.descripcion = cleaned_data["descripcion"]
        return cleaned_data

@admin.register(ResultadoAnalisis)
class ResultadoAnalisisAdmin(admin.ModelAdmin):
    form = ResultadoAnalisisAdminForm
    list_display = ("nombre", "fuente", "kpi_total_registros", "kpi_total_victimas", "actualizado")
    readonly_fields = (
        "actualizado",
        "kpi_total_registros",
        "kpi_total_victimas",
        "total_anos_evolucion",
        "total_categorias",
        "dashboard_preview",
    )
    search_fields = ("nombre", "fuente")
    list_filter = ("actualizado",)
    fields = (
        "archivo_json",
        "nombre",
        "fuente",
        "descripcion",
        "kpi_total_registros",
        "kpi_total_victimas",
        "total_anos_evolucion",
        "total_categorias",
        "dashboard_preview",
        "actualizado",
    )

    class Media:
        css = {"all": ("admin/css/analisis-upload.css",)}
        js = ("admin/js/analisis-upload.js",)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly_fields.append("nombre")
        return readonly_fields

    def _frontend_payload(self, obj):
        if not obj or not isinstance(obj.datos, dict):
            return {}
        try:
            return build_frontend_payload(obj)
        except Exception:
            return {}

    @admin.display(description="Total registros VBG")
    def kpi_total_registros(self, obj):
        stats = self._frontend_payload(obj).get("stats") or []
        return stats[0]["number"] if stats else "-"

    @admin.display(description="Total víctimas VBG")
    def kpi_total_victimas(self, obj):
        stats = self._frontend_payload(obj).get("stats") or []
        return stats[0]["number"] if stats else "-"

    @admin.display(description="Años en evolución")
    def total_anos_evolucion(self, obj):
        chart = ((self._frontend_payload(obj).get("charts") or {}).get("chart-evolucion")) or {}
        labels = ((chart.get("data") or {}).get("labels")) or []
        return len(labels)

    @admin.display(description="Categorías")
    def total_categorias(self, obj):
        chart = ((self._frontend_payload(obj).get("charts") or {}).get("chart-tipo")) or {}
        labels = ((chart.get("data") or {}).get("labels")) or []
        return len(labels)

    @admin.display(description="Vista previa")
    def dashboard_preview(self, obj):
        if not obj or not obj.datos:
            return "Sin datos disponibles."
        payload = self._frontend_payload(obj)
        metadata = payload.get("metadata") or {}
        return format_html(
            "<div>"
            "<p><strong>Nombre:</strong> {}</p>"
            "<p><strong>Fuente:</strong> {}</p>"
            "<p><strong>Total víctimas VBG:</strong> {}</p>"
            "<p><strong>Años en evolución temporal:</strong> {}</p>"
            "<p><strong>Total de categorías:</strong> {}</p>"
            "<p><strong>Fecha del análisis:</strong> {}</p>"
            "</div>",
            obj.nombre,
            obj.fuente,
            self.kpi_total_victimas(obj),
            self.total_anos_evolucion(obj),
            self.total_categorias(obj),
            metadata.get("fecha", "-"),
        )

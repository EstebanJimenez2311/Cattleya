from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import ResultadoAnalisis

DASHBOARD_NAME = "dashboard"


class ResultadoAnalisisAdminForm(forms.ModelForm):
    class Meta:
        model = ResultadoAnalisis
        fields = "__all__"
        help_texts = {
            "nombre": 'Valor permitido: "dashboard".',
            "datos": (
                "Estructura esperada: contexto, dashboard_principal, "
                "analisis_segmentado y foco_regional. "
                'Ejemplo corto: {"contexto": {...}, "dashboard_principal": {"kpis": '
                '{"total_registros_vbg": 613173, "total_victimas_vbg": 2088795}}, '
                '"analisis_segmentado": {...}, "foco_regional": {...}}'
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre != DASHBOARD_NAME:
            raise forms.ValidationError('El valor de "nombre" debe ser "dashboard".')
        return nombre

    def clean_datos(self):
        datos = self.cleaned_data.get("datos")
        ResultadoAnalisis.validate_datos_structure(datos)
        return datos


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
        "nombre",
        "fuente",
        "descripcion",
        "datos",
        "kpi_total_registros",
        "kpi_total_victimas",
        "total_anos_evolucion",
        "total_categorias",
        "dashboard_preview",
        "actualizado",
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["nombre"] = DASHBOARD_NAME
        return initial

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly_fields.append("nombre")
        return readonly_fields

    def _dashboard_kpis(self, obj):
        if not obj or not isinstance(obj.datos, dict):
            return {}
        dashboard = obj.datos.get("dashboard_principal") or {}
        return dashboard.get("kpis") or {}

    def _dashboard_evolucion(self, obj):
        if not obj or not isinstance(obj.datos, dict):
            return []
        dashboard = obj.datos.get("dashboard_principal") or {}
        return dashboard.get("evolucion_temporal") or []

    def _dashboard_categorias(self, obj):
        if not obj or not isinstance(obj.datos, dict):
            return []
        dashboard = obj.datos.get("dashboard_principal") or {}
        return dashboard.get("distribucion_categorica") or []

    @admin.display(description="Total registros VBG")
    def kpi_total_registros(self, obj):
        return self._dashboard_kpis(obj).get("total_registros_vbg", "-")

    @admin.display(description="Total victimas VBG")
    def kpi_total_victimas(self, obj):
        return self._dashboard_kpis(obj).get("total_victimas_vbg", "-")

    @admin.display(description="Anos en evolucion")
    def total_anos_evolucion(self, obj):
        return len(self._dashboard_evolucion(obj))

    @admin.display(description="Categorias")
    def total_categorias(self, obj):
        return len(self._dashboard_categorias(obj))

    @admin.display(description="Vista previa")
    def dashboard_preview(self, obj):
        if not obj or not obj.datos:
            return "Sin datos disponibles."
        return format_html(
            "<div>"
            "<p><strong>Total registros VBG:</strong> {}</p>"
            "<p><strong>Total victimas VBG:</strong> {}</p>"
            "<p><strong>Anos en evolucion temporal:</strong> {}</p>"
            "<p><strong>Total de categorias:</strong> {}</p>"
            "</div>",
            self.kpi_total_registros(obj),
            self.kpi_total_victimas(obj),
            self.total_anos_evolucion(obj),
            self.total_categorias(obj),
        )

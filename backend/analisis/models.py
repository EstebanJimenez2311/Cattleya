from django.core.exceptions import ValidationError
from django.db import models


def _require_keys(value, required_keys, path):
    if not isinstance(value, dict):
        raise ValidationError({path: "Debe ser un objeto JSON."})

    missing = [key for key in required_keys if key not in value]
    if missing:
        raise ValidationError({path: f"Faltan claves requeridas: {', '.join(missing)}."})


def _require_list_of_dicts(value, item_keys, path):
    if not isinstance(value, list):
        raise ValidationError({path: "Debe ser una lista."})

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValidationError({path: f"El elemento {index} debe ser un objeto."})
        missing = [key for key in item_keys if key not in item]
        if missing:
            raise ValidationError(
                {path: f"El elemento {index} no contiene: {', '.join(missing)}."}
            )


class ResultadoAnalisis(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fuente = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    datos = models.JSONField()
    actualizado = models.DateTimeField(auto_now=True)

    @staticmethod
    def validate_datos_structure(datos):
        root_keys = [
            "contexto",
            "dashboard_principal",
            "analisis_segmentado",
            "foco_regional",
        ]
        _require_keys(datos, root_keys, "datos")

        contexto = datos["contexto"]
        _require_keys(
            contexto,
            ["fuente", "dataset", "cobertura", "periodo", "territorio_foco"],
            "datos.contexto",
        )
        _require_keys(
            contexto["periodo"],
            ["inicio", "fin"],
            "datos.contexto.periodo",
        )
        _require_keys(
            contexto["cobertura"],
            ["alcance", "criterio"],
            "datos.contexto.cobertura",
        )
        if "generated_at" in contexto and not isinstance(contexto["generated_at"], str):
            raise ValidationError({"datos.contexto.generated_at": "Debe ser texto ISO-8601."})

        dashboard = datos["dashboard_principal"]
        _require_keys(
            dashboard,
            ["kpis", "evolucion_temporal", "distribucion_categorica"],
            "datos.dashboard_principal",
        )
        _require_keys(
            dashboard["kpis"],
            ["total_registros_vbg", "total_victimas_vbg"],
            "datos.dashboard_principal.kpis",
        )
        _require_list_of_dicts(
            dashboard["evolucion_temporal"],
            ["ano", "victimas", "variacion_pct"],
            "datos.dashboard_principal.evolucion_temporal",
        )
        _require_list_of_dicts(
            dashboard["distribucion_categorica"],
            ["categoria", "total_victimas"],
            "datos.dashboard_principal.distribucion_categorica",
        )

        segmentado = datos["analisis_segmentado"]
        _require_keys(
            segmentado,
            ["grupos_etarios", "poblaciones_especiales"],
            "datos.analisis_segmentado",
        )
        _require_keys(
            segmentado["grupos_etarios"],
            ["distribucion", "top_delitos_por_grupo"],
            "datos.analisis_segmentado.grupos_etarios",
        )
        _require_list_of_dicts(
            segmentado["grupos_etarios"]["distribucion"],
            ["grupo_etario", "total_victimas", "porcentaje"],
            "datos.analisis_segmentado.grupos_etarios.distribucion",
        )
        _require_list_of_dicts(
            segmentado["grupos_etarios"]["top_delitos_por_grupo"],
            ["grupo_etario", "grupo_delito", "total_victimas"],
            "datos.analisis_segmentado.grupos_etarios.top_delitos_por_grupo",
        )
        _require_list_of_dicts(
            segmentado["poblaciones_especiales"],
            ["poblacion", "total", "porcentaje"],
            "datos.analisis_segmentado.poblaciones_especiales",
        )

        regional = datos["foco_regional"]
        _require_keys(
            regional,
            ["territorio", "comparativas", "top_delitos"],
            "datos.foco_regional",
        )
        if not isinstance(regional["territorio"], str):
            raise ValidationError({"datos.foco_regional.territorio": "Debe ser texto."})
        _require_keys(
            regional["comparativas"],
            ["evolucion_vs_nacional", "perfil_delitos_vs_nacional"],
            "datos.foco_regional.comparativas",
        )
        _require_list_of_dicts(
            regional["comparativas"]["evolucion_vs_nacional"],
            ["ano", "victimas_atl", "victimas_nacional", "pct_atl"],
            "datos.foco_regional.comparativas.evolucion_vs_nacional",
        )
        _require_list_of_dicts(
            regional["comparativas"]["perfil_delitos_vs_nacional"],
            [
                "grupo_delito",
                "nacional",
                "atlantico",
                "pct_atl_vs_nacional",
                "pct_nacional",
                "pct_atlantico",
            ],
            "datos.foco_regional.comparativas.perfil_delitos_vs_nacional",
        )
        _require_list_of_dicts(
            regional["top_delitos"],
            ["grupo_delito", "total_victimas", "porcentaje"],
            "datos.foco_regional.top_delitos",
        )

        if "feminicidio" in dashboard:
            _require_keys(
                dashboard["feminicidio"],
                ["serie_anual", "serie_anual_por_sexo"],
                "datos.dashboard_principal.feminicidio",
            )
            _require_list_of_dicts(
                dashboard["feminicidio"]["serie_anual"],
                ["ano", "total_victimas"],
                "datos.dashboard_principal.feminicidio.serie_anual",
            )
            _require_list_of_dicts(
                dashboard["feminicidio"]["serie_anual_por_sexo"],
                ["ano", "sexo", "victimas"],
                "datos.dashboard_principal.feminicidio.serie_anual_por_sexo",
            )

    def clean(self):
        super().clean()
        self.validate_datos_structure(self.datos)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Resultado de Análisis"
        verbose_name_plural = "Resultados de Análisis"
        ordering = ["-actualizado"]

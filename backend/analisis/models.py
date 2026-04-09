import math

from django.core.exceptions import ValidationError
from django.db import models


def _sanitize_json_numbers(value):
    if isinstance(value, dict):
        return {key: _sanitize_json_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_json_numbers(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


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
        if isinstance(datos, dict) and {"metadata", "dashboard"}.issubset(datos.keys()):
            ResultadoAnalisis._validate_notebook_export(datos)
            return

        if isinstance(datos, dict) and {
            "contexto",
            "dashboard_principal",
            "analisis_segmentado",
            "foco_regional",
        }.issubset(datos.keys()):
            ResultadoAnalisis._validate_legacy_structure(datos)
            return

        if isinstance(datos, dict) and {
            "informacion_general_notebook",
            "carga_de_datos",
            "analisis_exploratorio_datos",
            "preprocesamiento_ml",
            "resultados_modelado",
            "evaluacion_profunda",
            "interpretabilidad",
            "predicciones_prophet",
        }.issubset(datos.keys()):
            ResultadoAnalisis._validate_predictive_structure(datos)
            return

        raise ValidationError(
            {
                "datos": (
                    "La estructura del JSON no es compatible. "
                    "Se esperaba un export con claves metadata/dashboard, "
                    "la estructura legacy contexto/dashboard_principal/analisis_segmentado/foco_regional "
                    "o un export predictivo con módulos de ML y predicciones."
                )
            }
        )

    @staticmethod
    def _validate_notebook_export(datos):
        _require_keys(datos, ["metadata", "dashboard"], "datos")
        _require_keys(datos["metadata"], ["nombre", "fecha", "fuente"], "datos.metadata")

        if not isinstance(datos["dashboard"], dict):
            raise ValidationError({"datos.dashboard": "Debe ser un objeto JSON."})

        insights = datos.get("insights", [])
        if insights and not isinstance(insights, list):
            raise ValidationError({"datos.insights": "Debe ser una lista."})

    @staticmethod
    def _validate_predictive_structure(datos):
        _require_keys(
            datos,
            [
                "informacion_general_notebook",
                "carga_de_datos",
                "analisis_exploratorio_datos",
                "preprocesamiento_ml",
                "resultados_modelado",
                "evaluacion_profunda",
                "interpretabilidad",
                "predicciones_prophet",
            ],
            "datos",
        )

        info = datos["informacion_general_notebook"]
        _require_keys(
            info,
            ["titulo", "descripcion_general", "estructura_modular", "librerias_cargadas"],
            "datos.informacion_general_notebook",
        )
        if not isinstance(info["estructura_modular"], list):
            raise ValidationError(
                {"datos.informacion_general_notebook.estructura_modular": "Debe ser una lista."}
            )
        if not isinstance(info["librerias_cargadas"], list):
            raise ValidationError(
                {"datos.informacion_general_notebook.librerias_cargadas": "Debe ser una lista."}
            )

        carga = datos["carga_de_datos"]
        _require_keys(
            carga,
            ["ruta_datos", "shape_raw", "columnas_raw", "head_raw"],
            "datos.carga_de_datos",
        )
        if not isinstance(carga["shape_raw"], list) or len(carga["shape_raw"]) != 2:
            raise ValidationError({"datos.carga_de_datos.shape_raw": "Debe ser una lista de dos elementos."})
        if not isinstance(carga["columnas_raw"], list):
            raise ValidationError({"datos.carga_de_datos.columnas_raw": "Debe ser una lista."})
        if not isinstance(carga["head_raw"], list):
            raise ValidationError({"datos.carga_de_datos.head_raw": "Debe ser una lista."})

        eda = datos["analisis_exploratorio_datos"]
        _require_keys(
            eda,
            [
                "tipos_de_datos",
                "nulos_por_columna",
                "estadisticas_descriptivas",
                "distribucion_variable_objetivo",
                "ratio_desbalance_vcm",
                "casos_vcm_por_patron",
            ],
            "datos.analisis_exploratorio_datos",
        )

        pre = datos["preprocesamiento_ml"]
        _require_keys(
            pre,
            [
                "columnas_eliminadas",
                "X_shape_inicial",
                "y_distribucion_inicial",
                "variables_numericas",
                "variables_categoricas",
                "estrategia_imputacion",
                "encoding_categorias",
                "X_shape_final_ml_preprocesado",
                "train_test_split",
            ],
            "datos.preprocesamiento_ml",
        )

        resultados = datos["resultados_modelado"]
        _require_keys(
            resultados,
            ["comparacion_modelos", "random_forest", "xgboost", "logistic_regression"],
            "datos.resultados_modelado",
        )

        evaluacion = datos["evaluacion_profunda"]
        _require_keys(
            evaluacion,
            ["umbral_decision_optimo_rf", "cross_validation_random_forest"],
            "datos.evaluacion_profunda",
        )

        interpretabilidad = datos["interpretabilidad"]
        _require_keys(
            interpretabilidad,
            ["top_20_feature_importance_rf", "shap_global_description"],
            "datos.interpretabilidad",
        )

        predicciones = datos["predicciones_prophet"]
        _require_keys(
            predicciones,
            [
                "circunstancias_modeladas",
                "prediccion_nacional_vcm_anual",
                "predicciones_por_circunstancia_anual",
            ],
            "datos.predicciones_prophet",
        )
        _require_list_of_dicts(
            predicciones["prediccion_nacional_vcm_anual"],
            ["anio", "prediccion", "minimo", "maximo"],
            "datos.predicciones_prophet.prediccion_nacional_vcm_anual",
        )
        _require_list_of_dicts(
            predicciones["predicciones_por_circunstancia_anual"],
            ["Circunstancia", "Año", "Predicción", "Mínimo (IC95%)", "Máximo (IC95%)", "Var% vs 2025"],
            "datos.predicciones_prophet.predicciones_por_circunstancia_anual",
        )

    @staticmethod
    def _validate_legacy_structure(datos):
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
        self.datos = _sanitize_json_numbers(self.datos)
        self.validate_datos_structure(self.datos)

    def save(self, *args, **kwargs):
        self.datos = _sanitize_json_numbers(self.datos)
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Resultado de Análisis"
        verbose_name_plural = "Resultados de Análisis"
        ordering = ["-actualizado"]

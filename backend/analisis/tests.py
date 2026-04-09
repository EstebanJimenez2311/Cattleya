from django.core.exceptions import ValidationError
from django.test import TestCase

from analisis.models import ResultadoAnalisis


def build_valid_payload():
    return {
        "contexto": {
            "fuente": "EDA2-Fiscalia.ipynb",
            "dataset": "Conteo_de_Victimas_V2_2018-2026-V5.csv",
            "generated_at": "2026-04-08T12:00:00",
            "cobertura": {
                "alcance": "Colombia",
                "criterio": "Registros VBG con a_o_hechos <= 2025",
            },
            "periodo": {"inicio": 2018, "fin": 2025},
            "territorio_foco": "atlantico",
        },
        "dashboard_principal": {
            "kpis": {
                "total_registros_vbg": 613173,
                "total_victimas_vbg": 2088795,
            },
            "evolucion_temporal": [
                {"ano": 2018, "victimas": 227497, "variacion_pct": None},
                {"ano": 2019, "victimas": 247516, "variacion_pct": 8.799676},
            ],
            "distribucion_categorica": [
                {"categoria": "violencia intrafamiliar", "total_victimas": 832825},
                {"categoria": "lesiones personales", "total_victimas": 370277},
            ],
            "feminicidio": {
                "serie_anual": [
                    {"ano": 2018, "total_victimas": 680},
                    {"ano": 2019, "total_victimas": 639},
                ],
                "serie_anual_por_sexo": [
                    {"ano": 2018, "sexo": "femenino", "victimas": 613},
                    {"ano": 2018, "sexo": "masculino", "victimas": 66},
                ],
            },
        },
        "analisis_segmentado": {
            "grupos_etarios": {
                "distribucion": [
                    {
                        "grupo_etario": "ninez (0-13)",
                        "total_victimas": 320760,
                        "porcentaje": 18.9,
                    }
                ],
                "top_delitos_por_grupo": [
                    {
                        "grupo_etario": "ninez (0-13)",
                        "grupo_delito": "delitos sexuales",
                        "total_victimas": 150904,
                    }
                ],
            },
            "poblaciones_especiales": [
                {"poblacion": "NNA", "total": 539142, "porcentaje": 25.81}
            ],
        },
        "foco_regional": {
            "territorio": "atlantico",
            "comparativas": {
                "evolucion_vs_nacional": [
                    {
                        "ano": 2018,
                        "victimas_atl": 8233,
                        "victimas_nacional": 227497,
                        "pct_atl": 3.62,
                    }
                ],
                "perfil_delitos_vs_nacional": [
                    {
                        "grupo_delito": "amenazas",
                        "nacional": 216580,
                        "atlantico": 11340,
                        "pct_atl_vs_nacional": 5.24,
                        "pct_nacional": 10.4,
                        "pct_atlantico": 15.5,
                    }
                ],
            },
            "top_delitos": [
                {
                    "grupo_delito": "violencia intrafamiliar",
                    "total_victimas": 24852,
                    "porcentaje": 34.1,
                }
            ],
        },
    }


class ResultadoAnalisisValidationTests(TestCase):
    def test_valid_payload_passes_model_validation(self):
        resultado = ResultadoAnalisis(
            nombre="eda_fiscalia_vbg",
            fuente="notebook",
            descripcion="Analisis consolidado",
            datos=build_valid_payload(),
        )

        resultado.full_clean()

    def test_missing_root_key_fails_validation(self):
        payload = build_valid_payload()
        payload.pop("foco_regional")
        resultado = ResultadoAnalisis(
            nombre="eda_fiscalia_vbg",
            fuente="notebook",
            descripcion="Analisis consolidado",
            datos=payload,
        )

        with self.assertRaises(ValidationError):
            resultado.full_clean()

    def test_missing_nested_key_fails_validation(self):
        payload = build_valid_payload()
        payload["dashboard_principal"]["kpis"].pop("total_victimas_vbg")
        resultado = ResultadoAnalisis(
            nombre="eda_fiscalia_vbg",
            fuente="notebook",
            descripcion="Analisis consolidado",
            datos=payload,
        )

        with self.assertRaises(ValidationError):
            resultado.full_clean()

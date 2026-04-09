import json
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from analisis.models import ResultadoAnalisis
from analisis.services import build_frontend_payload, import_analysis_file, parse_analysis_json


def build_legacy_payload():
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


def build_notebook_payload():
    return {
        "metadata": {
            "nombre": "analisis_vbg_colombia",
            "fecha": "2026-04-02",
            "fuente": "Conteo_de_Victimas_V2_2018-2026-V5.csv",
        },
        "dashboard": {
            "panorama": {
                "evolucion_anual_vbg": [
                    {"ano": 2018, "victimas": 198463.0, "variacion_pct": None},
                    {"ano": 2019, "victimas": 215931.0, "variacion_pct": 8.8},
                    {"ano": 2025, "victimas": 252418.0, "variacion_pct": -1.32},
                ],
                "kpis": {
                    "total_casos_vbg": 1802681.0,
                    "promedio_anual_vbg": 225335.125,
                },
            },
            "geografico": {
                "geografico_vbg": [
                    {
                        "departamento_hecho": "bogota, d. c.",
                        "total_victimas": 433862.0,
                        "porcentaje": 24.1,
                    },
                    {
                        "departamento_hecho": "antioquia",
                        "total_victimas": 214952.0,
                        "porcentaje": 11.9,
                    },
                ]
            },
            "regional_atlantico": {
                "atlantico_delitos_vbg": [
                    {
                        "grupo_delito": "violencia intrafamiliar",
                        "total_victimas": 24852.0,
                        "porcentaje": 39.5,
                    },
                    {
                        "grupo_delito": "lesiones personales",
                        "total_victimas": 11689.0,
                        "porcentaje": 18.6,
                    },
                ]
            },
            "demografia": {
                "etario_vbg": [
                    {
                        "grupo_etario": "ninez (0-13)",
                        "total_victimas": 277266.0,
                        "porcentaje": 19.0,
                    },
                    {
                        "grupo_etario": "adulto (27-59)",
                        "total_victimas": 689223.0,
                        "porcentaje": 47.2,
                    },
                ]
            },
            "tendencias_delitos": {
                "comparativo_delitos_atl_vs_nacional": [
                    {"grupo_delito": "amenazas", "pct_atlantico": 15.5, "pct_nacional": 10.4}
                ]
            },
            "feminicidio": {
                "feminicidio_anual": [
                    {"ano": 2022, "feminicidios": 831.0},
                    {"ano": 2025, "feminicidios": 595.0},
                ]
            },
        },
        "insights": [
            {
                "tipo": "tendencia_temporal",
                "titulo": "Tendencia al alza en VBG",
                "descripcion": "La violencia basada en género muestra una tendencia general al alza.",
            }
        ],
    }


class ResultadoAnalisisValidationTests(TestCase):
    def test_legacy_payload_passes_model_validation(self):
        resultado = ResultadoAnalisis(
            nombre="eda_fiscalia_vbg",
            fuente="notebook",
            descripcion="Analisis consolidado",
            datos=build_legacy_payload(),
        )

        resultado.full_clean()

    def test_notebook_payload_passes_model_validation(self):
        resultado = ResultadoAnalisis(
            nombre="analisis_vbg_colombia",
            fuente="json",
            descripcion="Carga desde notebook",
            datos=build_notebook_payload(),
        )

        resultado.full_clean()

    def test_missing_root_key_fails_validation(self):
        payload = build_legacy_payload()
        payload.pop("foco_regional")
        resultado = ResultadoAnalisis(
            nombre="eda_fiscalia_vbg",
            fuente="notebook",
            descripcion="Analisis consolidado",
            datos=payload,
        )

        with self.assertRaises(ValidationError):
            resultado.full_clean()


class ResultadoAnalisisImportTests(TestCase):
    def test_parse_analysis_json_supports_nan(self):
        parsed = parse_analysis_json(
            '{"metadata":{"nombre":"test","fecha":"2026-04-02","fuente":"csv"},'
            '"dashboard":{"panorama":{"evolucion_anual_vbg":[{"ano":2018,"victimas":1,"variacion_pct":NaN}],"kpis":{"total_casos_vbg":1}}}}'
        )
        value = parsed["dashboard"]["panorama"]["evolucion_anual_vbg"][0]["variacion_pct"]
        self.assertIsNone(value)

    def test_import_analysis_file_creates_resultado(self):
        payload = build_notebook_payload()
        file_obj = BytesIO(json.dumps(payload).encode("utf-8"))
        file_obj.name = "analisis_vbg_results.json"

        resultado, created = import_analysis_file(file_obj)

        self.assertTrue(created)
        self.assertEqual(resultado.nombre, "analisis_vbg_colombia")
        self.assertEqual(ResultadoAnalisis.objects.count(), 1)

    def test_build_frontend_payload_returns_chart_configs(self):
        resultado = ResultadoAnalisis.objects.create(
            nombre="analisis_vbg_colombia",
            fuente="json",
            descripcion="Carga desde notebook",
            datos=build_notebook_payload(),
        )

        payload = build_frontend_payload(resultado)

        self.assertIn("stats", payload)
        self.assertIn("charts", payload)
        self.assertIn("chart-evolucion", payload["charts"])
        self.assertIn("chart-comparativo-delitos", payload["charts"])
        self.assertIn("chart-feminicidio-sexo", payload["charts"])
        self.assertIn("metadata_cards", payload)
        self.assertEqual(payload["source_schema"], "notebook_export")


class ResultadoAnalisisApiTests(TestCase):
    def test_dashboard_endpoint_returns_frontend_payload(self):
        ResultadoAnalisis.objects.create(
            nombre="analisis_vbg_colombia",
            fuente="json",
            descripcion="Carga desde notebook",
            datos=build_notebook_payload(),
        )

        response = self.client.get("/api/analisis/dashboard/")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["nombre"], "analisis_vbg_colombia")
        self.assertIn("chart-tipo", body["charts"])

    def test_upload_endpoint_creates_resultado(self):
        payload = build_notebook_payload()
        upload = SimpleUploadedFile(
            "analisis_vbg_results.json",
            json.dumps(payload).encode("utf-8"),
            content_type="application/json",
        )

        response = self.client.post("/api/analisis/cargar-json/", {"archivo": upload})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ResultadoAnalisis.objects.count(), 1)


class ResultadoAnalisisAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        self.client.force_login(self.user)

    def test_admin_add_form_hides_raw_datos_field(self):
        response = self.client.get("/admin/analisis/resultadoanalisis/add/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name=\"archivo_json\"")
        self.assertNotContains(response, "name=\"datos\"")

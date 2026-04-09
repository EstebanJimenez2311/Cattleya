import json
import math
from copy import deepcopy

from django.core.exceptions import ValidationError

from .models import ResultadoAnalisis


CHART_COLORS = {
    "magenta": "#9D2D6A",
    "magenta_dark": "#822157",
    "orange": "#F28C28",
    "orange_dark": "#d4700a",
    "rose": "#c44d8e",
    "cream": "#FDEEE9",
}


def _json_constant_parser(_value):
    return None


def decode_uploaded_bytes(content):
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValidationError("No fue posible decodificar el archivo JSON.")


def parse_analysis_json(raw_text):
    try:
        parsed = json.loads(raw_text, parse_constant=_json_constant_parser)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"JSON inválido: {exc.msg}") from exc

    return sanitize_json_numbers(parsed)


def sanitize_json_numbers(value):
    if isinstance(value, dict):
        return {key: sanitize_json_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_json_numbers(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def is_legacy_analysis_payload(datos):
    return isinstance(datos, dict) and {
        "contexto",
        "dashboard_principal",
        "analisis_segmentado",
        "foco_regional",
    }.issubset(datos.keys())


def is_notebook_analysis_payload(datos):
    return isinstance(datos, dict) and {"metadata", "dashboard"}.issubset(datos.keys())


def get_analysis_name(payload):
    metadata = payload.get("metadata") or {}
    return metadata.get("nombre") or "dashboard"


def get_analysis_source(payload, fallback="json"):
    metadata = payload.get("metadata") or {}
    return metadata.get("fuente") or fallback


def get_analysis_description(payload, fallback=""):
    metadata = payload.get("metadata") or {}
    fecha = metadata.get("fecha")
    nombre = metadata.get("nombre") or "Análisis cargado"
    if fecha:
        return f"{nombre} cargado desde exportación JSON del {fecha}."
    return fallback or f"{nombre} cargado desde exportación JSON."


def import_analysis_payload(payload, *, nombre=None, fuente=None, descripcion=None):
    cleaned_payload = sanitize_json_numbers(deepcopy(payload))
    resolved_name = nombre or get_analysis_name(cleaned_payload)
    resolved_source = fuente or get_analysis_source(cleaned_payload)
    resolved_description = descripcion or get_analysis_description(cleaned_payload)

    resultado, created = ResultadoAnalisis.objects.update_or_create(
        nombre=resolved_name,
        defaults={
            "fuente": resolved_source,
            "descripcion": resolved_description,
            "datos": cleaned_payload,
        },
    )
    return resultado, created


def import_analysis_file(file_obj, *, nombre=None, fuente=None, descripcion=None):
    raw_text = decode_uploaded_bytes(file_obj.read())
    payload = parse_analysis_json(raw_text)
    return import_analysis_payload(
        payload,
        nombre=nombre,
        fuente=fuente or getattr(file_obj, "name", "json"),
        descripcion=descripcion,
    )


def _compact_number(value):
    if value in (None, ""):
        return "N/D"
    if isinstance(value, (int, float)):
        return f"{value:,.0f}".replace(",", ".")
    return str(value)


def _percent(value):
    if value in (None, ""):
        return "N/D"
    return f"{value:.1f}%"


def _title_case(value):
    if value in (None, ""):
        return "N/D"
    return str(value).replace("_", " ").title()


def _build_chart_config(chart_type, labels, dataset_label, dataset_data, *, horizontal=False, doughnut=False):
    colors = [
        CHART_COLORS["magenta"],
        CHART_COLORS["magenta_dark"],
        CHART_COLORS["orange"],
        CHART_COLORS["cream"],
        CHART_COLORS["orange_dark"],
        CHART_COLORS["rose"],
        "#6b1a47",
    ]
    dataset = {
        "label": dataset_label,
        "data": dataset_data,
    }

    if chart_type == "line":
        dataset.update(
            {
                "borderColor": CHART_COLORS["magenta"],
                "backgroundColor": "rgba(157,45,106,0.08)",
                "borderWidth": 3,
                "pointBackgroundColor": CHART_COLORS["magenta"],
                "pointRadius": 5,
                "fill": True,
                "tension": 0.35,
            }
        )
    elif doughnut:
        dataset.update({"backgroundColor": colors[: len(dataset_data)], "borderWidth": 0, "hoverOffset": 8})
    else:
        dataset.update(
            {
                "backgroundColor": colors[: len(dataset_data)] if chart_type != "bar" or not horizontal else CHART_COLORS["magenta"],
                "borderRadius": 8,
                "hoverBackgroundColor": CHART_COLORS["orange"],
            }
        )

    options = {
        "responsive": True,
        "maintainAspectRatio": False,
        "plugins": {"legend": {"display": doughnut}},
    }

    if doughnut:
        options["plugins"]["legend"] = {"position": "right"}
    else:
        options["scales"] = {
            "y": {"grid": {"color": "rgba(0,0,0,0.05)"}},
            "x": {"grid": {"display": False}},
        }
        if horizontal:
            options["indexAxis"] = "y"

    return {
        "type": chart_type,
        "data": {"labels": labels, "datasets": [dataset]},
        "options": options,
    }


def _build_multi_dataset_chart(chart_type, labels, datasets, *, horizontal=False, stacked=False):
    colors = [
        CHART_COLORS["magenta"],
        CHART_COLORS["orange"],
        CHART_COLORS["magenta_dark"],
        CHART_COLORS["orange_dark"],
        CHART_COLORS["rose"],
        "#6b1a47",
    ]
    resolved_datasets = []

    for index, dataset in enumerate(datasets):
        color = dataset.get("color") or colors[index % len(colors)]
        item = {
            "label": dataset.get("label", f"Serie {index + 1}"),
            "data": dataset.get("data", []),
            "backgroundColor": color,
            "borderColor": color,
            "borderWidth": 2,
            "borderRadius": 8,
            "tension": 0.35,
        }
        if chart_type == "line":
            item.update(
                {
                    "fill": False,
                    "pointBackgroundColor": color,
                    "pointRadius": 4,
                }
            )
        resolved_datasets.append(item)

    options = {
        "responsive": True,
        "maintainAspectRatio": False,
        "plugins": {"legend": {"display": True, "position": "bottom"}},
    }

    if chart_type != "doughnut":
        options["scales"] = {
            "y": {"grid": {"color": "rgba(0,0,0,0.05)"}, "stacked": stacked},
            "x": {"grid": {"display": False}, "stacked": stacked},
        }
        if horizontal:
            options["indexAxis"] = "y"

    return {
        "type": chart_type,
        "data": {"labels": labels, "datasets": resolved_datasets},
        "options": options,
    }


def _build_grouped_series(rows, *, label_key, group_key, value_key, top_n=None):
    ordered_labels = []
    grouped = {}

    for row in rows:
        label = str(row.get(label_key, ""))
        group = _title_case(row.get(group_key, ""))
        value = row.get(value_key, 0) or 0

        if label not in ordered_labels:
            ordered_labels.append(label)
        grouped.setdefault(group, {})[label] = value

    datasets = []
    for index, (group, values) in enumerate(grouped.items()):
        datasets.append(
            {
                "label": group,
                "data": [values.get(label, 0) for label in ordered_labels],
                "color": None,
            }
        )

    if top_n:
        datasets = datasets[:top_n]

    return ordered_labels, datasets


def build_frontend_payload(resultado):
    datos = sanitize_json_numbers(resultado.datos or {})

    if is_legacy_analysis_payload(datos):
        return _build_frontend_from_legacy(resultado, datos)
    if is_notebook_analysis_payload(datos):
        return _build_frontend_from_notebook(resultado, datos)

    raise ValidationError("La estructura almacenada no es compatible con el frontend.")


def _build_frontend_from_notebook(resultado, datos):
    metadata = datos.get("metadata") or {}
    dashboard = datos.get("dashboard") or {}
    panorama = dashboard.get("panorama") or {}
    geografico = dashboard.get("geografico") or {}
    regional = dashboard.get("regional_atlantico") or {}
    demografia = dashboard.get("demografia") or {}
    tendencias = dashboard.get("tendencias_delitos") or {}
    feminicidio = dashboard.get("feminicidio") or {}
    insights = datos.get("insights") or []

    evolucion = panorama.get("evolucion_anual_vbg") or []
    geografia = sorted(
        geografico.get("geografico_vbg") or [],
        key=lambda item: item.get("total_victimas", 0),
        reverse=True,
    )[:10]
    grupos_etarios = demografia.get("etario_vbg") or []
    poblaciones = demografia.get("poblaciones_especiales_vbg") or []
    top_delitos_por_etario = sorted(
        demografia.get("top_delitos_por_etario") or [],
        key=lambda item: item.get("total_victimas", 0),
        reverse=True,
    )
    top_delitos = sorted(
        regional.get("atlantico_delitos_vbg") or [],
        key=lambda item: item.get("total_victimas", 0),
        reverse=True,
    )
    comparativo_delitos = sorted(
        tendencias.get("comparativo_delitos_atl_vs_nacional") or [],
        key=lambda item: item.get("atlantico", 0),
        reverse=True,
    )
    evolucion_atlantico = tendencias.get("evolucion_atlantico_por_delito") or []
    atlantico_vs_nacional = regional.get("atlantico_vs_nacional_evolucion") or []
    feminicidio_anual = feminicidio.get("feminicidio_anual") or []
    feminicidio_por_sexo = feminicidio.get("feminicidio_por_sexo_anual") or []
    kpis = panorama.get("kpis") or {}

    feminicidio_labels, feminicidio_datasets = _build_grouped_series(
        feminicidio_por_sexo,
        label_key="ano",
        group_key="sexo",
        value_key="victimas",
    )
    delitos_labels, delitos_datasets = _build_grouped_series(
        evolucion_atlantico,
        label_key="a_o_hechos",
        group_key="grupo_delito",
        value_key="total_victimas",
        top_n=4,
    )

    chart_configs = {
        "chart-home": _build_chart_config(
            "doughnut",
            [_title_case(item.get("grupo_delito", "")) for item in top_delitos[:5]],
            "Atlantico",
            [item.get("porcentaje", 0) for item in top_delitos[:5]],
            doughnut=True,
        ),
        "chart-evolucion": _build_chart_config(
            "line",
            [str(item.get("ano", "")) for item in evolucion],
            "Victimas VBG",
            [item.get("victimas", 0) for item in evolucion],
        ),
        "chart-departamentos": _build_chart_config(
            "bar",
            [_title_case(item.get("departamento_hecho", "")) for item in geografia],
            "Victimas",
            [item.get("total_victimas", 0) for item in geografia],
            horizontal=True,
        ),
        "chart-edad": _build_chart_config(
            "bar",
            [_title_case(item.get("grupo_etario", "")) for item in grupos_etarios],
            "Victimas",
            [item.get("total_victimas", 0) for item in grupos_etarios],
        ),
        "chart-tipo": _build_chart_config(
            "doughnut",
            [_title_case(item.get("grupo_delito", "")) for item in top_delitos[:5]],
            "Atlantico",
            [item.get("total_victimas", 0) for item in top_delitos[:5]],
            doughnut=True,
        ),
        "chart-meses": _build_chart_config(
            "bar",
            [str(item.get("ano", "")) for item in feminicidio_anual],
            "Feminicidios",
            [item.get("feminicidios", 0) for item in feminicidio_anual],
        ),
        "chart-atlantico-share": _build_chart_config(
            "line",
            [str(item.get("ano", "")) for item in atlantico_vs_nacional],
            "Participacion de Atlantico (%)",
            [item.get("pct_atl", 0) for item in atlantico_vs_nacional],
        ),
        "chart-poblaciones": _build_chart_config(
            "doughnut",
            [_title_case(item.get("poblacion", "")) for item in poblaciones],
            "Participacion",
            [item.get("porcentaje", 0) for item in poblaciones],
            doughnut=True,
        ),
        "chart-comparativo-delitos": _build_multi_dataset_chart(
            "bar",
            [_title_case(item.get("grupo_delito", "")) for item in comparativo_delitos[:6]],
            [
                {
                    "label": "Peso nacional (%)",
                    "data": [item.get("pct_nacional", 0) for item in comparativo_delitos[:6]],
                    "color": CHART_COLORS["magenta"],
                },
                {
                    "label": "Peso Atlantico (%)",
                    "data": [item.get("pct_atlantico", 0) for item in comparativo_delitos[:6]],
                    "color": CHART_COLORS["orange"],
                },
            ],
            horizontal=True,
        ),
        "chart-top-delitos-etario": _build_chart_config(
            "bar",
            [
                f"{_title_case(item.get('grupo_etario', ''))}: {_title_case(item.get('grupo_delito', ''))}"
                for item in top_delitos_por_etario[:8]
            ],
            "Victimas",
            [item.get("total_victimas", 0) for item in top_delitos_por_etario[:8]],
            horizontal=True,
        ),
        "chart-feminicidio-sexo": _build_multi_dataset_chart(
            "bar",
            feminicidio_labels,
            feminicidio_datasets,
            stacked=True,
        ),
        "chart-tendencia-atlantico": _build_multi_dataset_chart(
            "line",
            delitos_labels,
            delitos_datasets,
        ),
    }

    chart_copy = deepcopy(chart_configs)
    chart_copy["chart-home"]["meta"] = {
        "title": "Composicion del foco regional en Atlantico",
        "description": "Distribucion de victimas por grupo delictivo dentro del foco regional cargado.",
    }
    chart_copy["chart-evolucion"]["meta"] = {
        "title": "Evolucion anual de victimas VBG",
        "description": "Serie nacional consolidada en el export del notebook.",
    }
    chart_copy["chart-departamentos"]["meta"] = {
        "title": "Top departamentos con mayor carga de victimas",
        "description": "Comparativo de concentracion territorial con los departamentos mas afectados.",
    }
    chart_copy["chart-edad"]["meta"] = {
        "title": "Distribucion por grupo etario",
        "description": "Victimas acumuladas por grupo de edad dentro del periodo analizado.",
    }
    chart_copy["chart-tipo"]["meta"] = {
        "title": "Tipos de delito predominantes en Atlantico",
        "description": "Participacion absoluta de los principales grupos delictivos en el foco regional.",
    }
    chart_copy["chart-meses"]["meta"] = {
        "title": "Evolucion anual de feminicidios",
        "description": "Serie anual incluida en el JSON cargado.",
    }
    chart_copy["chart-atlantico-share"]["meta"] = {
        "title": "Peso anual de Atlantico frente al total nacional",
        "description": "Porcentaje de victimas de Atlantico dentro del acumulado nacional por anio.",
    }
    chart_copy["chart-poblaciones"]["meta"] = {
        "title": "Poblaciones especiales con registro en VBG",
        "description": "Participacion porcentual de poblaciones priorizadas dentro del total observado.",
    }
    chart_copy["chart-comparativo-delitos"]["meta"] = {
        "title": "Comparativo Atlantico vs nacional por grupo delictivo",
        "description": "Contraste entre el peso porcentual de cada delito en Atlantico y en el total nacional.",
    }
    chart_copy["chart-top-delitos-etario"]["meta"] = {
        "title": "Cruce etario y delito con mayor volumen",
        "description": "Combinaciones de grupo etario y delito que concentran mas victimas.",
    }
    chart_copy["chart-feminicidio-sexo"]["meta"] = {
        "title": "Feminicidio anual por sexo",
        "description": "Desagregacion por sexo reportada en el export del notebook.",
    }
    chart_copy["chart-tendencia-atlantico"]["meta"] = {
        "title": "Evolucion de delitos clave en Atlantico",
        "description": "Series temporales por grupo delictivo para el foco regional.",
    }

    latest_year = evolucion[-1] if evolucion else {}
    top_department = geografia[0] if geografia else {}
    top_age = max(grupos_etarios, key=lambda item: item.get("total_victimas", 0), default={})
    top_delito = top_delitos[0] if top_delitos else {}
    top_population = max(poblaciones, key=lambda item: item.get("porcentaje", 0), default={})

    fallback_insights = [
        {
            "tipo": "resumen",
            "titulo": "Mayor concentracion territorial",
            "descripcion": (
                f"{_title_case(top_department.get('departamento_hecho', 'Sin dato'))} concentra "
                f"{_percent(top_department.get('porcentaje', 0))} del total registrado."
            ),
        },
        {
            "tipo": "resumen",
            "titulo": "Grupo etario mas afectado",
            "descripcion": (
                f"{_title_case(top_age.get('grupo_etario', 'Sin dato'))} registra "
                f"{_compact_number(top_age.get('total_victimas'))} victimas."
            ),
        },
        {
            "tipo": "resumen",
            "titulo": "Modalidad predominante en Atlantico",
            "descripcion": (
                f"{_title_case(top_delito.get('grupo_delito', 'Sin dato'))} acumula "
                f"{_percent(top_delito.get('porcentaje', 0))} de los casos del foco regional."
            ),
        },
    ]

    return {
        "nombre": resultado.nombre,
        "fuente": resultado.fuente,
        "actualizado": resultado.actualizado,
        "metadata": metadata,
        "stats": [
            {
                "number": _compact_number(kpis.get("total_casos_vbg")),
                "label": "Total de victimas VBG",
            },
            {
                "number": _compact_number(kpis.get("promedio_anual_vbg")),
                "label": "Promedio anual de victimas",
            },
            {
                "number": _compact_number(len(geografico.get("geografico_vbg") or [])),
                "label": "Territorios con registro",
            },
            {
                "number": f"{evolucion[0].get('ano', 'N/D')}-{latest_year.get('ano', 'N/D')}" if evolucion else "N/D",
                "label": "Rango temporal del analisis",
            },
        ],
        "highlights": insights[:3] if insights else fallback_insights,
        "charts": chart_copy,
        "sections": {
            "stats_subtitle": (
                "Estas cifras y visualizaciones se actualizan a partir del JSON mas reciente "
                "cargado en ResultadoAnalisis."
            ),
            "hero_subtitle": (
                "Leer las raices es mirar lo que sostiene la historia: este tablero se alimenta "
                "directamente del JSON analitico cargado en el backend."
            ),
            "source_summary": (
                f"Fuente base: {metadata.get('fuente', 'N/D')} | Fecha del corte: {metadata.get('fecha', 'N/D')} | "
                f"Principal concentracion territorial: {_title_case(top_department.get('departamento_hecho', 'N/D'))}."
            ),
        },
        "metadata_cards": [
            {"label": "Nombre del analisis", "value": metadata.get("nombre", resultado.nombre)},
            {"label": "Fecha del export", "value": metadata.get("fecha", "N/D")},
            {"label": "Fuente", "value": metadata.get("fuente", resultado.fuente)},
            {"label": "Poblacion prioritaria mas alta", "value": _title_case(top_population.get("poblacion", "N/D"))},
        ],
        "raw": datos,
        "available_sections": list(dashboard.keys()),
        "source_schema": "notebook_export",
        "chart_notes": {
            "chart-meses": "No hay serie mensual en el archivo; se usa la evolucion anual de feminicidios.",
            "chart-comparativo-delitos": "El comparativo usa peso porcentual dentro de cada universo, no volumen absoluto.",
            "chart-tendencia-atlantico": "Se muestran las primeras series delictivas disponibles en el export regional.",
        },
        "extra_series": {
            "comparativo_delitos_atl_vs_nacional": tendencias.get("comparativo_delitos_atl_vs_nacional") or [],
        },
    }


def _build_frontend_from_legacy(resultado, datos):
    contexto = datos.get("contexto") or {}
    dashboard = datos.get("dashboard_principal") or {}
    segmentado = datos.get("analisis_segmentado") or {}
    regional = datos.get("foco_regional") or {}
    evolucion = dashboard.get("evolucion_temporal") or []
    categorias = dashboard.get("distribucion_categorica") or []
    grupos_etarios = ((segmentado.get("grupos_etarios") or {}).get("distribucion")) or []
    top_delitos = regional.get("top_delitos") or []
    comparativas = regional.get("comparativas") or {}
    evolucion_vs_nacional = comparativas.get("evolucion_vs_nacional") or []
    perfil_vs_nacional = comparativas.get("perfil_delitos_vs_nacional") or []
    poblaciones = segmentado.get("poblaciones_especiales") or []
    feminicidio = dashboard.get("feminicidio") or {}
    feminicidio_sexo = feminicidio.get("serie_anual_por_sexo") or []
    fem_labels, fem_datasets = _build_grouped_series(
        feminicidio_sexo,
        label_key="ano",
        group_key="sexo",
        value_key="victimas",
    )

    return {
        "nombre": resultado.nombre,
        "fuente": resultado.fuente,
        "actualizado": resultado.actualizado,
        "metadata": contexto,
        "stats": [
            {
                "number": _compact_number((dashboard.get("kpis") or {}).get("total_victimas_vbg")),
                "label": "Total de victimas VBG",
            },
            {
                "number": _compact_number(len(categorias)),
                "label": "Categorias analizadas",
            },
            {
                "number": _compact_number(len(grupos_etarios)),
                "label": "Grupos etarios con datos",
            },
            {
                "number": f"{(contexto.get('periodo') or {}).get('inicio', 'N/D')}-{(contexto.get('periodo') or {}).get('fin', 'N/D')}",
                "label": "Rango temporal del analisis",
            },
        ],
        "highlights": [
            {
                "tipo": "resumen",
                "titulo": "Territorio foco",
                "descripcion": f"El analisis tiene foco regional en {_title_case(regional.get('territorio', 'N/D'))}.",
            },
            {
                "tipo": "resumen",
                "titulo": "Categoria principal",
                "descripcion": (
                    f"{_title_case(categorias[0].get('categoria', 'N/D'))} lidera la distribucion disponible."
                    if categorias
                    else "No hay categorias disponibles."
                ),
            },
            {
                "tipo": "resumen",
                "titulo": "Serie temporal disponible",
                "descripcion": f"Se cargaron {len(evolucion)} puntos en la evolucion temporal.",
            },
        ],
        "charts": {
            "chart-home": _build_chart_config(
                "doughnut",
                [_title_case(item.get("categoria", "")) for item in categorias[:5]],
                "Distribucion",
                [item.get("total_victimas", 0) for item in categorias[:5]],
                doughnut=True,
            ),
            "chart-evolucion": _build_chart_config(
                "line",
                [str(item.get("ano", "")) for item in evolucion],
                "Victimas VBG",
                [item.get("victimas", 0) for item in evolucion],
            ),
            "chart-departamentos": _build_chart_config(
                "bar",
                [_title_case(item.get("grupo_delito", "")) for item in top_delitos],
                "Victimas",
                [item.get("total_victimas", 0) for item in top_delitos],
                horizontal=True,
            ),
            "chart-edad": _build_chart_config(
                "bar",
                [_title_case(item.get("grupo_etario", "")) for item in grupos_etarios],
                "Victimas",
                [item.get("total_victimas", 0) for item in grupos_etarios],
            ),
            "chart-tipo": _build_chart_config(
                "doughnut",
                [_title_case(item.get("categoria", "")) for item in categorias[:5]],
                "Distribucion",
                [item.get("total_victimas", 0) for item in categorias[:5]],
                doughnut=True,
            ),
            "chart-meses": _build_chart_config(
                "bar",
                [str(item.get("ano", "")) for item in evolucion],
                "Victimas VBG",
                [item.get("victimas", 0) for item in evolucion],
            ),
            "chart-atlantico-share": _build_chart_config(
                "line",
                [str(item.get("ano", "")) for item in evolucion_vs_nacional],
                "Peso del territorio foco (%)",
                [item.get("pct_atl", 0) for item in evolucion_vs_nacional],
            ),
            "chart-poblaciones": _build_chart_config(
                "doughnut",
                [_title_case(item.get("poblacion", "")) for item in poblaciones],
                "Participacion",
                [item.get("porcentaje", 0) for item in poblaciones],
                doughnut=True,
            ),
            "chart-comparativo-delitos": _build_multi_dataset_chart(
                "bar",
                [_title_case(item.get("grupo_delito", "")) for item in perfil_vs_nacional],
                [
                    {
                        "label": "Peso nacional (%)",
                        "data": [item.get("pct_nacional", 0) for item in perfil_vs_nacional],
                        "color": CHART_COLORS["magenta"],
                    },
                    {
                        "label": "Peso territorio foco (%)",
                        "data": [item.get("pct_atlantico", 0) for item in perfil_vs_nacional],
                        "color": CHART_COLORS["orange"],
                    },
                ],
                horizontal=True,
            ),
            "chart-top-delitos-etario": _build_chart_config(
                "bar",
                [_title_case(item.get("grupo_etario", "")) for item in grupos_etarios],
                "Victimas",
                [item.get("total_victimas", 0) for item in grupos_etarios],
                horizontal=True,
            ),
            "chart-feminicidio-sexo": _build_multi_dataset_chart(
                "bar",
                fem_labels,
                fem_datasets,
                stacked=True,
            ),
            "chart-tendencia-atlantico": _build_chart_config(
                "line",
                [str(item.get("ano", "")) for item in evolucion_vs_nacional],
                "Victimas territorio foco",
                [item.get("victimas_atl", 0) for item in evolucion_vs_nacional],
            ),
        },
        "sections": {
            "stats_subtitle": "Resumen del export legacy cargado en ResultadoAnalisis.",
            "hero_subtitle": "Esta pagina esta conectada al analisis cargado en backend y adapta la visualizacion segun el esquema disponible.",
            "source_summary": f"Fuente base: {contexto.get('fuente', resultado.fuente)} | Territorio foco: {_title_case(regional.get('territorio', 'N/D'))}.",
        },
        "metadata_cards": [
            {"label": "Fuente", "value": contexto.get("fuente", resultado.fuente)},
            {"label": "Dataset", "value": contexto.get("dataset", "N/D")},
            {"label": "Cobertura", "value": (contexto.get("cobertura") or {}).get("alcance", "N/D")},
            {"label": "Territorio foco", "value": _title_case(regional.get("territorio", "N/D"))},
        ],
        "raw": datos,
        "source_schema": "legacy_dashboard",
        "chart_notes": {
            "chart-meses": "La serie replica la evolucion temporal general disponible en el esquema legacy.",
        },
    }

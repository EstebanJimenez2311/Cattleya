import unicodedata


VIOLENCE_SIGNAL_GROUPS = {
    "violencia_fisica": [
        "golpe",
        "golpes",
        "agresion",
        "agresiones",
        "agresion fisica",
        "lesion",
        "lesiones",
        "maltrato fisico",
        "arma blanca",
        "violencia intrafamiliar",
    ],
    "violencia_psicologica": [
        "violencia psicologica",
        "amenaza",
        "amenazas",
        "hostigamiento",
        "intimidacion",
        "humillacion",
        "manipulacion",
        "acoso",
        "acoso laboral",
        "acoso judicial",
        "acoso en medios",
    ],
    "violencia_sexual": [
        "violencia sexual",
        "abuso sexual",
        "violacion",
        "acoso sexual",
        "tocamientos",
        "explotacion sexual",
    ],
    "violencia_economica": [
        "violencia economica",
        "violencia patrimonial",
        "economica",
        "patrimonial",
        "control economico",
        "dependencia economica",
        "retencion de documentos",
        "dano patrimonial",
    ],
    "feminicidio": [
        "feminicidio",
        "intento de feminicidio",
        "triple feminicidio",
        "asesinada",
        "hallada sin vida",
        "crimen de genero",
    ],
}

WOMEN_CONTEXT_TERMS = [
    "mujer",
    "mujeres",
    "nina",
    "ninas",
    "adolescente",
    "joven",
    "victima",
    "victimas",
    "madre",
    "hija",
    "hijas",
    "esposa",
    "novia",
    "pareja",
    "expareja",
    "genero",
    "violencia contra la mujer",
    "violencias basadas en genero",
]

AMBITO_TERMS = {
    "pareja": ["pareja", "expareja", "esposo", "esposa", "novio", "novia"],
    "familiar": ["familia", "familiar", "hogar", "madre", "hija", "hijas", "padre", "hermano", "hermana"],
    "comunitario": ["transporte publico", "bus", "calle", "via publica", "barrio"],
    "institucional": ["empresa", "laboral", "trabajo", "institucion", "ministerio", "universidad", "medios"],
}

EXCLUDED_CONTEXT_TERMS = [
    "guerra",
    "oriente medio",
    "iran",
    "israel",
    "otan",
    "pentagono",
    "mercenarios",
    "fuerza publica",
    "eln",
    "disidencias",
    "farc",
    "accidente aereo",
    "atraco",
    "robo",
    "sicari",
    "deporte",
    "futbol",
    "mundial",
    "seleccion colombia",
    "croacia",
    "francia",
    "dolar",
    "petroleo",
]

PRIMARY_KEYWORDS = sorted(
    {
        keyword
        for keywords in VIOLENCE_SIGNAL_GROUPS.values()
        for keyword in keywords
    }
)


def normalize_text(text):
    normalized = unicodedata.normalize("NFD", str(text or "").lower())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def _contains_any(text, keywords):
    normalized = normalize_text(text)
    return any(keyword in normalized for keyword in keywords)


def detect_violence_signals(text):
    normalized = normalize_text(text)
    return {
        group: any(keyword in normalized for keyword in keywords)
        for group, keywords in VIOLENCE_SIGNAL_GROUPS.items()
    }


def detect_ambito_signals(text):
    normalized = normalize_text(text)
    return {
        ambito: any(keyword in normalized for keyword in keywords)
        for ambito, keywords in AMBITO_TERMS.items()
    }


def has_women_context(text):
    return _contains_any(text, WOMEN_CONTEXT_TERMS)


def has_excluded_context(text):
    return _contains_any(text, EXCLUDED_CONTEXT_TERMS)


def contains_keywords(text):
    normalized = normalize_text(text)
    signals = detect_violence_signals(normalized)
    women_context = has_women_context(normalized)
    ambito_signals = detect_ambito_signals(normalized)

    if has_excluded_context(normalized) and not women_context:
        return False

    if signals["feminicidio"]:
        return True

    if signals["violencia_sexual"] and women_context:
        return True

    if signals["violencia_psicologica"] and women_context:
        return True

    if signals["violencia_economica"] and women_context:
        return True

    if signals["violencia_fisica"] and women_context and any(ambito_signals.values()):
        return True

    if women_context and any(ambito_signals.values()) and (
        "violencia" in normalized or "maltrato" in normalized or "acoso" in normalized
    ):
        return True

    return False


def is_gender_violence_related(title, description=""):
    title_text = normalize_text(title)
    description_text = normalize_text(description)
    combined_text = f"{title_text} {description_text}".strip()

    if has_excluded_context(combined_text) and not has_women_context(combined_text):
        return False

    title_signals = detect_violence_signals(title_text)
    combined_signals = detect_violence_signals(combined_text)
    women_context = has_women_context(combined_text)
    ambito_signals = detect_ambito_signals(combined_text)

    if title_signals["feminicidio"] or combined_signals["feminicidio"]:
        return True

    if combined_signals["violencia_sexual"] and women_context:
        return True

    if combined_signals["violencia_psicologica"] and women_context:
        return True

    if combined_signals["violencia_economica"] and women_context:
        return True

    if combined_signals["violencia_fisica"] and women_context and any(ambito_signals.values()):
        return True

    if women_context and any(ambito_signals.values()) and (
        "violencia" in combined_text or "maltrato" in combined_text or "acoso" in combined_text
    ):
        return True

    return False

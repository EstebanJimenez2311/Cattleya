import re
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit, urlunsplit

from django.utils import timezone

from .filters import normalize_text


CITY_NAMES = [
    "bogota",
    "medellin",
    "cali",
    "barranquilla",
    "cartagena",
    "bucaramanga",
]

CITY_LABELS = {
    "bogota": "Bogota",
    "medellin": "Medellin",
    "cali": "Cali",
    "barranquilla": "Barranquilla",
    "cartagena": "Cartagena",
    "bucaramanga": "Bucaramanga",
}


def clean_text(text):
    cleaned = re.sub(r"<[^>]+>", " ", str(text or ""))
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def parse_publication_date(raw_date):
    if not raw_date:
        return timezone.now()

    if hasattr(raw_date, "tm_year"):
        return timezone.make_aware(timezone.datetime(*raw_date[:6]), timezone.get_current_timezone())

    try:
        parsed = parsedate_to_datetime(str(raw_date))
        if parsed is None:
            raise ValueError("parsedate_to_datetime devolvio None")
        if timezone.is_naive(parsed):
            return timezone.make_aware(parsed, timezone.get_current_timezone())
        return parsed
    except Exception:
        return timezone.now()


def extract_city(text):
    normalized = normalize_text(text)

    for city in CITY_NAMES:
        if city in normalized:
            return CITY_LABELS[city]

    for city in CITY_NAMES:
        pattern = rf"\b(?:en|de)\s+{re.escape(city)}\b"
        if re.search(pattern, normalized):
            return CITY_LABELS[city]

    return "No especificada"


def normalize_url(url, max_length=1000):
    raw_url = clean_text(url)
    if not raw_url:
        return ""

    try:
        parsed = urlsplit(raw_url)
        normalized = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    except Exception:
        normalized = raw_url

    if len(normalized) <= max_length:
        return normalized

    return normalized[:max_length]

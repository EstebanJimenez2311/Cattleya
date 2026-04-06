from dataclasses import dataclass
import sys

from noticias.models import Noticia

from .article_scraper import ArticleScraper
from .cleaner import clean_text, extract_city, normalize_url, parse_publication_date
from .filters import is_gender_violence_related
from .parsers import caracol, el_espectador, el_tiempo
from .rss_reader import read_feed


MAX_RELEVANT_PER_SOURCE = 10


@dataclass(frozen=True)
class SourceConfig:
    key: str
    name: str
    feed_url: str
    feed_mode: str
    base_url: str
    parser: object


SOURCES = [
    SourceConfig(
        key="el_tiempo",
        name="El Tiempo",
        feed_url="https://www.eltiempo.com/sitemap-articles-current.xml",
        feed_mode="sitemap",
        base_url="https://www.eltiempo.com",
        parser=el_tiempo,
    ),
    SourceConfig(
        key="el_espectador",
        name="El Espectador",
        feed_url="https://www.elespectador.com/arc/outboundfeeds/news-sitemap/?outputType=xml",
        feed_mode="sitemap",
        base_url="https://www.elespectador.com",
        parser=el_espectador,
    ),
    SourceConfig(
        key="caracol",
        name="Caracol Radio",
        feed_url="https://caracol.com.co/arc/outboundfeeds/news-sitemap/latest/?outputType=xml",
        feed_mode="sitemap",
        base_url="https://caracol.com.co",
        parser=caracol,
    ),
]


class RSSImporter:
    def __init__(self):
        self.scraper = ArticleScraper()
        self.summary = {
            "saved": 0,
            "duplicates": 0,
            "filtered": 0,
            "errors": 0,
            "relevant_processed": 0,
        }

    def _log(self, message):
        try:
            print(message)
        except UnicodeEncodeError:
            safe_message = message.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(
                sys.stdout.encoding or "utf-8",
                errors="replace",
            )
            print(safe_message)

    def _is_relevant(self, title, description):
        return is_gender_violence_related(title, description)

    def _build_description(self, source_config, html, fallback_description):
        extracted_summary = source_config.parser.extract_summary(html)
        description = clean_text(extracted_summary or fallback_description)
        return description

    def _process_entry(self, source_config, entry):
        title = clean_text(getattr(entry, "title", ""))
        description_hint = clean_text(getattr(entry, "summary", "") or getattr(entry, "description", ""))
        raw_url = clean_text(getattr(entry, "link", ""))
        url = normalize_url(raw_url)

        if not title or not raw_url:
            self.summary["filtered"] += 1
            self._log(f"[FILTER] Descartada: {title or 'sin titulo'}")
            return "filtered"

        if not self._is_relevant(title, description_hint):
            self.summary["filtered"] += 1
            self._log(f"[FILTER] Descartada: {title}")
            return "filtered"

        self.summary["relevant_processed"] += 1
        self._log(f"[FILTER] Relevante: {title}")

        if Noticia.objects.filter(url=url).exists():
            self.summary["duplicates"] += 1
            self._log(f"[DUPLICADO] Ya existe: {url}")
            return "duplicate"

        try:
            self._log("[SCRAPER] Extrayendo articulo...")
            html, final_url = self.scraper.fetch_html(raw_url)
            url = normalize_url(final_url or raw_url)
            description = self._build_description(source_config, html, description_hint)
        except Exception as error:
            self.summary["errors"] += 1
            self._log(f"[ERROR] fallo en scraping: {error}")
            return "error"

        if not is_gender_violence_related(title, description):
            self.summary["filtered"] += 1
            self._log(f"[FILTER] Descartada: {title}")
            return "filtered"

        if len(description) < 100:
            self.summary["filtered"] += 1
            self._log(f"[FILTER] Descartada: {title}")
            return "filtered"

        publication_date = parse_publication_date(
            getattr(entry, "published", "")
            or getattr(entry, "updated", "")
            or getattr(entry, "pubDate", "")
        )
        city = extract_city(f"{title} {description}")

        try:
            Noticia.objects.create(
                titulo=title[:200],
                descripcion=description,
                contenido=None,
                fecha_publicacion=publication_date,
                fuente=source_config.name,
                url=url,
                ciudad=city,
                es_prueba=False,
            )
            self.summary["saved"] += 1
            self._log(f"[SUCCESS] Guardado: {title}")
            return "saved"
        except Exception as error:
            self.summary["errors"] += 1
            self._log(f"[ERROR] fallo en scraping: {error}")
            return "error"

    def import_source(self, source_config):
        self._log(f"[INFO] Leyendo fuente {source_config.name}...")

        try:
            entries = read_feed(source_config)
        except Exception as error:
            self.summary["errors"] += 1
            self._log(f"[ERROR] fallo en scraping: {error}")
            return

        relevant_count = 0
        for entry in entries:
            if relevant_count >= MAX_RELEVANT_PER_SOURCE:
                self._log(f"[LIMIT] Limite alcanzado ({MAX_RELEVANT_PER_SOURCE})")
                break

            result = self._process_entry(source_config, entry)
            if result != "filtered":
                relevant_count += 1

    def import_all(self):
        for source in SOURCES:
            self.import_source(source)
        return self.summary


def run():
    importer = RSSImporter()
    return importer.import_all()

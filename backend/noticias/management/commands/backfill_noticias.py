from collections import OrderedDict
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from noticias.services.rss_importer import SOURCES, RSSImporter
from noticias.services.rss_reader import read_sitemap_index_url, read_sitemap_url


EL_ESPECTADOR_SECTION_INDEXES = [
    "https://www.elespectador.com/arc/outboundfeeds/sitemap-index/section/genero-y-diversidad/?outputType=xml",
    "https://www.elespectador.com/arc/outboundfeeds/sitemap-index/section/judicial/?outputType=xml",
    "https://www.elespectador.com/arc/outboundfeeds/sitemap-index/section/bogota/?outputType=xml",
    "https://www.elespectador.com/arc/outboundfeeds/sitemap-index/section/actualidad/?outputType=xml",
]


def month_range(start_year):
    today = date.today()
    year = start_year
    month = 1
    while (year, month) <= (today.year, today.month):
        yield year, month
        month += 1
        if month > 12:
            month = 1
            year += 1


def day_range(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


class Command(BaseCommand):
    help = "Ejecuta un backfill historico de noticias desde un anio dado usando sitemaps/archivos."

    def add_arguments(self, parser):
        parser.add_argument("--since-year", type=int, default=2020)
        parser.add_argument(
            "--sources",
            nargs="+",
            choices=["el_tiempo", "el_espectador", "caracol"],
            default=["el_tiempo", "el_espectador", "caracol"],
        )

    def handle(self, *args, **options):
        since_year = options["since_year"]
        selected_sources = set(options["sources"])
        importer = RSSImporter()
        source_map = {source.key: source for source in SOURCES}

        if "el_tiempo" in selected_sources:
            entries = []
            for year, month in month_range(since_year):
                sitemap_url = f"https://www.eltiempo.com/sitemap-articles-{year:04d}-{month:02d}.xml"
                self.stdout.write(f"[EL TIEMPO] Leyendo {sitemap_url}")
                entries.extend(self._safe_read_sitemap(sitemap_url))
            importer.import_entries(source_map["el_tiempo"], entries)

        if "el_espectador" in selected_sources:
            child_sitemaps = []
            for index_url in EL_ESPECTADOR_SECTION_INDEXES:
                self.stdout.write(f"[EL ESPECTADOR] Leyendo indice {index_url}")
                child_sitemaps.extend(self._safe_read_sitemap_index(index_url))

            unique_child_sitemaps = list(OrderedDict.fromkeys(child_sitemaps))
            entries = []
            for sitemap_url in unique_child_sitemaps:
                self.stdout.write(f"[EL ESPECTADOR] Leyendo {sitemap_url}")
                entries.extend(self._safe_read_sitemap(sitemap_url))
            importer.import_entries(source_map["el_espectador"], entries)

        if "caracol" in selected_sources:
            entries = []
            start_date = date(since_year, 1, 1)
            end_date = date.today()
            for current_date in day_range(start_date, end_date):
                sitemap_url = (
                    f"https://caracol.com.co/arc/outboundfeeds/sitemap/"
                    f"{current_date.isoformat()}/?outputType=xml"
                )
                self.stdout.write(f"[CARACOL] Leyendo {sitemap_url}")
                entries.extend(self._safe_read_sitemap(sitemap_url))
            importer.import_entries(source_map["caracol"], entries)

        summary = importer.summary
        self.stdout.write("")
        self.stdout.write("Resumen de backfill:")
        self.stdout.write(f"Guardadas: {summary['saved']}")
        self.stdout.write(f"Duplicadas: {summary['duplicates']}")
        self.stdout.write(f"Filtradas: {summary['filtered']}")
        self.stdout.write(f"Errores: {summary['errors']}")
        self.stdout.write(f"Relevantes procesadas: {summary['relevant_processed']}")

    def _safe_read_sitemap(self, sitemap_url):
        try:
            return read_sitemap_url(sitemap_url)
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"[WARN] No se pudo leer {sitemap_url}: {exc}"))
            return []

    def _safe_read_sitemap_index(self, sitemap_url):
        try:
            return read_sitemap_index_url(sitemap_url)
        except Exception as exc:
            self.stdout.write(self.style.WARNING(f"[WARN] No se pudo leer indice {sitemap_url}: {exc}"))
            return []

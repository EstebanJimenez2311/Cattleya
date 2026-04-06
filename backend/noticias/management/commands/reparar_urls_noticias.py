from django.core.management.base import BaseCommand

from noticias.models import Noticia
from noticias.services.filters import normalize_text
from noticias.services.rss_importer import SOURCES
from noticias.services.rss_reader import read_feed


class Command(BaseCommand):
    help = "Repara URLs truncadas en noticias usando coincidencia exacta por titulo dentro de las fuentes configuradas."

    def handle(self, *args, **options):
        source_map = {source.name: source for source in SOURCES}
        feed_cache = {}
        repaired = 0
        unresolved = 0

        suspects = [noticia for noticia in Noticia.objects.all() if len(noticia.url or "") == 200]

        for noticia in suspects:
            source = source_map.get(noticia.fuente)
            if not source:
                unresolved += 1
                self.stdout.write(self.style.WARNING(f"Sin fuente compatible para: {noticia.id}"))
                continue

            if source.name not in feed_cache:
                feed_cache[source.name] = read_feed(source)

            expected_title = normalize_text(noticia.titulo)
            matched_link = None

            for entry in feed_cache[source.name]:
                entry_title = normalize_text(getattr(entry, "title", ""))
                if entry_title == expected_title:
                    matched_link = getattr(entry, "link", "")
                    break

            if matched_link and matched_link != noticia.url:
                Noticia.objects.filter(id=noticia.id).update(url=matched_link)
                repaired += 1
                self.stdout.write(self.style.SUCCESS(f"Reparada noticia {noticia.id}: {matched_link}"))
            else:
                unresolved += 1
                self.stdout.write(self.style.WARNING(f"No se encontro match para noticia {noticia.id}"))

        self.stdout.write("")
        self.stdout.write(f"URLs reparadas: {repaired}")
        self.stdout.write(f"Sin resolver: {unresolved}")

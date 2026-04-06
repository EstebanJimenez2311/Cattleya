import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import Q

from noticias.models import Noticia


class Command(BaseCommand):
    help = "Marca como noticias de prueba los registros cargados desde fixtures y deja las demas como reales."

    def handle(self, *args, **options):
        fixtures_dir = Path(__file__).resolve().parents[2] / "fixtures"
        fixture_urls = set()

        for fixture_path in sorted(fixtures_dir.glob("noticias_seed*.json")):
            with fixture_path.open(encoding="utf-8") as fixture_file:
                payload = json.load(fixture_file)
            for item in payload:
                data = item.get("fields", item)
                fixture_urls.add(data["url"])

        Noticia.objects.update(es_prueba=False)
        marked = Noticia.objects.filter(
            Q(url__in=fixture_urls) | Q(url__startswith="https://test-cattleya.local/") | Q(fuente="CargaManual")
        ).update(es_prueba=True)
        real = Noticia.objects.filter(es_prueba=False).count()

        self.stdout.write(f"Noticias marcadas como prueba: {marked}")
        self.stdout.write(f"Noticias reales: {real}")

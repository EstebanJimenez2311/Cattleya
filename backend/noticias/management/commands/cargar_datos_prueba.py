import json
from pathlib import Path

from django.core.management.base import BaseCommand

from noticias.models import Noticia


class Command(BaseCommand):
    help = "Carga noticias de prueba usando el ORM para ejecutar la clasificacion automatica."

    def handle(self, *args, **options):
        creadas = 0
        actualizadas = 0
        fixtures_dir = Path(__file__).resolve().parents[2] / "fixtures"

        for fixture_path in sorted(fixtures_dir.glob("noticias_seed*.json")):
            with fixture_path.open(encoding="utf-8") as fixture_file:
                payload = json.load(fixture_file)

            for item in payload:
                data = item.get("fields", item)
                noticia, created = Noticia.objects.update_or_create(
                    url=data["url"],
                    defaults={
                        "titulo": data["titulo"],
                        "descripcion": data["descripcion"],
                        "contenido": data.get("contenido"),
                        "fecha_publicacion": data["fecha_publicacion"],
                        "fuente": data["fuente"],
                        "ciudad": data["ciudad"],
                        "verificada": data.get("verificada", False),
                        "es_prueba": True,
                    },
                )
                if created:
                    creadas += 1
                else:
                    actualizadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Noticias procesadas: {creadas + actualizadas} (creadas={creadas}, actualizadas={actualizadas})"
            )
        )

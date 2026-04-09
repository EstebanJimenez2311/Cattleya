from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from analisis.services import decode_uploaded_bytes, import_analysis_payload, parse_analysis_json


class Command(BaseCommand):
    help = "Carga un archivo JSON de análisis y crea/actualiza ResultadoAnalisis."

    def add_arguments(self, parser):
        parser.add_argument("ruta", nargs="?", help="Ruta al archivo JSON exportado.")
        parser.add_argument("--nombre", dest="nombre", help="Nombre a usar para el análisis.")
        parser.add_argument("--descripcion", dest="descripcion", help="Descripción opcional.")

    def handle(self, *args, **options):
        ruta = options.get("ruta")
        if not ruta:
            raise CommandError("Debes indicar la ruta del archivo JSON. Ejemplo: python manage.py cargar_analisis data.json")

        path = Path(ruta)
        if not path.exists():
            raise CommandError(f"No se encontró el archivo: {path}")

        raw_text = decode_uploaded_bytes(path.read_bytes())
        payload = parse_analysis_json(raw_text)
        resultado, created = import_analysis_payload(
            payload,
            nombre=options.get("nombre"),
            descripcion=options.get("descripcion"),
        )
        verbo = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f"Análisis {verbo}: {resultado.nombre}"))

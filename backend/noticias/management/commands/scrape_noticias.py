from django.core.management.base import BaseCommand

from noticias.services.rss_importer import run


class Command(BaseCommand):
    help = "Ejecuta el pipeline RSS + scraping para noticias relevantes sobre violencia contra la mujer"

    def handle(self, *args, **options):
        summary = run()
        self.stdout.write("")
        self.stdout.write("Resumen de ejecucion:")
        self.stdout.write(f"Guardadas: {summary['saved']}")
        self.stdout.write(f"Duplicadas: {summary['duplicates']}")
        self.stdout.write(f"Filtradas: {summary['filtered']}")
        self.stdout.write(f"Errores: {summary['errors']}")
        self.stdout.write(f"Relevantes procesadas: {summary['relevant_processed']}")

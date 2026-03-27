from django.core.management.base import BaseCommand
from noticias.services.rss_importer import RSSImporter

class Command(BaseCommand):
    help = 'Importa noticias desde fuentes RSS colombianas relacionadas con violencia contra la mujer'

    def handle(self, *args, **options):
        importer = RSSImporter()
        importer.import_all()
import feedparser
from datetime import datetime
from ..models import Noticia

class RSSImporter:
    # Fuentes RSS colombianas
    RSS_SOURCES = [
        {
            'url': 'https://www.eltiempo.com/rss/colombia.xml',
            'fuente': 'El Tiempo'
        },
        {
            'url': 'https://www.elespectador.com/rss/colombia.xml',
            'fuente': 'El Espectador'
        },
        {
            'url': 'https://www.elheraldo.co/rss/colombia',
            'fuente': 'El Heraldo'
        }
    ]

    # Keywords para filtrar noticias relacionadas con violencia contra la mujer
    VIOLENCE_KEYWORDS = [
        'violencia', 'feminicidio', 'abuso', 'mujer', 'género', 'feminista',
        'machismo', 'acoso', 'agresión', 'asesinato', 'muerte', 'violación',
        'intrafamiliar', 'doméstica', 'física', 'psicológica', 'sexual'
    ]

    def __init__(self):
        self.imported_count = 0
        self.filtered_count = 0
        self.duplicate_count = 0

    def is_violence_related(self, title, description):
        """Verifica si la noticia está relacionada con violencia contra la mujer"""
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in self.VIOLENCE_KEYWORDS)

    def is_duplicate(self, url, titulo):
        """Verifica si la noticia ya existe por URL o título"""
        return Noticia.objects.filter(url=url).exists() or \
               Noticia.objects.filter(titulo=titulo).exists()

    def parse_date(self, published):
        """Convierte fecha del RSS a datetime"""
        try:
            # Intentar diferentes formatos de fecha
            for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S']:
                try:
                    return datetime.strptime(published, fmt)
                except ValueError:
                    continue
            # Si no coincide ningún formato, usar fecha actual
            return datetime.now()
        except:
            return datetime.now()

    def import_from_source(self, source):
        """Importa noticias de una fuente RSS específica"""
        try:
            feed = feedparser.parse(source['url'])
            fuente = source['fuente']

            print(f"  Feed {fuente}: {len(feed.entries)} entradas encontradas")

            for entry in feed.entries[:10]:  # Limitar a 10 por fuente
                titulo = entry.title if hasattr(entry, 'title') else ''
                descripcion = entry.description if hasattr(entry, 'description') else ''
                url = entry.link if hasattr(entry, 'link') else ''
                published = entry.published if hasattr(entry, 'published') else ''

                print(f"    Procesando: {titulo[:30]}...")

                # Filtrar por contenido relacionado con violencia
                if not self.is_violence_related(titulo, descripcion):
                    print(f"      Filtrada (no violencia): {titulo[:30]}...")
                    self.filtered_count += 1
                    continue

                # Verificar duplicados
                if self.is_duplicate(url, titulo):
                    print(f"      Duplicada: {titulo[:30]}...")
                    self.duplicate_count += 1
                    continue

                # Parsear fecha
                fecha_publicacion = self.parse_date(published)

                # Crear noticia
                Noticia.objects.create(
                    titulo=titulo,
                    descripcion=descripcion,
                    contenido='',  # No disponible en RSS básico
                    fecha_publicacion=fecha_publicacion,
                    fuente=fuente,
                    url=url,
                    ciudad='Colombia'  # Default para Colombia
                )

                self.imported_count += 1
                print(f"      Importada: {titulo[:30]}...")

        except Exception as e:
            print(f"Error importando de {fuente}: {str(e)}")

    def import_all(self):
        """Importa de todas las fuentes RSS"""
        print("Iniciando importación de noticias RSS...")
        print(f"Fuentes: {len(self.RSS_SOURCES)}")

        for source in self.RSS_SOURCES:
            print(f"Procesando {source['fuente']}...")
            self.import_from_source(source)

        print("Resumen de importación:")
        print(f"Importadas: {self.imported_count}")
        print(f"Filtradas: {self.filtered_count}")
        print(f"Duplicadas: {self.duplicate_count}")
        print("Importación completada!")
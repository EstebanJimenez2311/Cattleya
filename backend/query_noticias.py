import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from noticias.models import Noticia

print('total', Noticia.objects.count())
print('recientes', Noticia.objects.order_by('-fecha_publicacion')[:20].count())
print('verificada', Noticia.objects.filter(verificada=True).count())
# if field es_publicado does not exist in this model, skip; use verificada
print('todos', Noticia.objects.all().count())

print('primeras 5 recientes:')
for n in Noticia.objects.order_by('-fecha_publicacion')[:5]:
    print(n.id, n.fecha_publicacion, n.titulo, n.tipo_violencia, n.nivel_riesgo, n.verificada)

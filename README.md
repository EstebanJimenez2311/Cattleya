# CATTLEYA

CATTLEYA es una plataforma técnica para ingestión, clasificación y visualización de noticias sobre violencia de género y casos sensibles en Colombia. El proyecto combina un backend Django + Django REST Framework con un frontend estático en HTML, CSS y JavaScript sin frameworks.

## Problema que resuelve

El sistema automatiza el ciclo de ingestión de noticias desde fuentes RSS y sitemap: detecta contenido relevante, clasifica tipos de violencia, guarda registros verificados y ofrece datos procesados para consumo en un frontend y en un panel de administración.

## Tecnologías usadas

- Python 3.x
- Django 6.0.3
- Django REST Framework 3.17.1
- SQLite / PostgreSQL (configurable)
- JavaScript vanilla
- HTML + CSS puro
- Requests, feedparser, BeautifulSoup
- Netlify Functions (solo documentación histórica)

## Arquitectura general

- `backend/`: código Django, servicios de ingestión, API REST, admin personalizado.
- `cattleya-sitio/`: frontend estático, componentes Web Components y scripts de consumo de API.
- `backend/noticias/`: núcleo de noticias, modelo `Noticia`, clasificación automática y servicios de scraping.
- `backend/analisis/`: resultados de análisis exportados a JSON y guardados en `ResultadoAnalisis`.
- `backend/estadisticas/`: endpoints dinámicos de métricas calculadas.

## Cómo correr el proyecto

1. Instalar dependencias:

```bash
cd backend
pip install -r requirements.txt
```

2. Migrar la base de datos:

```bash
python manage.py migrate
```

3. Crear superusuario opcional:

```bash
python manage.py createsuperuser
```

4. Iniciar el servidor Django:

```bash
python manage.py runserver
```

5. Abrir el frontend estático en un servidor simple o con Live Server. El frontend espera la API en `http://127.0.0.1:8000`.

## Estructura de carpetas simplificada

- `backend/`
  - `config/`: configuración de Django, admin personalizado, rutas.
  - `noticias/`: modelo de noticias, API, servicios de scraping.
  - `analisis/`: modelo `ResultadoAnalisis`, endpoints de análisis.
  - `estadisticas/`: lógica de métricas y endpoints.
- `cattleya-sitio/`
  - `js/`: scripts de página.
  - `css/`: estilos.
  - `assets/components/`: Web Components reutilizables.
  - `netlify/functions/`: funciones obsoletas de proxy de noticias.

## Nota técnica

La arquitectura actual está diseñada para separar claramente la ingestión de noticias, la clasificación automática y la entrega de datos a una UI ligera. El frontend no usa React ni frameworks pesados; en su lugar consume una API REST construida con Django.

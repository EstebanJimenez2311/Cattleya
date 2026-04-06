# BACKEND

## Visión general

El backend de CATTLEYA está implementado con Django y Django REST Framework. Su propósito es ingestar noticias, clasificar contenido relevante, almacenar registros normalizados y exponer APIs para consumo por el frontend y otros sistemas.

## Apps principales

### `noticias/`

#### Modelo `Noticia`

`Noticia` es el modelo central del dominio de noticias. Sus campos principales son:

- `titulo`, `descripcion`, `contenido`
- `fecha_publicacion`
- `fuente`, `url`, `ciudad`
- banderas booleanas de tipos de violencia: `violencia_fisica`, `violencia_psicologica`, `violencia_sexual`, `violencia_economica`, `violencia_patrimonial`, `feminicidio`
- `ambito_violencia`, `nivel_riesgo`
- `verificada`, `es_prueba`

El método `save()` aplica clasificación automática antes de persistir:

- `clasificar_violencia()` detecta palabras clave en el título y descripción.
- `inferir_ambito()` determina el ámbito del caso (`pareja`, `familiar`, `institucional`, `comunitario`, `otro`).
- `calcular_riesgo()` asigna un nivel: `bajo`, `medio`, `alto`, `critico`.

#### Servicios

El backend define una capa de servicios en `backend/noticias/services/` para separar lógica de ingestión, limpieza y filtrado:

- `rss_reader.py`: lee feeds RSS, HTML o sitemap.
- `article_scraper.py`: extrae contenido de artículos y maneja HTML.
- `cleaner.py`: normaliza texto, limpia HTML, parsing de fechas y URLs.
- `filters.py`: lógica de detección de violencia de género y exclusión de contexto no relevante.
- `rss_importer.py`: orquesta la lectura de fuentes, filtra noticias irrelevantes, evita duplicados y guarda `Noticia`.

#### Parsers

El directorio `backend/noticias/services/parsers/` contiene adaptadores específicos para fuentes como `caracol`, `el_espectador`, `el_tiempo`. Estos parsers abstraen diferencias de estructura entre los diferentes sitemaps y feeds.

### `analisis/`

#### Modelo `ResultadoAnalisis`

El backend tiene un modelo de análisis:

- `nombre`
- `fuente`
- `descripcion`
- `datos` (`JSONField`)
- `actualizado`

Este modelo almacena resultados de análisis estructurados en JSON, lo que permite consultar conjuntos de datos que provienen de procesamiento externo o notebooks.

#### Uso esperado

La app se usa para exponer resultados analíticos en la API y en el admin. El campo `datos` es un `JSONField` flexible, utilizable para métricas agregadas, series temporales o reportes generados fuera del runtime de Django.

### `estadisticas/`

#### Lógica dinámica

`estadisticas` no persiste resúmenes en un modelo propio. En su lugar, las vistas calculan métricas a partir de `Noticia`:

- conteo por tipo de violencia
- conteo por ámbito
- total de noticias y total verificadas
- tendencias mensuales
- porcentaje de tipos de violencia

#### Nota técnica

El archivo `backend/estadisticas/serializers.py` contiene definiciones duplicadas de clases que conviene limpiar. Esto no es parte del diseño funcional, sino una inconsistencia de implementación.

## API REST

El backend expone tres áreas principales:

- `api/noticias/`
- `api/analisis/`
- `api/estadisticas/`

Estas APIs son construidas con DRF y permiten tanto listados CRUD como endpoints dedicados de resumen.

## Admin personalizado

La app `config` extiende el admin de Django con un dashboard propio y una ruta adicional `/admin/monitor/`. El admin se configura desde `backend/config/admin.py`.

## Configuración y dependencias

Dependencias clave en `backend/requirements.txt`:

- Django 6.0.3
- djangorestframework 3.17.1
- requests
- feedparser
- beautifulsoup4
- django-cors-headers
- psycopg2-binary

## Nota de integración

El frontend no depende de Netlify Functions para el consumo de noticias. La función `cattleya-sitio/netlify/functions/noticias-proxy.js` se mantiene como referencia histórica, pero el flujo real actual usa directamente el backend Django.

# DATA_PIPELINE

## Flujo completo de datos

La arquitectura actual sigue este flujo:

1. `backend/noticias/services/rss_importer.py` lee fuentes de noticias.
2. `rss_reader.py` obtiene entradas desde RSS, HTML o sitemap.
3. El contenido se filtra con reglas de `filters.py` para detectar violencia de género.
4. `article_scraper.py` extrae texto del artículo y `cleaner.py` normaliza fechas, URLs y ciudades.
5. Se crea un registro `Noticia` y se aplica clasificación automática en `save()`.
6. El frontend consume APIs REST y el admin muestra métricas y resultados de análisis.

## Notebooks y exportación a JSON

La aplicación `analisis` está diseñada para alojar resultados de procesamiento estructurado en `ResultadoAnalisis`, cuyo campo `datos` es un `JSONField`.

- El repositorio no contiene notebooks `.ipynb` visibles.
- El diseño sugiere que los notebooks producen JSON que luego se carga en `ResultadoAnalisis`.
- La ruta `/admin/monitor/` también expone un botón para ejecutar el comando `cargar_analisis`.

### Nota de inconsistencia

En el código actual se hace referencia a `cargar_analisis` en el admin, pero no se encuentra una implementación existente para ese comando dentro del repositorio.

## Componentes del pipeline de scraping

### `backend/noticias/services/rss_importer.py`

- Define fuentes en `SOURCES` para `El Tiempo`, `El Espectador` y `Caracol`.
- Limita la importación a `MAX_RELEVANT_PER_SOURCE` por fuente.
- Valida duplicados por URL.
- Clasifica y guarda solo noticias relevantes.

### `backend/noticias/services/filters.py`

- Contiene reglas de detección de violencia de género.
- Excluye contexto no relevante, como violencia geopolítica o deportes.
- Evalúa términos de violencia y contexto femenino antes de aceptar una noticia.

### `backend/noticias/services/cleaner.py`

- Normaliza HTML y elimina etiquetas.
- Convierte fechas de RSS a `datetime` consciente de zona.
- Extrae la ciudad desde el texto.
- Normaliza URLs y recorta a longitud válida.

## Datos almacenados

### `Noticia`

- Se guarda con metadatos de fuente, ciudad, fecha y clasificación.
- Los campos booleanos de violencia se calculan automáticamente.
- `nivel_riesgo` y `ambito_violencia` son inferidos antes de guardar.

### `ResultadoAnalisis`

- Almacena análisis de más alto nivel.
- `datos` puede ser cualquier estructura JSON relevante para métricas, series temporales o segmentación.

## Recomendación para completar el pipeline

- Implementar la management command `cargar_analisis` de modo que lea exportaciones JSON desde notebooks y cree/actualice `ResultadoAnalisis`.
- Asegurar que el pipeline de notebooks exporte datos con formato compatible a la estructura esperada por `analisis.models.ResultadoAnalisis`.
- Mantener el código de scraping separado del análisis offline para facilitar mantenimiento.

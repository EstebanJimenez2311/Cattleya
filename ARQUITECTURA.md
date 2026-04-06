# CATTLEYA — Arquitectura del sistema

## Arquitectura por capas

### Frontend
- Sitio estático en `cattleya-sitio/`.
- HTML, CSS y JavaScript vanilla.
- Componentes reutilizables bajo `assets/components/`.
- Consume directamente la API Django en `http://127.0.0.1:8000`.
- Incluye un proxy de Netlify obsoleto en `cattleya-sitio/netlify/functions/noticias-proxy.js` que no forma parte del flujo principal.

### API
- Backend Django en `backend/`.
- Django REST Framework para endpoints JSON.
- Rutas principales en `backend/config/urls.py`:
  - `api/` → `noticias`
  - `api/analisis/` → `analisis`
  - `api/estadisticas/` → `estadisticas`
- Endpoints definidos con `DefaultRouter` y vistas basadas en clases.

### Lógica de negocio
- La app `noticias/` implementa la ingestión y clasificación de noticias.
- La app `analisis/` guarda resultados analíticos en `ResultadoAnalisis`.
- La app `estadisticas/` calcula métricas dinámicas a partir de `Noticia`.
- Servicios de scraping y normalización residen en `backend/noticias/services/`.

### Base de datos
- Modelo principal: `Noticia`.
- Modelo analítico: `ResultadoAnalisis`.
- Base de datos compatible con PostgreSQL, pero el proyecto incluye SQLite para desarrollo.

## Flujo completo

1. Scraping de fuentes RSS y sitemap.
2. Filtrado de noticias relevantes.
3. Scraping de contenido de artículo y limpieza.
4. Guardado de `Noticia` con clasificación automática.
5. Cálculo dinámico de métricas en `estadisticas`.
6. Exposición de datos a través de la API.
7. Frontend consume la API y renderiza contenido.

## Decisiones importantes

### Por qué no se usa React
- El frontend busca ser ligero y fácil de desplegar como sitio estático.
- La aplicación prioriza una UX sencilla sin la complejidad de frameworks modernos.
- La integración con la API se puede lograr con fetch y Web Components.

### Por qué DRF
- DRF facilita la creación de endpoints JSON consistentes.
- Permite exponer modelos y acciones personalizadas sin reconstruir un router manual.
- Encaja bien con la arquitectura modular de Django.

### Por qué separación por apps
- `noticias/` agrupa todo lo relacionado con ingestión, filtrado y modelo de caso.
- `analisis/` separa los resultados de procesamiento estructurado en JSON.
- `estadisticas/` mantiene la lógica de métricas fuera del dominio principal de noticias.
- `config/` concentra configuración global, admin y rutas.

## Notas técnicas

- La página de admin usa una plantilla personalizada en `backend/templates/admin/index.html`.
- La ruta `/admin/monitor/` se agrega en `backend/config/admin.py`.
- Existe una inconsistencia: el botón `cargar_analisis` en el admin depende de un comando que no se encuentra en el repositorio.
- `backend/estadisticas/serializers.py` tiene definiciones duplicadas que deberían limpiarse para evitar confusiones.

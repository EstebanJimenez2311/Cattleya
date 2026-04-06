# ADMIN

## Admin personalizado de Django

El admin de CATTLEYA está extendido para ofrecer una experiencia de control interna más cercana a un dashboard de producto. La configuración principal está en `backend/config/admin.py` y en las plantillas bajo `backend/templates/admin/`.

### Personalizaciones clave

- `backend/config/admin.py` inyecta una ruta extra `/admin/monitor/` usando `admin.site.get_urls()`.
- El admin usa encabezados personalizados en `backend/config/urls.py`:
  - `site_header`: "Cattleya Admin"
  - `site_title`: "Cattleya Dashboard"
  - `index_title`: "Panel de gestion y monitoreo"
- La plantilla principal del dashboard es `backend/templates/admin/index.html`.

### Qué hace el panel base

El dashboard actual ofrece:

- Resumen rápido de métricas internas.
- Accesos directos al sitio público, al panel técnico y al cambio de contraseña.
- Listado de aplicaciones y modelos registrados en el admin.

### Sección `/admin/monitor/`

Esta sección se construye con `monitor_view` en `backend/config/admin.py` y muestra:

- Total de resultados de análisis (`ResultadoAnalisis`).
- Fecha de la última actualización de análisis.
- Total de noticias en `Noticia`.
- Distribución de niveles de riesgo.
- Distribución por ámbito de violencia.
- Enlaces directos a endpoints de API:
  - `/api/analisis/resultados/`
  - `/api/estadisticas/resumen/`
  - `/api/estadisticas/tendencia/`

### Acciones disponibles

- `Ejecutar cargar_analisis`: envía un POST al admin monitor para disparar el comando interno `cargar_analisis`.
- Ver sitio público directamente desde el admin.
- Acceso a la gestión de modelos a través del listado de app/modelo.

### Notas técnicas

- El admin monitor usa `TemplateResponse` para renderizar `admin/monitor.html`.
- El botón de acción `cargar_analisis` depende de `call_command('cargar_analisis')`.
- Revisión de repositorio: no se encontró una implementación de la management command `cargar_analisis` dentro del código disponible. Esto es una inconsistencia técnica que debe resolverse al integrar el pipeline de análisis.

## Modelos registrados relevantes

- `analisis.models.ResultadoAnalisis`
- `noticias.models.Noticia` via API y administración estándar.

## Cómo extender el admin

1. Agregar nuevas rutas personalizadas en `backend/config/admin.py`.
2. Crear vistas protegidas con `admin.site.admin_view()`.
3. Usar plantillas Django bajo `backend/templates/admin/` para conservar la estética del admin.

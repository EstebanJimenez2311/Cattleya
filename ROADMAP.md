# ROADMAP

## Fase 1 — Plataforma actual

Objetivo principal:
- Ingestión automatizada de noticias.
- Clasificación de violencia de género.
- API REST para consumo de frontend.
- Admin personalizado con dashboard y panel técnico.

Características implementadas:
- Modelo `Noticia` con clasificación automática.
- Servicios de scraping y limpieza en `backend/noticias/services/`.
- API para noticias, análisis y estadísticas.
- Frontend HTML/CSS/JS que consume API directa.
- Panel adicional `/admin/monitor/` para métricas y operaciones.

## Fase 2 — Notebooks y análisis avanzado

Meta:
- Integrar notebooks de análisis en el flujo de datos.
- Exportar resultados a JSON.
- Persistir esos resultados en `ResultadoAnalisis`.
- Mejorar el panel técnico con análisis históricos.

Tareas clave:
- Crear notebooks reproducibles para extracción y modelado.
- Añadir comando `cargar_analisis` real que cargue resultados en el backend.
- Expander `analisis/` con endpoints de consulta de series y metadatos.
- Documentar formatos JSON esperados.

## Fase 3 — Visualización avanzada

Meta:
- Dashboard interactivo del frontend con gráficos.
- Filtros por ciudad, tipo de violencia y período.
- Visualizaciones de tendencia y riesgo.

Tareas clave:
- Añadir componentes visuales en `cattleya-sitio/assets/components/`.
- Consumir `/api/estadisticas/tendencia/` y `/api/estadisticas/tipos/`.
- Crear páginas de insights y mapas.

## Mejoras futuras

- Implementar backend de tareas en segundo plano (Celery, RQ o cron).
- Agregar permisos y roles en el admin.
- Añadir tests automatizados para cada endpoint.
- Documentar y versionar el contrato de API.
- Considerar despliegue en un contenedor o plataforma PaaS.

## Riesgos y pendientes

- Hay una inconsistencia en el admin: el botón `cargar_analisis` apunta a un comando no disponible en el repositorio.
- `estadisticas/serializers.py` requiere limpieza de definiciones duplicadas.
- Los notebooks de análisis no están incluidos en el repositorio actual.

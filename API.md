# API

## Noticias

### GET /api/noticias/

Descripción:
- Lista todas las noticias activas (excluye `es_prueba`).
- Devuelve todos los campos de `Noticia`.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
[
  {
    "id": 1,
    "titulo": "Caso de violencia de género en Bogotá",
    "descripcion": "Resumen del caso...",
    "contenido": "Texto completo...",
    "fecha_publicacion": "2026-04-01T10:00:00Z",
    "fuente": "El Tiempo",
    "url": "https://...",
    "ciudad": "Bogota",
    "violencia_fisica": true,
    "violencia_psicologica": false,
    "violencia_sexual": false,
    "violencia_economica": false,
    "violencia_patrimonial": false,
    "feminicidio": false,
    "ambito_violencia": "pareja",
    "nivel_riesgo": "alto",
    "verificada": false,
    "es_prueba": false,
    "created_at": "2026-04-01T10:01:00Z",
    "updated_at": "2026-04-01T10:01:00Z",
    "tipo_violencia": "fisica"
  }
]
```

### GET /api/noticias/recientes/

Descripción:
- Devuelve las noticias más recientes.
- Está pensado para el frontend y usa la misma serialización que el listado.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
[
  {
    "titulo": "Noticia reciente...",
    "descripcion": "...",
    "fecha_publicacion": "2026-04-01T10:00:00Z",
    "fuente": "Caracol Radio",
    "url": "https://...",
    "ciudad": "Medellin",
    "tipo_violencia": "psicologica",
    "nivel_riesgo": "medio"
  }
]
```

### GET /api/noticias/resumen/

Descripción:
- Devuelve estadísticas agregadas de noticias.
- Incluye conteos por tipo de violencia, por ciudad, por ámbito y por nivel de riesgo.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
{
  "tipo_violencia": [
    {"tipo_violencia": "fisica", "count": 12},
    {"tipo_violencia": "psicologica", "count": 8}
  ],
  "ciudad": [
    {"ciudad": "Bogota", "count": 10},
    {"ciudad": "Medellin", "count": 5}
  ],
  "ambito_violencia": [
    {"ambito_violencia": "pareja", "count": 9}
  ],
  "nivel_riesgo": [
    {"nivel_riesgo": "alto", "count": 7}
  ],
  "casos_criticos": 3
}
```

## Análisis

### GET /api/analisis/resultados/

Descripción:
- Lista todos los resultados de análisis almacenados en `ResultadoAnalisis`.
- Cada elemento incluye metadatos y el objeto `datos` con el JSON de análisis.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
[
  {
    "id": 1,
    "nombre": "resumen_general",
    "fuente": "notebooks",
    "descripcion": "Resumen de métricas extraídas",
    "datos": {
      "categorias": ["física", "psicológica"],
      "total": 34
    },
    "actualizado": "2026-04-01T12:00:00Z"
  }
]
```

### GET /api/analisis/resultados/{nombre}/

Descripción:
- Devuelve un resultado de análisis específico por su campo `nombre`.

Parámetros:
- `nombre`: identificador único del análisis.

Ejemplo de respuesta:

```json
{
  "id": 1,
  "nombre": "resumen_general",
  "fuente": "notebooks",
  "descripcion": "Resumen de métricas extraídas",
  "datos": {
    "categorias": ["física", "psicológica"],
    "total": 34
  },
  "actualizado": "2026-04-01T12:00:00Z"
}
```

## Estadísticas

### GET /api/estadisticas/resumen/

Descripción:
- Devuelve métricas generales sobre las noticias almacenadas.
- Incluye totales, conteo por tipo de violencia, ámbitos y ciudades.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
{
  "total_noticias": 42,
  "total_verificadas": 17,
  "tipos_violencia": {
    "fisica": 18,
    "psicologica": 12,
    "sexual": 4
  },
  "ambitos": {
    "pareja": 15,
    "familiar": 10
  },
  "ciudades_top": [
    {"ciudad": "Bogota", "cantidad": 16},
    {"ciudad": "Medellin", "cantidad": 9}
  ]
}
```

### GET /api/estadisticas/tendencia/

Descripción:
- Devuelve la evolución mensual de noticias.
- Agrupa por mes y calcula totales y verificadas.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
[
  {
    "mes": "2026-01",
    "total": 9,
    "verificadas": 3,
    "tipos_violencia": {
      "fisica": 5,
      "psicologica": 2
    }
  }
]
```

### GET /api/estadisticas/tipos/

Descripción:
- Devuelve el porcentaje y la cantidad de cada tipo de violencia.
- Selecciona solo los tipos con al menos una incidencia.

Parámetros:
- Ninguno.

Ejemplo de respuesta:

```json
[
  {"tipo": "Fisica", "cantidad": 18, "porcentaje": 42.86},
  {"tipo": "Psicologica", "cantidad": 12, "porcentaje": 28.57}
]
```

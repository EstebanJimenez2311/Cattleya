# FRONTEND

## Estructura del frontend

El frontend de CATTLEYA es un sitio estático en `cattleya-sitio/` que utiliza HTML, CSS y JavaScript puro.

Carpetas relevantes:

- `cattleya-sitio/js/`: código de interacción y consumo de API.
- `cattleya-sitio/css/`: estilos base, diseños y animaciones.
- `cattleya-sitio/assets/components/`: Web Components reutilizables.
- `cattleya-sitio/data/charts.js`: datos de gráficos y configuraciones de visualización.
- `cattleya-sitio/netlify/functions/`: función obsoleta de proxy de noticias.

## Uso de Web Components

El proyecto incluye varios Web Components customizados:

- `cat-card.js`
- `cat-chart.js`
- `cat-cta-banner.js`
- `cat-footer.js`
- `cat-help-btn.js`
- `cat-navbar.js`
- `cat-page-hero.js`
- `cat-section-header.js`
- `cat-stat-card.js`
- `cat-surface.js`

Estos componentes encapsulan la UI y facilitan la composición de páginas sin depender de frameworks.

## Consumo de la API

El frontend se conecta directamente al backend Django en `http://127.0.0.1:8000`.

Ejemplo clave:

- `cattleya-sitio/js/noticias.js` usa `fetch('http://127.0.0.1:8000/api/noticias/recientes/')`.

Flujo de consumo:

1. El script obtiene noticias recientes desde la API.
2. Convierte campos del backend a un formato amigable para la UI.
3. Renderiza cada noticia en tarjetas y carruseles.

## Archivos clave

- `cattleya-sitio/js/main.js`: punto de entrada general.
- `cattleya-sitio/js/noticias.js`: carga noticias y construye la experiencia editorial.
- `cattleya-sitio/js/raiz-datos.js`: probablemente se usa en páginas de datos y visualización.
- `cattleya-sitio/data/charts.js`: contiene datos estáticos para gráficos.

## Notas de diseño

- No se usa React ni Vue. Esto mantiene el proyecto ligero y fácil de desplegar como sitio estático.
- Las páginas están diseñadas para consumir APIs directas y usar componentes modulares.
- La función Netlify en `cattleya-sitio/netlify/functions/noticias-proxy.js` se declara como `DEPRECATED` y se mantiene solo como referencia histórica.

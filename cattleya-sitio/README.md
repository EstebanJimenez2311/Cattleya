# 🌸 CATTLEYA — Datos que no callan

> Proyecto de Técnico en Programación para Analítica de Datos  
> Análisis de datos gubernamentales sobre violencia contra la mujer en Colombia

[![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)](https://github.com)
[![HTML](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

## 🌺 ¿Por qué Cattleya?

La **Cattleya trianae** es la orquídea nacional de Colombia. Florece en condiciones adversas, en alturas donde pocas plantas sobreviven. La elegimos como símbolo porque cada mujer que ha enfrentado la violencia demuestra exactamente esa clase de fortaleza.

El nombre también es un **acrónimo navegable** que estructura todo el proyecto:

| Letra | Sección | Descripción |
|-------|---------|-------------|
| **C** | Contexto | Marco legal colombiano, tipos de violencia, Ley Rosa Elvira Cely |
| **A** | Análisis | EDA y estadística descriptiva con gráficos interactivos |
| **T** | Tendencias | Estadística inferencial y modelo de Machine Learning |
| **T** | Testimonios | Noticias y casos documentados |
| **L** | Lucha | Recursos de ayuda y líneas de emergencia |
| **E** | Equipo | Quiénes somos y por qué este proyecto importa |
| **Y** | Yo Decido | Entregables del proyecto de grado |
| **A** | Alertas | Las cifras más urgentes |

---

## 📁 Estructura del proyecto

```
cattleya/
│
├── index.html              ← Página principal
├── analisis.html           ← EDA + estadística descriptiva
├── tendencias.html         ← Inferencial + Machine Learning
├── contexto.html           ← Marco legal y tipos de violencia
├── testimonios.html        ← Noticias y casos documentados
├── lucha.html              ← Líneas de ayuda y recursos
├── equipo.html             ← About us
├── yo-decido.html          ← Entregables para el jurado
├── alertas.html            ← Cifras de impacto
├── cattleya.html           ← ¿Qué es Cattleya? + acrónimo
│
├── components/             ← Web Components reutilizables
│   ├── index.js            ← Importador central
│   ├── cat-navbar.js       ← <cat-navbar active="inicio">
│   ├── cat-footer.js       ← <cat-footer>
│   ├── cat-page-hero.js    ← <cat-page-hero letter="C" title="...">
│   ├── cat-stat-card.js    ← <cat-stat-card number="182K" label="...">
│   ├── cat-card.js         ← <cat-card icon="👊" title="..." text="...">
│   ├── cat-chart.js        ← <cat-chart chart-id="..." title="...">
│   ├── cat-cta-banner.js   ← <cat-cta-banner title="..." btn-href="...">
│   └── cat-section-header.js
│
├── data/
│   └── charts.js           ← Datos centralizados de todos los gráficos
│
├── css/
│   └── styles.css          ← Estilos globales y paleta de colores
│
├── js/
│   └── main.js             ← Utilidades generales
│
└── assets/
    ├── logo-claro.png
    └── logo-magenta.png
```

---

## 🎨 Paleta de colores

| Nombre | Hex | Uso |
|--------|-----|-----|
| Magenta Identidad | `#9D2D6A` | Navbar, headers, elementos de marca |
| Crema Pétalo | `#FDEEE9` | Fondos de cards, secciones suaves |
| Naranja Acción | `#F28C28` | Botones CTA, alertas, links activos |
| Blanco Nieve | `#FFFFFF` | Fondo general |
| Púrpura Profundo | `#822157` | Títulos, contraste tipográfico |
| Gris Carbón | `#333333` | Texto cuerpo |

---

## 🧩 Guía de Web Components

Cada componente es un archivo independiente en `/components/`. Para usar cualquiera, incluye en tu página:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="data/charts.js"></script>
<script src="components/index.js"></script>
```

### `<cat-navbar active="...">`
```html
<!-- Valores: inicio | analisis | educacion | cattleya -->
<cat-navbar active="analisis"></cat-navbar>
```

### `<cat-page-hero>`
```html
<cat-page-hero
  letter="A" position="Segunda"
  title="Análisis"
  subtitle="EDA y estadística descriptiva.">
</cat-page-hero>
```

### `<cat-stat-card>`
```html
<!-- Estática -->
<cat-stat-card number="182K" label="casos registrados"></cat-stat-card>

<!-- Con contador animado -->
<cat-stat-card animate target="78" suffix="%" label="víctimas son mujeres"></cat-stat-card>

<!-- Variante oscura -->
<cat-stat-card variant="dark" number="60%" label="no denunciados"></cat-stat-card>
```

### `<cat-card>`
```html
<cat-card icon="👊" title="Violencia Física" text="Descripción..."></cat-card>
<cat-card icon="📜" title="Ley 1761" text="..." variant="highlight"></cat-card>
<cat-card icon="📊" title="Ver análisis" text="..." href="analisis.html"></cat-card>
```

### `<cat-chart>`
```html
<cat-chart
  chart-id="chart-evolucion"
  title="Evolución anual de casos"
  description="¿Aumentaron o disminuyeron los casos?"
  height="320">
</cat-chart>
```

Registrar los datos del gráfico en `data/charts.js`:
```javascript
window.CHARTS['chart-evolucion'] = {
  type: 'line',
  data: { labels: [...], datasets: [{ data: [...] }] },
  options: { ... }
};
```

### `<cat-cta-banner>`
```html
<cat-cta-banner
  title="¿Necesitas ayuda ahora?"
  text="No estás sola."
  btn-text="Ver líneas de ayuda →"
  btn-href="lucha.html">
</cat-cta-banner>
```

### `<cat-section-header>`
```html
<cat-section-header
  label="EDA"
  title="¿Qué dicen los datos?"
  subtitle="Cada gráfico responde una pregunta clave.">
</cat-section-header>
```

---

## 🛠️ Cómo correr el proyecto localmente

```bash
# Opción 1 — Python
cd cattleya/
python -m http.server 3000
# Abrir http://localhost:3000

# Opción 2 — Node.js
npx serve cattleya/

# Opción 3 — VS Code
# Instalar extensión Live Server → clic derecho en index.html → Open with Live Server
```

> ⚠️ Los Web Components requieren un servidor HTTP. No abrir `index.html` directo como archivo (file://).

---

## 📊 Cómo conectar los datos reales del análisis en Python

```python
# En tu Jupyter Notebook, exportar resultados así:
resultados = {
    "labels": df['tipo_violencia'].value_counts().index.tolist(),
    "data":   df['tipo_violencia'].value_counts().values.tolist(),
}
# Luego pegar esos arrays en data/charts.js en el gráfico correspondiente
```

---

## 🌿 Flujo de trabajo Git para el equipo

```bash
# 1. Cada integrante trabaja en su rama
git checkout -b feature/mi-seccion

# 2. Guardar cambios con mensajes descriptivos
git add .
git commit -m "feat: agregar gráfico de evolución anual"

# 3. Subir la rama
git push origin feature/mi-seccion

# 4. Abrir Pull Request hacia dev en GitHub
```

### Convención de commits
```
feat:     nueva funcionalidad o página
fix:      corrección de bug
style:    cambios visuales
data:     actualización de datos o gráficos
docs:     cambios en README u otros docs
refactor: reorganización sin cambio de comportamiento
```

### Ramas recomendadas
```
main                  ← versión estable (solo merge aprobado)
dev                   ← integración del equipo
feature/analisis      ← gráficos y EDA
feature/contexto      ← marco legal
feature/testimonios   ← noticias
feature/equipo        ← about us y entregables
```

---

## 📂 Entregables del proyecto

| Entregable | Estado |
|-----------|--------|
| Informe de tratamiento de datos | 🔄 En progreso |
| Informe de análisis (EDA + ML) | 🔄 En progreso |
| Notebook EDA (Jupyter) | 🔄 En progreso |
| Notebook Machine Learning | 🔄 En progreso |
| Dataset procesado (CSV) | 🔄 En progreso |
| Sitio web CATTLEYA | ✅ En desarrollo |

---

## 👥 Equipo

| Integrante | Rol |
|-----------|-----|
| [Nombre 1] | Arquitectura web, backend e integración |
| [Nombre 2] | Análisis descriptivo e inferencial |
| [Nombre 3] | Machine Learning y visualizaciones |
| [Nombre 4] | Contenido, diseño y redacción |

---

## 📜 Marco legal

- **Ley 1257 de 2008** — Prevención y sanción de violencia contra las mujeres
- **Ley 1761 de 2015** — *"Rosa Elvira Cely"* — Feminicidio como delito autónomo
- **Ley 1719 de 2014** — Acceso a la justicia para víctimas de violencia sexual
- **Convención Belém do Pará (1994)** — Marco internacional ratificado por Colombia

---

## 🆘 Líneas de ayuda en Colombia

| Línea | Entidad |
|-------|---------|
| **155** | Línea Mujer — 24/7, gratuita |
| **123** | Emergencias nacionales |
| **141** | ICBF |
| **018000112998** | Fiscalía — Denuncia anónima |

---

*"La orquídea no pregunta si el viento es demasiado fuerte. Florece igual."*

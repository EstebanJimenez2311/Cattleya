#!/bin/bash
# ============================================================
#  CATTLEYA — Script de inicialización del repositorio Git
#  Ejecutar desde la carpeta raíz del proyecto: bash setup-git.sh
# ============================================================

echo ""
echo "🌸 CATTLEYA — Configurando repositorio Git"
echo "============================================"

# ── 1. CONFIGURAR NOMBRE Y EMAIL (editar con los datos del equipo)
# git config --global user.name "Tu Nombre"
# git config --global user.email "tu@email.com"

# ── 2. INICIALIZAR REPO
git init
echo "✅ Repositorio inicializado"

# ── 3. COMMIT 1 — Estructura base y sistema de diseño
git add css/styles.css js/main.js .gitignore
git commit -m "feat: sistema de diseño base

- Paleta de colores Cattleya (magenta, crema, naranja, púrpura)
- Tipografía Playfair Display + DM Sans
- Navbar fija magenta con dropdowns en hover
- Componentes: stat cards, chart containers, cards grid
- Botones primary/outline, CTA banner, footer
- Animaciones con IntersectionObserver
- Diseño responsive"

echo "✅ Commit 1/6 — Sistema de diseño"

# ── 4. COMMIT 2 — Assets del proyecto
git add assets/
git commit -m "feat: assets visuales del proyecto

- Logo Cattleya versión magenta (sobre fondos claros)
- Logo Cattleya versión crema (sobre fondos oscuros)
- Orquídea Cattleya trianae como identidad visual del proyecto"

echo "✅ Commit 2/6 — Assets"

# ── 5. COMMIT 3 — Página principal
git add index.html cattleya.html
git commit -m "feat: página principal y presentación del proyecto

index.html:
- Hero con mensaje de impacto y cifras clave animadas
- 4 stat cards con contadores numéricos
- Preview de análisis con gráfico Chart.js
- CTA de línea de ayuda

cattleya.html:
- Significado de la orquídea Cattleya trianae
- Acrónimo C·A·T·T·L·E·Y·A con grid navegable"

echo "✅ Commit 3/6 — Página principal"

# ── 6. COMMIT 4 — Secciones de análisis
git add analisis.html tendencias.html alertas.html
git commit -m "feat: secciones de análisis de datos

analisis.html:
- EDA con 5 gráficos interactivos Chart.js
- Evolución anual, distribución por departamento
- Grupos de edad, tipo de violencia, estacionalidad

tendencias.html:
- Estructura para estadística inferencial
- Placeholder para modelo Machine Learning y métricas

alertas.html:
- Cifras clave de impacto con diseño visual de alto contraste"

echo "✅ Commit 4/6 — Análisis"

# ── 7. COMMIT 5 — Secciones educativas e informativas
git add contexto.html testimonios.html lucha.html
git commit -m "feat: secciones educativas y de ayuda

contexto.html:
- Tipos de violencia de género reconocidos
- Ley 1257 de 2008, Ley 1719 de 2014
- Ley 1761 de 2015 (Rosa Elvira Cely) — feminicidio autónomo
- Artículo 104A: 6 circunstancias configurantes
- Artículo 104B: agravantes y penas
- Convención Belém do Pará

testimonios.html:
- Estructura para noticias y casos documentados

lucha.html:
- Líneas de emergencia Colombia (155, 123, 141, Fiscalía)
- 5 pasos de acción para víctimas
- CTA de ayuda inmediata"

echo "✅ Commit 5/6 — Educativas y ayuda"

# ── 8. COMMIT 6 — Equipo y entregables
git add equipo.html yo-decido.html README.md
git commit -m "feat: equipo, entregables y documentación

equipo.html:
- Cards del equipo de trabajo
- Sección visión/misión
- Significado del nombre Cattleya

yo-decido.html:
- Cards de entregables con botones de descarga
- Informe de tratamiento de datos
- Informe de análisis
- Notebooks Jupyter
- Dataset procesado
- Código fuente del sitio
- Sección de fuentes de datos

README.md:
- Documentación completa del proyecto
- Estructura de archivos
- Stack técnico
- Instrucciones de instalación
- Marco legal referenciado
- Tabla del equipo"

echo "✅ Commit 6/6 — Equipo, entregables y README"

# ── RESUMEN
echo ""
echo "============================================"
echo "🎉 Repositorio listo con $(git log --oneline | wc -l) commits"
echo ""
echo "👉 Próximos pasos para subir a GitHub:"
echo ""
echo "  1. Crea el repositorio en https://github.com/new"
echo "     - Nombre sugerido: cattleya"
echo "     - Descripción: Análisis de datos sobre violencia contra la mujer en Colombia"
echo "     - Visibilidad: Public"
echo "     - ⚠️ NO inicializar con README (ya tenemos uno)"
echo ""
echo "  2. Conecta y sube:"
echo "     git remote add origin https://github.com/TU_USUARIO/cattleya.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""
echo "  3. (Opcional) Activar GitHub Pages:"
echo "     Settings → Pages → Source: main branch → / (root)"
echo "     Tu sitio estará en: https://TU_USUARIO.github.io/cattleya"
echo ""
echo "🌸 ¡Cattleya lista para florecer en la web!"

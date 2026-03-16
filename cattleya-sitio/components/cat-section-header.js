/**
 * <cat-section-header label="..." title="..." subtitle="...">
 *
 * Atributos:
 *   label    — etiqueta pequeña encima del título (ej: "Estadística Descriptiva")
 *   title    — título principal (soporta <em> y <br> como texto)
 *   subtitle — párrafo descriptivo debajo del título
 *
 * Uso:
 *   <cat-section-header
 *     label="Estadística Descriptiva"
 *     title="Los datos hablan, &lt;em&gt;nosotros escuchamos&lt;/em&gt;"
 *     subtitle="Análisis exploratorio aplicado a datos gubernamentales.">
 *   </cat-section-header>
 */
class CatSectionHeader extends HTMLElement {
  connectedCallback() { this._render(); }

  _render() {
    const label    = this.getAttribute('label')    || '';
    const title    = this.getAttribute('title')    || '';
    const subtitle = this.getAttribute('subtitle') || '';

    this.innerHTML = `
      ${label    ? `<span class="section-label">${label}</span>` : ''}
      ${title    ? `<h2 class="section-title">${title}</h2>` : ''}
      ${subtitle ? `<p class="section-subtitle">${subtitle}</p>` : ''}
    `;
  }
}

customElements.define('cat-section-header', CatSectionHeader);

/**
 * <cat-page-hero letter="C" title="Contexto" subtitle="...">
 *
 * Atributos:
 *   letter   — letra del acrónimo (ej: "C")
 *   position — "Primera", "Segunda", etc.
 *   title    — título de la página
 *   subtitle — descripción corta
 *
 * Uso:
 *   <cat-page-hero
 *     letter="A"
 *     position="Segunda"
 *     title="Análisis"
 *     subtitle="EDA y estadística descriptiva con gráficos interactivos.">
 *   </cat-page-hero>
 */
class CatPageHero extends HTMLElement {
  static get observedAttributes() {
    return ['letter', 'position', 'title', 'subtitle'];
  }

  connectedCallback() { this._render(); }
  attributeChangedCallback() { this._render(); }

  _render() {
    const letter   = this.getAttribute('letter')   || '';
    const position = this.getAttribute('position') || '';
    const title    = this.getAttribute('title')    || '';
    const subtitle = this.getAttribute('subtitle') || '';

    const badge = letter
      ? `<div class="page-hero__letter-badge">
           <strong>${letter}</strong>${position ? ` · ${position} letra de CATTLEYA` : ''}
         </div>`
      : '';

    this.innerHTML = `
      <div class="page-hero">
        ${badge}
        <h1>${title}</h1>
        ${subtitle ? `<p>${subtitle}</p>` : ''}
      </div>
    `;
  }
}

customElements.define('cat-page-hero', CatPageHero);

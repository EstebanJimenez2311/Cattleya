/**
 * <cat-card icon="👊" title="Violencia Física" text="Descripción...">
 *
 * Atributos:
 *   icon     — emoji o texto del ícono
 *   title    — título de la card
 *   text     — texto descriptivo
 *   variant  — "default" | "highlight" (borde magenta)
 *   href     — si se incluye, la card entera es un enlace
 *
 * Uso:
 *   <cat-card icon="👊" title="Violencia Física" text="Todo acto que cause daño..."></cat-card>
 *   <cat-card icon="📜" title="Ley 1761" text="..." variant="highlight"></cat-card>
 *   <cat-card icon="📊" title="Análisis" text="..." href="analisis.html"></cat-card>
 */
class CatCard extends HTMLElement {
  connectedCallback() { this._render(); }

  _render() {
    const icon    = this.getAttribute('icon')    || '';
    const title   = this.getAttribute('title')   || '';
    const text    = this.getAttribute('text')    || '';
    const variant = this.getAttribute('variant') || 'default';
    const href    = this.getAttribute('href')    || '';

    const highlightStyle = variant === 'highlight'
      ? 'style="border: 2px solid var(--magenta);"'
      : '';

    const inner = `
      <div class="card__icon">${icon}</div>
      <div class="card__title">${title}</div>
      <div class="card__text">${text}</div>
    `;

    this.innerHTML = href
      ? `<a href="${href}" class="card" ${highlightStyle}>${inner}</a>`
      : `<div class="card" ${highlightStyle}>${inner}</div>`;
  }
}

customElements.define('cat-card', CatCard);

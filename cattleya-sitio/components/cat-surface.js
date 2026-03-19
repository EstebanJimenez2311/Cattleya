/**
 * <cat-surface variant="default|cream|tint" padding="28px" radius="28px">
 *   ...cualquier contenido...
 * </cat-surface>
 *
 * Contenedor visual reutilizable para agrupar cards, métricas o grids.
 */
class CatSurface extends HTMLElement {
  connectedCallback() {
    if (this.dataset.rendered === 'true') return;

    const content = this.innerHTML;
    const variant = this.getAttribute('variant') || 'default';
    const padding = this.getAttribute('padding');
    const radius = this.getAttribute('radius');

    const styleVars = [
      padding ? `--cat-surface-padding:${padding}` : '',
      radius ? `--cat-surface-radius:${radius}` : '',
    ].filter(Boolean).join(';');

    this.innerHTML = `
      <div class="cat-surface cat-surface--${variant}"${styleVars ? ` style="${styleVars}"` : ''}>
        <div class="cat-surface__inner">${content}</div>
      </div>
    `;

    this.dataset.rendered = 'true';
  }
}

customElements.define('cat-surface', CatSurface);

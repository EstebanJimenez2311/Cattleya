/**
 * <cat-cta-banner title="..." text="..." btn-text="..." btn-href="...">
 *
 * Atributos:
 *   title    — título del banner
 *   text     — texto descriptivo
 *   btn-text — texto del botón (default: "Ver más →")
 *   btn-href — URL del botón (default: "lucha.html")
 *
 * Uso:
 *   <cat-cta-banner
 *     title="¿Necesitas ayuda ahora?"
 *     text="No estás sola. Hay personas dispuestas a escucharte."
 *     btn-text="Ver líneas de ayuda →"
 *     btn-href="lucha.html">
 *   </cat-cta-banner>
 */
class CatCtaBanner extends HTMLElement {
  connectedCallback() { this._render(); }

  _render() {
    const title   = this.getAttribute('title')    || '¿Necesitas ayuda ahora?';
    const text    = this.getAttribute('text')     || '';
    const btnText = this.getAttribute('btn-text') || 'Ver más →';
    const btnHref = this.getAttribute('btn-href') || 'lucha.html';

    this.innerHTML = `
      <div class="cta-banner">
        <h2>${title}</h2>
        ${text ? `<p>${text}</p>` : ''}
        <a href="${btnHref}" class="btn-outline"
           style="display:inline-flex;border-color:rgba(255,255,255,0.6);">
          ${btnText}
        </a>
      </div>
    `;
  }
}

customElements.define('cat-cta-banner', CatCtaBanner);

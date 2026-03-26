/**
 * <cat-help-btn>
 *
 * Botón flotante "¿Necesitas Ayuda?" que acompaña al usuario
 * en toda la página. Enlaza a lucha.html.
 *
 * Uso:
 *   <cat-help-btn></cat-help-btn>
 *   (colocar justo antes de </body> en cada página)
 */
class CatHelpBtn extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <style>
        .cat-help-fab {
          position: fixed;
          bottom: 28px;
          right: 28px;
          z-index: 9999;
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: #d4700a;
          color: #ffffff;
          font-family: 'DM Sans', sans-serif;
          font-size: 0.92rem;
          font-weight: 600;
          text-decoration: none;
          padding: 13px 22px;
          border-radius: 999px;
          box-shadow: 0 6px 24px rgba(212,112,10,0.45);
          transition: transform 0.2s, box-shadow 0.2s;
          white-space: nowrap;
        }
        .cat-help-fab:hover {
          transform: translateY(-3px);
          box-shadow: 0 10px 32px rgba(212,112,10,0.55);
          color: #ffffff;
        }
        .cat-help-fab:active {
          transform: translateY(0);
        }
        .cat-help-fab__icon {
          font-size: 1.1rem;
          line-height: 1;
        }
      </style>
      <a href="lucha.html" class="cat-help-fab" aria-label="¿Necesitas ayuda?">
        <span class="cat-help-fab__icon">🆘</span>
        ¿Necesitas Ayuda?
      </a>
    `;
  }
}

customElements.define('cat-help-btn', CatHelpBtn);
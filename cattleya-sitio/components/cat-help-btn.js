/**
 * <cat-help-btn>
 *
 * Boton flotante "¿Necesitas Ayuda?" que acompana al usuario
 * en toda la pagina. Enlaza a lucha.html.
 *
 * Uso:
 *   <cat-help-btn></cat-help-btn>
 *   (colocar justo antes de </body> en cada pagina)
 */
if (!customElements.get('cat-help-btn')) {
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
          <span class="cat-help-fab__icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
              <path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <circle cx="12" cy="17" r="1" fill="currentColor"/>
              <path d="M10.29 3.86L1.82 18A2 2 0 003.53 21h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"
                    stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            </svg>
          </span>
          ¿Necesitas Ayuda?
        </a>
      `;
    }
  }

  customElements.define('cat-help-btn', CatHelpBtn);
}

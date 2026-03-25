/**
 * <cat-footer>
 *
 * Uso:
 *   <cat-footer></cat-footer>
 */
class CatFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <footer class="footer">
        <div class="footer-grid">
          <div class="footer-brand">
            <a href="index.html" class="footer-logo">
              <svg width="34" height="34" viewBox="0 0 36 36" fill="none">
                <ellipse cx="18" cy="18" rx="10" ry="14" fill="#F6871D" opacity="0.9"/>
                <ellipse cx="8" cy="15" rx="7" ry="4" fill="#fff" opacity="0.65" transform="rotate(-20 8 15)"/>
                <ellipse cx="28" cy="15" rx="7" ry="4" fill="#fff" opacity="0.65" transform="rotate(20 28 15)"/>
                <ellipse cx="18" cy="25" rx="5" ry="7" fill="#fff" opacity="0.45"/>
                <circle cx="18" cy="18" r="3.5" fill="#8B2467"/>
              </svg>
              <span class="footer-logo-text">Cattleya</span>
            </a>
            <p class="footer-description">
              Plataforma institucional de análisis y visualización de datos para la transparencia, prevención y disminución de la violencia de género en el territorio nacional.
            </p>
            <div class="footer-socials">
              <button class="social-icon" aria-label="Compartir" type="button">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </button>
              <button class="social-icon" aria-label="Sitio web" type="button">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
              </button>
            </div>
          </div>

          <div class="footer-col">
            <h4>Explorar</h4>
            <a href="index.html">Inicio</a>
            <a href="raiz-datos.html">Power Bi</a>
            <a href="analisis.html">Prototipo</a>
          </div>

          <div class="footer-col">
            <h4>Recursos</h4>
            <a href="contexto.html">Metodología</a>
            <a href="testimonios.html">Información y educación</a>
          </div>

          <div class="footer-col">
            <h4>Contacto</h4>
            <a href="lucha.html">Línea de ayuda</a>
            <a href="equipo.html">Nosotros</a>
          </div>
        </div>

        <div class="footer-bottom">
          <p>© 2024 Cattleya. Todos los derechos reservados.</p>
          <div class="footer-bottom-links">
            <a href="#">Política de Privacidad</a>
            <a href="#">Términos de Uso</a>
            <a href="equipo.html">Créditos del Equipo</a>
          </div>
        </div>
      </footer>
    `;
  }
}

customElements.define('cat-footer', CatFooter);

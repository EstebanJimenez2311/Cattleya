/**
 * <cat-footer>
 *
 * Uso:
 *   <cat-footer></cat-footer>
 */
class CatFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <footer>
        <div class="footer__inner">
          <div>
            <div class="footer__brand-name">CATTLEYA</div>
            <p class="footer__tagline">
              Datos que no callan. Un proyecto de análisis de datos
              sobre violencia contra la mujer en Colombia.
            </p>
          </div>
          <div class="footer__col">
            <h4>Análisis</h4>
            <ul>
              <li><a href="analisis.html">Estadística Descriptiva</a></li>
              <li><a href="tendencias.html">Tendencias y ML</a></li>
            </ul>
          </div>
          <div class="footer__col">
            <h4>Proyecto</h4>
            <ul>
              <li><a href="contexto.html">Contexto</a></li>
              <li><a href="equipo.html">Equipo</a></li>
              <li><a href="yo-decido.html">Entregables</a></li>
              <li><a href="lucha.html">Línea de Ayuda</a></li>
            </ul>
          </div>
        </div>
        <div class="footer__bottom">
          <span>© 2025 Cattleya · Proyecto de Grado · Técnico en Programación para Analítica de Datos</span>
          <span>Hecho con 💜 para que los datos no callen</span>
        </div>
      </footer>
    `;
  }
}

customElements.define('cat-footer', CatFooter);

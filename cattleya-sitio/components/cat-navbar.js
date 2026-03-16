/**
 * <cat-navbar active="inicio|analisis|educacion|cattleya">
 *
 * Uso:
 *   <cat-navbar active="analisis"></cat-navbar>
 */
class CatNavbar extends HTMLElement {
  static get observedAttributes() { return ['active']; }

  connectedCallback() { this._render(); }
  attributeChangedCallback() { this._render(); }

  get active() { return this.getAttribute('active') || 'inicio'; }

  _isActive(key) {
    return this.active === key ? 'class="active"' : '';
  }

  _render() {
    this.innerHTML = `
      <style>
        cat-navbar { display: block; }
      </style>
      <nav class="navbar" id="navbar">
        <a class="navbar__brand" href="index.html">
          <img src="assets/logo-claro.png" alt="Cattleya" class="navbar__logo" id="navbar-logo">
          <span class="navbar__name">CATTLEYA</span>
        </a>
        <ul class="navbar__links">

          <li>
            <a href="index.html" ${this._isActive('inicio')}>Inicio</a>
          </li>

          <li>
            <a href="#" ${this._isActive('analisis')}>
              Análisis <span class="dropdown-arrow">▾</span>
            </a>
            <div class="dropdown">
              <a href="analisis.html">📊 Estadística Descriptiva</a>
              <a href="tendencias.html">📈 Tendencias y Machine Learning</a>
              <a href="analisis.html#powerbi">🖥️ Power BI</a>
            </div>
          </li>

          <li>
            <a href="#" ${this._isActive('educacion')}>
              Información y educación <span class="dropdown-arrow">▾</span>
            </a>
            <div class="dropdown">
              <a href="contexto.html">📚 Contexto y Marco Legal</a>
              <a href="testimonios.html">📰 Noticias y Testimonios</a>
              <a href="lucha.html">🆘 Línea de Ayuda</a>
            </div>
          </li>

          <li>
            <a href="#" ${this._isActive('cattleya')}>
              ¿Qué es Cattleya? <span class="dropdown-arrow">▾</span>
            </a>
            <div class="dropdown">
              <a href="cattleya.html">🌸 El Acrónimo C·A·T·T·L·E·Y·A</a>
              <a href="equipo.html#vision">🎯 Visión y Misión</a>
              <a href="equipo.html">👥 El Equipo</a>
              <hr>
              <a href="yo-decido.html">📁 Entregables</a>
            </div>
          </li>

          <li>
            <a href="lucha.html" class="navbar__panico">🆘 Necesito Ayuda</a>
          </li>
        </ul>
      </nav>
    `;

    // Swap logo claro→magenta al hacer scroll
    const logo = this.querySelector('#navbar-logo');
    const onScroll = () => {
      logo.src = window.scrollY > 80
        ? 'assets/logo-magenta.png'
        : 'assets/logo-claro.png';
    };
    // Remover listener previo si el componente se re-renderiza
    window.removeEventListener('scroll', this._onScroll);
    this._onScroll = onScroll;
    window.addEventListener('scroll', this._onScroll);
  }

  disconnectedCallback() {
    window.removeEventListener('scroll', this._onScroll);
  }
}

customElements.define('cat-navbar', CatNavbar);

/**
 * <cat-navbar active="inicio|analisis|educacion|cattleya">
 *
 * Navbar tipo pill flotante. Diseño extraído del equipo de diseño.
 * Incluye dropdowns en desktop y menú hamburger en mobile.
 *
 * Uso:
 *   <cat-navbar active="analisis"></cat-navbar>
 *
 * Valores para active:
 *   inicio | analisis | educacion | cattleya
 */
class CatNavbar extends HTMLElement {
  static get observedAttributes() { return ['active']; }

  connectedCallback()            { this._render(); this._bindEvents(); }
  attributeChangedCallback()     { this._render(); this._bindEvents(); }
  disconnectedCallback()         { this._cleanup(); }

  get active() { return this.getAttribute('active') || 'inicio'; }

  // Marca el link activo dentro de cada <li> con dropdown button
  _activeClass(key) {
    return this.active === key ? ' active' : '';
  }

  _render() {
    this.innerHTML = `
      <div class="nav-wrapper">

        <!-- ── PILL NAVBAR ── -->
        <nav class="cat-pill-navbar">

          <!-- Logo -->
          <a href="index.html" class="cat-logo">
            <svg class="cat-logo-icon" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="18" cy="18" rx="10" ry="14" fill="#F6871D" opacity="0.9"/>
              <ellipse cx="8"  cy="15" rx="7"  ry="4"  fill="#fff" opacity="0.65" transform="rotate(-20 8 15)"/>
              <ellipse cx="28" cy="15" rx="7"  ry="4"  fill="#fff" opacity="0.65" transform="rotate(20 28 15)"/>
              <ellipse cx="18" cy="25" rx="5"  ry="7"  fill="#fff" opacity="0.45"/>
              <circle  cx="18" cy="18" r="3.5"          fill="#8B2467"/>
            </svg>
            <span class="cat-logo-text">Cattleya</span>
          </a>

          <!-- Links desktop -->
          <div class="cat-nav-links" id="cat-desktop-links">

            <a href="index.html" class="cat-nav-link${this._activeClass('inicio')}">
              Inicio
            </a>

            <a href="analisis.html" class="cat-nav-link${this._activeClass('analisis')}">
              Power BI
            </a>

            <!-- Dropdown: Información y educación -->
            <div class="cat-dropdown" id="cat-dd1">
              <button class="cat-nav-btn${this._activeClass('educacion')}"
                      onclick="this.closest('.cat-dropdown').querySelector('.cat-drop-menu').classList.toggle('open'); this.classList.toggle('active')">
                Información y educación <span class="cat-caret">▾</span>
              </button>
              <div class="cat-drop-menu" id="cat-dd1-menu">
                <a href="contexto.html">📚 Metodología y Marco Legal</a>
                <a href="testimonios.html">📰 Noticias y blogs</a>
                <a href="lucha.html">🆘 Línea de ayuda</a>
              </div>
            </div>

            <a href="tendencias.html" class="cat-nav-link">
              Prototipo
            </a>

            <!-- Dropdown: ¿Qué es Cattleya? -->
            <div class="cat-dropdown" id="cat-dd2">
              <button class="cat-nav-btn${this._activeClass('cattleya')}"
                      onclick="this.closest('.cat-dropdown').querySelector('.cat-drop-menu').classList.toggle('open'); this.classList.toggle('active')">
                ¿Qué es Cattleya? <span class="cat-caret">▾</span>
              </button>
              <div class="cat-drop-menu" id="cat-dd2-menu">
                <a href="cattleya.html">🌸 El Acrónimo C·A·T·T·L·E·Y·A</a>
                <a href="equipo.html#vision">🎯 Visión / Misión</a>
                <a href="equipo.html">👥 Equipo</a>
                <hr class="cat-drop-hr">
                <a href="yo-decido.html">📁 Entregables</a>
              </div>
            </div>

          </div>

          <!-- Hamburger mobile -->
          <button class="cat-hamburger" id="cat-hamburger" aria-label="Menú">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </nav>

        <!-- ── MENÚ MOBILE ── -->
        <div class="cat-mobile-menu" id="cat-mobile-menu">
          <a href="index.html" class="cat-mob-item">Inicio</a>
          <a href="analisis.html" class="cat-mob-item">Power BI</a>

          <button class="cat-mob-item" onclick="
            const s = this.nextElementSibling;
            s.classList.toggle('open');
            this.classList.toggle('active');">
            Información y educación <span class="cat-mob-caret">▾</span>
          </button>
          <div class="cat-mob-sub">
            <a href="contexto.html">📚 Metodología y Marco Legal</a>
            <a href="testimonios.html">📰 Noticias y blogs</a>
            <a href="lucha.html">🆘 Línea de ayuda</a>
          </div>

          <a href="tendencias.html" class="cat-mob-item">Prototipo</a>

          <button class="cat-mob-item" onclick="
            const s = this.nextElementSibling;
            s.classList.toggle('open');
            this.classList.toggle('active');">
            ¿Qué es Cattleya? <span class="cat-mob-caret">▾</span>
          </button>
          <div class="cat-mob-sub">
            <a href="cattleya.html">🌸 El Acrónimo C·A·T·T·L·E·Y·A</a>
            <a href="equipo.html#vision">🎯 Visión / Misión</a>
            <a href="equipo.html">👥 Equipo</a>
            <a href="yo-decido.html">📁 Entregables</a>
          </div>
        </div>

      </div>
    `;
  }

  _bindEvents() {
    // Hamburger toggle
    const ham  = this.querySelector('#cat-hamburger');
    const menu = this.querySelector('#cat-mobile-menu');
    if (!ham || !menu) return;

    this._hamHandler = () => {
      ham.classList.toggle('open');
      menu.classList.toggle('open');
    };
    ham.addEventListener('click', this._hamHandler);

    // Cerrar dropdowns desktop al hacer clic fuera
    this._outsideHandler = (e) => {
      if (!this.contains(e.target)) {
        this.querySelectorAll('.cat-drop-menu.open').forEach(m => m.classList.remove('open'));
        this.querySelectorAll('.cat-nav-btn.active').forEach(b => b.classList.remove('active'));
      }
    };
    document.addEventListener('click', this._outsideHandler);
  }

  _cleanup() {
    document.removeEventListener('click', this._outsideHandler);
  }
}

customElements.define('cat-navbar', CatNavbar);

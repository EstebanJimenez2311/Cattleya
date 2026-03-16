/**
 * <cat-stat-card number="182K" label="casos registrados" variant="light|dark" animate>
 *
 * Atributos:
 *   number  — valor a mostrar (ej: "182K", "78%", "1 de cada 3")
 *   label   — descripción de la cifra
 *   variant — "light" (fondo blanco, texto magenta) | "dark" (fondo magenta, texto blanco)
 *             Por defecto: "light"
 *   animate — si está presente, anima el número con data-target y data-suffix
 *   target  — número final para la animación (ej: "182000")
 *   suffix  — sufijo para la animación (ej: "%", "K")
 *   color   — color del número (opcional, ej: "var(--naranja)")
 *
 * Uso básico:
 *   <cat-stat-card number="182K" label="casos registrados"></cat-stat-card>
 *
 * Con animación:
 *   <cat-stat-card animate target="78" suffix="%" label="víctimas son mujeres"></cat-stat-card>
 *
 * Variante oscura:
 *   <cat-stat-card variant="dark" number="60%" label="no denunciados"></cat-stat-card>
 */
class CatStatCard extends HTMLElement {
  connectedCallback() { this._render(); }

  _render() {
    const number  = this.getAttribute('number')  || '';
    const label   = this.getAttribute('label')   || '';
    const variant = this.getAttribute('variant') || 'light';
    const animate = this.hasAttribute('animate');
    const target  = this.getAttribute('target')  || '';
    const suffix  = this.getAttribute('suffix')  || '';
    const color   = this.getAttribute('color')   || '';

    const colorStyle = color ? `style="color:${color}"` : '';

    const numContent = animate
      ? `<span class="cat-counter" data-target="${target}" data-suffix="${suffix}">${target}${suffix}</span>`
      : number;

    this.innerHTML = `
      <div class="stat-card ${variant === 'dark' ? 'stat-card--dark' : ''}">
        <div class="stat-card__number" ${colorStyle}>${numContent}</div>
        <div class="stat-card__label">${label}</div>
      </div>
    `;

    // Animar si corresponde
    if (animate && target) {
      const el = this.querySelector('.cat-counter');
      this._observeAndAnimate(el, parseFloat(target), suffix);
    }
  }

  _observeAndAnimate(el, target, suffix) {
    const fmt = n => target >= 1000
      ? Math.floor(n).toLocaleString('es-CO')
      : Math.floor(n);

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          let t0 = null;
          const step = ts => {
            if (!t0) t0 = ts;
            const p = Math.min((ts - t0) / 2200, 1);
            const e = 1 - Math.pow(1 - p, 4);
            el.textContent = fmt(e * target) + suffix;
            if (p < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    observer.observe(el);
  }
}

customElements.define('cat-stat-card', CatStatCard);

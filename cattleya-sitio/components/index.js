/**
 * components/index.js — Importa y registra todos los Web Components
 *
 * Uso en cada página HTML:
 *   <script src="components/index.js"></script>
 *
 * Cada componente se auto-registra con customElements.define()
 * No es necesario hacer nada más — simplemente usa los tags en el HTML.
 */

const BASE = document.currentScript
  ? document.currentScript.src.replace('index.js', '')
  : 'components/';

const components = [
  'cat-navbar',
  'cat-footer',
  'cat-page-hero',
  'cat-stat-card',
  'cat-card',
  'cat-surface',
  'cat-chart',
  'cat-cta-banner',
  'cat-section-header',
  'cat-help-btn',
  'cat-chatbot-btn'
];

components.forEach(name => {
  const src = `${BASE}${name}.js`;
  const alreadyLoaded = Array.from(document.scripts).some(script => script.src === src);
  if (alreadyLoaded) return;

  const script = document.createElement('script');
  script.src = src;
  document.head.appendChild(script);
});

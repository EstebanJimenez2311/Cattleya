/**
 * <cat-chart chart-id="miGrafico" title="Título" description="Descripción" height="320">
 *
 * Este componente crea el contenedor visual de un gráfico.
 * Los datos y la inicialización de Chart.js se manejan desde data/charts.js
 *
 * Atributos:
 *   chart-id    — ID único del canvas (debe coincidir con el registro en charts.js)
 *   title       — título del gráfico
 *   description — descripción/pregunta que responde el gráfico
 *   height      — altura del canvas en px (default: 320)
 *
 * Uso:
 *   <cat-chart
 *     chart-id="chart-evolucion"
 *     title="Evolución anual de casos"
 *     description="¿Aumentaron o disminuyeron los casos?">
 *   </cat-chart>
 *
 * Luego en data/charts.js registrar:
 *   CHARTS['chart-evolucion'] = { type: 'line', data: {...}, options: {...} }
 */
class CatChart extends HTMLElement {
  connectedCallback() { this._render(); }

  _render() {
    const chartId   = this.getAttribute('chart-id')    || `chart-${Math.random().toString(36).slice(2,7)}`;
    const title     = this.getAttribute('title')       || '';
    const desc      = this.getAttribute('description') || '';
    const height    = this.getAttribute('height')      || '320';

    this.innerHTML = `
      <div class="chart-container">
        ${title ? `<h3>${title}</h3>` : ''}
        ${desc  ? `<p style="font-size:0.82rem;color:#666;margin-bottom:16px;">${desc}</p>` : ''}
        <div class="chart-canvas-wrap" style="height:${height}px;">
          <canvas id="${chartId}"></canvas>
        </div>
      </div>
    `;

    // Esperar a que Chart.js y charts.js estén cargados
    this._initChart(chartId);
  }

  _initChart(chartId) {
    const tryInit = () => {
      if (typeof Chart === 'undefined' || typeof window.CHARTS === 'undefined') {
        setTimeout(tryInit, 50);
        return;
      }
      const config = window.CHARTS[chartId];
      if (!config) {
        console.warn(`[cat-chart] No se encontró configuración para: ${chartId}`);
        return;
      }
      const canvas = this.querySelector(`#${chartId}`);
      if (!canvas) return;
      new Chart(canvas.getContext('2d'), config);
    };
    tryInit();
  }
}

customElements.define('cat-chart', CatChart);

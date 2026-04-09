/**
 * <cat-chart chart-id="mi-grafico" title="Titulo" description="Descripcion" height="320">
 *
 * Contenedor visual para un grafico de Chart.js.
 * La configuracion se toma desde window.CHARTS[chart-id].
 */
class CatChart extends HTMLElement {
  connectedCallback() {
    this._render();
  }

  disconnectedCallback() {
    this._destroyChart();
  }

  _destroyChart() {
    if (this._chart) {
      this._chart.destroy();
      this._chart = null;
    }
  }

  _render() {
    const chartId = this.getAttribute('chart-id') || `chart-${Math.random().toString(36).slice(2, 7)}`;
    const title = this.getAttribute('title') || '';
    const description = this.getAttribute('description') || '';
    const height = this.getAttribute('height') || '320';

    this._destroyChart();

    this.innerHTML = `
      <div class="chart-container">
        ${title ? `<h3>${title}</h3>` : ''}
        ${description ? `<p style="font-size:0.84rem;color:#6b5561;margin-bottom:16px;line-height:1.6;">${description}</p>` : ''}
        <div class="chart-canvas-wrap" style="height:${height}px;">
          <canvas id="${chartId}" aria-label="${title || chartId}" role="img"></canvas>
        </div>
      </div>
    `;

    this._initChart(chartId);
  }

  _cloneConfig(config) {
    if (typeof structuredClone === 'function') {
      return structuredClone(config);
    }
    return JSON.parse(JSON.stringify(config));
  }

  _initChart(chartId) {
    const maxAttempts = 120;
    let attempts = 0;

    const tryInit = () => {
      if (!this.isConnected) return;

      if (typeof Chart === 'undefined' || typeof window.CHARTS === 'undefined') {
        attempts += 1;
        if (attempts < maxAttempts) setTimeout(tryInit, 50);
        return;
      }

      const config = window.CHARTS[chartId];
      if (!config) {
        attempts += 1;
        if (attempts < maxAttempts) setTimeout(tryInit, 100);
        return;
      }

      const canvas = this.querySelector(`#${chartId}`);
      if (!canvas) return;

      this._destroyChart();
      this._chart = new Chart(canvas.getContext('2d'), this._cloneConfig(config));
    };

    tryInit();
  }
}

customElements.define('cat-chart', CatChart);

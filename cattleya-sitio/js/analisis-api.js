(function () {
  function resolveApiBaseUrl() {
    const runtimeConfig = window.CATTLEYA_CONFIG || {};
    const configuredBase = String(runtimeConfig.API_BASE_URL || '').trim().replace(/\/+$/, '');
    const hostname = window.location.hostname;
    const isLocalhost =
      hostname === '127.0.0.1' ||
      hostname === 'localhost' ||
      window.location.protocol === 'file:';

    if (isLocalhost) {
      return 'http://127.0.0.1:8000';
    }

    return configuredBase;
  }

  const apiBaseUrl = resolveApiBaseUrl();

  function buildUrl(path) {
    return `${apiBaseUrl.replace(/\/$/, '')}${path}`;
  }

  function rerender(el) {
    if (el && typeof el._render === 'function') el._render();
  }

  function normalizeText(value) {
    if (value === null || value === undefined || value === '') return 'N/D';
    return String(value).trim();
  }

  function ensureChartDefaults() {
    if (typeof Chart === 'undefined' || window.__cattleyaAnalisisDefaultsApplied) return;

    Chart.defaults.color = '#6B5561';
    Chart.defaults.font.family = "'DM Sans', sans-serif";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.boxWidth = 10;
    Chart.defaults.plugins.legend.labels.boxHeight = 10;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(61, 35, 48, 0.94)';
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.cornerRadius = 12;
    Chart.defaults.plugins.tooltip.titleColor = '#FFFFFF';
    Chart.defaults.plugins.tooltip.bodyColor = '#FDEEE9';
    Chart.defaults.animation.duration = 500;

    window.__cattleyaAnalisisDefaultsApplied = true;
  }

  function hideElement(el) {
    if (!el) return;
    el.style.display = 'none';
  }

  function updateStatCards(stats) {
    const cards = Array.from(document.querySelectorAll('[data-analisis-stat]'));

    cards.forEach((card, index) => {
      const stat = Array.isArray(stats) ? stats[index] : null;
      if (!stat) {
        hideElement(card);
        return;
      }

      card.style.display = '';
      card.setAttribute('number', normalizeText(stat.number));
      card.setAttribute('label', normalizeText(stat.label));
      rerender(card);
    });
  }

  function updateHighlights(highlights) {
    const cards = Array.from(document.querySelectorAll('[data-analisis-highlight]'));

    cards.forEach((card, index) => {
      const item = Array.isArray(highlights) ? highlights[index] : null;
      if (!item) {
        hideElement(card);
        return;
      }

      card.style.display = '';
      card.setAttribute('icon', `[${index + 1}]`);
      card.setAttribute('title', normalizeText(item.titulo || item.title || `Hallazgo ${index + 1}`));
      card.setAttribute('text', normalizeText(item.descripcion || item.texto || item.description || ''));
      rerender(card);
    });

    const visibleHighlights = (highlights || []).length;
    const hallazgosSection = document.querySelector('[data-analisis-highlight="0"]')?.closest('.section--bg');
    if (hallazgosSection && !visibleHighlights) {
      hideElement(hallazgosSection);
    }
  }

  function updateMetadataCards(cards) {
    const host = document.querySelector('[data-analisis-meta-list]');
    if (!host) return;

    if (!Array.isArray(cards) || !cards.length) {
      host.innerHTML = '';
      return;
    }

    host.innerHTML = '';

    cards.forEach((item) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'analisis-meta__item';

      const label = document.createElement('span');
      label.className = 'analisis-meta__label';
      label.textContent = normalizeText(item.label);

      const value = document.createElement('p');
      value.className = 'analisis-meta__value';
      value.textContent = normalizeText(item.value);

      wrapper.appendChild(label);
      wrapper.appendChild(value);
      host.appendChild(wrapper);
    });
  }

  function resolveSectionValue(sections, ...keys) {
    for (const key of keys) {
      if (sections && sections[key]) return sections[key];
    }
    return '';
  }

  function updateTextSections(payload) {
    const sections = payload.sections || {};

    const hero = document.querySelector('[data-analisis-hero]');
    const heroSubtitle = resolveSectionValue(sections, 'heroSubtitle', 'hero_subtitle');
    if (hero && heroSubtitle) {
      hero.setAttribute('subtitle', heroSubtitle);
      rerender(hero);
    }

    const statsHeader = document.querySelector('[data-analisis-stats-header]');
    const statsSubtitle = resolveSectionValue(sections, 'statsSubtitle', 'stats_subtitle');
    if (statsHeader && statsSubtitle) {
      statsHeader.setAttribute('subtitle', statsSubtitle);
      rerender(statsHeader);
    }

    const intro = document.querySelector('[data-analisis-intro]');
    const introSubtitle = resolveSectionValue(sections, 'introSubtitle', 'intro_subtitle');
    if (intro && introSubtitle) {
      intro.setAttribute('subtitle', introSubtitle);
      rerender(intro);
    }

    const source = document.querySelector('[data-analisis-source]');
    const sourceSummary = resolveSectionValue(sections, 'sourceSummary', 'source_summary');
    if (source && sourceSummary) {
      source.textContent = sourceSummary;
    }

    const method = document.querySelector('[data-analisis-method]');
    const methodNote = resolveSectionValue(sections, 'methodNote', 'method_note');
    if (method) {
      if (methodNote) {
        method.innerHTML = '';
        const strong = document.createElement('strong');
        strong.textContent = 'Como leer este tablero:';
        method.appendChild(strong);
        method.appendChild(document.createTextNode(` ${methodNote}`));
      } else {
        hideElement(method);
      }
    }
  }

  function applyChartMeta(chartEl, chartConfig, fallbackTitle) {
    const title = chartConfig && chartConfig.meta && chartConfig.meta.title ? chartConfig.meta.title : (fallbackTitle || 'Visualización');
    const description = chartConfig && chartConfig.meta && chartConfig.meta.description ? chartConfig.meta.description : '';

    chartEl.setAttribute('title', title);
    chartEl.setAttribute('description', description);
    rerender(chartEl);
  }

  function mapChartsToSlots(charts) {
    const chartEntries = Object.entries(charts || {});
    const slots = Array.from(document.querySelectorAll('cat-chart'));

    slots.forEach((chartEl, index) => {
      const entry = chartEntries[index];
      const oldId = chartEl.getAttribute('chart-id');

      if (!entry) {
        hideElement(chartEl.closest('.analysis-grid') || chartEl);
        return;
      }

      const chartId = entry[0];
      const chartConfig = entry[1];

      chartEl.style.display = '';
      chartEl.setAttribute('chart-id', chartId);
      applyChartMeta(chartEl, chartConfig, oldId);
    });

    return Object.fromEntries(chartEntries);
  }

  function updateCharts(charts) {
    ensureChartDefaults();
    window.CHARTS = mapChartsToSlots(charts || {});

    document.querySelectorAll('cat-chart').forEach((chartEl) => {
      const chartId = chartEl.getAttribute('chart-id');
      const config = window.CHARTS[chartId];
      if (!config) return;
      rerender(chartEl);
    });
  }

  function injectChartNotes(notes) {
    document.querySelectorAll('[data-analisis-note]').forEach((note) => note.remove());

    const chartEntries = Object.entries(window.CHARTS || {});
    const chartElements = Array.from(document.querySelectorAll('cat-chart')).filter((el) => el.style.display !== 'none');

    chartElements.forEach((chartEl, index) => {
      const entry = chartEntries[index];
      const chartId = entry ? entry[0] : null;
      const text = chartId && notes ? notes[chartId] : null;
      if (!chartId || !text) return;

      const host = chartEl.parentElement;
      if (!host) return;

      const note = document.createElement('p');
      note.className = 'analisis-note';
      note.setAttribute('data-analisis-note', chartId);
      note.textContent = text;
      host.appendChild(note);
    });
  }

  async function fetchJson(path) {
    const response = await fetch(buildUrl(path));
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} en ${path}`);
    }
    return response.json();
  }

  function applyPayload(payload) {
    updateStatCards(payload.stats || []);
    updateMetadataCards(payload.metadata_cards || payload.metadataCards || []);
    updateHighlights(payload.highlights || []);
    updateTextSections(payload);
    updateCharts(payload.charts || {});
    injectChartNotes(payload.chart_notes || payload.chartNotes || {});
  }

  async function loadAnalysisDashboard() {
    if (!apiBaseUrl) return;

    try {
      const payload = await fetchJson('/api/analisis/dashboard/');
      applyPayload(payload || {});
    } catch (error) {
      console.warn('[analisis-api] No se pudo cargar el análisis desde la base de datos.', error);

      const source = document.querySelector('[data-analisis-source]');
      if (source) {
        source.textContent = 'No fue posible leer el JSON cargado en la base de datos desde /api/analisis/dashboard/.';
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadAnalysisDashboard);
  } else {
    loadAnalysisDashboard();
  }
})();

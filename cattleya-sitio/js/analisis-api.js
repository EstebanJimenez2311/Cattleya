(function () {
  const apiBaseUrl = (window.CATTLEYA_CONFIG && window.CATTLEYA_CONFIG.API_BASE_URL) || '';
  const numberFormatter = new Intl.NumberFormat('es-CO');
  const percentFormatter = new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  });
  const monthFormatter = new Intl.DateTimeFormat('es-CO', {
    month: 'short',
    year: 'numeric',
  });

  const PALETTE = {
    magenta: '#9D2D6A',
    magentaDark: '#822157',
    orange: '#F28C28',
    orangeDark: '#D4700A',
    rose: '#C44D8E',
    cream: '#FDEEE9',
    plum: '#5A2443',
    ink: '#3D2330',
    muted: '#6B5561',
    grid: 'rgba(157, 45, 106, 0.10)',
    magentaSoft: 'rgba(157, 45, 106, 0.14)',
    orangeSoft: 'rgba(242, 140, 40, 0.18)',
    creamLine: 'rgba(253, 238, 233, 0.95)',
  };

  const TYPE_META = {
    feminicidio: { label: 'Feminicidio', color: PALETTE.magenta },
    sexual: { label: 'Violencia sexual', color: PALETTE.orange },
    fisica: { label: 'Violencia fisica', color: PALETTE.magentaDark },
    psicologica: { label: 'Violencia psicologica', color: PALETTE.rose },
    economica: { label: 'Violencia economica', color: PALETTE.orangeDark },
    patrimonial: { label: 'Violencia patrimonial', color: PALETTE.plum },
  };

  const AMBITO_META = {
    familiar: 'Familiar',
    pareja: 'Pareja',
    comunitario: 'Comunitario',
    institucional: 'Institucional',
    otro: 'Otro',
  };

  function buildUrl(path) {
    return `${apiBaseUrl.replace(/\/$/, '')}${path}`;
  }

  function rerender(el) {
    if (el && typeof el._render === 'function') el._render();
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function repairMojibake(value) {
    if (typeof value !== 'string' || !/Ã|Â/.test(value)) return value;

    try {
      const bytes = Uint8Array.from(Array.from(value, (char) => char.charCodeAt(0) & 0xff));
      return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    } catch (error) {
      return value;
    }
  }

  function normalizeText(value) {
    if (value === null || value === undefined || value === '') return 'N/D';

    const repaired = repairMojibake(String(value).trim());
    if (/^no especificada$/i.test(repaired)) return 'Sin ciudad especificada';
    return repaired;
  }

  function formatNumber(value) {
    const number = Number(value || 0);
    return numberFormatter.format(number);
  }

  function formatPercent(value, digits) {
    const number = Number(value || 0);
    if (typeof digits === 'number') {
      return `${number.toFixed(digits).replace('.', ',')}%`;
    }
    return `${percentFormatter.format(number)}%`;
  }

  function formatMonthLabel(value) {
    if (!value) return 'Sin fecha';
    const date = new Date(`${value}-01T00:00:00`);
    if (Number.isNaN(date.getTime())) return value;
    return normalizeText(monthFormatter.format(date)).replace('.', '');
  }

  function sortDescending(items) {
    return [...items].sort((left, right) => right.value - left.value);
  }

  function ensureChartDefaults() {
    if (typeof Chart === 'undefined' || window.__cattleyaAnalisisDefaultsApplied) return;

    Chart.defaults.color = PALETTE.muted;
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

  function baseScales(overrides) {
    return Object.assign(
      {
        x: {
          grid: { color: PALETTE.grid, drawBorder: false },
          ticks: { color: PALETTE.muted },
          border: { display: false },
        },
        y: {
          grid: { color: PALETTE.grid, drawBorder: false },
          ticks: { color: PALETTE.muted },
          border: { display: false },
          beginAtZero: true,
        },
      },
      overrides || {}
    );
  }

  function buildHorizontalBarChart(items, datasetLabel, tooltipLabel, chartOptions) {
    const resolvedOptions = chartOptions || {};

    return {
      type: 'bar',
      data: {
        labels: items.map((item) => item.label),
        datasets: [{
          label: datasetLabel,
          data: items.map((item) => item.value),
          backgroundColor: items.map((item) => item.color),
          borderRadius: 999,
          borderSkipped: false,
          maxBarThickness: 24,
        }],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label(context) {
                return tooltipLabel(context, items[context.dataIndex]);
              },
            },
          },
        },
        scales: baseScales({
          x: {
            grid: { color: PALETTE.grid, drawBorder: false },
            ticks: {
              color: PALETTE.muted,
              callback(value) {
                if (typeof resolvedOptions.tickFormatter === 'function') {
                  return resolvedOptions.tickFormatter(value);
                }
                return formatNumber(value);
              },
            },
            border: { display: false },
            beginAtZero: true,
            suggestedMax: resolvedOptions.suggestedMax,
          },
          y: {
            grid: { display: false, drawBorder: false },
            ticks: { color: PALETTE.ink },
            border: { display: false },
          },
        }),
      },
    };
  }

  function buildVolumeChart(labels, totals, verified) {
    return {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Noticias totales',
            data: totals,
            borderColor: PALETTE.magenta,
            backgroundColor: PALETTE.magentaSoft,
            pointBackgroundColor: PALETTE.magenta,
            pointBorderColor: '#FFFFFF',
            pointBorderWidth: 2,
            pointRadius: 5,
            borderWidth: 3,
            fill: true,
            tension: 0.32,
          },
          {
            label: 'Noticias verificadas',
            data: verified,
            borderColor: PALETTE.orange,
            backgroundColor: PALETTE.orangeSoft,
            pointBackgroundColor: PALETTE.orange,
            pointBorderColor: '#FFFFFF',
            pointBorderWidth: 2,
            pointRadius: 4,
            borderWidth: 2,
            borderDash: [6, 6],
            fill: false,
            tension: 0.25,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label(context) {
                return `${context.dataset.label}: ${formatNumber(context.raw)}`;
              },
            },
          },
        },
        scales: baseScales({
          y: {
            grid: { color: PALETTE.grid, drawBorder: false },
            ticks: {
              color: PALETTE.muted,
              precision: 0,
              callback(value) {
                return formatNumber(value);
              },
            },
            border: { display: false },
            beginAtZero: true,
          },
          x: {
            grid: { display: false, drawBorder: false },
            ticks: { color: PALETTE.muted },
            border: { display: false },
          },
        }),
      },
    };
  }

  function buildStackedCompositionChart(labels, series) {
    return {
      type: 'bar',
      data: {
        labels,
        datasets: series.map((item) => ({
          label: item.label,
          data: item.data,
          backgroundColor: item.color,
          borderRadius: 12,
          borderSkipped: false,
          maxBarThickness: 40,
        })),
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label(context) {
                return `${context.dataset.label}: ${formatNumber(context.raw)}`;
              },
            },
          },
        },
        scales: baseScales({
          x: {
            stacked: true,
            grid: { display: false, drawBorder: false },
            ticks: { color: PALETTE.muted },
            border: { display: false },
          },
          y: {
            stacked: true,
            grid: { color: PALETTE.grid, drawBorder: false },
            ticks: {
              color: PALETTE.muted,
              precision: 0,
              callback(value) {
                return formatNumber(value);
              },
            },
            border: { display: false },
            beginAtZero: true,
          },
        }),
      },
    };
  }

  function buildCoverageChart(verifiedCount, unverifiedCount, totalCount) {
    return {
      type: 'bar',
      data: {
        labels: ['Cobertura del conjunto'],
        datasets: [
          {
            label: 'Verificadas',
            data: [verifiedCount],
            backgroundColor: PALETTE.orange,
            borderRadius: 999,
            borderSkipped: false,
            barPercentage: 0.55,
            categoryPercentage: 0.9,
          },
          {
            label: 'Sin verificar',
            data: [unverifiedCount],
            backgroundColor: PALETTE.magentaSoft,
            borderColor: PALETTE.magenta,
            borderWidth: 1.5,
            borderRadius: 999,
            borderSkipped: false,
            barPercentage: 0.55,
            categoryPercentage: 0.9,
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label(context) {
                const share = totalCount ? (Number(context.raw) / totalCount) * 100 : 0;
                return `${context.dataset.label}: ${formatNumber(context.raw)} (${formatPercent(share)})`;
              },
            },
          },
        },
        scales: baseScales({
          x: {
            stacked: true,
            grid: { color: PALETTE.grid, drawBorder: false },
            ticks: {
              color: PALETTE.muted,
              precision: 0,
              callback(value) {
                return formatNumber(value);
              },
            },
            border: { display: false },
            suggestedMax: totalCount,
          },
          y: {
            stacked: true,
            grid: { display: false, drawBorder: false },
            ticks: { color: PALETTE.ink },
            border: { display: false },
          },
        }),
      },
    };
  }

  function updateStatCards(stats) {
    document.querySelectorAll('[data-analisis-stat]').forEach((card) => {
      const index = Number(card.getAttribute('data-analisis-stat'));
      const stat = stats[index];
      if (!stat) return;
      card.setAttribute('number', stat.number || 'N/D');
      card.setAttribute('label', stat.label || '');
      rerender(card);
    });
  }

  function updateHighlights(highlights) {
    document.querySelectorAll('[data-analisis-highlight]').forEach((card) => {
      const index = Number(card.getAttribute('data-analisis-highlight'));
      const item = highlights[index];
      if (!item) return;
      card.setAttribute('icon', `[${index + 1}]`);
      card.setAttribute('title', item.titulo || `Hallazgo ${index + 1}`);
      card.setAttribute('text', item.descripcion || '');
      rerender(card);
    });
  }

  function updateMetadataCards(cards) {
    const host = document.querySelector('[data-analisis-meta-list]');
    if (!host || !Array.isArray(cards) || !cards.length) return;

    host.innerHTML = cards.map((item) => `
      <div class="analisis-meta__item">
        <span class="analisis-meta__label">${escapeHtml(item.label || '')}</span>
        <p class="analisis-meta__value">${escapeHtml(item.value || 'N/D')}</p>
      </div>
    `).join('');
  }

  function updateTextSections(model) {
    const hero = document.querySelector('[data-analisis-hero]');
    if (hero && model.sections.heroSubtitle) {
      hero.setAttribute('subtitle', model.sections.heroSubtitle);
      rerender(hero);
    }

    const statsHeader = document.querySelector('[data-analisis-stats-header]');
    if (statsHeader && model.sections.statsSubtitle) {
      statsHeader.setAttribute('subtitle', model.sections.statsSubtitle);
      rerender(statsHeader);
    }

    const intro = document.querySelector('[data-analisis-intro]');
    if (intro && model.sections.introSubtitle) {
      intro.setAttribute('subtitle', model.sections.introSubtitle);
      rerender(intro);
    }

    const source = document.querySelector('[data-analisis-source]');
    if (source && model.sections.sourceSummary) {
      source.textContent = model.sections.sourceSummary;
    }

    const method = document.querySelector('[data-analisis-method]');
    if (method && model.sections.methodNote) {
      method.innerHTML = `<strong>Como leer este tablero:</strong> ${escapeHtml(model.sections.methodNote)}`;
    }
  }

  function updateCharts(charts) {
    ensureChartDefaults();
    window.CHARTS = Object.assign({}, charts || {});

    document.querySelectorAll('cat-chart').forEach((chartEl) => {
      const chartId = chartEl.getAttribute('chart-id');
      const config = window.CHARTS[chartId];
      if (!config) return;
      rerender(chartEl);
    });
  }

  function injectChartNotes(notes) {
    Object.entries(notes || {}).forEach(([chartId, text]) => {
      const chart = document.querySelector(`cat-chart[chart-id="${chartId}"]`);
      if (!chart || !text) return;

      const host = chart.parentElement;
      if (!host) return;

      let note = host.querySelector(`[data-analisis-note="${chartId}"]`);
      if (!note) {
        note = document.createElement('p');
        note.className = 'analisis-note';
        note.setAttribute('data-analisis-note', chartId);
        host.appendChild(note);
      }
      note.textContent = text;
    });
  }

  async function fetchJson(path, optional) {
    const response = await fetch(buildUrl(path));
    if (!response.ok) {
      if (optional && response.status === 404) return null;
      throw new Error(`HTTP ${response.status} en ${path}`);
    }
    return response.json();
  }

  function normalizeTypeKey(value) {
    const text = normalizeText(value)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');

    if (text.includes('feminicidio')) return 'feminicidio';
    if (text.includes('sexual')) return 'sexual';
    if (text.includes('fisica')) return 'fisica';
    if (text.includes('psicologica')) return 'psicologica';
    if (text.includes('economica')) return 'economica';
    if (text.includes('patrimonial')) return 'patrimonial';

    return text.replace(/\s+/g, '_');
  }

  function buildTypeItems(rawTypes, rawTypesList, totalNoticias) {
    const itemsFromEndpoint = Array.isArray(rawTypesList)
      ? rawTypesList
        .map((item) => {
          const key = normalizeTypeKey(item.tipo);
          const meta = TYPE_META[key] || {};

          return {
            key,
            label: meta.label || normalizeText(item.tipo),
            value: Number(item.cantidad || 0),
            color: meta.color || PALETTE.magenta,
            percentage: Number(item.porcentaje || 0),
          };
        })
        .filter((item) => item.value > 0)
      : [];

    if (itemsFromEndpoint.length) {
      return sortDescending(itemsFromEndpoint);
    }

    return sortDescending(
      Object.entries(rawTypes || {})
        .map(([key, value]) => ({
          key,
          label: (TYPE_META[key] && TYPE_META[key].label) || normalizeText(key),
          value: Number(value || 0),
          color: (TYPE_META[key] && TYPE_META[key].color) || PALETTE.magenta,
          percentage: totalNoticias ? (Number(value || 0) / totalNoticias) * 100 : 0,
        }))
        .filter((item) => item.value > 0)
    );
  }

  function buildAmbitoItems(rawAmbitos, totalNoticias) {
    const items = Object.entries(rawAmbitos || {})
      .map(([key, value]) => ({
        key,
        label: AMBITO_META[key] || normalizeText(key),
        value: Number(value || 0),
        color: key === 'pareja' ? PALETTE.orange : PALETTE.magenta,
        percentage: totalNoticias ? (Number(value || 0) / totalNoticias) * 100 : 0,
      }))
      .filter((item) => item.value > 0);

    return sortDescending(items).map((item, index) => ({
      ...item,
      color: [PALETTE.magenta, PALETTE.orange, PALETTE.magentaDark, PALETTE.rose, PALETTE.orangeDark][index % 5],
    }));
  }

  function buildCityItems(rawCities, totalNoticias) {
    return (rawCities || []).map((item, index) => ({
      label: normalizeText(item.ciudad),
      value: Number(item.cantidad || 0),
      color: index === 0 ? PALETTE.magenta : index === 1 ? PALETTE.orange : PALETTE.magentaSoft,
      percentage: totalNoticias ? (Number(item.cantidad || 0) / totalNoticias) * 100 : 0,
    }));
  }

  function buildTrendRows(rawTrend) {
    return (rawTrend || [])
      .map((item) => ({
        monthKey: item.mes,
        label: formatMonthLabel(item.mes),
        total: Number(item.total || 0),
        verified: Number(item.verificadas || 0),
        tipos: item.tipos_violencia || {},
      }))
      .sort((left, right) => String(left.monthKey).localeCompare(String(right.monthKey)));
  }

  function buildMonthlyTypeSeries(typeItems, trendRows) {
    return typeItems.map((type) => ({
      key: type.key,
      label: type.label,
      color: type.color,
      data: trendRows.map((row) => Number((row.tipos && row.tipos[type.key]) || 0)),
    }));
  }

  function deriveInsights(totalNoticias, totalVerificadas, typeItems, cityItems, trendRows) {
    const highlights = [];
    const dominantType = typeItems[0];
    const topCity = cityItems[0];
    const unspecifiedCity = cityItems.find((item) => /sin ciudad especificada/i.test(item.label));
    const previousMonth = trendRows.length > 1 ? trendRows[trendRows.length - 2] : null;
    const latestMonth = trendRows[trendRows.length - 1];

    if (dominantType) {
      highlights.push({
        titulo: 'La carga se concentra en un tipo principal',
        descripcion: `${dominantType.label} concentra ${formatPercent(dominantType.percentage)} del conjunto clasificado por el backend.`,
      });
    }

    if (unspecifiedCity && unspecifiedCity.value > 0) {
      highlights.push({
        titulo: 'La georreferenciacion sigue siendo incompleta',
        descripcion: `${formatNumber(unspecifiedCity.value)} de ${formatNumber(totalNoticias)} noticias aparecen sin ciudad especificada, asi que la lectura territorial debe hacerse con cautela.`,
      });
    } else if (topCity) {
      highlights.push({
        titulo: 'Existe una concentracion territorial visible',
        descripcion: `${topCity.label} aporta ${formatPercent(topCity.percentage)} del total de noticias disponibles en el backend.`,
      });
    }

    if (totalVerificadas === 0) {
      highlights.push({
        titulo: 'La capa de verificacion es el principal vacio',
        descripcion: 'Ninguna noticia del conjunto actual aparece marcada como verificada, lo que limita la comparacion entre volumen y calidad del registro.',
      });
    } else if (latestMonth && previousMonth) {
      const delta = latestMonth.total - previousMonth.total;
      const direction = delta >= 0 ? 'subio' : 'bajo';
      highlights.push({
        titulo: 'La serie temporal ya muestra variacion entre meses',
        descripcion: `Entre ${previousMonth.label} y ${latestMonth.label}, el volumen ${direction} ${formatNumber(Math.abs(delta))} noticias.`,
      });
    }

    return highlights.slice(0, 3);
  }

  function buildModel(resumen, tendencia, tipos, dashboard) {
    const totalNoticias = Number(resumen.total_noticias || 0);
    const totalVerificadas = Number(resumen.total_verificadas || 0);
    const typeItems = buildTypeItems(resumen.tipos_violencia, tipos, totalNoticias);
    const cityItems = buildCityItems(resumen.ciudades_top, totalNoticias);
    const ambitoItems = buildAmbitoItems(resumen.ambitos, totalNoticias);
    const trendRows = buildTrendRows(tendencia);
    const latestMonth = trendRows[trendRows.length - 1];
    const firstMonth = trendRows[0];
    const periodLabel = firstMonth && latestMonth ? `${firstMonth.label} - ${latestMonth.label}` : 'Sin serie temporal';
    const monthlyTypeSeries = buildMonthlyTypeSeries(typeItems, trendRows);
    const totalUnverified = Math.max(totalNoticias - totalVerificadas, 0);
    const verificationShare = totalNoticias ? (totalVerificadas / totalNoticias) * 100 : 0;
    const dominantType = typeItems[0];
    const topCity = cityItems[0];
    const dashboardName = dashboard && dashboard.nombre ? normalizeText(dashboard.nombre) : 'API de estadisticas';

    const charts = {
      'chart-panorama-tipos': buildHorizontalBarChart(
        typeItems,
        'Noticias clasificadas',
        function (_context, item) {
          return `${item.label}: ${formatNumber(item.value)} (${formatPercent(item.percentage)})`;
        }
      ),
      'chart-series-volumen': buildVolumeChart(
        trendRows.map((row) => row.label),
        trendRows.map((row) => row.total),
        trendRows.map((row) => row.verified)
      ),
      'chart-series-composicion': buildStackedCompositionChart(
        trendRows.map((row) => row.label),
        monthlyTypeSeries
      ),
      'chart-ciudades': buildHorizontalBarChart(
        cityItems,
        'Noticias',
        function (_context, item) {
          return `${item.label}: ${formatNumber(item.value)} (${formatPercent(item.percentage)})`;
        }
      ),
      'chart-ambitos': buildHorizontalBarChart(
        ambitoItems,
        'Noticias',
        function (_context, item) {
          return `${item.label}: ${formatNumber(item.value)} (${formatPercent(item.percentage)})`;
        }
      ),
      'chart-cobertura-tipos': buildHorizontalBarChart(
        typeItems.map((item) => ({
          ...item,
          value: Number(item.percentage.toFixed(2)),
        })),
        'Participacion',
        function (_context, item) {
          return `${item.label}: ${formatPercent(item.percentage)}`;
        },
        {
          tickFormatter(value) {
            return `${value}%`;
          },
          suggestedMax: 100,
        }
      ),
      'chart-calidad-registro': buildCoverageChart(totalVerificadas, totalUnverified, totalNoticias),
    };

    const methodNote = [
      'los graficos muestran conteos de noticias clasificadas por el backend, no tasas poblacionales.',
      'Las categorias sin incidencia se omiten para mejorar la legibilidad.',
      'Las noticias sin ciudad y las noticias no verificadas se mantienen visibles porque son parte de la calidad real del registro.',
    ].join(' ');

    return {
      stats: [
        { number: formatNumber(totalNoticias), label: 'Noticias clasificadas' },
        { number: formatNumber(typeItems.length), label: 'Tipos con incidencia' },
        { number: formatNumber(cityItems.length), label: 'Ciudades con registro' },
        { number: periodLabel, label: 'Periodo observado' },
      ],
      metadataCards: [
        { label: 'Fuente de datos', value: dashboardName },
        { label: 'Endpoint principal', value: '/api/estadisticas' },
        { label: 'Tipo dominante', value: dominantType ? dominantType.label : 'N/D' },
        { label: 'Ultimo mes disponible', value: latestMonth ? latestMonth.label : 'N/D' },
      ],
      highlights: deriveInsights(totalNoticias, totalVerificadas, typeItems, cityItems, trendRows),
      charts,
      chartNotes: {
        'chart-series-volumen': trendRows.length < 3
          ? 'La serie aun es corta, asi que conviene leerla como pulso operativo y no como tendencia consolidada.'
          : 'La comparacion entre volumen y verificacion ayuda a separar actividad de calidad editorial.',
        'chart-ciudades': cityItems.some((item) => /sin ciudad especificada/i.test(item.label))
          ? 'Las noticias sin ciudad explicita no se eliminan: se muestran como categoria para evidenciar el vacio de georreferenciacion.'
          : 'El ranking refleja solo ciudades con ubicacion informada en el backend.',
        'chart-calidad-registro': totalVerificadas === 0
          ? 'Hoy no hay noticias verificadas, por lo que este grafico funciona como alerta de calidad del registro.'
          : 'La barra resume que parte del conjunto ya paso por verificacion.',
      },
      sections: {
        heroSubtitle: `Este tablero se alimenta en vivo desde ${buildUrl('/api/estadisticas/resumen/')} y convierte el backend en comparaciones legibles, consistentes y accionables.`,
        statsSubtitle: 'Los indicadores se calculan con los endpoints de resumen, tendencia y tipos del backend activo, sin depender de graficos hardcodeados.',
        introSubtitle: 'Empezamos por el ranking de tipos porque la comparacion ordenada es la forma mas estable de leer magnitudes cuando el conjunto cambia.',
        sourceSummary: `Fuente activa: ${dashboardName}. Total analizado: ${formatNumber(totalNoticias)} noticias. Ultimo corte visible: ${latestMonth ? latestMonth.label : 'N/D'}.`,
        methodNote,
      },
    };
  }

  function applyModel(model) {
    updateStatCards(model.stats);
    updateMetadataCards(model.metadataCards);
    updateHighlights(model.highlights);
    updateTextSections(model);
    updateCharts(model.charts);
    injectChartNotes(model.chartNotes);
  }

  async function loadAnalysisDashboard() {
    if (!apiBaseUrl) return;

    try {
      const [resumen, tendencia, tipos, dashboard] = await Promise.all([
        fetchJson('/api/estadisticas/resumen/'),
        fetchJson('/api/estadisticas/tendencia/'),
        fetchJson('/api/estadisticas/tipos/'),
        fetchJson('/api/analisis/dashboard/', true),
      ]);

      const model = buildModel(resumen || {}, tendencia || [], tipos || [], dashboard || null);
      applyModel(model);
    } catch (error) {
      console.warn('[analisis-api] No se pudo construir el tablero analitico.', error);

      const source = document.querySelector('[data-analisis-source]');
      if (source) {
        source.textContent = 'No fue posible leer los endpoints del backend. Revisa la URL del API o el estado del servicio antes de interpretar esta pagina.';
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadAnalysisDashboard);
  } else {
    loadAnalysisDashboard();
  }
})();

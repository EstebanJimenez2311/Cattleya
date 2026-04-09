(function () {
  const RSS_FEEDS = [
    // El Espectador
    'https://www.elespectador.com/rss/judicial.xml',
    'https://www.elespectador.com/rss/colombia.xml',
    // El Heraldo (Barranquilla)
    'https://www.elheraldo.co/rss/feed.xml',
    // Caracol Radio
    'https://caracol.com.co/rss/colombia.xml',
    // RCN Radio
    'https://www.rcnradio.com/feed',
    // El Tiempo
    'https://www.eltiempo.com/rss/colombia.xml'
  ];

  // En desarrollo local usa allorigins como fallback.
  // En producción (Netlify) usa la función serverless propia.
  const IS_NETLIFY = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
  const RSS_PROXY = IS_NETLIFY
    ? '/.netlify/functions/noticias-proxy?url='
    : 'https://api.allorigins.win/get?url=';
  const CACHE_KEY = 'cattleya_rss_cache_v4';
  const CACHE_DURATION = 30 * 60 * 1000;
  const MAX_RENDER = 6;
  const DEBUG = true;
  const PRIORIDAD_RIESGO = { Alto: 3, Medio: 2, Bajo: 1 };
  const LOCATION_TERMS = [
    'colombia',
    'barranquilla',
    'atlantico',
    'bogota',
    'medellin',
    'cali',
    'soledad'
  ];
  const FEMALE_TERMS = [
    'mujer',
    'mujeres',
    'violencia contra la mujer',
    'violencia de genero',
    'violencias basadas en genero',
    'victima',
    'victimas',
    'femenicida',
    'su pareja',
    'ella'
  ];
  const VIOLENCE_TERMS = [
    'feminicidio',
    'violacion',
    'abuso',
    'agresion',
    'violencia',
    'violencia sexual',
    'violencia intrafamiliar',
    'amenaza',
    'golpe',
    'golpiza',
    'hostigamiento',
    'maltrato',
    'asesin'
  ];
  const EXCLUDED_TERMS = [
    'licor',
    'ruido',
    'movilidad',
    'microtrafico',
    'orden publico',
    'recompensa',
    'capturados',
    'hurto',
    'extorsion',
    'sicariato',
    'semana santa'
  ];
  const INTERNAL_FALLBACK_NEWS = [
    {
      title: 'Violencias contra las mujeres no ceden en 2025: 119 feminicidios y miles de casos de abuso',
      description: 'Un balance nacional advierte que persisten altos niveles de feminicidios, violencia intrafamiliar, delitos sexuales y otras violencias basadas en genero contra las mujeres en Colombia.',
      url: 'https://caracol.com.co/2026/01/30/violencias-contra-las-mujeres-no-ceden-en-2025-119-feminicidios-y-miles-de-casos-de-abuso/',
      source: 'Caracol Radio',
      publishedAt: '2026-01-30T11:51:00-05:00',
      content: 'Colombia registra altos niveles de feminicidios, violencia intrafamiliar y delitos sexuales contra las mujeres, con especial impacto en varias regiones del pais.'
    },
    {
      title: 'Violencia contra la mujer en 2025: 111 casos de feminicidios y 13.832 delitos sexuales',
      description: 'La Defensoria del Pueblo advirtio que la violencia contra las mujeres sigue siendo una problematica persistente en distintas regiones de Colombia.',
      url: 'https://www.elespectador.com/judicial/violencia-contra-la-mujer-en-2025-111-casos-de-feminicidios-y-13832-delitos-sexuales/',
      source: 'El Espectador',
      publishedAt: '2025-12-26T19:58:00-05:00',
      content: 'Entre enero y noviembre de 2025 se registraron feminicidios y delitos sexuales contra mujeres en Colombia, segun el mas reciente balance de la Defensoria.'
    },
    {
      title: 'Bogota reporta 10 feminicidios y 17 mil casos de violencia intrafamiliar contra mujeres en 2025',
      description: 'Entre enero y junio de 2025, Bogota registro feminicidios, aumento de homicidios de mujeres y miles de casos de violencia intrafamiliar y delitos sexuales.',
      url: 'https://caracol.com.co/2025/08/21/bogota-reporta-10-feminicidios-y-17-mil-casos-de-violencia-intrafamiliar-contra-mujeres-en-2025/',
      source: 'Caracol Radio',
      publishedAt: '2025-08-21T17:55:00-05:00',
      content: 'Bogota registro feminicidios, violencia intrafamiliar contra mujeres y delitos sexuales, con concentracion en varias localidades de la ciudad.'
    },
    {
      title: 'Cali aumento los homicidios y las denuncias por violencia sexual contra las mujeres',
      description: 'Un informe del Observatorio para la Equidad de las Mujeres advierte sobre el aumento de homicidios de mujeres y denuncias por violencia sexual en Cali.',
      url: 'https://caracol.com.co/2026/03/06/cali-aumento-los-homicidios-y-las-denuncias-por-violencia-sexual-contra-las-mujeres/',
      source: 'Caracol Radio',
      publishedAt: '2026-03-06T09:31:00-05:00',
      content: 'En Cali aumentaron los homicidios de mujeres y las denuncias por violencia sexual, segun datos del Observatorio para la Equidad de las Mujeres.'
    },
    {
      title: 'Feminicidio en Anori: un hombre asesino a una mujer ante la mirada indolente de varias personas',
      description: 'En Anori, Antioquia, un caso de feminicidio genero rechazo de las autoridades y reavivo las alertas sobre la violencia contra las mujeres en la region.',
      url: 'https://caracol.com.co/2025/12/30/feminicidio-en-anori-un-hombre-asesino-a-una-mujer-ante-la-mirada-indolente-de-varias-personas/',
      source: 'Caracol Radio',
      publishedAt: '2025-12-30T17:06:00-05:00',
      content: 'Medellin y Antioquia reportan un feminicidio en Anori, donde una mujer fue asesinada por un hombre en via publica.'
    },
    {
      title: 'Gobierno lanza Salvia en Barranquilla en medio de grave crisis de violencia contra la mujer',
      description: 'La plataforma Salvia fue presentada en Barranquilla para activar rutas de denuncia, seguimiento y acompanamiento frente a violencias basadas en genero.',
      url: 'https://caracol.com.co/2025/11/25/gobierno-lanza-salvia-en-barranquilla-en-medio-de-grave-crisis-de-violencia-contra-la-mujer/',
      source: 'Caracol Radio',
      publishedAt: '2025-11-25T14:35:00-05:00',
      content: 'Barranquilla y el Atlantico enfrentan una crisis de violencia contra la mujer, mientras el Gobierno impulsa rutas de atencion y prevencion.'
    }
  ];

  function normalizeText(text) {
    return String(text || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  }

  function limpiarHTML(html) {
    const div = document.createElement('div');
    div.innerHTML = String(html || '');
    return (div.textContent || div.innerText || '').replace(/\s+/g, ' ').trim();
  }

  function escapeHtml(text) {
    return String(text || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function formatDate(dateString) {
    try {
      if (!dateString) {
        return 'Fecha no disponible';
      }

      return new Intl.DateTimeFormat('es-CO', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      }).format(new Date(dateString));
    } catch (error) {
      return 'Fecha no disponible';
    }
  }

  function detectarFuente(url) {
    const normalizedUrl = normalizeText(url);

    if (normalizedUrl.includes('eltiempo')) {
      return 'El Tiempo';
    }

    if (normalizedUrl.includes('elespectador')) {
      return 'El Espectador';
    }

    return 'Medio colombiano';
  }

  function getSourceLabel(source, url) {
    if (typeof source === 'string' && source.trim()) {
      return source.trim();
    }

    if (source && typeof source === 'object' && typeof source.name === 'string' && source.name.trim()) {
      return source.name.trim();
    }

    return detectarFuente(url);
  }

  function getCache() {
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      if (!raw) {
        return null;
      }

      const parsed = JSON.parse(raw);
      const expired = Date.now() - parsed.timestamp > CACHE_DURATION;
      const valid = Array.isArray(parsed.data) && parsed.data.length > 0;

      if (expired || !valid) {
        localStorage.removeItem(CACHE_KEY);
        return null;
      }

      return parsed.data;
    } catch (error) {
      return null;
    }
  }

  function setCache(data) {
    if (!Array.isArray(data) || !data.length) {
      return;
    }

    try {
      localStorage.setItem(
        CACHE_KEY,
        JSON.stringify({
          timestamp: Date.now(),
          data: data
        })
      );
    } catch (error) {
      if (DEBUG) {
        console.warn('[CattleyaNoticias] no se pudo guardar cache', error);
      }
    }
  }

  async function fetchRSSFeeds() {
    const requests = RSS_FEEDS.map(async (url) => {
      try {
        const response = await fetch(RSS_PROXY + encodeURIComponent(url));

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        // La función serverless propia devuelve XML directo.
        // allorigins (local) devuelve { contents: "..." }.
        let xmlText;
        const contentType = response.headers.get('content-type') || '';
        if (contentType.includes('xml')) {
          xmlText = await response.text();
        } else {
          const data = await response.json();
          xmlText = data.contents || '';
        }
        const parser = new DOMParser();
        const xml = parser.parseFromString(xmlText, 'text/xml');
        const items = Array.from(xml.querySelectorAll('item')).map((item) => ({
          title: item.querySelector('title') ? item.querySelector('title').textContent || '' : '',
          description: limpiarHTML(item.querySelector('description') ? item.querySelector('description').textContent || '' : ''),
          url: item.querySelector('link') ? item.querySelector('link').textContent || '#' : '#',
          publishedAt: item.querySelector('pubDate') ? item.querySelector('pubDate').textContent || '' : '',
          content: limpiarHTML(item.querySelector('content\\:encoded') ? item.querySelector('content\\:encoded').textContent || '' : '')
        }));

        if (DEBUG) {
          console.log('[CattleyaNoticias] feed cargado', { url: url, items: items.length });
        }

        return items;
      } catch (error) {
        console.warn('[CattleyaNoticias] fallo un feed RSS', { url: url, error: error.message });
        return [];
      }
    });

    const results = await Promise.all(requests);
    return results.flat();
  }

  function detectarCiudad(texto) {
    const normalized = normalizeText(texto);

    if (normalized.includes('barranquilla')) return 'Barranquilla';
    if (normalized.includes('soledad')) return 'Soledad';
    if (normalized.includes('atlantico')) return 'Atlantico';
    if (normalized.includes('bogota')) return 'Bogota';
    if (normalized.includes('medellin')) return 'Medellin';
    if (normalized.includes('cali')) return 'Cali';

    return 'No especificado';
  }

  function clasificarViolencia(texto) {
    const normalized = normalizeText(texto);

    if (normalized.includes('feminicidio')) return 'Feminicidio';
    if (normalized.includes('violacion') || normalized.includes('abuso sexual')) return 'Violencia sexual';
    if (normalized.includes('agresion') || normalized.includes('golpe') || normalized.includes('golpiza')) return 'Violencia fisica';
    if (normalized.includes('amenaza') || normalized.includes('hostigamiento')) return 'Violencia psicologica';
    if (normalized.includes('violencia intrafamiliar')) return 'Violencia intrafamiliar';

    return 'Otro';
  }

  function calcularRiesgo(texto) {
    const normalized = normalizeText(texto);

    if (normalized.includes('feminicidio')) return 'Alto';
    if (
      normalized.includes('grave') ||
      normalized.includes('brutal') ||
      normalized.includes('violacion') ||
      normalized.includes('abuso sexual')
    ) {
      return 'Medio';
    }

    return 'Bajo';
  }

  function includesAny(text, terms) {
    return terms.some((term) => text.includes(term));
  }

  function esNoticiaRelevante(item) {
    const text = normalizeText(`${item.title} ${item.description} ${item.content}`);
    const hasLocation = includesAny(text, LOCATION_TERMS);
    const hasFemaleReference = includesAny(text, FEMALE_TERMS);
    const hasViolenceReference = includesAny(text, VIOLENCE_TERMS);
    const hasExcludedContext = includesAny(text, EXCLUDED_TERMS);

    if (hasExcludedContext && !hasFemaleReference) {
      return false;
    }

    return hasLocation && hasFemaleReference && hasViolenceReference;
  }

  function enriquecer(item) {
    const text = `${item.title} ${item.description} ${item.content}`;

    return {
      title: item.title || 'Sin titulo disponible',
      description: item.description || 'No hay descripcion disponible para esta noticia.',
      url: item.url || '#',
      source: getSourceLabel(item.source, item.url),
      publishedAt: item.publishedAt || '',
      formattedDate: formatDate(item.publishedAt),
      ciudad: detectarCiudad(text),
      tipoViolencia: clasificarViolencia(text),
      nivelRiesgo: calcularRiesgo(text),
      isFallback: Boolean(item.isFallback)
    };
  }

  function sortNoticias(left, right) {
    const riskDiff = PRIORIDAD_RIESGO[right.nivelRiesgo] - PRIORIDAD_RIESGO[left.nivelRiesgo];

    if (riskDiff !== 0) {
      return riskDiff;
    }

    return new Date(right.publishedAt).getTime() - new Date(left.publishedAt).getTime();
  }

  function getFallbackNews() {
    const fallback = Array.isArray(window.CATTLEYA_FALLBACK_NEWS) && window.CATTLEYA_FALLBACK_NEWS.length
      ? window.CATTLEYA_FALLBACK_NEWS
      : INTERNAL_FALLBACK_NEWS;

    const normalizedFallback = fallback.map((item) => ({
      title: item.title,
      description: item.description,
      url: item.url,
      source: getSourceLabel(item.source, item.url),
      publishedAt: item.publishedAt,
      content: item.content || item.description,
      isFallback: true
    }));

    if (DEBUG) {
      console.log('[CattleyaNoticias] getFallbackNews', {
        total: normalizedFallback.length,
        items: normalizedFallback.map((item) => ({
          source: item.source,
          title: item.title,
          url: item.url
        }))
      });
    }

    return normalizedFallback;
  }

  function mergeWithFallback(noticias) {
    const current = Array.isArray(noticias) ? noticias.slice() : [];
    const knownUrls = new Set(current.map((item) => item.url));
    const fallback = getFallbackNews()
      .map(enriquecer)
      .filter((item) => !knownUrls.has(item.url));

    for (let index = 0; index < fallback.length && current.length < MAX_RENDER; index += 1) {
      current.push(fallback[index]);
    }

    const merged = current
      .sort(sortNoticias)
      .slice(0, MAX_RENDER);

    if (DEBUG) {
      console.log('[CattleyaNoticias] mergeWithFallback', {
        rssCount: Array.isArray(noticias) ? noticias.length : 0,
        mergedCount: merged.length,
        mergedItems: merged.map((item) => ({
          source: item.source,
          isFallback: item.isFallback,
          title: item.title
        }))
      });
    }

    return merged;
  }

  async function obtenerNoticias() {
    const cached = getCache();
    if (cached) {
      return cached;
    }

    const raw = await fetchRSSFeeds();

    if (DEBUG) {
      console.log('[CattleyaNoticias] raw RSS items', {
        total: raw.length,
        sample: raw.slice(0, 10).map((item) => ({
          title: item.title,
          url: item.url,
          publishedAt: item.publishedAt
        }))
      });
    }

    const noticias = raw
      .filter(esNoticiaRelevante)
      .map((item) => ({
        title: limpiarHTML(item.title),
        description: limpiarHTML(item.description),
        url: item.url,
        publishedAt: item.publishedAt,
        source: detectarFuente(item.url),
        content: limpiarHTML(item.content)
      }))
      .map(enriquecer);

    if (DEBUG) {
      console.log('[CattleyaNoticias] noticias RSS filtradas', {
        total: noticias.length,
        items: noticias.map((item) => ({
          source: item.source,
          title: item.title,
          riesgo: item.nivelRiesgo
        }))
      });
    }

    const processed = mergeWithFallback(noticias);
    setCache(processed);
    return processed;
  }

  function getRiskBadge(risk) {
    if (risk === 'Alto') {
      return { icon: '🔴', className: 'alto', label: 'Alto riesgo' };
    }

    if (risk === 'Medio') {
      return { icon: '🟠', className: 'medio', label: 'Riesgo medio' };
    }

    return { icon: '🟢', className: 'bajo', label: 'Riesgo bajo' };
  }

  function renderState(container, type, message) {
    container.innerHTML = `
      <div class="noticias-estado noticias-estado--${type}">
        <p>${escapeHtml(message)}</p>
      </div>
    `;
  }

  function buildSlide(item) {
    const badge = getRiskBadge(item.nivelRiesgo);

    return `
      <div class="carrusel-slide">
        <article class="noticia-item">
          <div class="noticia-item__top">
            <span class="noticia-item__fuente">${escapeHtml(item.source)}</span>
            <span class="noticia-item__fecha">${escapeHtml(item.formattedDate)}</span>
          </div>
          <h3 class="noticia-item__titulo">${escapeHtml(item.title)}</h3>
          <p class="noticia-item__descripcion">${escapeHtml(item.description)}</p>
          <div class="noticia-item__badges">
            <span class="noticia-badge noticia-badge--tipo">${escapeHtml(item.tipoViolencia)}</span>
            <span class="noticia-badge noticia-badge--riesgo noticia-badge--${badge.className}">
              ${badge.icon} ${escapeHtml(badge.label)}
            </span>
            <span class="noticia-badge noticia-badge--ciudad">${escapeHtml(item.ciudad)}</span>
          </div>
          <div class="noticia-item__footer">
            <span>Nivel detectado: ${escapeHtml(item.nivelRiesgo)}</span>
            <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">Leer noticia</a>
          </div>
        </article>
      </div>
    `;
  }

  function initSlider(container) {
    const track = container.querySelector('[data-carrusel-track]');
    const slides = Array.from(container.querySelectorAll('.carrusel-slide'));
    const dots = Array.from(container.querySelectorAll('.carrusel-dot'));
    const prevBtn = container.querySelector('[data-carrusel-prev]');
    const nextBtn = container.querySelector('[data-carrusel-next]');
    const wrapper = container.querySelector('.carrusel-wrapper');

    if (!track || slides.length <= 1) {
      if (prevBtn) prevBtn.disabled = true;
      if (nextBtn) nextBtn.disabled = true;
      return;
    }

    let current = 0;
    let autoPlay = null;

    if (DEBUG) {
      console.log('[CattleyaNoticias] initSlider', {
        slides: slides.length,
        dots: dots.length,
        hasTrack: Boolean(track),
        hasPrevBtn: Boolean(prevBtn),
        hasNextBtn: Boolean(nextBtn)
      });
    }

    function measureSlides() {
      if (!slides.length) {
        return;
      }

      track.style.width = `${slides.length * 100}%`;
      track.style.display = 'flex';

      slides.forEach((slide) => {
        slide.style.width = `${100 / slides.length}%`;
        slide.style.minWidth = `${100 / slides.length}%`;
        slide.style.flex = `0 0 ${100 / slides.length}%`;
        slide.style.boxSizing = 'border-box';
      });

      if (DEBUG) {
        console.log('[CattleyaNoticias] measureSlides', {
          trackWidth: track.getBoundingClientRect().width,
          wrapperWidth: wrapper ? wrapper.getBoundingClientRect().width : 0,
          firstSlideWidth: slides[0].getBoundingClientRect().width,
          firstSlideOffsetLeft: slides[0].offsetLeft
        });
      }
    }

    function goTo(index) {
      current = (index + slides.length) % slides.length;
      const offsetPercent = -(current * (100 / slides.length));
      track.style.transform = `translateX(${offsetPercent}%)`;

      if (DEBUG) {
        console.log('[CattleyaNoticias] goTo', {
          requestedIndex: index,
          current: current,
          offsetPercent: offsetPercent
        });
      }

      dots.forEach((dot, dotIndex) => {
        dot.classList.toggle('active', dotIndex === current);
      });
    }

    function stopAutoPlay() {
      if (autoPlay) {
        window.clearInterval(autoPlay);
        autoPlay = null;
      }
    }

    function startAutoPlay() {
      stopAutoPlay();
      autoPlay = window.setInterval(() => goTo(current + 1), 7000);
    }

    prevBtn.addEventListener('click', () => {
      if (DEBUG) {
        console.log('[CattleyaNoticias] click prev', { current: current });
      }
      goTo(current - 1);
      startAutoPlay();
    });

    nextBtn.addEventListener('click', () => {
      if (DEBUG) {
        console.log('[CattleyaNoticias] click next', { current: current });
      }
      goTo(current + 1);
      startAutoPlay();
    });

    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        if (DEBUG) {
          console.log('[CattleyaNoticias] click dot', { index: index, current: current });
        }
        goTo(index);
        startAutoPlay();
      });
    });

    if (wrapper) {
      wrapper.addEventListener('mouseenter', stopAutoPlay);
      wrapper.addEventListener('mouseleave', startAutoPlay);
    }

    measureSlides();
    goTo(0);
    startAutoPlay();
  }

  function renderNoticias(container, noticias) {
    const usesFallback = noticias.some((item) => item.isFallback);
    const slides = noticias.slice(0, MAX_RENDER).map(buildSlide).join('');
    const dots = noticias
      .slice(0, MAX_RENDER)
      .map((_, index) => `<button type="button" class="carrusel-dot ${index === 0 ? 'active' : ''}" aria-label="Ir a noticia ${index + 1}"></button>`)
      .join('');

    container.innerHTML = `
      ${usesFallback ? '<div class="noticias-disclaimer">Contenido complementado con casos documentados seleccionados por el equipo cuando los feeds RSS no entregan resultados utilizables.</div>' : ''}
      <div class="carrusel-wrapper">
        <div class="carrusel-track" data-carrusel-track>
          ${slides}
        </div>
      </div>
      <div class="carrusel-controls">
        <button type="button" class="carrusel-btn" data-carrusel-prev aria-label="Anterior">&larr;</button>
        <div class="carrusel-dots">${dots}</div>
        <button type="button" class="carrusel-btn" data-carrusel-next aria-label="Siguiente">&rarr;</button>
      </div>
    `;

    initSlider(container);
  }

  async function init() {
    const container = document.getElementById('testimonios-container');
    if (!container) {
      return;
    }

    renderState(container, 'loading', 'Cargando casos recientes de Colombia...');

    try {
      const noticias = await obtenerNoticias();

      if (!noticias.length) {
        renderState(container, 'empty', 'No hay casos recientes disponibles.');
        return;
      }

      renderNoticias(container, noticias);
    } catch (error) {
      const fallback = getFallbackNews()
        .map(enriquecer)
        .sort(sortNoticias)
        .slice(0, MAX_RENDER);

      if (fallback.length) {
        renderNoticias(container, fallback);
        return;
      }

      renderState(container, 'error', 'No se pudieron cargar las noticias.');
    }
  }

  window.CattleyaNoticias = {
    init: init,
    fetchRSSFeeds: fetchRSSFeeds,
    obtenerNoticias: obtenerNoticias,
    esNoticiaRelevante: esNoticiaRelevante,
    clasificarViolencia: clasificarViolencia,
    calcularRiesgo: calcularRiesgo,
    detectarCiudad: detectarCiudad
  };

  document.addEventListener('DOMContentLoaded', init);
})();

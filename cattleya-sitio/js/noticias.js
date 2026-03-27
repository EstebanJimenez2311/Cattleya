(function () {
  const MAX_RENDER = 6;
  const DEBUG = true;

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

  async function obtenerNoticias() {
    try {
      if (DEBUG) {
        console.log('[CattleyaNoticias] Fetching desde API Django...');
      }

      // Fetch directo a la API de Django
      const response = await fetch('http://127.0.0.1:8000/api/noticias/recientes/');

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      // Mapear datos del backend al formato esperado por el frontend
      const noticias = data.map(item => ({
        title: item.titulo,
        description: item.descripcion,
        url: item.url,
        source: item.fuente,
        publishedAt: item.fecha_publicacion,
        formattedDate: formatDate(item.fecha_publicacion),
        ciudad: item.ciudad,
        tipoViolencia: item.tipo_violencia,
        nivelRiesgo: item.nivel_riesgo,
        isFallback: false
      }));

      if (DEBUG) {
        console.log('[CattleyaNoticias] Datos obtenidos de API', {
          total: noticias.length,
          items: noticias.map(item => ({
            source: item.source,
            title: item.title.substring(0, 30) + '...',
            riesgo: item.nivelRiesgo
          }))
        });
      }

      return noticias;

    } catch (error) {
      console.error('[CattleyaNoticias] Error obteniendo noticias:', error);
      throw error; // Re-throw para que el caller maneje el error
    }
  }

  function getRiskBadge(risk) {
    if (risk === 'alto') {
      return { icon: '🔴', className: 'alto', label: 'Alto riesgo' };
    }

    if (risk === 'medio') {
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
    const slides = noticias.slice(0, MAX_RENDER).map(buildSlide).join('');
    const dots = noticias
      .slice(0, MAX_RENDER)
      .map((_, index) => `<button type="button" class="carrusel-dot ${index === 0 ? 'active' : ''}" aria-label="Ir a noticia ${index + 1}"></button>`)
      .join('');

    container.innerHTML = `
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
      renderState(container, 'error', 'Error al cargar las noticias. Verifica que el servidor backend esté ejecutándose.');
    }
  }

  window.CattleyaNoticias = {
    init: init,
    obtenerNoticias: obtenerNoticias
  };

  document.addEventListener('DOMContentLoaded', init);
})();

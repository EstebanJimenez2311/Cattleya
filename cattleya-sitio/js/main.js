// ============================================
//  CATTLEYA - JS Global
// ============================================

function initRevealAnimations() {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll(
      '.fade-up, .fade-up-slow, .fade-left, .fade-right, .section-title, .stat-card, .card, .acronimo__item, .chart-container, .entregable-card, .linea-card'
    ).forEach((el) => {
      el.classList.add('is-visible');
      el.style.opacity = '1';
      el.style.transform = 'none';
      el.dataset.revealBound = 'true';
    });
    return;
  }

  const revealTargets = document.querySelectorAll(
    '.fade-up, .fade-up-slow, .fade-left, .fade-right, .section-title, .stat-card, .card, .acronimo__item, .chart-container, .entregable-card, .linea-card'
  );

  if (!revealTargets.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;

      if (
        entry.target.classList.contains('fade-up') ||
        entry.target.classList.contains('fade-up-slow') ||
        entry.target.classList.contains('fade-left') ||
        entry.target.classList.contains('fade-right') ||
        entry.target.classList.contains('section-title')
      ) {
        entry.target.classList.add('is-visible');
      } else {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }

      if (entry.target.classList.contains('stat-card')) {
        entry.target.classList.add('is-visible');
      }

      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });

  function revealElement(el) {
    if (
      el.classList.contains('fade-up') ||
      el.classList.contains('fade-up-slow') ||
      el.classList.contains('fade-left') ||
      el.classList.contains('fade-right') ||
      el.classList.contains('section-title') ||
      el.classList.contains('stat-card')
    ) {
      el.classList.add('is-visible');
    } else {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }
  }

  revealTargets.forEach((el) => {
    if (el.dataset.revealBound === 'true') return;

    const usesClassAnimation =
      el.classList.contains('fade-up') ||
      el.classList.contains('fade-up-slow') ||
      el.classList.contains('fade-left') ||
      el.classList.contains('fade-right') ||
      el.classList.contains('section-title');

    if (!usesClassAnimation) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'opacity 0.65s ease, transform 0.65s ease';
    }

    el.dataset.revealBound = 'true';
    observer.observe(el);

    const rect = el.getBoundingClientRect();
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const alreadyVisible = rect.top < viewportHeight * 0.94 && rect.bottom > 0;
    if (alreadyVisible) {
      revealElement(el);
      observer.unobserve(el);
    }
  });
}

function initRevealStagger() {
  const groups = document.querySelectorAll('.cards-grid, .stats-inner, .analisis-stats, .analisis-meta, .analysis-grid');
  groups.forEach((group) => {
    Array.from(group.children).forEach((child, index) => {
      if (!child.style.getPropertyValue('--fd')) {
        child.style.setProperty('--fd', `${index * 0.07}s`);
      }
    });
  });
}

function initFactsCarousel() {
  const host = document.querySelector('[data-facts-carousel]');
  if (!host) return;

  const slides = Array.from(host.querySelectorAll('[data-fact-slide]'));
  const dotsHost = host.querySelector('[data-facts-dots]');
  const progress = host.querySelector('[data-facts-progress]');
  const prevBtn = host.querySelector('[data-facts-prev]');
  const nextBtn = host.querySelector('[data-facts-next]');

  if (!slides.length || !dotsHost || !prevBtn || !nextBtn) return;

  let current = 0;
  let intervalId = null;
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  dotsHost.innerHTML = slides
    .map((_, index) => `<button type="button" class="facts-carousel__dot${index === 0 ? ' active' : ''}" aria-label="Ir al dato ${index + 1}"></button>`)
    .join('');

  const dots = Array.from(dotsHost.querySelectorAll('.facts-carousel__dot'));

  function paint(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => {
      slide.classList.toggle('active', slideIndex === current);
    });
    dots.forEach((dot, dotIndex) => {
      dot.classList.toggle('active', dotIndex === current);
    });

    if (progress) {
      progress.style.transform = `scaleX(${(current + 1) / slides.length})`;
    }
  }

  function stop() {
    if (intervalId) {
      window.clearInterval(intervalId);
      intervalId = null;
    }
  }

  function start() {
    if (reducedMotion || slides.length <= 1) return;
    stop();
    intervalId = window.setInterval(() => paint(current + 1), 5200);
  }

  prevBtn.addEventListener('click', () => {
    paint(current - 1);
    start();
  });

  nextBtn.addEventListener('click', () => {
    paint(current + 1);
    start();
  });

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      paint(index);
      start();
    });
  });

  host.addEventListener('mouseenter', stop);
  host.addEventListener('mouseleave', start);
  host.addEventListener('focusin', stop);
  host.addEventListener('focusout', start);

  paint(0);
  start();
}

function initSupportQuotes() {
  const card = document.querySelector('[data-support-quote-card]');
  const textEl = document.querySelector('[data-support-quote-text]');
  const authorEl = document.querySelector('[data-support-quote-author]');
  const dotsHost = document.querySelector('[data-support-quote-dots]');

  if (!card || !textEl || !authorEl || !dotsHost) return;

  const quotes = [
    {
      text: 'La violencia no empieza cuando deja marcas visibles; empieza cuando alguien siente que ya no puede decidir en paz.',
      author: 'Mensaje de prevencion y cuidado'
    },
    {
      text: 'Escuchar a tiempo puede ser la diferencia entre una alarma ignorada y una red de apoyo que si responde.',
      author: 'Cuidado colectivo y acompanamiento'
    },
    {
      text: 'Nombrar el control, el miedo o la humillacion tambien es una forma de proteger a una mujer.',
      author: 'Prevencion desde el lenguaje'
    },
    {
      text: 'Ninguna mujer deberia sentirse obligada a demostrar dolor extremo para que su miedo sea tomado en serio.',
      author: 'Ruta de atencion con enfoque humano'
    }
  ];

  let current = 0;
  let timerId = null;
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  dotsHost.innerHTML = quotes
    .map((_, index) => `<button type="button" class="support-quote__dot${index === 0 ? ' active' : ''}" aria-label="Ver cita ${index + 1}"></button>`)
    .join('');

  const dots = Array.from(dotsHost.querySelectorAll('.support-quote__dot'));

  function paint(index) {
    current = (index + quotes.length) % quotes.length;
    const item = quotes[current];

    textEl.style.opacity = '0';
    textEl.style.transform = 'translateY(10px)';

    window.setTimeout(() => {
      textEl.textContent = item.text;
      authorEl.textContent = item.author;
      textEl.style.opacity = '1';
      textEl.style.transform = 'translateY(0)';
    }, reducedMotion ? 0 : 140);

    dots.forEach((dot, dotIndex) => {
      dot.classList.toggle('active', dotIndex === current);
    });
  }

  function stop() {
    if (timerId) {
      window.clearInterval(timerId);
      timerId = null;
    }
  }

  function start() {
    if (reducedMotion || quotes.length <= 1) return;
    stop();
    timerId = window.setInterval(() => paint(current + 1), 4600);
  }

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      paint(index);
      start();
    });
  });

  card.addEventListener('mouseenter', stop);
  card.addEventListener('mouseleave', start);
  card.addEventListener('focusin', stop);
  card.addEventListener('focusout', start);

  paint(0);
  start();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initRevealStagger();
    initRevealAnimations();
    initFactsCarousel();
    initSupportQuotes();
  });
} else {
  initRevealStagger();
  initRevealAnimations();
  initFactsCarousel();
  initSupportQuotes();
}

window.addEventListener('load', () => {
  initRevealStagger();
  initRevealAnimations();
  initFactsCarousel();
  initSupportQuotes();
});

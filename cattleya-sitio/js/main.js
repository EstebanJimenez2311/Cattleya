// ============================================
//  CATTLEYA - JS Global
// ============================================

// Reveal shared content blocks when they enter the viewport.
const revealTargets = document.querySelectorAll(
  '.fade-up, .fade-up-slow, .fade-left, .fade-right, .section-title, .stat-card, .card, .acronimo__item, .chart-container, .entregable-card, .linea-card'
);

if (revealTargets.length) {
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

  revealTargets.forEach((el) => {
    const usesClassAnimation =
      el.classList.contains('fade-up') ||
      el.classList.contains('fade-up-slow') ||
      el.classList.contains('fade-left') ||
      el.classList.contains('fade-right') ||
      el.classList.contains('section-title');

    if (!usesClassAnimation) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    }

    observer.observe(el);
  });
}

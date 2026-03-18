// ============================================
//  CATTLEYA - JS Global
// ============================================

// Reveal shared content blocks when they enter the viewport.
const revealTargets = document.querySelectorAll(
  '.stat-card, .card, .acronimo__item, .chart-container, .entregable-card, .linea-card'
);

if (revealTargets.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });

  revealTargets.forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

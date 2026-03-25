/* ── RIPPLE en el botón PBI ── */
const _btn    = document.getElementById('btnPbi');
const _ripple = document.getElementById('rdRippleEl');

if (_btn && _ripple) {
  _btn.addEventListener('click', function (e) {
    const r = _btn.getBoundingClientRect();
    _ripple.style.left = (e.clientX - r.left - 4) + 'px';
    _ripple.style.top  = (e.clientY - r.top  - 4) + 'px';
    _ripple.classList.remove('is-active');
    void _ripple.offsetWidth;
    _ripple.classList.add('is-active');
  });
}

/* ── CARGA LAZY del iframe ── */
function rdLoadPBI() {
  const frame   = document.getElementById('pbiFrame');
  const overlay = document.getElementById('pbiOverlay');

  if (!frame || !overlay) return;

  if (frame.src === 'about:blank') {
    frame.src = 'about:blank'; /* ← cambiar por la URL real de embed */
  }

  overlay.style.opacity    = '0';
  overlay.style.transition = 'opacity 0.35s ease';
  setTimeout(() => { overlay.style.display = 'none'; }, 370);
}

/* ── FADE-IN por scroll con IntersectionObserver ── */
const _obs = new IntersectionObserver(
  entries => entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('is-visible');
      _obs.unobserve(e.target);
    }
  }),
  { threshold: 0.15 }
);

document.querySelectorAll('.js-fade').forEach(el => _obs.observe(el));

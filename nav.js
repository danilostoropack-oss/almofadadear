(function () {
  'use strict';

  /* ──────────────────────────────────────────
     SCROLL BEHAVIOR  (hero-mode ↔ scrolled)
  ────────────────────────────────────────── */
  var nav = document.getElementById('nav');
  if (!nav) return;

  function onScroll() {
    if (window.scrollY > 60) {
      nav.classList.remove('hero-mode');
      nav.classList.add('scrolled');
    } else {
      nav.classList.add('hero-mode');
      nav.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ──────────────────────────────────────────
     DESKTOP DROPDOWNS
  ────────────────────────────────────────── */
  var items = nav.querySelectorAll('.nav-item.has-dropdown');

  function closeAll(except) {
    items.forEach(function (item) {
      if (item !== except) item.classList.remove('open');
    });
  }

  items.forEach(function (item) {
    var btn = item.querySelector('.nav-dropdown-toggle');
    if (!btn) return;

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var wasOpen = item.classList.contains('open');
      closeAll(null);
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* Close when clicking outside */
  document.addEventListener('click', function () { closeAll(null); });
  nav.addEventListener('click', function (e) { e.stopPropagation(); });

  /* Close on Escape */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll(null);
  });

  /* ──────────────────────────────────────────
     MOBILE HAMBURGER
  ────────────────────────────────────────── */
  var hamburger = document.getElementById('navHamburger');
  var mobileNav = document.getElementById('navMobile');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = hamburger.classList.toggle('open');
      mobileNav.classList.toggle('open', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    /* Close mobile nav on outside click */
    document.addEventListener('click', function (e) {
      if (mobileNav.classList.contains('open') && !nav.contains(e.target)) {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  /* ──────────────────────────────────────────
     MOBILE ACCORDION
  ────────────────────────────────────────── */
  var mobToggles = nav.querySelectorAll('.nav-mob-toggle');
  mobToggles.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wasOpen = btn.classList.contains('open');
      /* Close all siblings */
      mobToggles.forEach(function (b) { b.classList.remove('open'); });
      if (!wasOpen) btn.classList.add('open');
    });
  });

})();

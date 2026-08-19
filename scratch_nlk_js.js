// ── Close cart + mobile nav ─────────────────────────────────────
  function closeDrawers() {
    var mob = document.getElementById('mobile-nav');
    if (mob) mob.classList.remove('active');
    if (typeof nlkResetPanels === 'function') nlkResetPanels();
    var lux = document.getElementById('lux-cart-drawer');
    if (lux) lux.classList.remove('is-open');
    var overlay = document.getElementById('header-overlay');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
    var drawer = document.querySelector('wi-cartdrawer');
    if (drawer && typeof drawer.closeCartdrawer === 'function') drawer.closeCartdrawer();
  }

  function toggleMenu() {
    if (typeof nlkResetPanels === 'function') nlkResetPanels();
    document.getElementById('mobile-nav').classList.add('active');
    document.getElementById('header-overlay').classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function openCart() {
    var drawer = document.querySelector('wi-cartdrawer');
    if (drawer && typeof drawer.openCart === 'function') {
      drawer.openCart({ refresh: true, mode: 'refresh' });
      return;
    }
    if (typeof updateCartDrawer === 'function') updateCartDrawer();
    var lux = document.getElementById('lux-cart-drawer');
    if (lux) lux.classList.add('is-open');
    var overlay = document.getElementById('header-overlay');
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  window.openCart = openCart;
  window.closeDrawers = closeDrawers;

  // ── Mobile menu: Dawn-style slide panels (not accordion) ────────
  var nlkStack = ['nlk-panel-root'];

  function nlkUpdateHead() {
    var back = document.getElementById('nlk-back');
    var title = document.getElementById('nlk-head-title');
    var logo = document.getElementById('nlk-head-logo');
    var atRoot = nlkStack.length <= 1;

    if (back) back.classList.toggle('is-visible', !atRoot);
    if (logo) logo.classList.toggle('is-hidden', !atRoot);
    if (title) {
      title.classList.toggle('is-visible', !atRoot);
      if (atRoot) {
        title.textContent = '';
      } else {
        var current = document.getElementById(nlkStack[nlkStack.length - 1]);
        title.textContent = current ? (current.getAttribute('data-nlk-title') || '') : '';
      }
    }
  }

  function nlkResetPanels() {
    nlkStack = ['nlk-panel-root'];
    var viewport = document.getElementById('nlk-viewport');
    if (viewport) viewport.classList.remove('is-sub-open');
    document.querySelectorAll('#mobile-nav .nlk-submenu').forEach(function(panel) {
      panel.classList.remove('is-open', 'is-behind');
      panel.scrollTop = 0;
    });
    var rootScroll = document.querySelector('#mobile-nav .nlk-root-scroll');
    if (rootScroll) rootScroll.scrollTop = 0;
    nlkUpdateHead();
  }

  function nlkOpenPanel(panelId) {
    var next = document.getElementById(panelId);
    if (!next || !next.classList.contains('nlk-submenu')) return;

    var viewport = document.getElementById('nlk-viewport');
    var currentId = nlkStack[nlkStack.length - 1];

    if (currentId !== 'nlk-panel-root') {
      var current = document.getElementById(currentId);
      if (current) {
        current.classList.remove('is-open');
        current.classList.add('is-behind');
      }
    }

    next.classList.add('is-open');
    next.classList.remove('is-behind');
    next.scrollTop = 0;
    nlkStack.push(panelId);

    if (viewport) viewport.classList.add('is-sub-open');
    nlkUpdateHead();
  }

  function nlkGoBack() {
    if (nlkStack.length <= 1) return;

    var viewport = document.getElementById('nlk-viewport');
    var closingId = nlkStack.pop();
    var closing = document.getElementById(closingId);
    if (closing) closing.classList.remove('is-open', 'is-behind');

    var prevId = nlkStack[nlkStack.length - 1];

    if (prevId === 'nlk-panel-root') {
      if (viewport) viewport.classList.remove('is-sub-open');
      document.querySelectorAll('#mobile-nav .nlk-submenu.is-behind').forEach(function(p) {
        p.classList.remove('is-behind');
      });
    } else {
      var prev = document.getElementById(prevId);
      if (prev) {
        prev.classList.add('is-open');
        prev.classList.remove('is-behind');
      }
    }

    nlkUpdateHead();
  }

  window.nlkResetPanels = nlkResetPanels;
  window.nlkOpenPanel = nlkOpenPanel;
  window.nlkGoBack = nlkGoBack;

  document.addEventListener('click', function(e) {
    var trigger = e.target.closest('[data-nlk-open]');
    if (trigger && trigger.closest('#mobile-nav')) {
      e.preventDefault();
      nlkOpenPanel(trigger.getAttribute('data-nlk-open'));
      return;
    }
    if (e.target.closest('#mobile-nav [data-nlk-back]') || e.target.closest('#nlk-back')) {
      e.preventDefault();
      nlkGoBack();
      return;
    }
    var leaf = e.target.closest('#mobile-nav a.nlk-row:not(.nlk-row--trigger)');
    if (leaf) closeDrawers();
  });

  document.addEventListener('DOMContentLoaded', function() {
    nlkResetPanels();
  });

  document.addEventListener('keydown', function(e) {
    if (e.key !== 'Escape') return;
    var mob = document.getElementById('mobile-nav');
    if (!mob || !mob.classList.contains('active')) return;
    if (nlkStack.length > 1) {
      e.preventDefault();
      nlkGoBack();
      return;
    }
    closeDrawers();
  });

  // ── Touch/iPad mega menu: first tap opens, second navigates ──────
  (function() {
    document.querySelectorAll('.nav-li').forEach(function(li) {
      var link = li.querySelector('.nav-a');
      var mega = li.querySelector('.mega-menu');
      if (!link || !mega) return;
      link.addEventListener('touchstart', function(e) {
        if (!li.classList.contains('mega-touch-open')) {
          e.preventDefault();
          document.querySelectorAll('.nav-li.mega-touch-open').forEach(function(other) {
            other.classList.remove('mega-touch-open');
          });
          li.classList.add('mega-touch-open');
        }
      }, { passive: false });
    });
    document.addEventListener('touchstart', function(e) {
      if (!e.target.closest('.nav-li')) {
        document.querySelectorAll('.nav-li.mega-touch-open').forEach(function(li) {
          li.classList.remove('mega-touch-open');
        });
      }
    }, { passive: true });
  })();

try{
  /* Im Squarespace-Editor (iframe) eigene Navigation/Cursor aus, native Navigation an */
  try { if (window.top !== window.self) document.documentElement.classList.add('ts-in-editor'); } catch (e) { document.documentElement.classList.add('ts-in-editor'); }
  /* Sicherung: Läuft das Skript im Footer nicht (Fehler, Blocker), blendet sich nichts ein –
     dann nach 3 s alles zeigen, damit z. B. Impressum und Datenschutz nie leer bleiben */
  setTimeout(function () { if (!window.TS_READY) document.documentElement.classList.add('ts-noreveal'); }, 3000);
  /* Überschriften erst hereingleiten lassen, wenn ihre Schrift da ist (höchstens 1,2 s) – sonst hüpfen sie beim Schrift-Tausch */
  (function () {
    var d = document.documentElement;
    if (!document.fonts || !document.fonts.load) return;
    d.classList.add('ts-font-wait');
    var tsw = ['/twitch-startseite', '/live', '/mitspielen', '/charakter', '/bestenliste', '/statistiken'].indexOf(location.pathname.replace(/\/$/, '')) > -1;
    var done = function () { requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.remove('ts-font-wait'); }); }); };
    var t = setTimeout(done, 1200);
    document.fonts.load(tsw ? '700 1em Cinzel' : '800 1em Syne').then(function () { clearTimeout(t); done(); }, done);
  })();
  /* Seitenübergang: kam der Besuch über einen internen Link, startet die Seite hinter dem Vorhang */
  try { if (sessionStorage.getItem('ts-trans') === '1') { sessionStorage.removeItem('ts-trans'); if (!document.documentElement.classList.contains('ts-in-editor') && !matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('ts-trans-in'); } } catch (e) {}

}catch(e){console.warn("vorschau",e)}
;
try{
(() => {
  const html = document.documentElement;
  const body = document.body;
  const inEditor = html.classList.contains('ts-in-editor');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const fx = finePointer && !reduceMotion && !inEditor;

  /* ---------- Sprunglink + Navigation an den Anfang der Seite ----------
     Der Footer-Code landet am Ende von <body>. Für Tastatur und Screenreader gehören
     „Zum Inhalt springen“, Header und Menü aber nach vorn – optisch ändert sich nichts (alles fest positioniert). */
  const skip = document.querySelector('[data-ts-skip]');
  const main = document.querySelector('main, #page, #sections');
  if (main && !main.id) main.id = 'ts-main';
  if (skip && main) {
    skip.setAttribute('href', '#' + main.id);
    skip.addEventListener('click', e => { e.preventDefault(); main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); main.scrollIntoView(); });
  }
  if (!inEditor) [document.getElementById('ts-menu'), document.querySelector('[data-ts-header]'), skip].forEach(el => { if (el) body.prepend(el); });

  /* ---------- Hallo an alle, die in den Code schauen ---------- */
  try {
    console.log('%cMoin! 👋', 'font: 800 28px Syne, system-ui, sans-serif; color: #6ee7b7;');
    console.log('%cEcht sein statt perfekt wirken – auch im Quelltext.\nDu schaust gern unter die Haube? Schreib mir: moin@trutzstaehler.de', 'font: 13px/1.6 Inter, system-ui, sans-serif; color: #9aaba3;');
  } catch (e) {}

  /* ---------- Intro-Animation (nach einem Seitenübergang erst, wenn der Vorhang aufgeht) ---------- */
  const introDelay = html.classList.contains('ts-trans-in') ? 420 : 0;
  requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(() => body.classList.add('ts-loaded'), introDelay)));

  /* ---------- Bilder: Squarespace-CDN liefert passend zur Anzeigegröße (spart am Handy viel Datenvolumen) ---------- */
  document.querySelectorAll('img[loading="lazy"][src*="squarespace-cdn.com"]:not([srcset])').forEach(img => {
    const m = img.getAttribute('src').match(/^(.*?)\?format=(\d+)w$/);
    const w = img.getBoundingClientRect().width;
    if (!m || !w || img.currentSrc) return;
    const max = Math.max(+m[2], 750);
    const set = [300, 500, 750, 1000, 1500, 2500].filter(x => x <= max);
    img.sizes = `${Math.ceil(w)}px`;
    img.srcset = set.map(x => `${m[1]}?format=${x}w ${x}w`).join(', ');
  });

  /* ---------- Seitenübergang: Vorhang fährt hoch, dann wechselt die Seite ---------- */
  if (!inEditor && !reduceMotion) {
    document.addEventListener('click', e => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = e.target.closest && e.target.closest('a[href]');
      if (!a || a.target && a.target !== '_self' || a.hasAttribute('download') || a.hasAttribute('data-ts-no-trans')) return;
      const raw = a.getAttribute('href');
      if (!raw || raw.charAt(0) === '#' || !/^https?:$/.test(a.protocol) || a.origin !== location.origin) return;
      if (a.pathname === location.pathname && a.search === location.search) return;
      e.preventDefault();
      try { sessionStorage.setItem('ts-trans', '1'); } catch (err) {}
      html.classList.remove('ts-trans-in');
      html.classList.add('ts-trans-leave');
      setTimeout(() => { location.href = a.href; }, 480);
      setTimeout(() => html.classList.remove('ts-trans-leave'), 4000);
    });
    addEventListener('pageshow', e => { if (e.persisted) html.classList.remove('ts-trans-leave', 'ts-trans-in'); });
  }

  /* ---------- Cookie-Einstellungen von Squarespace: statt schwebend über dem Footer als Link in der Footer-Leiste ---------- */
  const cookieLink = document.querySelector('[data-ts-cookie]');
  let cookieFloat = null;
  const textOf = (el) => ((el.shadowRoot ? el.shadowRoot.textContent : '') + ' ' + (el.textContent || '')).replace(/\s+/g, ' ').trim();
  const parentOf = (a) => a.parentElement || (a.getRootNode && a.getRootNode().host) || null;
  const fixedAncestor = (el) => { for (let a = el; a && a !== document.body; a = parentOf(a)) { if (getComputedStyle(a).position === 'fixed') return a; } return null; };
  const shown = (d) => { const r = d.getBoundingClientRect(); const cs = getComputedStyle(d); return r.height > 0 && r.width > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0'; };
  // Ist im selben festen Rahmen gerade ein Banner mit längerem Text sichtbar? Dann nichts anfassen.
  const bannerVisible = (root) => [...root.querySelectorAll('*'), ...(root.shadowRoot ? root.shadowRoot.querySelectorAll('*') : [])].some(d => {
    const own = [...d.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    return own.length > 60 && shown(d);
  });
  const findCookieFloat = () => {
    // 1. Squarespace: <div class="cookie-banner-manager"><section class="manage-cookies-bar …"><button class="manage-bar-action">
    const sq = document.querySelector('.cookie-banner-manager .manage-cookies-bar');
    if (sq) { cookieFloat = sq.querySelector('.manage-bar-action, button') || sq; if (cookieLink) { cookieLink.hidden = false; document.documentElement.classList.add('ts-cookie-ok'); } return; }
    // 2. Reserve, falls Squarespace den Aufbau ändert: kleiner fester Knopf mit kurzem „Cookie“-Text
    if (cookieFloat && document.contains(cookieFloat) && cookieFloat.hasAttribute('data-ts-cookie-float')) return;
    // kleiner, sichtbarer Knopf mit kurzem „Cookie“-Text, der selbst oder über einen Rahmen fest auf dem Bildschirm sitzt.
    // Das große Banner beim ersten Besuch hat viel Text und bleibt deshalb unangetastet.
    const hit = [...document.body.querySelectorAll('*')].find(el => {
      if (el.closest('.ts, .tsw') || /^(SCRIPT|STYLE|svg|path)$/i.test(el.tagName)) return false;
      const t = textOf(el);
      if (!/cookie/i.test(t) || t.length > 40) return false;
      const r = el.getBoundingClientRect();
      if (r.height <= 0 || r.height > 90 || r.width <= 0 || r.width > 420) return false;
      const fa = fixedAncestor(el);
      return !!fa && !bannerVisible(fa);
    });
    if (!hit) return;
    cookieFloat = hit;
    hit.setAttribute('data-ts-cookie-float', '');
    if (cookieLink) cookieLink.hidden = false;
  };
  if (cookieLink) {
    cookieLink.addEventListener('click', () => {
      findCookieFloat();
      if (!cookieFloat) return;
      cookieFloat.removeAttribute('data-ts-cookie-float');
      const inner = cookieFloat.shadowRoot ? cookieFloat.shadowRoot.querySelector('button, a') : null;
      const target = cookieFloat.matches('button, a') ? cookieFloat : (inner || cookieFloat.querySelector('button, a') || cookieFloat);
      target.click();
    });
    [300, 1500, 4000, 8000, 15000].forEach(ms => setTimeout(findCookieFloat, ms));
    // nach „Akzeptieren“ im Banner erscheint der Knopf neu
    document.addEventListener('click', () => setTimeout(findCookieFloat, 600), true);
  }

  /* ---------- Twitch-Bereich (WoW Forever): Unternavigation mit Weg zurück zur Homepage ---------- */
  const tsw = document.querySelector('.tsw');
  if (tsw) {
    const TSW_PAGES = [['/twitch-startseite', 'Start'], ['/live', 'Live'], ['/mitspielen', 'Mitspielen'], ['/charakter', 'Charakter'], ['/bestenliste', 'Bestenliste'], ['/statistiken', 'Statistiken']];
    const here = (location.pathname.replace(/\/+$/, '') || '/').toLowerCase();
    const sub = document.createElement('nav');
    sub.className = 'tsw-subnav';
    sub.setAttribute('aria-label', 'Twitch-Bereich');
    sub.innerHTML = `<div class="ts-container tsw-subnav__inner">
      <a class="tsw-subnav__home" href="/"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>Homepage</a>
      <ul class="tsw-subnav__list">${TSW_PAGES.map(([href, label]) => `<li><a href="${href}"${here === href ? ' aria-current="page"' : ''}>${label}</a></li>`).join('')}</ul>
    </div>`;
    tsw.prepend(sub);
    // Instagram: auf Twitch-Seiten das WoW-/Twitch-Konto, sonst das private Konto
    document.querySelectorAll('[data-ts-insta]').forEach(a => { a.href = 'https://www.instagram.com/trutz.stahl/'; });
    document.querySelectorAll('[data-ts-insta-handle]').forEach(el => { el.textContent = '@trutz.stahl'; });
    document.querySelectorAll('.ts-nav-link[href="/twitch-startseite"]').forEach(a => { a.classList.add('is-active'); a.setAttribute('aria-current', 'page'); });
  }

  /* ---------- Große Headlines in ihre Spalte einpassen ---------- */
  const fitOne = el => {
    const before = el.style.getPropertyValue('font-size');
    el.style.removeProperty('font-size');
    const avail = el.clientWidth;
    if (!avail) { if (before) el.style.setProperty('font-size', before, 'important'); return; }
    const left = el.getBoundingClientRect().left;
    const lines = el.querySelectorAll('.ts-line > span');
    const need = lines.length
      ? Math.max(...[...lines].map(s => { const r = s.getBoundingClientRect(); return r.left - left + Math.max(r.width, s.scrollWidth); }))
      : el.scrollWidth;
    if (need > avail + 1) {
      const size = parseFloat(getComputedStyle(el).fontSize) * (avail / need) * 0.98;
      /* Winzige Abweichungen ignorieren, damit nichts zuckt */
      const keep = before && Math.abs(parseFloat(before) - size) < 0.75;
      el.style.setProperty('font-size', keep ? before : `${size}px`, 'important');
    }
  };
  const fitEls = [...document.querySelectorAll('[data-ts-fit]')];
  const fitAll = () => fitEls.forEach(fitOne);
  fitAll();
  /* Während des Ladens auf jede Größenänderung reagieren – danach ist Ruhe: nur noch, wenn eine Schrift
     ankommt oder sich die Breite wirklich ändert (Drehen, Fenster), nie beim Scrollen */
  let ro = null, fitDelay;
  if ('ResizeObserver' in window && fitEls.length) {
    ro = new ResizeObserver(() => { clearTimeout(fitDelay); fitDelay = setTimeout(fitAll, 30); });
    fitEls.forEach(el => { ro.observe(el); el.querySelectorAll('.ts-line > span').forEach(s => ro.observe(s)); });
  }
  const onFonts = () => fitAll();
  if (document.fonts) {
    document.fonts.addEventListener('loadingdone', onFonts);
    if (document.fonts.ready) document.fonts.ready.then(fitAll);
  }
  const settle = () => setTimeout(() => {
    fitAll();
    if (ro) { ro.disconnect(); ro = null; }
  }, 1500);
  if (document.readyState === 'complete') settle(); else addEventListener('load', () => { fitAll(); settle(); }, { once: true });
  let fitTimer;
  /* Nur bei echter Breitenänderung neu einpassen – am Handy feuert „resize“ auch, wenn beim Scrollen die Adressleiste ein- und ausfährt */
  let fitW = innerWidth;
  addEventListener('resize', () => { if (Math.abs(innerWidth - fitW) < 2) return; fitW = innerWidth; clearTimeout(fitTimer); fitTimer = setTimeout(fitAll, 120); });

  /* ---------- Aktiver Navigationspunkt ---------- */
  const path = location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.ts-nav-link').forEach(a => {
    const href = a.getAttribute('href');
    if (href !== '/' && (path === href || path.startsWith(href + '/'))) { a.classList.add('is-active'); a.setAttribute('aria-current', 'page'); }
  });

  /* ---------- Header: Glas beim Scrollen, aus- und einblenden ---------- */
  const header = document.querySelector('[data-ts-header]');
  if (!document.querySelector('.ts-hero')) header.classList.add('is-solid');
  /* Erst nach einer deutlichen Bewegung aus- bzw. einblenden – am Handy wackelt scrollY beim Schwung-Scrollen,
     Nachfedern und Ein-/Ausfahren der Adressleiste ständig um ein paar Pixel, sonst springt der Header */
  let lastY = Math.max(0, scrollY), acc = 0, headTick = false;
  const onScroll = () => {
    headTick = false;
    const y = Math.max(0, scrollY), dy = y - lastY;
    lastY = y;
    header.classList.toggle('is-scrolled', y > 24);
    if (y < 240 || body.classList.contains('ts-menu-open')) { acc = 0; header.classList.remove('is-hidden'); return; }
    if (y >= document.documentElement.scrollHeight - innerHeight - 2 || !dy) return; // Gummiband am Seitenende ignorieren
    if ((dy > 0) !== (acc > 0)) acc = 0;
    acc += dy;
    if (acc > 16) header.classList.add('is-hidden');
    else if (acc < -48) header.classList.remove('is-hidden');
  };
  addEventListener('scroll', () => { if (!headTick) { headTick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- Mobile-Menü ---------- */
  const toggle = document.querySelector('[data-ts-menu-toggle]');
  const menu = document.getElementById('ts-menu');
  /* Bei offenem Menü ist der Rest der Seite für Tastatur und Screenreader gesperrt (inert) –
     der Header bleibt frei, damit man das Menü über den Burger wieder schließen kann */
  const setMenu = (open, refocus) => {
    const was = body.classList.contains('ts-menu-open');
    body.classList.toggle('ts-menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    menu.setAttribute('aria-hidden', String(!open));
    [...body.children].forEach(el => { if (el !== menu && el !== header && !el.matches('script, style')) el.inert = open; });
    if (open && !was) { const first = menu.querySelector('a'); if (first) setTimeout(() => first.focus({ preventScroll: true }), 50); }
    if (!open && was && refocus) toggle.focus();
  };
  toggle.addEventListener('click', () => setMenu(!body.classList.contains('ts-menu-open'), true));
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape' && body.classList.contains('ts-menu-open')) setMenu(false, true); });
  matchMedia('(min-width: 1024px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

  /* ---------- Custom Cursor (wirkt auf alle Links der Seite) ---------- */
  if (fx) {
    const dot = document.querySelector('.ts-cursor-dot');
    const ring = document.querySelector('.ts-cursor-ring');
    let mx = -100, my = -100, rx = mx, ry = my, first = true, idle = true;
    addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      if (first) { rx = mx; ry = my; first = false; }
      dot.style.transform = `translate3d(${mx}px, ${my}px, 0)`;
      body.classList.add('ts-has-cursor');
      if (idle) { idle = false; requestAnimationFrame(loop); }
    }, { passive: true });
    document.addEventListener('mouseleave', () => body.classList.remove('ts-has-cursor'));
    document.addEventListener('mouseover', e => {
      body.classList.toggle('ts-cursor-hover', !!e.target.closest('a, button, [role="button"], input[type="submit"], label'));
    });
    /* Ring folgt weich; steht die Maus still, schläft die Schleife (spart Akku) */
    function loop() {
      rx += (mx - rx) * 0.16; ry += (my - ry) * 0.16;
      ring.style.transform = `translate3d(${rx}px, ${ry}px, 0)`;
      if (Math.abs(mx - rx) + Math.abs(my - ry) > 0.1) requestAnimationFrame(loop); else idle = true;
    }
  }

  /* ---------- Magnetische Buttons ---------- */
  if (fx) {
    document.querySelectorAll('.ts-magnetic').forEach(el => {
      const inner = el.querySelector('.ts-btn__inner');
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        const x = e.clientX - (r.left + r.width / 2), y = e.clientY - (r.top + r.height / 2);
        el.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        if (inner) inner.style.transform = `translate(${x * 0.12}px, ${y * 0.12}px)`;
      });
      el.addEventListener('mouseleave', () => {
        const ease = 'transform .7s cubic-bezier(.16,1,.3,1)';
        el.style.transition = `${ease}, box-shadow .5s, border-color .4s, color .4s`;
        el.style.transform = '';
        if (inner) { inner.style.transition = ease; inner.style.transform = ''; }
        setTimeout(() => { el.style.transition = ''; if (inner) inner.style.transition = ''; }, 700);
      });
    });
  }

  /* ---------- 3D-Tilt + Lichtpunkt auf Karten ---------- */
  document.querySelectorAll('.ts-tilt').forEach(card => {
    card.addEventListener('pointermove', e => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      card.style.setProperty('--mx', `${px * 100}%`);
      card.style.setProperty('--my', `${py * 100}%`);
      if (fx) card.style.transform = `perspective(900px) rotateX(${(0.5 - py) * 7}deg) rotateY(${(px - 0.5) * 9}deg) translateY(-4px)`;
    });
    card.addEventListener('pointerleave', () => { card.style.transform = ''; });
  });

  /* ---------- Parallax der Lichtflächen ---------- */
  if (fx) {
    const orbs = document.querySelectorAll('[data-ts-parallax]');
    if (orbs.length) addEventListener('mousemove', e => {
      const cx = e.clientX - innerWidth / 2, cy = e.clientY - innerHeight / 2;
      orbs.forEach(o => { const f = parseFloat(o.dataset.tsParallax); o.style.transform = `translate3d(${cx * f}px, ${cy * f}px, 0)`; });
    }, { passive: true });
  }

  /* ---------- Einblenden beim Scrollen ---------- */
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
  }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.ts-reveal').forEach(el => { if (!el.closest('.ts-hero')) io.observe(el); });
  window.TS_READY = true; // für die Sicherung im Header: Einblenden läuft, Inhalte nicht zwangsweise zeigen

  /* ---------- Hero: Sternenfeld / Konstellation ---------- */
  const canvas = document.getElementById('ts-hero-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    const hero = canvas.closest('.ts-hero');
    const animate = !reduceMotion;
    let w = 0, h = 0, points = [], running = false, ready = false;
    const mouse = { x: -9999, y: -9999 };

    const build = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      const nw = canvas.clientWidth, nh = canvas.clientHeight;
      /* Nur die Höhe geändert (Adressleiste am Handy)? Sterne behalten, nicht neu würfeln */
      if (points.length && nw === w && Math.abs(nh - h) < 160) { h = nh; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); return; }
      w = nw; h = nh;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.round(Math.min(110, (w * h) / 14000));
      points = Array.from({ length: count }, () => ({
        x: Math.random() * w, y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.18, vy: (Math.random() - 0.5) * 0.18,
        r: Math.random() * 1.3 + 0.3,
        c: Math.random() > 0.7 ? '74,222,128' : (Math.random() > 0.5 ? '110,231,183' : '246,250,247'),
      }));
    };

    const draw = () => {
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < points.length; i++) {
        const p = points[i];
        if (animate) {
          p.x += p.vx; p.y += p.vy;
          const dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
          if (d2 < 22000) { const f = (22000 - d2) / 22000 * 0.6, d = Math.sqrt(d2 + 1); p.x += dx / d * f; p.y += dy / d * f; }
          if (p.x < -20) p.x = w + 20; if (p.x > w + 20) p.x = -20;
          if (p.y < -20) p.y = h + 20; if (p.y > h + 20) p.y = -20;
        }
        for (let j = i + 1; j < points.length; j++) {
          const q = points[j], d = Math.hypot(p.x - q.x, p.y - q.y);
          if (d < 130) {
            ctx.strokeStyle = `rgba(154,171,163,${(1 - d / 130) * 0.12})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
          }
        }
        ctx.fillStyle = `rgba(${p.c},0.75)`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
      }
    };

    const tick = () => { if (!running) return; draw(); if (animate) requestAnimationFrame(tick); };
    const resume = () => { if (ready && !running) { running = true; if (animate) tick(); } };

    /* Erst ein ruhiges Bild, die Bewegung startet nach dem Laden – so bleibt der Seitenaufbau flott */
    build(); draw();
    const go = () => setTimeout(() => { ready = true; if (!document.hidden && canvas.getBoundingClientRect().bottom > 0) resume(); }, 400);
    if (document.readyState === 'complete') go(); else addEventListener('load', go, { once: true });
    let rt;
    addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { build(); draw(); }, 150); });
    hero.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    hero.addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });
    new IntersectionObserver(([en]) => { if (en.isIntersecting && !document.hidden) resume(); else running = false; }).observe(canvas);
    document.addEventListener('visibilitychange', () => { if (document.hidden) running = false; else resume(); });
  }

  /* ---------- Footer: Jahr, Rechtslinks aus dem Squarespace-Footer, nach oben ---------- */
  document.querySelectorAll('[data-ts-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
  const nativeFooter = document.getElementById('footer-sections');
  if (nativeFooter) {
    document.querySelectorAll('[data-ts-native]').forEach(el => {
      const match = [...nativeFooter.querySelectorAll('a[href]')].find(a => a.textContent.trim().toLowerCase().startsWith(el.dataset.tsNative.toLowerCase()));
      if (match) el.setAttribute('href', match.getAttribute('href'));
    });
  }
  document.querySelectorAll('[data-ts-totop]').forEach(el => el.addEventListener('click', e => {
    e.preventDefault();
    scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  }));
})();

}catch(e){console.warn("vorschau",e)}
;
try{
window.TS_SHOP = {
  kategorien: [
    { id: 'stream-widgets', nr: '01', titel: 'Stream-Widgets', text: 'Overlays für OBS – in fertigen Themen wie World of Warcraft oder in deinem ganz eigenen Stil.', link: '/shop/stream-widgets', farbe: 'rgb(74, 222, 128)' },
    { id: 'buecher',        nr: '02', titel: 'Bücher',         text: 'Kinderbücher und Malbücher aus dem Kreativhafen.',                   link: '/shop/buecher',        farbe: 'rgb(110, 231, 183)' }
    // weitere Kategorie: { id: 'merch', nr: '03', titel: 'Merch', text: '…', link: '/shop/merch', farbe: 'rgb(74, 222, 128)' }
  ],
  /* Themen der Stream-Widgets (Seite /shop/stream-widgets). Neues Thema = neuer Eintrag + neue Seite */
  themen: [
    { id: 'wow',    nr: '01', titel: 'World of Warcraft', text: 'Questlog, Ruf, Bosse und goldene Rahmen – die Widgets im Stil von Azeroth.', link: '/shop/stream-widgets/world-of-warcraft', farbe: '#ffd100' },
    { id: 'custom', nr: '02', titel: 'Dein eigener Stil', label: 'Auf Bestellung', text: 'Dein Spiel, dein Stil: Ich gestalte die Widgets in deinem eigenen Thema.', link: '/shop/stream-widgets/eigener-stil', farbe: 'rgb(110, 231, 183)' },
    { id: 'gta6', nr: '03', titel: 'Neon City', text: 'Sonnenuntergang, Palmen, Neon und Gangs: Missionen statt Quests, Respekt statt Ruf, Revierkampf statt Schlacht – im Look der neuen Großstadt-Krimis.', link: '/shop/stream-widgets/neon-city', farbe: '#ff3d9a' }
    // weiteres Thema: { id: 'diablo', nr: '03', titel: 'Diablo', text: '…', link: '/shop/stream-widgets/diablo', farbe: '#c0392b' }
  ],
  produkte: [
    /* ---------- Stream-Widgets (jedes inkl. Standard-Paket) ---------- */
    { kat: 'stream-widgets', thema: 'wow', id: 'wheel',    icon: '☸',  titel: 'Glücksrad & Quests', text: 'Glücksrad mit Questlog und „Aktive Quests“ – dreht bei Kanalpunkten, Follows, Subs und !rad.', preis: '14,90 €', link: '/store/p/gluecksrad-und-quests' },
    /* Pause-Spiele – jedes einzeln */
    { kat: 'stream-widgets', thema: 'wow', id: 'boss',     icon: '⚔',  titel: 'Pause: Bosskampf',   text: 'Ein Boss aus WoW: Der Chat kämpft mit !angriff, reagiert auf Fähigkeiten und würfelt um die Beute.', preis: '14,90 €', link: '/store/p/pause-bosskampf' },
    { kat: 'stream-widgets', thema: 'wow', id: 'quiz',     icon: '❓', titel: 'Pause: Azeroth-Quiz', text: 'WoW-Fragen mit !A bis !D – jeder hat eine Stimme, richtige Antworten bringen Punkte und Ruf.',      preis: '12,90 €', link: '/store/p/pause-azeroth-quiz' },
    { kat: 'stream-widgets', thema: 'wow', id: 'darkspear',icon: '🏴', titel: 'Pause: Darkspear-Schlacht', text: 'Allianz gegen Horde um Stützpunkte und Flagge – der Chat kämpft mit !allianz und !horde.',     preis: '12,90 €', link: '/store/p/pause-darkspear-schlacht' },
    { kat: 'stream-widgets', thema: 'wow', id: 'fish',     icon: '🎣', titel: 'Pause: Angeln',      text: 'Mit !angeln die Angel auswerfen – bei jedem Fischschwarm beißt etwas an. Beste Angler im Stream.', preis: '12,90 €', link: '/store/p/pause-angeln' },
    { kat: 'stream-widgets', thema: 'wow', id: 'riddle',   icon: '🧩', titel: 'Pause: Azeroth-Rätsel', text: 'Ein WoW-Begriff, Buchstabe für Buchstabe – wer ihn zuerst in den Chat schreibt, gewinnt.',        preis: '12,90 €', link: '/store/p/pause-azeroth-raetsel' },
    { kat: 'stream-widgets', thema: 'wow', id: 'giveaway', icon: '🎁', titel: 'Beute des Tages',    text: 'Faire Verlosung per Chat-Befehl – mit Endspurt, Ziehungs-Animation und Gewinner-Historie.',        preis: '14,90 €', link: '/store/p/beute-des-tages' },
    { kat: 'stream-widgets', thema: 'wow', id: 'voting',   icon: '🗳️', titel: 'Umfrage',            text: 'Der Chat stimmt ab – Live-Ergebnisse, Sudden Death bei Gleichstand, Siegertreppchen.',            preis: '9,90 €', link: '/store/p/umfrage' },
    { kat: 'stream-widgets', thema: 'wow', id: 'level',    icon: '🏰', titel: 'Aufbauspiel',        text: 'Jede Chat-Nachricht baut am Gebäude mit – mit Buffs, Strafen, Fraktionen und Bestenliste.',        preis: '14,90 €', link: '/store/p/aufbauspiel' },
    { kat: 'stream-widgets', thema: 'wow', id: 'bingo',    icon: '🎯', titel: 'Stream-Bingo',       text: 'Bingo-Feld mit eigenen Zielen – der Chat meldet Felder, du bestätigst.',                           preis: '9,90 €', link: '/store/p/stream-bingo' },
    { kat: 'stream-widgets', thema: 'wow', id: 'coin',     icon: '🪙', titel: 'Münzwurf',           text: '3D-Münze mit Kopf, Zahl und seltener Kante – per Befehl, Kanalpunkten oder Knopfdruck.',          preis: '9,90 €', link: '/store/p/muenzwurf' },
    { kat: 'stream-widgets', thema: 'wow', id: 'rep',      icon: '🏅', titel: 'Ruf',                text: 'Zuschauer sammeln Ruf bei deiner Fraktion – Ränge von Neutral bis Ehrfürchtig. Ruf aus Spielen gibt es im Wunsch-Paket.',                   preis: '14,90 €', link: '/store/p/ruf' },
    { kat: 'stream-widgets', thema: 'wow', id: 'char',     icon: '🧙', titel: 'Charakter',          text: 'Leveling-Tracker mit Erfahrungsleiste und goldenem Stufenband bei „Ding!“.',                      preis: '9,90 €', link: '/store/p/charakter' },
    { kat: 'stream-widgets', thema: 'wow', id: 'metrics',  icon: '📈', titel: 'Metrics',            text: 'Ziele im Rotations-Fenster, „Zuletzt“-Leiste und ein Chat-Fenster im WoW-Rahmen.',               preis: '14,90 €', link: '/store/p/metrics' },
    { kat: 'stream-widgets', thema: 'wow', id: 'counter',  icon: '🔢', titel: 'Zähler',             text: 'Bild mit Zahl – Tode, Wipes, Bosse. Zählen per Knopf oder Chat-Befehl.',                          preis: '9,90 €', link: '/store/p/zaehler' },
    { kat: 'stream-widgets', thema: 'wow', id: 'wunsch',   icon: '✦',  titel: 'Wunsch-Paket',       text: 'Mehrere Widgets in einer Datei – du wählst, ich baue es dir und schicke es per Mail.',            preis: 'ab 22,90 €', link: '/shop/stream-widgets/world-of-warcraft/wunsch-paket', highlight: true },
    /* ---------- Neon City ---------- */
    { kat: 'stream-widgets', thema: 'gta6', id: 'wheel-gta6', icon: '☸', titel: 'Glücksrad & Missionen', text: 'Glücksrad mit Missions-Log und „Aktive Missionen“ – dreht bei Kanalpunkten, Follows, Subs und !rad.', preis: '14,90 €', link: '/store/p/gluecksrad-und-quests-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'giveaway-gta6', icon: '🎁', titel: 'Beute des Tages', text: 'Faire Verlosung per Chat-Befehl – mit Endspurt, Ziehungs-Animation und Gewinner-Historie.', preis: '14,90 €', link: '/store/p/beute-des-tages-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'voting-gta6', icon: '🗳️', titel: 'Umfrage', text: 'Der Chat stimmt ab – Live-Ergebnisse, Sudden Death bei Gleichstand, Siegertreppchen.', preis: '9,90 €', link: '/store/p/umfrage-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'level-gta6', icon: '🏰', titel: 'Aufbauspiel', text: 'Jede Chat-Nachricht baut am Gebäude mit – mit Buffs, Strafen, Gangs und Bestenliste.', preis: '14,90 €', link: '/store/p/aufbauspiel-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'bingo-gta6', icon: '🎯', titel: 'Stream-Bingo', text: 'Bingo-Feld mit eigenen Zielen – der Chat meldet Felder, du bestätigst.', preis: '9,90 €', link: '/store/p/stream-bingo-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'coin-gta6', icon: '🪙', titel: 'Münzwurf', text: '3D-Münze mit Kopf, Zahl und seltener Kante – per Befehl, Kanalpunkten oder Knopfdruck.', preis: '9,90 €', link: '/store/p/muenzwurf-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'rep-gta6', icon: '🏅', titel: 'Respekt', text: 'Zuschauer sammeln Respekt bei deiner Gang – Ränge von Neutral bis Ehrfürchtig.', preis: '14,90 €', link: '/store/p/ruf-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'char-gta6', icon: '🧙', titel: 'Charakter', text: 'Leveling-Tracker mit Erfahrungsleiste und leuchtendem Level-up-Banner.', preis: '9,90 €', link: '/store/p/charakter-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'metrics-gta6', icon: '📈', titel: 'Metrics', text: 'Ziele im Rotations-Fenster, „Zuletzt“-Leiste und ein Chat-Fenster im Neon-Rahmen.', preis: '14,90 €', link: '/store/p/metrics-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'counter-gta6', icon: '🔢', titel: 'Zähler', text: 'Bild mit Zahl – Tode, Wipes, Bosse. Zählen per Knopf oder Chat-Befehl.', preis: '9,90 €', link: '/store/p/zaehler-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'boss-gta6', icon: '⚔', titel: 'Pause: Bosskampf', text: 'Gang-Bosse der Stadt: Der Chat kämpft mit !angriff, reagiert mit !deckung & Co. und würfelt um Neonketten, Geldkoffer und Villen.', preis: '14,90 €', link: '/store/p/pause-bosskampf-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'quiz-gta6', icon: '❓', titel: 'Pause: Quiz', text: 'Quizfragen mit !A bis !D – jeder hat eine Stimme, richtige Antworten bringen Punkte.', preis: '12,90 €', link: '/store/p/pause-azeroth-quiz-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'darkspear-gta6', icon: '🏴', titel: 'Pause: Revierkampf', text: 'Zwei Gangs um Blocks und Beutetasche – der Chat kämpft mit !neon und !sunset.', preis: '12,90 €', link: '/store/p/pause-darkspear-schlacht-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'fish-gta6', icon: '🎣', titel: 'Pause: Angeln', text: 'Mit !angeln die Angel auswerfen – bei jedem Fischschwarm beißt etwas an. Beste Angler im Stream.', preis: '12,90 €', link: '/store/p/pause-angeln-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'riddle-gta6', icon: '🧩', titel: 'Pause: Rätsel', text: 'Ein Begriff, Buchstabe für Buchstabe – wer ihn zuerst in den Chat schreibt, gewinnt.', preis: '12,90 €', link: '/store/p/pause-azeroth-raetsel-gta6' },
    { kat: 'stream-widgets', thema: 'gta6', id: 'wunsch-gta6', icon: '✦', titel: 'Wunsch-Paket', text: 'Mehrere Widgets in einer Datei – du wählst, ich baue es dir und schicke es per Mail.', preis: 'ab 22,90 €', link: '/shop/stream-widgets/neon-city/wunsch-paket', highlight: true },
    /* ---------- Dein eigener Stil ---------- */
    { kat: 'stream-widgets', thema: 'custom', id: 'eigenes-thema', icon: '🎨', titel: 'Eigenes Thema', text: 'Du nennst Spiel oder Stil, ich gestalte das Standard-Paket und deine Widgets passend dazu – per Mail geliefert.', preis: 'ab 49,90 €', link: '/store/p/eigenes-thema', highlight: true }
    /* ---------- Bücher (Beispiel – Kommentarzeichen entfernen und ausfüllen) ----------
    ,{ kat: 'buecher', id: 'loki-1', bild: 'https://…/cover.jpg', titel: 'Die Loki-Detektive', text: 'Maria Holm auf Ermittlungstour.', preis: '12,90 €', link: '/store/p/loki-detektive' }
    */
  ]
};

/* Darstellung: füllt alle Platzhalter <div data-tss-grid="kategorie-id"></div> und <div data-tss-cats></div> */
(() => {
  const S = window.TS_SHOP;
  const esc = s => String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const arrow = '<svg class="ts-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const card = (p, i) => {
    const media = p.bild ? `<img class="tss-card__img" src="${esc(p.bild)}" alt="" loading="lazy">` : `<span class="tss-card__icon" aria-hidden="true">${esc(p.icon || '✦')}</span>`;
    const tag = p.link ? 'a' : 'div';
    return `<${tag} class="tss-card${p.highlight ? ' tss-card--hi' : ''}"${p.link ? ` href="${esc(p.link)}"` : ''}>
      <div class="tss-card__media">${media}<span class="ts-label tss-card__nr">${String(i + 1).padStart(2, '0')}</span></div>
      <div class="tss-card__body">
        <h3 class="tss-card__title">${esc(p.titel)}</h3>
        <p class="tss-card__text">${esc(p.text)}</p>
        <div class="tss-card__foot">
          <span class="tss-card__price">${p.preis ? esc(p.preis) : '<span class="ts-label ts-muted">Preis im Shop</span>'}</span>
          <span class="ts-label tss-card__cta">${p.link ? 'Ansehen ' + arrow : 'Bald verfügbar'}</span>
        </div>
      </div></${tag}>`;
  };
  const run = () => {
    document.querySelectorAll('[data-tss-grid]').forEach(el => {
      const list = S.produkte.filter(p => p.kat === el.dataset.tssGrid && (!el.dataset.tssThema || p.thema === el.dataset.tssThema));
      el.innerHTML = list.length ? list.map(card).join('') : `<p class="tss-empty ts-label ts-muted">[ Hier entsteht gerade etwas – bald mehr ]</p>`;
      // Kleinunternehmer-Hinweis einmal unter dem Raster
      if (list.some(p => p.preis) && !(el.nextElementSibling && el.nextElementSibling.classList.contains('tss-tax'))) {
        el.insertAdjacentHTML('afterend', '<p class="ts-label ts-muted tss-tax">Alle Preise sind Endpreise · Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.</p>');
      }
    });
    document.querySelectorAll('[data-tss-themes]').forEach(el => {
      el.innerHTML = (S.themen || []).map(t => {
        const n = S.produkte.filter(p => p.thema === t.id).length;
        return `<a class="tss-cat" href="${esc(t.link)}" style="--tss-acc:${esc(t.farbe)}">
          <span class="ts-label tss-cat__nr">${esc(t.nr)} — ${esc(t.label || (n ? n + ' Produkt' + (n === 1 ? '' : 'e') : 'bald'))}</span>
          <span class="tss-cat__title">${esc(t.titel)}<i>.</i></span>
          <span class="tss-cat__text">${esc(t.text)}</span>
          <span class="ts-label tss-cat__go">Entdecken ${arrow}</span></a>`;
      }).join('');
    });
    document.querySelectorAll('[data-tss-cats]').forEach(el => {
      el.innerHTML = S.kategorien.map(k => {
        const n = S.produkte.filter(p => p.kat === k.id).length;
        return `<a class="tss-cat" href="${esc(k.link)}" style="--tss-acc:${esc(k.farbe)}">
          <span class="ts-label tss-cat__nr">${esc(k.nr)} — ${n ? n + ' Produkt' + (n === 1 ? '' : 'e') : 'bald'}</span>
          <span class="tss-cat__title">${esc(k.titel)}<i>.</i></span>
          <span class="tss-cat__text">${esc(k.text)}</span>
          <span class="ts-label tss-cat__go">Entdecken ${arrow}</span></a>`;
      }).join('');
    });
  };
  /* Produktbild: das erste Bild des Squarespace-Produkts automatisch in die Kachel holen
     (über die JSON-Ansicht der Produktseite, gleiche Domain). Ohne Bild bleibt das Symbol. */
  const fotos = () => {
    let cache = {};
    try { cache = JSON.parse(sessionStorage.getItem('tssFotos2') || '{}'); } catch (e) { cache = {}; }
    const save = () => { try { sessionStorage.setItem('tssFotos2', JSON.stringify(cache)); } catch (e) { /* egal */ } };
    const setImg = (card, url) => {
      const m = card.querySelector('.tss-card__media');
      if (!m || !url || m.querySelector('.tss-card__img')) return;
      const img = new Image();
      img.className = 'tss-card__img'; img.alt = ''; img.loading = 'lazy';
      img.onload = () => { m.querySelectorAll('.tss-card__icon').forEach(x => x.remove()); card.classList.add('tss-card--foto'); };
      img.onerror = () => img.remove();
      img.src = url + (url.includes('?') ? '' : '?format=750w');
      m.prepend(img);
    };
    document.querySelectorAll('a.tss-card[href*="/store/p/"]').forEach(card => {
      const href = card.getAttribute('href');
      if (card.querySelector('.tss-card__img')) return;
      if (cache[href] !== undefined) { setImg(card, cache[href]); return; }
      fetch(href + (href.includes('?') ? '&' : '?') + 'format=json', { credentials: 'same-origin' })
        .then(r => (r.ok ? r.json() : null))
        .then(j => {
          const it = j && (j.item || (j.items && j.items[0]));
          // Bilder des Produkts in Squarespace-Reihenfolge; „assetUrl“ zeigt teils nur auf einen Ordner
          const cands = [].concat((it && it.items) || [], it ? [it] : []).map(x => x && x.assetUrl).filter(u => u && !/\/$/.test(u));
          const url = cands[0] || '';
          if (url) { cache[href] = url; save(); }
          setImg(card, url);
        })
        .catch(() => {});
    });
  };
  const start = () => { run(); fotos(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();

}catch(e){console.warn("vorschau",e)}
;
try{
/* Produktseiten (Squarespace-Store) im Design: Titel aufteilen, Beschreibung gliedern, Brotkrumen auf den Shop */
(() => {
  const d = document.querySelector('.product-detail');
  if (!d) return;
  // Titel: „01 · Name – Untertitel" → Label „Untertitel" + großer Name
  const t = d.querySelector('.product-title');
  if (t && !t.dataset.tsp) {
    t.dataset.tsp = '1';
    const raw = t.textContent.replace(/^\s*\d+\s*·\s*/, '').trim();
    const [name, ...rest] = raw.split(' – ');
    const k = document.createElement('p');
    k.className = 'tsp-kicker';
    k.textContent = rest.join(' – ') || 'Shop';
    t.before(k);
    t.textContent = name;
    const dot = document.createElement('span'); dot.className = 'tsp-dot'; dot.textContent = '.';
    t.append(dot);
  }
  // Beschreibung: Großbuchstaben-Zeilen = Zwischenüberschrift, „• " = Aufzählung, erster Absatz = Einleitung
  d.querySelectorAll('.product-description').forEach(box => {
    box.querySelectorAll('p').forEach((p, i) => {
      const s = p.textContent.trim();
      if (!s) return;
      if (/^•\s*/.test(s)) { p.classList.add('tsp-li'); p.innerHTML = p.innerHTML.replace(/^\s*•\s*/, ''); }
      else if (s.length < 60 && s === s.toUpperCase() && /[A-ZÄÖÜ]/.test(s)) p.classList.add('tsp-h');
      else if (i === 0) p.classList.add('tsp-intro');
    });
  });
  // Kleinunternehmer-Hinweis unter dem Preis
  const price = d.querySelector('.product-price');
  if (price && !price.querySelector('.tsp-tax')) {
    const tax = document.createElement('span');
    tax.className = 'tsp-tax';
    tax.textContent = 'Endpreis · Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.';
    price.append(tax);
  }
  // Brotkrumen: „Shop" zeigt auf die Shop-Seite statt auf die versteckte Store-Seite
  const crumbs = d.querySelectorAll('.product-nav a');
  if (crumbs[0]) {
    const pth = location.pathname;
    // Thema aus dem Katalog (TS_SHOP) – passt automatisch für jedes neue Thema
    const S = window.TS_SHOP || {};
    const norm = (u) => String(u || '').replace(/\/+$/, '').toLowerCase();
    const prod = (S.produkte || []).find(p => p.link && norm(p.link) === norm(pth));
    const th = prod && prod.thema && (S.themen || []).find(x => x.id === prod.thema);
    const [href, txt] = th ? [th.link, String(th.titel).replace(/\u00AD/g, '')]
      : /eigenes-thema/i.test(pth) ? ['/shop/stream-widgets/eigener-stil', 'Dein eigener Stil']
      : /pause-|widget|gluecksrad|helden|muenz|mnz|zaehler|ruf|charakter|metrics|umfrage|bingo|aufbau|beute|wunsch/i.test(pth) ? ['/shop/stream-widgets/world-of-warcraft', 'World of Warcraft'] : ['/shop', 'Shop'];
    crumbs[0].href = href; crumbs[0].textContent = txt;
    if (txt === 'World of Warcraft') d.closest('.product-detail-section') && d.closest('.product-detail-section').classList.add('tss-gold');
  }
  if (crumbs[1]) crumbs[1].textContent = t ? t.textContent.replace(/\.$/, '') : crumbs[1].textContent;
})();

}catch(e){console.warn("vorschau",e)}
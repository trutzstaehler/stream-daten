"""Erzeugt die Squarespace-Code-Bloecke (im Design von trutzstaehler.de) und Vorschauseiten.

python3 website.py  -> ../03-website/*.html  und  ../03-website/vorschau/*.html
"""
import os, sys, io, json, base64, html, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel as K
import motive  # noqa
import katalog as KAT
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '03-website')
PREV = os.path.join(OUT, 'vorschau')
BILDER = os.path.join(HERE, '..', '02-bilder')
esc = html.escape
ARROW = '<svg class="ts-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_DOWN = '<svg class="ts-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'
GRATIS_URL = '/s/Probierpaket_3-Ausmalbilder-gratis.pdf'


def store(slug):
    return f'/store/p/{slug}'


def btn(text, href, primary=True, arrow=ARROW, extra=''):
    cls = 'ts-btn--primary' if primary else 'ts-btn--ghost'
    return (f'<a href="{href}" class="ts-btn {cls} ts-magnetic"{extra}><span class="ts-btn__inner"><span class="ts-roll">'
            f'<span data-text="{esc(text)}">{esc(text)}</span></span>{arrow}</span></a>')


import re as _re


def mini(svg):
    """SVG verkleinern: Zahlen runden, Leerraum sparen, einfache Anfuehrungszeichen (kein JSON-Escaping)."""
    svg = _re.sub(r'(\d+\.\d+)', lambda m: str(round(float(m.group(1)))), svg)
    svg = _re.sub(r'\s+', ' ', svg).replace('> <', '><').replace('"', "'")
    return svg


def cap_cls(key):
    return ' class="is-long"' if len(K.MOTIFS[key]['name']) > 11 else ''


def thumb_svg(key):
    """Motiv ohne Namen als kompaktes Inline-SVG (Name steht als Text darunter)."""
    return mini(K.motif_svg(key)).replace('<svg ', "<svg aria-hidden='true' ", 1)


def lines_uri(key):
    """Vorlage fuer das Ausmal-Widget als SVG-Data-URI (1000 x 1100, mit Namen)."""
    svg = mini(K.motif_svg(key, with_name=True, w=1000, h=1100))
    return 'data:image/svg+xml;utf8,' + svg.replace('%', '%25').replace('#', '%23')


def webp_uri(path, w=360):
    im = Image.open(path).convert('RGB')
    im = im.resize((w, round(w * im.size[1] / im.size[0])), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=72, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def bunt(key, w=260):
    return webp_uri(os.path.join(BILDER, 'motive-ausgemalt', key + '.png'), w)


# ======================================================================= CSS
CSS = r'''
<style>
  /* ===== Ausmalbilder (ts-am) – nutzt die ts-/tss-Bausteine der Seite ===== */
  .ts-am { position: relative; isolation: isolate; overflow: hidden; overflow: clip; }
  .ts-am__orb { position: absolute; z-index: -1; right: -14%; top: 0; width: 56vw; height: 56vw; max-width: 860px; max-height: 860px; border-radius: 50%; pointer-events: none;
    background: radial-gradient(circle, rgba(46, 140, 108, .28) 0%, rgba(46, 140, 108, .16) 24%, rgba(46, 140, 108, .06) 46%, rgba(46, 140, 108, 0) 70%); }
  .ts-am .ts-line { padding-bottom: .16em; margin-bottom: -.16em; }
  .ts-am__ctas { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.75rem; }
  .ts .ts-am__chips { display: flex; flex-wrap: wrap; gap: .5rem; margin: 1.5rem 0 0; padding: 0; list-style: none; }
  .ts .ts-am__chips li { padding: 8px 13px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); color: var(--ts-text, #f6faf7); font-size: 10.5px; }
  .ts-am__block { padding-top: clamp(4.5rem, 8vw, 7.5rem); }
  .ts-am__blockhead { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--tss-line, rgba(255,255,255,.1)); }
  .ts .ts-am__h2 { margin-top: clamp(1.75rem, 3vw, 2.5rem); font-family: var(--ts-font-display, 'Syne', sans-serif); font-weight: 800; font-size: clamp(2rem, 5vw, 4.4rem); line-height: .98; letter-spacing: -0.03em; }
  .ts .ts-am__h2 i { font-style: normal; color: var(--tss-acc, #6ee7b7); }
  .ts .ts-am__sub { margin-top: .9rem; max-width: 42rem; color: var(--tss-text, rgba(246,250,247,.72)); font-size: clamp(15px, 1.3vw, 17.5px); line-height: 1.65; }
  .ts-am__end { padding-bottom: clamp(6rem, 11vw, 10rem); }

  /* Saison-Leiste */
  .ts-am-season { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(230px, 1fr); gap: 1px; margin: 2rem 0 0; padding: 0; list-style: none;
    overflow-x: auto; scroll-snap-type: x mandatory; background: var(--tss-line, rgba(255,255,255,.1)); border: 1px solid var(--tss-line, rgba(255,255,255,.1)); scrollbar-width: thin; }
  .ts-am-season li { scroll-snap-align: start; background: var(--ts-bg, #060608); }
  .ts .ts-am-season a { position: relative; display: flex; flex-direction: column; gap: .55rem; height: 100%; min-height: 190px; padding: 1.4rem 1.3rem 1.3rem; color: inherit; text-decoration: none; transition: background .3s; }
  .ts .ts-am-season a::before { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 3px; background: var(--c); opacity: .35; transition: opacity .3s; }
  .ts .ts-am-season a:hover { background: rgba(255,255,255,.03); }
  .ts .ts-am-season a:hover::before, .ts-am-season .is-now a::before { opacity: 1; }
  .ts-am-season__date { color: var(--c); }
  .ts .ts-am-season__name { font: 800 clamp(1.1rem, 1.35vw, 1.32rem)/1.08 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.025em; overflow-wrap: anywhere; hyphens: auto; }
  .ts .ts-am-season__sub { color: var(--tss-text, rgba(246,250,247,.72)); font-size: 14px; line-height: 1.5; }
  .ts .ts-am-season__state { margin-top: auto; display: inline-flex; align-self: flex-start; align-items: center; gap: .45rem; padding: 6px 11px; border-radius: 999px;
    border: 1px solid var(--tss-line, rgba(255,255,255,.1)); color: var(--ts-muted, #9aaba3); font-size: 10px; white-space: nowrap; }
  .ts-am-season .is-now .ts-am-season__state { border-color: var(--c); color: #060608; background: var(--c); }
  .ts-am-season .is-now .ts-am-season__state::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: #060608; animation: ts-am-pulse 1.6s infinite; }
  .ts-am-season .is-past { opacity: .5; }
  @keyframes ts-am-pulse { 50% { opacity: .25; } }

  /* Highlight-Karte (Saisonpaket) */
  .ts .ts-am-bundle { display: grid; gap: 2rem; margin-top: 2rem; padding: clamp(1.5rem, 4vw, 3rem); border-radius: 26px; align-items: center; }
  .ts .ts-am-bundle__price { display: flex; align-items: baseline; gap: .8rem; margin-top: 1.2rem; font: 800 clamp(2rem, 4vw, 3rem)/1 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.03em; }
  .ts .ts-am-bundle__price s { font-size: .45em; color: var(--ts-muted, #9aaba3); font-weight: 700; }
  .ts-am-bundle__art { position: relative; min-height: 260px; }
  .ts .ts-am-bundle__art img { position: absolute; width: 46% !important; height: auto !important; border-radius: 8px; background: #fbf9f4; padding: 6px; box-shadow: 0 30px 60px -30px rgba(0,0,0,.9); }
  .ts-am-bundle__art img:nth-child(1) { left: 0; top: 12%; transform: rotate(-6deg); }
  .ts-am-bundle__art img:nth-child(2) { left: 27%; top: 0; transform: rotate(2deg); z-index: 2; }
  .ts-am-bundle__art img:nth-child(3) { right: 0; top: 16%; transform: rotate(7deg); }

  /* Ausmal-Widget (wie im Kritzelbuch) */
  .ts-am-pick { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.5rem; }
  .ts .ts-am-pick button { padding: 9px 14px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); background: transparent; color: var(--ts-text, #f6faf7);
    font: 600 11px/1 var(--ts-font-mono, 'JetBrains Mono', monospace); letter-spacing: .12em; text-transform: uppercase; cursor: pointer; transition: background .25s, color .25s, border-color .25s; }
  .ts .ts-am-pick button:hover { border-color: rgba(110, 231, 183, .45); }
  .ts .ts-am-pick button[aria-pressed="true"] { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts-paint { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1.25rem; margin-top: 1.5rem; align-items: start; }
  .ts-paint__paper { position: relative; padding: clamp(.6rem, 1.6vw, 1.25rem); border-radius: 8px; background: #fbf9f4; box-shadow: 0 1px 0 rgba(255,255,255,.7) inset, 0 40px 80px -36px rgba(0,0,0,.9), 0 2px 8px rgba(0,0,0,.35); }
  .ts-paint__canvas { display: block; width: 100%; height: auto; aspect-ratio: 1000 / 1100; border-radius: 4px; cursor: crosshair; touch-action: pan-y; background: #fff; }
  .ts-paint.is-brush .ts-paint__canvas { touch-action: none; }
  .ts .ts-paint__done { position: absolute; left: 50%; top: 1rem; transform: translate(-50%, -10px); padding: 8px 14px; border-radius: 999px; background: #1d4d3f; color: #f6faf7; font-size: 11px; opacity: 0; pointer-events: none; transition: opacity .3s, transform .4s var(--ts-ease-out); white-space: nowrap; }
  .ts .ts-paint__done.is-on { opacity: 1; transform: translate(-50%, 0); }
  .ts-paint__tools { display: grid; gap: 1rem; padding: 1.1rem; border-radius: 22px; }
  .ts .ts-paint__label { color: var(--ts-muted, #9aaba3); font-size: 10.5px; }
  .ts-paint__swatches { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: .5rem; margin-top: .5rem; }
  .ts .ts-paint__sw { position: relative; aspect-ratio: 1; width: 100%; border-radius: 50%; border: 2px solid rgba(255,255,255,.14); background: var(--c); cursor: pointer; transition: transform .25s var(--ts-ease-out), border-color .2s; }
  .ts .ts-paint__sw:hover { transform: scale(1.08); }
  .ts .ts-paint__sw[aria-pressed="true"] { border-color: #f6faf7; transform: scale(1.12); box-shadow: 0 0 0 3px rgba(110,231,183,.45); }
  .ts-paint__modes, .ts-paint__acts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .5rem; margin-top: .5rem; }
  .ts-paint__acts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .ts .ts-paint__btn { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .35rem; min-height: 64px; padding: .6rem .4rem; border-radius: 16px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); background: rgba(255,255,255,.03); color: var(--ts-text, #f6faf7); font: 500 12.5px/1.15 var(--ts-font-body, Inter, sans-serif); cursor: pointer; transition: background .25s, border-color .25s, color .25s; }
  .ts .ts-paint__btn:hover { border-color: rgba(110,231,183,.45); }
  .ts .ts-paint__btn[aria-pressed="true"] { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts .ts-paint__btn:disabled { opacity: .35; cursor: default; }
  .ts .ts-paint__size { display: flex; align-items: center; gap: .75rem; margin-top: .5rem; }
  .ts-paint__size input { flex: 1; accent-color: #6ee7b7; }
  .ts .ts-paint__hint { color: var(--ts-muted, #9aaba3); font-size: 13px; line-height: 1.5; }

  /* Motiv-Parade */
  .ts-am-zoo { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(.6rem, 1.6vw, 1.1rem); margin-top: 2rem; }
  .ts .ts-am-zoo figure { margin: 0; padding: clamp(.4rem, 1vw, .7rem); border-radius: 6px; background: #fbf9f4; transform: rotate(var(--r, 0deg)); box-shadow: 0 24px 50px -28px rgba(0,0,0,.85); transition: transform .5s var(--ts-ease-out); }
  .ts .ts-am-zoo figure:hover { transform: rotate(0deg) translateY(-5px) scale(1.03); }
  .ts-am-zoo svg, .ts-am-zoo img { display: block; width: 100% !important; height: auto !important; }
  .ts .ts-am-zoo figcaption { margin-top: .35rem; text-align: center; font: 800 clamp(8px, .9vw, 12px)/1 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: 0; text-transform: uppercase; color: #1b1f1c; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .ts .ts-am-zoo figcaption.is-long { font-size: clamp(6.5px, .68vw, 9.5px); }
  .ts .ts-am-zoo .ts-am-door { position: relative; }
  .ts .ts-am-zoo .ts-am-door b { position: absolute; left: .45rem; top: .4rem; min-width: 1.9rem; height: 1.9rem; display: grid; place-items: center; border-radius: 999px; background: #060608; color: #f6faf7; font: 700 12px/1 var(--ts-font-mono, monospace); }

  /* Gratis + Kita */
  .ts .ts-am-split { display: grid; gap: 2rem; margin-top: 2rem; padding: clamp(1.5rem, 3.5vw, 2.75rem); border-radius: 26px; align-items: center; }
  .ts-am-thumbs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .8rem; }
  .ts .ts-am-thumbs img { display: block; width: 100% !important; height: auto !important; border-radius: 6px; background: #fbf9f4; padding: 5px; box-shadow: 0 24px 50px -28px rgba(0,0,0,.85); }
  .ts-am-thumbs img:nth-child(1) { transform: rotate(-3deg); } .ts-am-thumbs img:nth-child(2) { transform: translateY(-8px) rotate(1.5deg); } .ts-am-thumbs img:nth-child(3) { transform: rotate(2.5deg); }
  .ts .ts-am-note { margin-top: 1rem; color: rgba(246,250,247,.5); font-size: 13px; line-height: 1.6; }
  .ts .ts-am-list { list-style: none; margin: 1.25rem 0 0; padding: 0; display: grid; gap: .7rem; }
  .ts .ts-am-list li { position: relative; padding-left: 1.6rem; color: var(--tss-text, rgba(246,250,247,.72)); line-height: 1.55; }
  .ts .ts-am-list li::before { content: ""; position: absolute; left: 0; top: .5em; width: 8px; height: 8px; border-radius: 50%; background: var(--tss-acc, #6ee7b7); }
  .ts .ts-am-list b { color: #f6faf7; }
  .ts .ts-am-final { margin-top: clamp(3rem, 6vw, 5rem); padding: clamp(1.75rem, 4vw, 3rem); border-radius: 26px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.5rem; }
  .ts .ts-am-final p { font: 800 clamp(1.5rem, 3vw, 2.4rem)/1.05 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.025em; margin: 0; }

  @media (min-width: 640px) {
    .ts-am-zoo { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  }
  @media (min-width: 1024px) {
    .ts-paint { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: 2rem; }
    .ts-paint__tools { position: sticky; top: 110px; }
    .ts .ts-am-bundle, .ts .ts-am-split { grid-template-columns: minmax(0, 6fr) minmax(0, 5fr); gap: 3rem; }
    .ts-am-zoo { grid-template-columns: repeat(var(--cols, 6), minmax(0, 1fr)); }
  }
  @media (prefers-reduced-motion: reduce) {
    .ts .ts-am-zoo figure, .ts-am-bundle__art img, .ts-am-thumbs img { transform: none !important; }
    .ts-am-season .is-now .ts-am-season__state::before { animation: none; }
  }
</style>
'''

# ======================================================================= JS: Ausmal-Widget
PAINT_JS = r'''
<script>
/* Ausmalen: Farbeimer, Pinsel, Radierer, Zurück, Neu, Speichern, Drucken – mehrere Motive zur Auswahl */
(() => {
  document.querySelectorAll('[data-am-paint]').forEach(root => {
    const MOTIVE = JSON.parse(root.querySelector('script[type="application/json"]').textContent);
    const COLORS = ['#e8505b', '#f6a33b', '#f7d046', '#8bc34a', '#2e9e6a', '#5ec8e5', '#3f7fd9', '#9b6ad6', '#f29bc4', '#a0683f', '#7d7d7d', '#2b2b2b'];
    const NAMES = ['Rot', 'Orange', 'Gelb', 'Hellgrün', 'Grün', 'Hellblau', 'Blau', 'Lila', 'Rosa', 'Braun', 'Grau', 'Schwarz'];
    const cv = root.querySelector('canvas'), ctx = cv.getContext('2d');
    const W = cv.width, H = cv.height;
    const paint = document.createElement('canvas'); paint.width = W; paint.height = H;
    const pctx = paint.getContext('2d', { willReadFrequently: true });
    const msg = root.querySelector('[data-paint-msg]'), undoBtn = root.querySelector('[data-act="undo"]'), size = root.querySelector('[data-paint-size]');
    const pick = root.querySelector('[data-am-pick]');
    let wall = null, color = COLORS[2], mode = 'fill', stack = [], drawing = false, last = null, msgT, cur = null, img = null;

    /* Saison-Motiv zuerst: data-default oder Saison nach Datum */
    const seasonKey = () => {
      const d = new Date(), md = (d.getMonth() + 1) * 100 + d.getDate();
      const s = md >= 1001 && md <= 1031 ? 'halloween' : md >= 1101 && md <= 1111 ? 'laterne' : md >= 1112 && md <= 1224 ? 'advent' : (md >= 1225 || md <= 228) ? 'winter' : null;
      const m = MOTIVE.find(x => x.saison === s); return m ? m.key : MOTIVE[0].key;
    };

    const sw = root.querySelector('[data-paint-colors]');
    sw.innerHTML = COLORS.map((c, i) => `<button type="button" class="ts-paint__sw" style="--c:${c}" data-c="${c}" aria-label="${NAMES[i]}" aria-pressed="${c === color}"></button>`).join('');
    sw.addEventListener('click', e => {
      const b = e.target.closest('[data-c]'); if (!b) return;
      color = b.dataset.c; sw.querySelectorAll('[data-c]').forEach(x => x.setAttribute('aria-pressed', x === b));
      if (mode === 'erase') setMode('fill');
    });
    const setMode = m => {
      mode = m; root.classList.toggle('is-brush', m !== 'fill');
      root.querySelectorAll('[data-mode]').forEach(b => b.setAttribute('aria-pressed', b.dataset.mode === m));
    };
    root.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

    const say = (t, ms = 1600) => { msg.textContent = t; msg.classList.add('is-on'); clearTimeout(msgT); msgT = setTimeout(() => msg.classList.remove('is-on'), ms); };
    const render = () => { ctx.globalCompositeOperation = 'source-over'; ctx.drawImage(paint, 0, 0); if (img) { ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(img, 0, 0, W, H); } ctx.globalCompositeOperation = 'source-over'; };
    const key = () => 'ts-am-' + cur.key;
    const store = () => { try { localStorage.setItem(key(), paint.toDataURL('image/png')); } catch (e) {} };
    const push = () => { stack.push(pctx.getImageData(0, 0, W, H)); if (stack.length > 20) stack.shift(); undoBtn.disabled = false; };
    const hex = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));

    /* Farbeimer: füllt die Fläche innerhalb der schwarzen Linien */
    const fill = (x, y) => {
      x = Math.round(x); y = Math.round(y);
      if (!wall || x < 0 || y < 0 || x >= W || y >= H || wall[y * W + x]) return false;
      push();
      const id = pctx.getImageData(0, 0, W, H), d = id.data, [r, g, b] = mode === 'erase' ? [255, 255, 255] : hex(color);
      const seen = new Uint8Array(W * H), q = new Int32Array(W * H); let h = 0, t = 0;
      q[t++] = y * W + x; seen[y * W + x] = 1;
      while (h < t) {
        const p = q[h++], px = p % W;
        const o = p * 4; d[o] = r; d[o + 1] = g; d[o + 2] = b; d[o + 3] = 255;
        const n = [px > 0 ? p - 1 : -1, px < W - 1 ? p + 1 : -1, p - W, p + W];
        for (let k = 0; k < 4; k++) { const v = n[k]; if (v >= 0 && v < W * H && !seen[v]) { seen[v] = 1; if (!wall[v]) q[t++] = v; else { const vo = v * 4; d[vo] = r; d[vo + 1] = g; d[vo + 2] = b; d[vo + 3] = 255; } } }
      }
      pctx.putImageData(id, 0, 0); render(); store(); return true;
    };
    const pos = e => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height]; };
    const stroke = (a, b) => {
      pctx.strokeStyle = mode === 'erase' ? '#ffffff' : color; pctx.lineCap = 'round'; pctx.lineJoin = 'round';
      pctx.lineWidth = +size.value * (mode === 'erase' ? 1.4 : 1);
      pctx.beginPath(); pctx.moveTo(a[0], a[1]); pctx.lineTo(b[0], b[1]); pctx.stroke(); render();
    };
    cv.addEventListener('pointerdown', e => {
      if (!wall) return;
      if (mode === 'fill') { if (fill(...pos(e))) { let tip = true; try { tip = !sessionStorage.getItem('ts-am-tip'); sessionStorage.setItem('ts-am-tip', '1'); } catch (er) {} if (tip) say('Toll! Nächste Fläche antippen'); } return; }
      e.preventDefault(); cv.setPointerCapture(e.pointerId); push(); drawing = true; last = pos(e); stroke(last, [last[0] + .01, last[1]]);
    });
    cv.addEventListener('pointermove', e => { if (!drawing) return; const p = pos(e); stroke(last, p); last = p; });
    const end = () => { if (drawing) { drawing = false; store(); } };
    cv.addEventListener('pointerup', end); cv.addEventListener('pointercancel', end); cv.addEventListener('pointerleave', end);

    undoBtn.addEventListener('click', () => { const s = stack.pop(); if (s) { pctx.putImageData(s, 0, 0); render(); store(); } undoBtn.disabled = !stack.length; });
    root.querySelector('[data-act="clear"]').addEventListener('click', () => { push(); pctx.fillStyle = '#fff'; pctx.fillRect(0, 0, W, H); render(); try { localStorage.removeItem(key()); } catch (e) {} say('Neues Blatt'); });
    const compose = () => {
      const out = document.createElement('canvas'); out.width = W; out.height = H + 70; const o = out.getContext('2d');
      o.fillStyle = '#fff'; o.fillRect(0, 0, out.width, out.height); o.drawImage(cv, 0, 0);
      o.fillStyle = '#7d7d7d'; o.font = '500 20px Inter, Arial, sans-serif'; o.textAlign = 'center';
      o.fillText(cur.paket + ' · trutzstaehler.de', W / 2, H + 44);
      return out.toDataURL('image/png');
    };
    root.querySelector('[data-act="save"]').addEventListener('click', () => {
      const a = document.createElement('a'); a.download = 'mein-' + cur.file + '.png'; a.href = compose(); document.body.appendChild(a); a.click(); a.remove(); say('Bild gespeichert');
    });
    root.querySelector('[data-act="print"]').addEventListener('click', () => {
      const w = window.open('', '_blank');
      if (!w) { say('Pop-up blockiert – nutze „Speichern“', 4000); return; }
      w.document.write('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Mein Ausmalbild</title><style>@page{margin:10mm}html,body{margin:0;height:100%;background:#fff}body{display:flex;align-items:center;justify-content:center}img{display:block;max-width:100%;max-height:100vh;object-fit:contain}</style></head><body><img alt="Mein ausgemaltes Bild"></body></html>');
      w.document.close();
      const im = w.document.querySelector('img'), go = () => { w.focus(); w.print(); };
      w.onafterprint = () => w.close();
      im.onload = go; im.src = compose();
      say('Druckansicht geöffnet');
    });

    /* Motiv laden: Linien als Wände merken, gespeichertes Bild wiederherstellen */
    const load = k => {
      cur = MOTIVE.find(m => m.key === k) || MOTIVE[0]; stack = []; undoBtn.disabled = true; wall = null;
      cv.setAttribute('aria-label', 'Ausmalbild ' + cur.name + ' – tippe hinein, um Flächen auszumalen');
      if (pick) pick.querySelectorAll('[data-k]').forEach(b => b.setAttribute('aria-pressed', b.dataset.k === cur.key));
      const im = new Image();
      im.onload = () => {
        img = im;
        const t = document.createElement('canvas'); t.width = W; t.height = H; const tc = t.getContext('2d');
        tc.fillStyle = '#fff'; tc.fillRect(0, 0, W, H); tc.drawImage(im, 0, 0, W, H);
        const d = tc.getImageData(0, 0, W, H).data; wall = new Uint8Array(W * H);
        for (let i = 0; i < W * H; i++) wall[i] = d[i * 4] < 140 ? 1 : 0;
        pctx.fillStyle = '#fff'; pctx.fillRect(0, 0, W, H);
        let saved = null; try { saved = localStorage.getItem(key()); } catch (e) {}
        if (saved) { const s = new Image(); s.onload = () => { pctx.drawImage(s, 0, 0); render(); }; s.src = saved; } else render();
      };
      im.src = cur.src;
    };
    if (pick) {
      pick.innerHTML = MOTIVE.map(m => `<button type="button" data-k="${m.key}" aria-pressed="false">${m.name}</button>`).join('');
      pick.addEventListener('click', e => { const b = e.target.closest('[data-k]'); if (b) load(b.dataset.k); });
    }
    load(root.dataset.default || seasonKey());
  });
})();
</script>
'''


def paint_block(motive, default=None, head_left="[ Probier's aus ]", head_right='Direkt im Browser', titel='Mal gleich los.',
                sub='Farbe antippen, dann ins Bild tippen – der Farbeimer füllt die ganze Fläche. Mit dem Pinsel kannst du frei malen. Fertig? Speichere dein Bild oder drucke es aus.',
                anchor='ts-am-malen'):
    data = [dict(key=k, name=K.MOTIFS[k]['name'].title(), file=k, src=lines_uri(k), saison=K.MOTIFS[k]['pack'],
                 paket=KAT.paket(K.MOTIFS[k]['pack'])['name']) for k in motive]
    for d in data:  # Namen huebsch: KÜRBIS -> Kürbis
        d['name'] = d['name'].replace('Ä', 'ä').replace('Ö', 'ö').replace('Ü', 'ü') if d['name'].isupper() else d['name']
        d['file'] = d['name'].lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss').replace(' ', '-')
    dflt = f' data-default="{default}"' if default else ''
    pick = '<div class="ts-am-pick" role="group" aria-label="Motiv wählen" data-am-pick></div>' if len(motive) > 1 else ''
    return f'''
  <section id="{anchor}" class="ts-container ts-am__block" aria-labelledby="{anchor}-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">{esc(head_left)}</p><p class="ts-label ts-muted">{esc(head_right)}</p></div>
    <h2 id="{anchor}-t" class="ts-am__h2 ts-reveal">{titel}</h2>
    <p class="ts-am__sub ts-reveal">{esc(sub)}</p>
    <div class="ts-paint" data-am-paint{dflt}>
      <script type="application/json">{json.dumps(data, ensure_ascii=False)}</script>
      <div>
        {pick}
        <div class="ts-paint__paper ts-reveal" style="margin-top:1rem">
          <canvas class="ts-paint__canvas" width="1000" height="1100" role="img" aria-label="Ausmalbild"></canvas>
          <p class="ts-label ts-paint__done" data-paint-msg aria-live="polite"></p>
        </div>
      </div>
      <div class="ts-paint__tools ts-glass ts-reveal">
        <div><p class="ts-label ts-paint__label">Farbe</p><div class="ts-paint__swatches" role="group" aria-label="Farben" data-paint-colors></div></div>
        <div>
          <p class="ts-label ts-paint__label">Werkzeug</p>
          <div class="ts-paint__modes" role="group" aria-label="Werkzeug">
            <button type="button" class="ts-paint__btn" data-mode="fill" aria-pressed="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2a2 2 0 0 0 2.8 0L19 11Z"/><path d="m5 2 5 5M2 13h15M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4Z"/></svg>Farbeimer</button>
            <button type="button" class="ts-paint__btn" data-mode="brush" aria-pressed="false"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M9.06 11.9 17.1 3.86a2.83 2.83 0 1 1 4 4l-8.04 8.04"/><path d="M7.07 14.94c-1.66 0-3 1.35-3 3.02 0 1.33-2.5 1.52-2 2.02 1.08 1.1 2.49 2.02 4 2.02 2.2 0 4-1.8 4-4.04a3.01 3.01 0 0 0-3-3.02Z"/></svg>Pinsel</button>
            <button type="button" class="ts-paint__btn" data-mode="erase" aria-pressed="false"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m7 21-4.3-4.3a1 1 0 0 1 0-1.4l10-10a1 1 0 0 1 1.4 0l5.6 5.6a1 1 0 0 1 0 1.4L11 21M22 21H7M5 11l9 9"/></svg>Radierer</button>
          </div>
          <label class="ts-paint__size"><span class="ts-label ts-paint__label">Pinsel</span><input type="range" min="6" max="60" value="22" data-paint-size aria-label="Pinselgröße"></label>
        </div>
        <div class="ts-paint__acts">
          <button type="button" class="ts-paint__btn" data-act="undo" disabled><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg>Zurück</button>
          <button type="button" class="ts-paint__btn" data-act="clear"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>Neu</button>
          <button type="button" class="ts-paint__btn" data-act="save"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>Speichern</button>
          <button type="button" class="ts-paint__btn" data-act="print"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 9V3h12v6"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/></svg>Drucken</button>
        </div>
        <p class="ts-paint__hint">Tipp: Am Handy einfach mit dem Finger tippen. Dein Bild bleibt auf diesem Gerät gespeichert, bis du „Neu“ drückst.</p>
      </div>
    </div>
  </section>'''


def teile(body, wrap_open, scripts, namen):
    """Teilt einen Block an <!--@@TEIL@@--> in mehrere Code-Bloecke (je eigener Wrapper)."""
    parts = body.split('<!--@@TEIL@@-->')
    out = []
    for i, part in enumerate(parts):
        part = part.strip('\n')
        if i > 0:
            part = wrap_open + '\n' + part
        if i < len(parts) - 1:
            part = part + '\n</div>'
        hdr = f'<!-- ===== {namen[i]} ===== -->\n' if i > 0 else ''
        out.append(hdr + part + '\n' + scripts[i])
    return out


# ======================================================================= Kategorieseite
SAISON = [  # id, Datum-Label, Untertitel
    ('halloween', '31. Oktober', 'Freundliche Gruselfreunde – kein bisschen gruselig.'),
    ('laterne', '11. November', 'Sonne, Mond und Sterne – plus Laterne zum Basteln.'),
    ('advent', '1. – 24. Dezember', 'Jeden Tag ein Türchen zum Ausmalen.'),
    ('anhaenger', 'bis Heiligabend', 'Geschenkanhänger und Karten, von Kindern gemalt.'),
    ('winter', 'Dezember – Februar', 'Schneemann, Eisbär und Glücksschwein für Silvester.'),
]
# Zeitfenster (MMTT) fuer "Jetzt dran" – passt jedes Jahr
FENSTER = {'halloween': (1001, 1031), 'laterne': (1101, 1111), 'advent': (1112, 1224), 'anhaenger': (1201, 1224), 'winter': (1225, 228)}

SEASON_JS = r'''
<script>
/* Saison-Leiste: markiert „Jetzt dran“, „Als Nächstes“ und „Vorbei“ – jedes Jahr automatisch */
(() => {
  const list = document.querySelector('[data-am-season]'); if (!list) return;
  const d = new Date(), md = (d.getMonth() + 1) * 100 + d.getDate();
  const inWin = (a, b) => a <= b ? md >= a && md <= b : md >= a || md <= b;
  const items = [...list.querySelectorAll('[data-from]')];
  let next = null;
  items.forEach(li => {
    const a = +li.dataset.from, b = +li.dataset.to, st = li.querySelector('[data-state]');
    if (inWin(a, b)) { li.classList.add('is-now'); st.textContent = 'Jetzt dran'; }
    else if (a > b ? false : md > b && md < 1225) { li.classList.add('is-past'); st.textContent = 'Fürs nächste Jahr'; }
    else if (!next) { next = li; }
  });
  if (next && !list.querySelector('.is-now')) { next.querySelector('[data-state]').textContent = 'Als Nächstes'; }
  /* Countdown bis zum Fest */
  list.querySelectorAll('[data-fest]').forEach(li => {
    const [m, t] = li.dataset.fest.split('-').map(Number);
    let f = new Date(d.getFullYear(), m - 1, t); if (f < new Date(d.getFullYear(), d.getMonth(), d.getDate())) return;
    const n = Math.round((f - new Date(d.getFullYear(), d.getMonth(), d.getDate())) / 864e5);
    const st = li.querySelector('[data-state]');
    if (!li.classList.contains('is-now') || n > 60) return;
    st.textContent = n === 0 ? 'Heute!' : n === 1 ? 'Morgen ist es so weit' : 'Jetzt dran · noch ' + n + ' Tage';
  });
  /* Adventskalender: vor dem 1. Dezember Countdown, danach das heutige Türchen */
  const adv = list.querySelector('[data-am-advent].is-now [data-state]');
  if (adv) {
    if (md >= 1201 && md <= 1224) adv.textContent = 'Heute: Türchen ' + d.getDate();
    else { const n = Math.round((new Date(d.getFullYear(), 11, 1) - new Date(d.getFullYear(), d.getMonth(), d.getDate())) / 864e5); adv.textContent = n === 1 ? 'Morgen geht’s los' : 'Start in ' + n + ' Tagen'; }
  }
  /* aktuelle Saison zuerst sichtbar (Handy: horizontal scrollen) */
  const now = list.querySelector('.is-now') || next;
  if (now && list.scrollWidth > list.clientWidth) list.scrollLeft = now.offsetLeft - list.offsetLeft;
})();
</script>
'''
FEST = {'halloween': '10-31', 'laterne': '11-11', 'advent': '12-24', 'anhaenger': '12-24', 'winter': '12-31'}

FAQ = [
    ('Wie bekomme ich die Ausmalbilder?',
     'Direkt nach dem Kauf bekommst du eine E-Mail mit dem Download-Link. Du lädst eine PDF-Datei herunter (beim Saisonpaket und der Kita-Lizenz eine ZIP-Datei mit allen PDFs) und druckst die Seiten so oft aus, wie du möchtest. Es wird nichts verschickt.'),
    ('Für welches Alter sind die Bilder?',
     'Für Kinder ab etwa 2 Jahren – dicke Linien, große Flächen und zu jedem Bild der Name zum Mitlesen. Ältere Kinder (und Erwachsene) haben trotzdem Spaß: Die kleinen Details wie Glitzersterne und Muster wollen auch ausgemalt werden.'),
    ('Welches Papier und welcher Drucker?',
     'Jeder normale Drucker reicht, Schwarzweiß genügt. Drucke in A4, Hochformat, mit „Tatsächliche Größe“ bzw. 100 %. Für Filzstifte und die Laternen-Bastelvorlage empfehle ich etwas dickeres Papier (120–160 g/m²).'),
    ('Darf ich die Bilder in der Kita oder Schule kopieren?',
     'Die normalen Pakete sind für den privaten Gebrauch in deiner Familie. Für Kita, Schule, Hort, Verein oder Tagespflege gibt es die <a href="' + store(KAT.KITA['slug']) + '">Kita-Lizenz</a>: alle Pakete, kopieren für alle Gruppen einer Einrichtung, ohne Ablaufdatum – mit Lizenzurkunde.'),
    ('Kann ich auch auf dem Tablet malen?',
     'Ja! Oben auf dieser Seite kannst du einige Motive direkt im Browser ausmalen – mit Farbeimer, Pinsel und Speichern. Die PDFs lassen sich außerdem in Mal-Apps öffnen, die PDF-Dateien importieren können.'),
    ('Kann ich vom Kauf zurücktreten?',
     'Bei digitalen Inhalten erlischt das Widerrufsrecht, sobald der Download beginnt – darauf weise ich dich im Bestellprozess hin (siehe <a href="/widerruf">Widerrufsbelehrung</a>). Wenn etwas nicht funktioniert, schreib mir einfach: <a href="mailto:' + KAT.MAIL + '">' + KAT.MAIL + '</a>.'),
    ('Gibt es die Bilder auch als gedrucktes Buch?',
     'Die Saison-Pakete gibt es nur als PDF. Gedruckt gibt es meine Kritzelbücher mit Tieren und Dinos – mehr dazu im <a href="/kreativhafen">Kreativhafen</a>.'),
    ('Kommen noch weitere Pakete?',
     'Ja – für 2027 sind Fasching, Ostern und Muttertag geplant. Folge mir auf <a href="https://www.instagram.com/trutzstaehler/" target="_blank" rel="noopener">Instagram</a>, dann verpasst du nichts.'),
]


def jsonld():
    items = []
    for i, p in enumerate(KAT.PAKETE + [KAT.BUNDLE, KAT.KITA], 1):
        items.append({'@type': 'ListItem', 'position': i, 'item': {
            '@type': 'Product', 'name': f'{p["name"]} – {p["sub"]}', 'description': p['kurz'],
            'url': f'https://{KAT.DOMAIN}{store(p["slug"])}', 'brand': {'@type': 'Brand', 'name': 'Kreativhafen'},
            'offers': {'@type': 'Offer', 'price': f'{p["preis_cent"] / 100:.2f}', 'priceCurrency': 'EUR',
                       'availability': 'https://schema.org/InStock', 'url': f'https://{KAT.DOMAIN}{store(p["slug"])}'}}})
    data = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Ausmalbilder zum Ausdrucken – Kreativhafen', 'itemListElement': items}
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(__import__('re').sub('<[^>]+>', '', a))}} for q, a in FAQ]}
    return ('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'
            '<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + '</script>')


def kategorieseite():
    ein = KAT.euro(KAT.einzelsumme())
    seasons = ''
    for pid, datum, sub in SAISON:
        p = KAT.paket(pid); a, b = FENSTER[pid]
        adv = ' data-am-advent' if pid == 'advent' else ''
        seasons += (f'<li data-from="{a}" data-to="{b}" data-fest="{FEST[pid]}"{adv} style="--c:{p["farbe"]}"><a href="{store(p["slug"])}">'
                    f'<span class="ts-label ts-am-season__date">{esc(datum)}</span>'
                    f'<span class="ts-am-season__name">{esc(p["name"])}</span>'
                    f'<span class="ts-am-season__sub">{esc(sub)}</span>'
                    f'<span class="ts-label ts-am-season__state" data-state>{esc(p["preis"])}</span></a></li>')
    zoo_keys = ['hw01', 'hw02', 'hw09', 'lt01', 'lt03', 'lt08', 'ad06', 'ad11', 'ad24', 'wi01', 'wi05', 'wi08']
    rots = [-1.6, 1.2, -.7, 1.5, -1.1, .8]
    zoo = ''.join(f'<figure class="ts-reveal" style="--r:{rots[i % 6]}deg">{thumb_svg(k)}<figcaption{cap_cls(k)}>{esc(K.MOTIFS[k]["name"])}</figcaption></figure>' for i, k in enumerate(zoo_keys))
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in FAQ)
    B = KAT.BUNDLE
    body = f'''<!-- =====================================================================
  AUSMALBILDER – Kategorieseite /shop/ausmalbilder
  Einfügen: Seite „Ausmalbilder“ (URL /shop/ausmalbilder) → Code-Block → alles einfügen.
  Die Produktkacheln kommen automatisch aus TS_SHOP (kat: 'ausmalbilder').
  Gratis-PDF: Datei hochladen (Link → Datei) und bei Bedarf den Link {GRATIS_URL} anpassen.
====================================================================== -->
{CSS}
<div class="ts ts-am tss ts-bleed" style="padding-bottom:0">
  <div class="ts-am__orb" aria-hidden="true"></div>

  <section class="ts-container tss--top" aria-labelledby="ts-am-title" style="padding-bottom:0">
    <div class="tss-kicker"><p class="ts-label ts-muted">[ Shop — 03 Ausmalbilder ]</p><p class="ts-label ts-muted"><a href="/shop" style="color:inherit">← Zur Übersicht</a></p></div>
    <div class="tss-head">
      <h1 id="ts-am-title" class="tss-h1" data-ts-fit>Ausmal&shy;bilder<i>.</i></h1>
      <div>
        <p class="tss-lead">Kürbis, Laterne, 24 Türchen und ein Schneemann mit Zylinder: Ausmalbilder zum Ausdrucken – mit dicken Linien, großen Flächen und dem Namen zum Mitlesen. Sofort als PDF, für zu Hause oder die ganze Kita.</p>
        <ul class="ts-am__chips"><li class="ts-label">Ab 2 Jahren</li><li class="ts-label">52 Motive</li><li class="ts-label">PDF · A4</li><li class="ts-label">Sofort-Download</li></ul>
        <div class="ts-am__ctas">{btn('Pakete ansehen', '#ts-am-pakete', True, ARROW_DOWN, ' data-ts-no-trans')}{btn('Gratis probieren', '#ts-am-gratis', False, '', ' data-ts-no-trans')}</div>
      </div>
    </div>
    <ol class="ts-am-season ts-reveal" data-am-season aria-label="Die Saison im Überblick">{seasons}</ol>
  </section>

  <section id="ts-am-pakete" class="ts-container ts-am__block" aria-labelledby="ts-am-pakete-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Die Pakete ]</p><p class="ts-label ts-muted">Herbst &amp; Winter 2026</p></div>
    <h2 id="ts-am-pakete-t" class="ts-am__h2">Such dir deine Saison aus<i>.</i></h2>
    <div class="tss-grid" data-tss-grid="ausmalbilder" style="margin-top:2rem"></div>

    <div class="ts-am-bundle ts-glass ts-reveal">
      <div>
        <p class="ts-label ts-muted">[ Alles in einem ]</p>
        <h3 class="ts-am__h2" style="margin-top:1rem">Das Saison&shy;paket<i>.</i></h3>
        <p class="ts-am__sub">{esc(B['intro'])}</p>
        <p class="ts-am-bundle__price">{esc(B['preis'])} <s>einzeln {ein}</s></p>
        <div class="ts-am__ctas">{btn('Saisonpaket holen', store(B['slug']))}{btn('Für Kitas', '#ts-am-kita', False, '', ' data-ts-no-trans')}</div>
      </div>
      <div class="ts-am-bundle__art" aria-hidden="true"><img src="{bunt('lt03')}" alt="" loading="lazy" width="260" height="286"><img src="{bunt('ad11')}" alt="" loading="lazy" width="260" height="286"><img src="{bunt('wi05')}" alt="" loading="lazy" width="260" height="286"></div>
    </div>
  </section>

<!--@@TEIL@@-->
{paint_block(['hw01', 'lt01', 'ad11', 'ad24', 'wi01'])}

  <section class="ts-container ts-am__block" aria-labelledby="ts-am-zoo-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Ein Blick hinein ]</p><p class="ts-label ts-muted">12 von 52 Motiven</p></div>
    <h2 id="ts-am-zoo-t" class="ts-am__h2 ts-reveal">Große Flächen, dicke Linien<i>.</i></h2>
    <p class="ts-am__sub ts-reveal">Jedes Motiv hat seine eigene Seite – mit dem Namen in Buchstaben, die man ebenfalls ausmalen kann. Perfekt für kleine Hände und erste Malerfolge.</p>
    <div class="ts-am-zoo" style="--cols:6">{zoo}</div>
  </section>

<!--@@TEIL@@-->
  <section id="ts-am-gratis" class="ts-container ts-am__block" aria-labelledby="ts-am-gratis-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Gratis ]</p><p class="ts-label ts-muted">3 Motive · PDF</p></div>
    <div class="ts-am-split ts-glass ts-reveal">
      <div>
        <h2 id="ts-am-gratis-t" class="ts-am__h2" style="margin-top:0">Erst mal probieren<i>?</i></h2>
        <p class="ts-am__sub">Kürbis, Laterne und Tannenbaum – drei Motive zum Ausdrucken, ganz ohne Anmeldung. Damit ihr seht, ob die Bilder zu euren Kindern passen.</p>
        <div class="ts-am__ctas">{btn('Probierpaket herunterladen', GRATIS_URL, True, '<svg class="ts-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>', ' download')}</div>
        <p class="ts-am-note">PDF, A4, ca. 0,3 MB · für den privaten Gebrauch</p>
      </div>
      <div class="ts-am-thumbs" aria-hidden="true"><img src="{bunt('hw01')}" alt="" loading="lazy" width="260" height="286"><img src="{bunt('lt01')}" alt="" loading="lazy" width="260" height="286"><img src="{bunt('ad24')}" alt="" loading="lazy" width="260" height="286"></div>
    </div>
  </section>

  <section id="ts-am-kita" class="ts-container ts-am__block" aria-labelledby="ts-am-kita-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Für Kitas &amp; Schulen ]</p><p class="ts-label ts-muted">{esc(KAT.KITA['preis'])} · eine Einrichtung</p></div>
    <div class="ts-am-split ts-glass ts-reveal">
      <div>
        <h2 id="ts-am-kita-t" class="ts-am__h2" style="margin-top:0">Kopieren für alle Gruppen<i>.</i></h2>
        <p class="ts-am__sub">{esc(KAT.KITA['intro'])}</p>
        <div class="ts-am__ctas">{btn('Kita-Lizenz holen', store(KAT.KITA['slug']))}{btn('Rechnung für den Träger?', 'mailto:' + KAT.MAIL + '?subject=Kita-Lizenz%20Ausmalbilder', False, '')}</div>
      </div>
      <ul class="ts-am-list">
        <li><b>Alle 5 Pakete:</b> 52 Motive, Laternen-Bastelvorlage, Liedblatt, Türchen-Plan, 16 Anhänger und 4 Karten</li>
        <li><b>Eine Einrichtung, alle Gruppen:</b> drucken und kopieren, so oft ihr wollt</li>
        <li><b>Ohne Ablaufdatum</b> – auch nächstes Jahr wieder nutzbar</li>
        <li><b>Mit Lizenzurkunde</b> zum Abheften – für Leitung und Träger</li>
        <li><b>Saisonfertig:</b> Laternenfest, Adventskalender für die Gruppe, Weihnachtsgeschenke der Kinder</li>
      </ul>
    </div>
  </section>

  <section class="ts-container ts-am__block" aria-labelledby="ts-am-how-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ So einfach geht's ]</p><p class="ts-label ts-muted">01 / 03</p></div>
    <h2 id="ts-am-how-t" class="ts-am__h2 ts-reveal" style="margin-bottom:2rem">In drei Minuten am Maltisch<i>.</i></h2>
    <div class="tss-steps ts-reveal">
      <div class="tss-step"><h3>Aussuchen &amp; bezahlen</h3><p>Paket wählen und sicher über den Squarespace-Checkout bezahlen – mit Karte, PayPal &amp; Co.</p></div>
      <div class="tss-step"><h3>Download per Mail</h3><p>Sofort nach dem Kauf kommt der Download-Link. Kein Versand, kein Warten, kein Abo.</p></div>
      <div class="tss-step"><h3>Drucken &amp; malen</h3><p>A4, Schwarzweiß, so oft ihr wollt. Bild verkleckert? Einfach neu ausdrucken.</p></div>
    </div>
  </section>

  <section class="ts-container ts-am__block ts-am__end" aria-labelledby="ts-am-faq-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Fragen &amp; Antworten ]</p></div>
    <h2 id="ts-am-faq-t" class="ts-am__h2 ts-reveal" style="margin-bottom:1.5rem">Gut zu wissen<i>.</i></h2>
    <div class="tss-faq ts-reveal">{faq}</div>
    <div class="ts-am-final ts-glass ts-reveal">
      <p>Lust auf alle 52 Motive?</p>
      {btn('Saisonpaket für ' + B['preis'], store(B['slug']))}
    </div>
  </section>
</div>'''
    wrap_open = '<div class="ts ts-am tss ts-bleed" style="padding:0">'
    return teile(body, wrap_open, [jsonld() + SEASON_JS, PAINT_JS, ''],
                 ['Teil 1/3: Kopf, Saison-Leiste, Pakete, Saisonpaket (enthält das CSS für alle Teile – muss auf derselben Seite sein)',
                  'Teil 2/3: Ausmal-Widget + Motivvorschau', 'Teil 3/3: Gratis, Kita, So geht’s, FAQ'])


# ======================================================================= Produkt-Zusatzinfos
def produkt_block(p):
    pid = p['id']
    n = len(p['motive'])
    rots = [-1.6, 1.2, -.7, 1.5, -1.1, .8]
    if pid == 'advent':
        zoo = ''.join(f'<figure class="ts-reveal ts-am-door" style="--r:{rots[i % 6]}deg"><b>{i}</b>{thumb_svg(k)}<figcaption{cap_cls(k)}>{esc(K.MOTIFS[k]["name"])}</figcaption></figure>'
                      for i, k in enumerate(p['motive'], 1))
    else:
        zoo = ''.join(f'<figure class="ts-reveal" style="--r:{rots[i % 6]}deg">{thumb_svg(k)}<figcaption{cap_cls(k)}>{esc(K.MOTIFS[k]["name"])}</figcaption></figure>'
                      for i, k in enumerate(p['motive']))
    cols = 6 if n in (12, 24) else (5 if n == 10 else 4)
    widget_keys = {'halloween': ['hw01', 'hw04', 'hw09'], 'laterne': ['lt01', 'lt03', 'lt04'], 'advent': ['ad11', 'ad06', 'ad24'],
                   'winter': ['wi01', 'wi05', 'wi08'], 'anhaenger': ['ad10', 'ad09']}[pid]
    extras = ''.join(f'<li>{esc(e)}</li>' for e in p['extras'])
    if pid == 'anhaenger':
        sd = os.path.join(HERE, 'build', 'seiten', 'anhaenger')
        pages = ''.join(f'<figure class="ts-reveal" style="--r:{r}deg"><img src="{webp_uri(os.path.join(sd, f), 420)}" alt="{alt}" loading="lazy" width="420" height="594"><figcaption>{cap}</figcaption></figure>'
                        for f, r, alt, cap in [('p-2.png', -1.2, 'Seite mit 8 Geschenkanhängern zum Ausmalen', 'ANHÄNGER 1/2'),
                                               ('p-3.png', 1, 'Seite mit 8 weiteren Geschenkanhängern', 'ANHÄNGER 2/2'),
                                               ('p-4.png', -.6, 'Seite mit 4 Karten zum Ausmalen', 'KARTEN')])
        zoo_sec = f'''
  <section class="ts-container ts-am__block" aria-labelledby="ts-am-zoo-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Im Paket ]</p><p class="ts-label ts-muted">16 Anhänger · 4 Karten</p></div>
    <h2 id="ts-am-zoo-t" class="ts-am__h2 ts-reveal">Ausmalen, ausschneiden, verschenken<i>.</i></h2>
    <p class="ts-am__sub ts-reveal">Jeder Anhänger hat ein Loch fürs Geschenkband und Platz für „Für“ und „Von“. Die Karten: zweimal Frohe Weihnachten, einmal Gutes neues Jahr und ein großes Dankeschön.</p>
    <div class="ts-am-zoo" style="--cols:3">{pages}</div>
  </section>'''
    else:
        zoo_sec = '' if not n else f'''
  <section class="ts-container ts-am__block" aria-labelledby="ts-am-zoo-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Im Paket ]</p><p class="ts-label ts-muted">{n} Motive · je eine Seite</p></div>
    <h2 id="ts-am-zoo-t" class="ts-am__h2 ts-reveal">{"24 Türchen, 24 Bilder" if pid == "advent" else str(n) + " Motive warten auf Farbe"}<i>.</i></h2>
    <p class="ts-am__sub ts-reveal">Jedes Bild hat seine eigene A4-Seite – mit dicken Linien, großen Flächen und dem Namen zum Mitlesen.</p>
    <div class="ts-am-zoo" style="--cols:{cols}">{zoo}</div>
  </section>'''
    body = f'''<!-- =====================================================================
  AUSMALBILDER – Zusatzinfos für das Produkt „{p['name']}“ ({store(p['slug'])})
  Einfügen: Produkt bearbeiten → Bereich „Zusätzliche Informationen“ → Code-Block → alles einfügen.
====================================================================== -->
{CSS}
<div class="ts ts-am" style="--tss-acc:{p['farbe']}">
{paint_block(widget_keys, widget_keys[0], "[ Probier's aus ]", 'Motiv aus dem Paket', 'Erst mal ausprobieren<i>.</i>',
             'Ein paar Motive aus diesem Paket kannst du hier direkt ausmalen: Farbe antippen, ins Bild tippen – fertig. Speichern und Drucken geht auch.', 'ts-am-malen')}
<!--@@TEIL@@-->
{zoo_sec}
{'<!--@@TEIL@@-->' if pid in ('advent', 'anhaenger') else ''}
  <section class="ts-container ts-am__block ts-am__end" aria-labelledby="ts-am-extra-t">
    <div class="ts-am__blockhead ts-reveal"><p class="ts-label ts-muted">[ Außerdem drin ]</p></div>
    <div class="ts-am-split ts-glass ts-reveal">
      <div>
        <h2 id="ts-am-extra-t" class="ts-am__h2" style="margin-top:0">Mehr als nur Bilder<i>.</i></h2>
        <ul class="ts-am-list">{extras}<li>Eine Seite für Eltern mit Drucktipps</li></ul>
      </div>
      <div class="ts-am-thumbs" aria-hidden="true">{''.join(f'<img src="{bunt(k)}" alt="" loading="lazy" width="260" height="286">' for k in (p['cover']))}</div>
    </div>
    <div class="ts-am-final ts-glass ts-reveal">
      <p>Alle 5 Pakete für {esc(KAT.BUNDLE['preis'])}?</p>
      {btn('Zum Saisonpaket', store(KAT.BUNDLE['slug']))}
    </div>
  </section>
</div>'''
    wrap_open = f'<div class="ts ts-am" style="--tss-acc:{p["farbe"]}">'
    n_t = 3 if pid in ('advent', 'anhaenger') else 2
    namen = [f'Teil 1/{n_t} für „{p["name"]}“: Ausmal-Widget (enthält das CSS – zuerst einfügen)',
             f'Teil 2/{n_t} für „{p["name"]}“: ' + ('Motive' if n_t == 3 else 'Motive + Extras'), f'Teil 3/3 für „{p["name"]}“: Extras']
    return teile(body, wrap_open, [PAINT_JS, '', ''][:n_t], namen[:n_t])


# ======================================================================= Teaser + TS_SHOP
def teaser():
    tiles = ''.join(f'<img src="{bunt(k, 240)}" alt="" loading="lazy" width="260" height="286">' for k in ('hw01', 'lt01', 'ad24'))
    return f'''<!-- =====================================================================
  AUSMALBILDER – Teaser für Startseite oder Kreativhafen (Code-Block)
  Zeigt automatisch die aktuelle Saison an.
====================================================================== -->
<style>
  .ts-am-teaser {{ padding: clamp(3rem, 7vw, 6rem) 0; }}
  .ts .ts-am-teaser__box {{ display: grid; gap: 2rem; padding: clamp(1.5rem, 4vw, 3rem); border-radius: 26px; align-items: center; }}
  .ts .ts-am-teaser__t {{ margin-top: 1rem; font: 800 clamp(2rem, 5vw, 4rem)/.98 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.035em; }}
  .ts .ts-am-teaser__t i {{ font-style: normal; color: #6ee7b7; }}
  .ts .ts-am-teaser__p {{ margin-top: .9rem; max-width: 36rem; color: rgba(246,250,247,.72); line-height: 1.65; }}
  .ts-am-teaser__ctas {{ display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.5rem; }}
  .ts-am-teaser__art {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .8rem; }}
  .ts .ts-am-teaser__art img {{ display: block; width: 100% !important; height: auto !important; border-radius: 6px; background: #fbf9f4; padding: 5px; box-shadow: 0 24px 50px -28px rgba(0,0,0,.85); }}
  .ts-am-teaser__art img:nth-child(1) {{ transform: rotate(-3deg); }} .ts-am-teaser__art img:nth-child(2) {{ transform: translateY(-10px) rotate(1.5deg); }} .ts-am-teaser__art img:nth-child(3) {{ transform: rotate(2.5deg); }}
  @media (min-width: 1024px) {{ .ts .ts-am-teaser__box {{ grid-template-columns: minmax(0, 6fr) minmax(0, 5fr); gap: 3rem; }} }}
</style>
<section class="ts ts-am-teaser" aria-labelledby="ts-am-teaser-t">
  <div class="ts-container">
  <div class="ts-am-teaser__box ts-glass ts-reveal">
    <div>
      <p class="ts-label ts-muted" data-am-teaser-label>[ Neu im Kreativhafen · Ausmalbilder ]</p>
      <h2 id="ts-am-teaser-t" class="ts-am-teaser__t" data-am-teaser-title>Malen durch die Saison<i>.</i></h2>
      <p class="ts-am-teaser__p">Halloween, Laternenzeit, 24 Türchen zum Ausmalen und Winter: Ausmalbilder zum Ausdrucken – sofort als PDF. Drei Motive gibt es gratis.</p>
      <div class="ts-am-teaser__ctas">{btn('Zu den Ausmalbildern', '/shop/ausmalbilder')}{btn('Gratis probieren', '/shop/ausmalbilder#ts-am-gratis', False, '')}</div>
    </div>
    <div class="ts-am-teaser__art" aria-hidden="true">{tiles}</div>
  </div>
  </div>
</section>
<script>
/* Überschrift passend zur Saison */
(() => {{
  const t = document.querySelector('[data-am-teaser-title]'); if (!t) return;
  const d = new Date(), md = (d.getMonth() + 1) * 100 + d.getDate();
  const s = md >= 1001 && md <= 1031 ? 'Halloween kann kommen' : md >= 1101 && md <= 1111 ? 'Laterne, Laterne' : md >= 1112 && md <= 1130 ? 'Bald geht’s los: 24 Türchen' : md >= 1201 && md <= 1224 ? '24 Türchen zum Ausmalen' : (md >= 1225 || md <= 228) ? 'Malen, wenn’s draußen schneit' : null;
  if (s) t.innerHTML = s + '<i>.</i>';
}})();
</script>'''


def ts_shop():
    lines = []
    for p in KAT.PAKETE + [KAT.BUNDLE, KAT.KITA]:
        hi = ', highlight: true' if p['id'] in ('bundle',) else ''
        lines.append(f"    {{ kat: 'ausmalbilder', id: 'am-{p['id']}', icon: '✎', titel: {json.dumps(p['name'], ensure_ascii=False)}, "
                     f"text: {json.dumps(p['sub'] + '. ' + p['kurz'], ensure_ascii=False)}, preis: '{p['preis']}', link: '{store(p['slug'])}'{hi} }},")
    return f'''/* =====================================================================
   AUSMALBILDER – Ergänzungen für window.TS_SHOP (Einstellungen → Erweitert → Code-Injection)
   1) In  kategorien: [ … ]  diese Zeile ergänzen (Komma an der vorherigen Zeile nicht vergessen):
====================================================================== */
    {{ id: 'ausmalbilder', nr: '03', titel: 'Ausmalbilder', text: 'Halloween, Laterne, Adventskalender und Winter – Ausmalbilder zum Ausdrucken, sofort als PDF.', link: '/shop/ausmalbilder', farbe: 'rgb(110, 231, 183)' }}

/* =====================================================================
   2) In  produkte: [ … ]  diese Zeilen ergänzen (z. B. ganz am Ende, vor der schließenden Klammer ] ):
      Die Produktbilder holt sich die Kachel automatisch vom Squarespace-Produkt.
====================================================================== */
{chr(10).join(lines)}

/* =====================================================================
   3) Brotkrumen auf den Produktseiten („Shop › …“ soll „Ausmalbilder“ zeigen):
      Im Skript „Produktseiten (Squarespace-Store) im Design“ diese Zeile suchen:
        : /eigenes-thema/i.test(pth) ? ['/shop/stream-widgets/eigener-stil', 'Dein eigener Stil']
      und DIREKT DAVOR diese Zeile einfügen:
====================================================================== */
      : /\\/store\\/p\\/ausmalbilder-/i.test(pth) ? ['/shop/ausmalbilder', 'Ausmalbilder']
'''


# ======================================================================= Vorschau
def preview(name, block, title):
    """Vorschau mit dem echten globalen CSS/JS der Seite (aus der Live-Seite gelesen)."""
    assets = os.path.join(HERE, 'vorschau-assets')
    gcss = open(os.path.join(assets, 'global.css'), encoding='utf-8').read()
    gjs = open(os.path.join(assets, 'global.js'), encoding='utf-8').read()
    shop = open(os.path.join(OUT, '03_ts-shop-ergaenzung.js'), encoding='utf-8').read()
    # TS_SHOP-Eintraege fuer die Vorschau einspielen
    import re
    prods = re.findall(r"^\s*\{ kat: 'ausmalbilder'.*$", shop, re.M)
    cat = re.search(r"^\s*\{ id: 'ausmalbilder'.*$", shop, re.M).group(0)
    inject = f"<script>window.__AM_PRODS=[{''.join(prods)}];window.__AM_CAT={cat};</script>"
    gjs = gjs.replace("window.TS_SHOP = {", "window.TS_SHOP = {", 1)
    bilder = {p['slug']: 'file://' + os.path.abspath(os.path.join(BILDER, 'produkte', p['slug'], '1-titel.jpg')) for p in KAT.PAKETE + [KAT.BUNDLE, KAT.KITA]}
    gjs = gjs.replace("window.TS_SHOP = {", "window.__AM_BILD=" + json.dumps(bilder) + ";window.TS_SHOP = {", 1)
    gjs = gjs.replace("const run = () => {", "(window.TS_SHOP.produkte=window.TS_SHOP.produkte.concat((window.__AM_PRODS||[]).map(p=>Object.assign({},p,{bild:window.__AM_BILD[p.link.split('/').pop()]})))),window.TS_SHOP.kategorien.push(window.__AM_CAT);\n  const run = () => {", 1)
    doc = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vorschau – {esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Syne:wght@600;700;800&display=swap" rel="stylesheet">
<style>{gcss}</style>
<style>body{{margin:0;background:#060608;color:#f6faf7;font-family:Inter,system-ui,sans-serif}} .am-prev-bar{{position:sticky;top:0;z-index:99;background:#1d4d3f;color:#f6faf7;font:600 12px/1 JetBrains Mono,monospace;letter-spacing:.12em;text-transform:uppercase;padding:10px 16px}}</style>
{inject}
</head><body><div class="am-prev-bar">Vorschau · {esc(title)} · ohne Squarespace-Kopf/Fuß</div>
{block}
<script>{gjs}</script>
<script>/* Vorschau: alle Einblendungen sofort zeigen (auf der Seite macht das dein globales Skript) */
document.querySelectorAll('.ts-reveal').forEach(e=>e.classList.add('is-in'));</script>
</body></html>'''
    os.makedirs(PREV, exist_ok=True)
    open(os.path.join(PREV, name), 'w', encoding='utf-8').write(doc)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {}
    kat = kategorieseite()
    for i, t in enumerate(kat, 1):
        files[f'01-{i}_kategorieseite_shop-ausmalbilder_teil-{i}-von-{len(kat)}.html'] = t
    prod = {}
    for i, p in enumerate(KAT.PAKETE, 1):
        prod[p['id']] = produkt_block(p)
        for j, t in enumerate(prod[p['id']], 1):
            files[f'02-{i}{"abc"[j - 1]}_produkt-zusatzinfo_{p["slug"]}_teil-{j}-von-{len(prod[p["id"]])}.html'] = t
    files['03_ts-shop-ergaenzung.js'] = ts_shop()
    files['04_teaser_startseite-oder-kreativhafen.html'] = teaser()
    for n, c in files.items():
        open(os.path.join(OUT, n), 'w', encoding='utf-8').write(c)
        print(f'{n:78s} {len(c.encode()) / 1024:6.1f} KB')
    preview('kategorieseite.html', '\n'.join(kat), 'Kategorieseite /shop/ausmalbilder')
    for p in KAT.PAKETE:
        preview(f'produkt-{p["id"]}.html', '\n'.join(prod[p['id']]), 'Zusatzinfo ' + p['name'])
    preview('teaser.html', files['04_teaser_startseite-oder-kreativhafen.html'], 'Teaser')


if __name__ == '__main__':
    main()

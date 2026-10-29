"""Kreativhafen gratis: Code-Bloecke fuer /ausmalbilder, /gute-nacht-geschichten, die Geschichten-Seiten,
die Reiter-Leiste und das Regal auf /kreativhafen.

python3 kreativhafen_web.py -> ../08-kreativhafen-gratis/*.html (+ vorschau/)
Die Daten (Motive, PDFs, Bilder) kommen aus dem Repo-Ordner /kreativhafen ueber raw.githubusercontent.com.
"""
import os, sys, json, html, re, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel as K
import motive  # noqa
import katalog as KAT
import website as WEB          # CSS, btn(), Pfeile, Vorschau-Helfer
from geschichten import ALLE as GESCHICHTEN

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '08-kreativhafen-gratis')
PREV = os.path.join(OUT, 'vorschau')
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
esc = html.escape
BASIS = KAT.GRATIS_URL_BASIS
GESCH_URL = '/geschichten/'          # Blog-Sammlung fuer die einzelnen Geschichten
ARROW, ARROW_DOWN, btn = WEB.ARROW, WEB.ARROW_DOWN, WEB.btn
DL_ICON = '<svg class="ts-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>'
KAT_JSON = json.load(open(os.path.join(REPO, 'kreativhafen', 'ausmalbilder', 'daten', 'katalog.json'), encoding='utf-8'))
N_MOTIVE = sum(len(p['motive']) for p in KAT.ALLE_PAKETE)
N_PAKETE = len(KAT.ALLE_PAKETE)


def name_von(key):
    n = K.MOTIFS[key]['name']
    return n[0] + n[1:].lower()


# ======================================================================= Reiter-Leiste
REITER = [('/kreativhafen', 'Übersicht'), ('/gute-nacht-geschichten', 'Gute-Nacht-Geschichten', 'gratis'),
          ('/ausmalbilder', 'Ausmalbilder', 'gratis'), ('/malbuecher', 'Malbücher'), ('/romane', 'Romane')]

REITER_CSS = '''
  .ts-khr { position: relative; z-index: 3; padding-top: calc(var(--ts-header-space, 96px) + 1rem); }
  .ts-khr__bar { display: flex; gap: .4rem; overflow-x: auto; scrollbar-width: none; padding: .35rem; border: 1px solid var(--ts-line, rgba(255,255,255,.08)); border-radius: 999px; background: rgba(255,255,255,.025); width: max-content; max-width: 100%; }
  .ts-khr__bar::-webkit-scrollbar { display: none; }
  .ts .ts-khr__bar a { display: inline-flex; align-items: center; gap: .45rem; padding: 10px 16px; border-radius: 999px; color: var(--ts-muted, #9aaba3); text-decoration: none; white-space: nowrap; font: 500 14px/1 var(--ts-font-body, Inter, sans-serif); transition: background .25s, color .25s; }
  .ts .ts-khr__bar a:hover { color: var(--ts-text, #f6faf7); background: rgba(255,255,255,.04); }
  .ts .ts-khr__bar a[aria-current="page"] { background: #f6faf7; color: #060608; }
  .ts .ts-khr__bar a i { font-style: normal; padding: 3px 7px; border-radius: 999px; background: rgba(110,231,183,.16); color: #6ee7b7; font: 700 9.5px/1 var(--ts-font-mono, monospace); letter-spacing: .1em; text-transform: uppercase; }
  .ts .ts-khr__bar a[aria-current="page"] i { background: #1d4d3f; color: #f6faf7; }
'''


def reiter_html():
    items = ''
    for r in REITER:
        badge = f' <i>{r[2]}</i>' if len(r) > 2 else ''
        items += f'<a href="{r[0]}">{esc(r[1])}{badge}</a>'
    return f'''<nav class="ts ts-khr" aria-label="Kreativhafen">
  <div class="ts-container"><div class="ts-khr__bar">{items}</div></div>
</nav>
<script>
/* Reiter: aktiven Bereich markieren (Geschichten-Seiten gehören zu „Gute-Nacht-Geschichten“) */
(() => {{
  const p = location.pathname.replace(/\\/+$/, '') || '/';
  document.querySelectorAll('.ts-khr__bar a').forEach(a => {{
    const h = a.getAttribute('href');
    if (p === h || (h === '/gute-nacht-geschichten' && p.indexOf('{GESCH_URL.rstrip('/')}') === 0)) {{ a.setAttribute('aria-current', 'page'); a.scrollIntoView({{ block: 'nearest', inline: 'center' }}); }}
  }});
}})();
</script>'''


def reiter_block():
    return f'''<!-- =====================================================================
  KREATIVHAFEN – Reiter-Leiste (Code-Block)
  Ganz oben auf /kreativhafen, /malbuecher und /romane einfügen.
  (Auf /ausmalbilder, /gute-nacht-geschichten und den Geschichten-Seiten ist sie schon enthalten.)
====================================================================== -->
<style>{REITER_CSS}</style>
{reiter_html()}'''


# ======================================================================= CSS (gemeinsam)
KH_CSS = WEB.CSS.replace('</style>', REITER_CSS + r'''
  /* ---------- Kreativhafen gratis ---------- */
  .ts-kh2 .tss--top { padding-top: clamp(2rem, 4vw, 3rem); }
  .ts-am-packs { display: grid; gap: 1rem; margin-top: 2rem; grid-template-columns: minmax(0, 1fr); }
  .ts .ts-am-pack { display: flex; flex-direction: column; border-radius: 22px; overflow: hidden; scroll-margin-top: 120px; }
  .ts-am-pack__img { position: relative; aspect-ratio: 3 / 2; background: #0b100e; overflow: hidden; }
  .ts .ts-am-pack__img img { display: block; width: 100% !important; height: 100% !important; object-fit: cover; transition: transform .7s var(--ts-ease-out); }
  .ts-am-pack:hover .ts-am-pack__img img { transform: scale(1.04); }
  .ts .ts-am-pack__nr { position: absolute; left: 1rem; top: .9rem; color: rgba(246,250,247,.6); }
  .ts .ts-am-pack__tag { position: absolute; right: .9rem; top: .8rem; padding: 6px 11px; border-radius: 999px; background: rgba(6,6,8,.65); border: 1px solid var(--c); color: var(--c); font-size: 10px; }
  .ts-am-pack__body { display: flex; flex-direction: column; gap: .55rem; flex: 1; padding: 1.25rem 1.35rem 1.4rem; }
  .ts .ts-am-pack__t { font: 800 clamp(1.3rem, 1.8vw, 1.6rem)/1.05 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.025em; margin: 0; }
  .ts .ts-am-pack__t i { font-style: normal; color: var(--c); }
  .ts .ts-am-pack__s { color: var(--ts-muted, #9aaba3); font-size: 14px; line-height: 1.55; margin: 0; }
  .ts-am-pack__acts { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: auto; padding-top: .9rem; }
  .ts .ts-am-mini { display: inline-flex; align-items: center; gap: .45rem; padding: 10px 14px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); background: transparent; color: var(--ts-text, #f6faf7); font: 600 13px/1 var(--ts-font-body, Inter, sans-serif); text-decoration: none; cursor: pointer; transition: background .25s, color .25s, border-color .25s; }
  .ts .ts-am-mini:hover { border-color: rgba(110,231,183,.5); }
  .ts .ts-am-mini--hi { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts .ts-am-mini--hi:hover { background: #6ee7b7; border-color: #6ee7b7; }
  .ts .ts-am-mini svg { flex: none; }
  /* Galerie */
  .ts-am-filter { display: flex; gap: .45rem; overflow-x: auto; scrollbar-width: none; margin-top: 1.5rem; padding-bottom: .25rem; }
  .ts-am-filter::-webkit-scrollbar { display: none; }
  .ts .ts-am-filter button { flex: none; padding: 9px 14px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); background: transparent; color: var(--ts-text, #f6faf7); font: 600 11px/1 var(--ts-font-mono, monospace); letter-spacing: .1em; text-transform: uppercase; cursor: pointer; }
  .ts .ts-am-filter button[aria-pressed="true"] { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts-am-gal { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(.6rem, 1.4vw, 1rem); margin-top: 1.5rem; min-height: 200px; }
  .ts .ts-am-tile { position: relative; margin: 0; padding: .55rem .55rem .6rem; border-radius: 8px; background: #fbf9f4; box-shadow: 0 24px 50px -28px rgba(0,0,0,.85); transform: rotate(var(--r, 0deg)); transition: transform .45s var(--ts-ease-out); }
  .ts .ts-am-tile:hover { transform: rotate(0deg) translateY(-4px); }
  .ts-am-tile > svg { display: block; width: 100% !important; height: auto !important; }
  .ts .ts-am-tile__acts svg { width: 15px !important; height: 15px !important; flex: none; }
  .ts-am-tile__acts { display: grid; grid-template-columns: 1fr 1fr; gap: .35rem; margin-top: .45rem; }
  .ts .ts-am-tile__acts button { display: inline-flex; align-items: center; justify-content: center; gap: .3rem; padding: 8px 6px; border-radius: 999px; border: 1px solid #d7d3c8; background: #fff; color: #1b1f1c; font: 600 11.5px/1 var(--ts-font-body, Inter, sans-serif); cursor: pointer; }
  .ts .ts-am-tile__acts button:hover { background: #1b1f1c; color: #fff; border-color: #1b1f1c; }
  .ts .ts-am-gal__msg { grid-column: 1 / -1; color: var(--ts-muted, #9aaba3); }
  /* Geschichten */
  .ts-gn-today { display: grid; gap: 1.5rem; margin-top: 2rem; padding: clamp(1.25rem, 3.5vw, 2.5rem); border-radius: 26px; align-items: center; }
  .ts .ts-gn-today img { display: block; width: 100% !important; max-width: 340px; height: auto !important; margin: 0 auto; border-radius: 10px; background: #fbf9f4; padding: 8px; transform: rotate(-2deg); box-shadow: 0 40px 70px -30px rgba(0,0,0,.9); }
  .ts .ts-gn-meta { display: flex; flex-wrap: wrap; gap: .45rem; margin: 1rem 0 0; padding: 0; list-style: none; }
  .ts .ts-gn-meta li { padding: 6px 11px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); color: var(--ts-text, #f6faf7); font-size: 10.5px; }
  .ts-gn-filter { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1.5rem; }
  .ts .ts-gn-filter button { padding: 9px 14px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); background: transparent; color: var(--ts-text, #f6faf7); font: 600 11px/1 var(--ts-font-mono, monospace); letter-spacing: .1em; text-transform: uppercase; cursor: pointer; }
  .ts .ts-gn-filter button[aria-pressed="true"] { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts-gn-grid { display: grid; gap: 1rem; margin-top: 1.5rem; grid-template-columns: minmax(0, 1fr); }
  .ts .ts-gn-card { display: flex; flex-direction: column; border-radius: 22px; overflow: hidden; color: inherit; text-decoration: none; transition: transform .5s var(--ts-ease-out); }
  .ts .ts-gn-card:hover { transform: translateY(-4px); }
  .ts-gn-card[hidden] { display: none !important; }
  .ts .ts-gn-card__img { display: grid; place-items: center; aspect-ratio: 16 / 10; background: radial-gradient(70% 80% at 50% 100%, rgba(46,140,108,.35), transparent 70%), linear-gradient(180deg, rgba(29,77,63,.25), rgba(12,17,15,.4)); }
  .ts .ts-gn-card__img img { width: 46% !important; height: auto !important; border-radius: 8px; background: #fbf9f4; padding: 5px; transform: rotate(var(--r, -2deg)); box-shadow: 0 30px 50px -26px rgba(0,0,0,.9); }
  .ts-gn-card__body { display: flex; flex-direction: column; gap: .5rem; flex: 1; padding: 1.2rem 1.35rem 1.4rem; }
  .ts .ts-gn-card__t { margin: 0; font: 800 clamp(1.2rem, 1.7vw, 1.45rem)/1.1 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.02em; }
  .ts .ts-gn-card__s { margin: 0; color: var(--ts-muted, #9aaba3); font-size: 14.5px; line-height: 1.6; }
  .ts .ts-gn-card__m { display: flex; flex-wrap: wrap; gap: .4rem; margin-top: auto; padding-top: .8rem; color: #6ee7b7; }
  /* Einzelne Geschichte */
  .ts-gn-story { max-width: 46rem; margin: 0 auto; }
  .ts .ts-gn-h1 { margin: 1.25rem 0 0; font: 800 clamp(2.2rem, 6vw, 4.6rem)/.98 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.035em; }
  .ts .ts-gn-h1 i { font-style: normal; color: #6ee7b7; }
  .ts .ts-gn-lead { margin-top: 1rem; color: var(--ts-muted, #9aaba3); font-size: clamp(16px, 1.4vw, 19px); line-height: 1.65; }
  .ts-gn-tools { position: sticky; top: calc(var(--ts-header-space, 96px) - 16px); z-index: 4; display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1.5rem; padding: .5rem; border-radius: 999px; border: 1px solid var(--ts-line, rgba(255,255,255,.08)); background: rgba(6,6,8,.82); backdrop-filter: blur(12px); width: max-content; max-width: 100%; }
  .ts .ts-gn-tools button, .ts .ts-gn-tools a { display: inline-flex; align-items: center; gap: .4rem; padding: 9px 13px; border-radius: 999px; border: 1px solid transparent; background: transparent; color: var(--ts-text, #f6faf7); font: 500 13px/1 var(--ts-font-body, Inter, sans-serif); text-decoration: none; cursor: pointer; }
  .ts .ts-gn-tools button:hover, .ts .ts-gn-tools a:hover { border-color: var(--ts-line-strong, rgba(255,255,255,.14)); }
  .ts .ts-gn-tools button[aria-pressed="true"] { background: #f6faf7; color: #060608; }
  .ts-gn-text { --gn-size: 19px; margin-top: 2.25rem; }
  .ts .ts-gn-text p { margin: 0 0 1.15em; font: 400 var(--gn-size)/1.85 var(--ts-font-body, Inter, sans-serif); color: #e7ece9; }
  .ts .ts-gn-text p:first-child::first-letter { float: left; margin: .08em .12em 0 0; font: 800 3.4em/.8 var(--ts-font-display, 'Syne', sans-serif); color: #6ee7b7; }
  .ts .ts-gn-night { display: flex; align-items: center; gap: 1rem; margin: 2.5rem 0 0; padding: 1.4rem 1.5rem; border-radius: 22px; font: 700 clamp(1.15rem, 2vw, 1.45rem)/1.35 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.01em; }
  .ts .ts-gn-night svg { flex: none; color: #f7d046; }
  .ts .ts-gn-ask { margin-top: 1.25rem; padding: 1.4rem 1.5rem; border-radius: 22px; }
  .ts .ts-gn-ask ul { margin: .8rem 0 0; padding: 0; list-style: none; display: grid; gap: .55rem; }
  .ts .ts-gn-ask li { position: relative; padding-left: 1.5rem; color: var(--tss-text, rgba(246,250,247,.8)); line-height: 1.55; }
  .ts .ts-gn-ask li::before { content: "?"; position: absolute; left: 0; top: 0; color: #6ee7b7; font-weight: 800; }
  .ts-gn-motiv { display: grid; gap: 1.25rem; margin-top: 1.25rem; padding: 1.4rem 1.5rem; border-radius: 22px; align-items: center; }
  .ts .ts-gn-motiv__img { max-width: 220px; padding: .5rem; border-radius: 8px; background: #fbf9f4; transform: rotate(-2deg); box-shadow: 0 30px 50px -26px rgba(0,0,0,.9); }
  .ts .ts-gn-motiv__img svg { display: block; width: 100% !important; height: auto !important; }
  .ts .ts-gn-author { display: grid; grid-template-columns: 72px 1fr; gap: 1.1rem; align-items: start; margin-top: 1.25rem; padding: 1.4rem 1.5rem; border-radius: 22px; }
  .ts .ts-gn-author img { width: 72px !important; height: 72px !important; border-radius: 50%; object-fit: cover; }
  .ts .ts-gn-author p { margin: 0; color: var(--tss-text, rgba(246,250,247,.75)); line-height: 1.6; font-size: 15px; }
  .ts .ts-gn-author p + p { margin-top: .45rem; }
  .ts .ts-gn-author b { color: #f6faf7; }
  .ts .ts-gn-audio { margin-top: 1.5rem; padding: 1rem 1.2rem; border-radius: 18px; }
  .ts .ts-gn-audio audio { width: 100%; margin-top: .6rem; }
  .ts .ts-gn-reihe { margin-top: 1.25rem; }
  .ts .ts-gn-reihe ul { margin: .7rem 0 0; padding: 0; list-style: none; border-top: 1px solid var(--ts-line, rgba(255,255,255,.08)); }
  .ts .ts-gn-reihe li { display: flex; justify-content: space-between; gap: 1rem; padding: .85rem 0; border-bottom: 1px solid var(--ts-line, rgba(255,255,255,.08)); }
  .ts .ts-gn-reihe a { color: #f6faf7; font: 700 1.05rem/1.3 var(--ts-font-display, 'Syne', sans-serif); text-decoration: none; }
  .ts .ts-gn-reihe a:hover { color: #6ee7b7; }
  .ts .ts-gn-reihe .ts-label { color: var(--ts-muted, #9aaba3); white-space: nowrap; }
  /* Nachtmodus: dunkler, wärmer, größer – zum Vorlesen im abgedunkelten Kinderzimmer */
  html.ts-gn-dark .ts-gn-page { background: #050505; }
  html.ts-gn-dark .ts .ts-gn-text p { color: #e9dcc0; }
  html.ts-gn-dark .ts .ts-gn-text p:first-child::first-letter { color: #f7d046; }
  html.ts-gn-dark .ts-gn-dim { opacity: .25; transition: opacity .4s; }
  html.ts-gn-dark .ts-khr, html.ts-gn-dark .ts-header { opacity: .25; }
  @media (min-width: 640px) {
    .ts-am-gal { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ts-am-packs, .ts-gn-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (min-width: 1024px) {
    .ts-am-gal { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .ts-am-packs, .ts-gn-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ts-gn-today { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 3rem; }
    .ts-gn-motiv { grid-template-columns: 220px minmax(0, 1fr); }
  }
  @media print {
    .ts-khr, .ts-gn-tools, .ts-gn-noprint, header, footer, #footer-sections, .ts-header { display: none !important; }
    .ts .ts-gn-text p { color: #111 !important; font-size: 13pt !important; }
    .ts .ts-gn-h1, .ts .ts-gn-night, .ts .ts-gn-ask, .ts .ts-gn-ask li { color: #111 !important; background: none !important; border: 0 !important; }
    .ts-gn-motiv { page-break-before: always; }
    body, .ts-gn-page { background: #fff !important; }
  }
</style>''')

# ======================================================================= JS: Drucken + Widget (extern ladbar)
PRINT_JS = r'''
/* Ein Motiv als A4-Seite drucken (öffnet ein Druckfenster) */
window.tsKhPrint = (svg, name, paket) => {
  const w = window.open('', '_blank');
  if (!w) { alert('Bitte Pop-ups für diese Seite erlauben, um zu drucken.'); return; }
  w.document.write('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>' + name + ' – Ausmalbild</title>' +
    '<style>@page{size:A4;margin:12mm}html,body{margin:0;background:#fff}body{display:flex;flex-direction:column;align-items:center;justify-content:center;height:96vh;font:500 9pt Arial,sans-serif;color:#888}' +
    'svg{width:100%;max-height:88vh}p{margin:3mm 0 0;letter-spacing:.12em;text-transform:uppercase}</style></head><body>' + svg +
    '<p>' + (paket ? paket + ' · ' : '') + 'trutzstaehler.de/ausmalbilder</p></body></html>');
  w.document.close();
  w.onafterprint = () => w.close();
  setTimeout(() => { w.focus(); w.print(); }, 350);
};
'''

PAINT2_JS = WEB.PAINT_JS.replace(
    "document.querySelectorAll('[data-am-paint]').forEach(root => {\n    const MOTIVE = JSON.parse(root.querySelector('script[type=\"application/json\"]').textContent);",
    "document.querySelectorAll('[data-am-paint]').forEach(root => {\n    let MOTIVE = JSON.parse(root.querySelector('script[type=\"application/json\"]').textContent);"
).replace(
    "    load(root.dataset.default || seasonKey());\n  });",
    """    /* von außen ein Motiv laden (Galerie: „Ausmalen“) */
    window.tsAmPaint = m => {
      if (!MOTIVE.find(x => x.key === m.key)) { MOTIVE = MOTIVE.concat([m]); if (pick) { pick.insertAdjacentHTML('beforeend', `<button type="button" data-k="${m.key}" aria-pressed="false">${m.name}</button>`); } }
      load(m.key);
      root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    load(root.dataset.default || seasonKey());
  });""")
assert 'window.tsAmPaint' in PAINT2_JS and 'let MOTIVE' in PAINT2_JS

# ======================================================================= /ausmalbilder
FENSTER = {'halloween': (1001, 1031), 'laterne': (1101, 1111), 'advent': (1112, 1224), 'anhaenger': (1201, 1224), 'winter': (1225, 228)}
SAISON_LABEL = {'halloween': '31. Oktober', 'laterne': '11. November', 'advent': '1. – 24. Dezember', 'anhaenger': 'bis Heiligabend', 'winter': 'Dezember – Februar'}

GALERIE_JS = r'''
<script>
/* Ausmalbilder: Pakete, Galerie, Drucken, Ausmalen – Daten aus GitHub (wie helden.json) */
(() => {
  const BASIS = window.KH_BASIS || '__BASIS__';
  const gal = document.querySelector('[data-am-gal]'), filt = document.querySelector('[data-am-filter]'), packsEl = document.querySelector('[data-am-packs]');
  if (!gal) return;
  const cache = {}; let KAT = null;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const rots = [-1.4, 1.1, -.7, 1.3, -1, .8];
  const md = (() => { const d = new Date(); return (d.getMonth() + 1) * 100 + d.getDate(); })();
  const FEN = __FENSTER__;
  const inWin = w => { if (!w) return false; const [a, b] = w; return a <= b ? md >= a && md <= b : md >= a || md <= b; };
  const saisonPaket = () => { for (const id in FEN) if (inWin(FEN[id])) return id; return 'hafen'; };
  const icoP = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9V3h12v6"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/></svg>';
  const icoB = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2a2 2 0 0 0 2.8 0L19 11Z"/><path d="M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4Z"/></svg>';
  const icoD = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>';

  const motive = id => cache[id] ? Promise.resolve(cache[id]) :
    fetch(BASIS + 'ausmalbilder/daten/motive-' + id + '.json').then(r => r.json()).then(j => (cache[id] = j));
  const paketVon = key => KAT.pakete.find(p => p.motive.some(m => m.key === key));

  const zeige = async (id, scroll) => {
    filt.querySelectorAll('[data-p]').forEach(b => b.setAttribute('aria-pressed', b.dataset.p === id));
    gal.innerHTML = '<p class="ts-label ts-am-gal__msg">Motive werden geladen …</p>';
    const liste = id === 'alle' ? KAT.pakete.filter(p => p.anzahl) : KAT.pakete.filter(p => p.id === id);
    try {
      const daten = await Promise.all(liste.map(p => motive(p.id)));
      gal.innerHTML = liste.map((p, pi) => p.motive.map((m, i) =>
        `<figure class="ts-am-tile" style="--r:${rots[i % 6]}deg" data-key="${m.key}" data-pid="${p.id}">${daten[pi][m.key]}
          <figcaption class="ts-am-tile__acts"><button type="button" data-act="print" aria-label="${esc(m.name)} drucken">${icoP}Drucken</button><button type="button" data-act="paint" aria-label="${esc(m.name)} online ausmalen">${icoB}Ausmalen</button></figcaption></figure>`).join('')).join('');
      if (scroll) gal.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) { gal.innerHTML = '<p class="ts-label ts-am-gal__msg">Die Motive konnten gerade nicht geladen werden. Bitte später noch einmal versuchen.</p>'; }
  };
  gal.addEventListener('click', e => {
    const b = e.target.closest('[data-act]'); if (!b) return;
    const f = b.closest('[data-key]'), key = f.dataset.key, p = KAT.pakete.find(x => x.id === f.dataset.pid), m = p.motive.find(x => x.key === key);
    const svg = cache[p.id][key];
    if (b.dataset.act === 'print') window.tsKhPrint(svg, m.name, p.name);
    else if (window.tsAmPaint) window.tsAmPaint({ key, name: m.name, file: key, src: 'data:image/svg+xml;utf8,' + encodeURIComponent(svg), saison: p.id, paket: p.name });
  });

  fetch(BASIS + 'ausmalbilder/daten/katalog.json').then(r => r.json()).then(k => {
    KAT = k;
    /* Paket-Karten */
    if (packsEl) packsEl.innerHTML = k.pakete.map(p => `
      <article id="paket-${p.id}" class="ts-am-pack ts-glass" style="--c:${p.farbe}">
        <div class="ts-am-pack__img"><img src="${BASIS + p.karte}" alt="${esc(p.name)}: ${esc(p.sub)}" loading="lazy" width="1200" height="800">
          <span class="ts-label ts-am-pack__nr">${p.nr}</span><span class="ts-label ts-am-pack__tag">${inWin(FEN[p.id]) ? 'Jetzt dran' : esc(p.saison === 'ganzjährig' ? 'Ganzjährig' : p.saison)}</span></div>
        <div class="ts-am-pack__body">
          <h3 class="ts-am-pack__t">${esc(p.name)}${/[!?.]$/.test(p.name) ? '' : '<i>.</i>'}</h3>
          <p class="ts-am-pack__s">${esc(p.kurz)}</p>
          <div class="ts-am-pack__acts">
            <a class="ts-am-mini ts-am-mini--hi" href="${BASIS + p.pdf}" download>${icoD}PDF${p.pdf_mb ? ' · ' + String(p.pdf_mb).replace('.', ',') + ' MB' : ''}</a>
            ${p.anzahl ? `<button type="button" class="ts-am-mini" data-show="${p.id}">${p.anzahl} Motive ansehen</button>` : ''}
          </div>
        </div>
      </article>`).join('');
    if (packsEl) packsEl.addEventListener('click', e => { const b = e.target.closest('[data-show]'); if (b) zeige(b.dataset.show, true); });
    const zip = document.querySelector('[data-am-zip]');
    if (zip && k.alle_zip) { zip.href = BASIS + k.alle_zip; const t = zip.querySelector('[data-text]'); if (t && k.alle_zip_mb) { const s = 'Alle als ZIP · ' + String(k.alle_zip_mb).replace('.', ',') + ' MB'; t.textContent = s; t.dataset.text = s; } }
    /* Filter */
    filt.innerHTML = `<button type="button" data-p="alle" aria-pressed="false">Alle</button>` +
      k.pakete.filter(p => p.anzahl).map(p => `<button type="button" data-p="${p.id}" aria-pressed="false">${esc(p.name)}</button>`).join('');
    filt.addEventListener('click', e => { const b = e.target.closest('[data-p]'); if (b) zeige(b.dataset.p); });
    /* Start: ?motiv=hf03 (aus einer Geschichte) oder die aktuelle Saison */
    const q = new URLSearchParams(location.search).get('motiv');
    const start = q && paketVon(q) ? paketVon(q).id : saisonPaket();
    zeige(start).then(() => {
      if (q && paketVon(q)) { const b = gal.querySelector(`[data-key="${q}"] [data-act="paint"]`); if (b) b.click(); }
    });
  }).catch(() => { gal.innerHTML = '<p class="ts-label ts-am-gal__msg">Die Ausmalbilder konnten gerade nicht geladen werden. Bitte später noch einmal versuchen.</p>'; });
})();
</script>'''.replace('__BASIS__', BASIS).replace('__FENSTER__', json.dumps(FENSTER))

FAQ_AM = [
    ('Sind die Ausmalbilder wirklich kostenlos?', 'Ja. Alle Motive und PDFs sind kostenlos – ohne Anmeldung, ohne Newsletter, ohne Haken. Ich freue mich, wenn ihr die Seite weiterempfehlt.'),
    ('Dürfen wir die Bilder in der Kita oder Schule nutzen?', 'Sehr gern! Ihr dürft die Ausmalbilder zu Hause, in Kita, Krippe, Schule, Hort und Verein ausdrucken und kopieren. Bitte teilt den Link <b>trutzstaehler.de/ausmalbilder</b> statt der Dateien und verkauft die Bilder nicht.'),
    ('Wie drucke ich ein einzelnes Motiv?', 'Unter jedem Motiv steht „Drucken“. Es öffnet sich eine Druckansicht mit genau dieser A4-Seite. Für ganze Pakete gibt es oben das PDF zum Herunterladen.'),
    ('Für welches Alter sind die Bilder?', 'Für Kinder ab etwa 2 Jahren: dicke Linien, große Flächen und zu jedem Bild der Name in Buchstaben, die man ebenfalls ausmalen kann.'),
    ('Kann man auch am Tablet malen?', 'Ja. Mit „Ausmalen“ landet jedes Motiv im Mal-Werkzeug auf dieser Seite – mit Farbeimer, Pinsel, Speichern und Drucken. Das Bild bleibt nur auf eurem Gerät gespeichert.'),
    ('Welches Papier eignet sich?', 'Normales Druckerpapier reicht. Für Filzstifte, Wasserfarben oder die Laternen-Bastelvorlage ist etwas dickeres Papier (120–160 g/m²) schöner.'),
    ('Kommen neue Motive dazu?', 'Ja, regelmäßig – als Nächstes Fasching und Ostern. Schaut einfach wieder vorbei oder folgt mir auf <a href="https://www.instagram.com/trutzstaehler/" target="_blank" rel="noopener">Instagram</a>.'),
]


def jsonld_faq(faq):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(re.sub('<[^>]+>', '', a))}} for q, a in faq]}, ensure_ascii=False) + '</script>'


def seite_ausmalbilder():
    saison = ''
    for pid in ['halloween', 'laterne', 'advent', 'anhaenger', 'winter']:
        p = KAT.paket(pid); a, b = FENSTER[pid]
        adv = ' data-am-advent' if pid == 'advent' else ''
        saison += (f'<li data-from="{a}" data-to="{b}" data-fest="{WEB.FEST[pid]}"{adv} style="--c:{p["farbe"]}"><a href="#paket-{pid}" data-ts-no-trans>'
                   f'<span class="ts-label ts-am-season__date">{esc(SAISON_LABEL[pid])}</span><span class="ts-am-season__name">{esc(p["name"])}</span>'
                   f'<span class="ts-am-season__sub">{esc(p["sub"])}</span><span class="ts-label ts-am-season__state" data-state>PDF gratis</span></a></li>')
    teaser = GESCHICHTEN[:3]
    gcards = ''.join(f'''<a class="ts-gn-card ts-glass" href="{GESCH_URL}{g['slug']}"><div class="ts-gn-card__img"><img src="{BASIS}ausmalbilder/bilder/bunt/{g['motiv']}.webp" alt="" loading="lazy" width="360" height="396" style="--r:{r}deg"></div>
      <div class="ts-gn-card__body"><h3 class="ts-gn-card__t">{esc(g['titel'])}</h3><p class="ts-gn-card__s">{esc(g['teaser'])}</p><p class="ts-label ts-gn-card__m">{g['lesezeit']} Min. · ab {g['alter']} Jahren</p></div></a>'''
                     for g, r in zip(teaser, (-2, 1.5, -1)))
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in FAQ_AM)
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Ausmalbilder kostenlos zum Ausdrucken – Kreativhafen',
          'description': f'{N_MOTIVE} kostenlose Ausmalbilder für Kinder ab 2 Jahren in {N_PAKETE} Themen.', 'inLanguage': 'de',
          'url': f'https://{KAT.DOMAIN}/ausmalbilder', 'author': {'@type': 'Person', 'name': 'Trutz Stähler'},
          'isAccessibleForFree': True}
    body = f'''<!-- =====================================================================
  KREATIVHAFEN – Seite /ausmalbilder (kostenlos)  ·  Code-Block, alles einfügen
  Daten (Motive, PDFs, Bilder) kommen aus GitHub: {BASIS}
====================================================================== -->
{KH_CSS}
{reiter_html()}
<div class="ts ts-am tss ts-bleed ts-kh2 ts-gn-page" style="padding-top:0">
  <div class="ts-am__orb" aria-hidden="true"></div>
  <section class="ts-container tss--top" aria-labelledby="ts-am-title" style="padding-bottom:0">
    <div class="tss-kicker"><p class="ts-label ts-muted">[ Kreativhafen — Ausmalbilder ]</p><p class="ts-label ts-muted">Kostenlos · ohne Anmeldung</p></div>
    <div class="tss-head">
      <h1 id="ts-am-title" class="tss-h1" data-ts-fit>Ausmal&shy;bilder<i>.</i></h1>
      <div>
        <p class="tss-lead">{N_MOTIVE} Ausmalbilder zum kostenlosen Ausdrucken – vom Hamburger Hafen bis ins Weltall, von Halloween bis Silvester. Mit dicken Linien, großen Flächen und dem Namen zum Mitlesen. Einzeln drucken, als PDF laden oder direkt hier ausmalen.</p>
        <ul class="ts-am__chips"><li class="ts-label">Kostenlos</li><li class="ts-label">{N_MOTIVE} Motive</li><li class="ts-label">{N_PAKETE} Themen</li><li class="ts-label">Ab 2 Jahren</li></ul>
        <div class="ts-am__ctas">{btn('Motive ansehen', '#ts-am-galerie', True, ARROW_DOWN, ' data-ts-no-trans')}{btn('Alle als ZIP', BASIS + 'ausmalbilder/pdf/Alle-Ausmalbilder_Kreativhafen.zip', False, DL_ICON, ' data-am-zip download')}</div>
      </div>
    </div>
    <ol class="ts-am-season ts-reveal" data-am-season aria-label="Die Saison im Überblick">{saison}</ol>
  </section>

  <section id="ts-am-pakete" class="ts-container ts-am__block" aria-labelledby="ts-am-pakete-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Die Pakete ]</p><p class="ts-label ts-muted">{N_PAKETE} Themen · je ein PDF</p></div>
    <h2 id="ts-am-pakete-t" class="ts-am__h2">Such dir ein Thema aus<i>.</i></h2>
    <p class="ts-am__sub">Jedes Paket ist ein PDF mit Deckblatt zum Ausmalen, allen Motiven, Mal-Urkunde und Drucktipps. Bei „Laterne, Laterne“ ist eine Bastelvorlage dabei, beim Adventskalender ein Türchen-Plan.</p>
    <div class="ts-am-packs" data-am-packs><p class="ts-label ts-muted">Pakete werden geladen …</p></div>
  </section>

  <section id="ts-am-galerie" class="ts-container ts-am__block" aria-labelledby="ts-am-gal-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Alle Motive ]</p><p class="ts-label ts-muted">Einzeln drucken oder online ausmalen</p></div>
    <h2 id="ts-am-gal-t" class="ts-am__h2">Ein Motiv, ein Klick<i>.</i></h2>
    <div class="ts-am-filter" role="group" aria-label="Thema wählen" data-am-filter></div>
    <div class="ts-am-gal" data-am-gal aria-live="polite"></div>
  </section>

<!--@@TEIL@@-->
{WEB.paint_block(['hw01', 'lt01', 'ad11', 'wi01', 'hf03', 'fz03', 'wr01', 'og01'], None, "[ Probier's aus ]", 'Direkt im Browser', 'Mal gleich los<i>.</i>',
                 'Farbe antippen, dann ins Bild tippen – der Farbeimer füllt die ganze Fläche. In der Galerie oben holt „Ausmalen“ jedes Motiv hierher.', 'ts-am-malen')}

  <section class="ts-container ts-am__block" aria-labelledby="ts-am-gn-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Erst vorlesen, dann ausmalen ]</p><p class="ts-label ts-muted">Gute-Nacht-Geschichten</p></div>
    <h2 id="ts-am-gn-t" class="ts-am__h2">Zu jeder Geschichte ein Bild<i>.</i></h2>
    <p class="ts-am__sub">Kurze Geschichten zum Vorlesen – und am nächsten Morgen wird die Hauptfigur ausgemalt.</p>
    <div class="ts-gn-grid">{gcards}</div>
    <div class="ts-am__ctas">{btn('Alle Gute-Nacht-Geschichten', '/gute-nacht-geschichten')}</div>
  </section>

  <section class="ts-container ts-am__block ts-am__end" aria-labelledby="ts-am-faq-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Fragen &amp; Antworten ]</p></div>
    <h2 id="ts-am-faq-t" class="ts-am__h2" style="margin-bottom:1.5rem">Gut zu wissen<i>.</i></h2>
    <div class="tss-faq">{faq}</div>
    <div class="ts-am-final ts-glass">
      <p>Lust auf 50 Tiere am Stück?</p>
      {btn('Die Kritzelbücher', '/malbuecher')}
    </div>
  </section>
</div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{jsonld_faq(FAQ_AM)}
{WEB.SEASON_JS}
'''
    teile = WEB.teile(body, '<div class="ts ts-am tss ts-bleed ts-kh2 ts-gn-page" style="padding-top:0">',
                      ['<script>' + PRINT_JS + '</script>' + GALERIE_JS, PAINT2_JS],
                      ['Teil 1/2: Reiter, Kopf, Saison, Pakete, Galerie (enthält das CSS – zuerst einfügen)',
                       'Teil 2/2: Ausmal-Werkzeug, Geschichten, FAQ'])
    return teile


# ======================================================================= Geschichten (Übersicht)
SAISON_FENSTER = {'hw': (1001, 1031), 'lt': (1020, 1111), 'ad': (1112, 1224), 'wi': (1201, 228)}
DAUER = [('alle', 'Jede Länge'), ('kurz', 'Kurz · 1–3 Min.'), ('mittel', 'Mittel · 4–6 Min.'), ('lang', 'Lang · ab 7 Min.')]
ALTER = [('alle', 'Jedes Alter'), ('2', 'Für 2-Jährige'), ('4', 'Für 3–4-Jährige'), ('9', 'Ab 5 Jahren')]
FIGUREN = [
    ('Möwe Mats', 'hf03', 'Die neugierige Möwe vom Hamburger Hafen – mit eigener Geschichten-Reihe.', 'Mats'),
    ('Leuchtturm Lotte', 'hf02', 'Ihr Licht ist klein, ihr Herz ist groß.', 'Lotte'),
    ('Fähre Frieda', 'hf06', 'Bringt jeden Abend alle sicher nach Hause.', 'Frieda'),
    ('Kran Karl', 'hf05', 'Der größte Kran im Hafen – und der müdeste.', 'Karl'),
    ('Funki', 'mf02', 'Der kleine Drache, der kein Feuer spucken kann.', 'Funki'),
    ('Bagger Bruno', 'fz03', 'Will nie Feierabend machen.', 'Bruno'),
    ('Wichtel Wilbur', 'ad13', 'Bewacht im Advent jede Nacht ein Türchen.', 'Wilbur'),
    ('Gespenst Huhu', 'hw02', 'Fürchtet sich vor allem – sogar vor sich selbst.', 'Huhu'),
]


def saison_von(g):
    w = SAISON_FENSTER.get(g['motiv'][:2])
    return f'{w[0]}-{w[1]}' if w else ''


def heute_js():
    return r'''
<script>
/* Gute-Nacht-Geschichten: Geschichte für heute Abend, Saison-Auswahl, Suche und Filter */
(() => {
  const cards = [...document.querySelectorAll('#ts-gn-alle [data-gn-card]')];
  const d = new Date(), md = (d.getMonth() + 1) * 100 + d.getDate();
  const inWin = s => { if (!s) return false; const [a, b] = s.split('-').map(Number); return a <= b ? md >= a && md <= b : md >= a || md <= b; };
  /* Saison-Block */
  const sb = document.querySelector('[data-gn-saison]');
  const saison = cards.filter(c => inWin(c.dataset.saison));
  if (sb && saison.length) {
    const m = d.getMonth();
    sb.querySelector('[data-t]').innerHTML = (m === 9 || m === 10 ? 'Geschichten für den Herbst' : m === 11 ? 'Geschichten für den Advent' : 'Geschichten für den Winter') + '<i>.</i>';
    sb.querySelector('.ts-gn-grid').append(...saison.slice(0, 3).map(c => c.cloneNode(true)));
    sb.hidden = false;
  }
  /* Geschichte für heute Abend: Saison zuerst, sonst wechselnd nach Tag */
  const box = document.querySelector('[data-gn-today]');
  if (box && cards.length) {
    const pool = saison.length ? saison : cards, n = Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 864e5);
    const c = pool[n % pool.length];
    box.querySelector('[data-t]').textContent = c.dataset.titel;
    box.querySelector('[data-s]').textContent = c.dataset.teaser;
    box.querySelector('[data-m]').innerHTML = c.querySelector('.ts-gn-card__m').innerHTML;
    const img = box.querySelector('img'); img.src = c.querySelector('img').src; img.alt = c.dataset.titel;
    box.querySelectorAll('[data-href]').forEach(a => a.href = c.getAttribute('href'));
  }
  /* Filter + Suche */
  const f = document.querySelector('[data-gn-filter]'); if (!f) return;
  const q = document.querySelector('[data-gn-q]');
  let thema = 'alle', dauer = 'alle', alter = 'alle', form = 'alle';
  const ok = c => {
    const z = +c.dataset.zeit, a = +c.dataset.alter, s = (q && q.value || '').trim().toLowerCase();
    return (thema === 'alle' || c.dataset.themen.split(',').includes(thema))
      && (dauer === 'alle' || (dauer === 'kurz' ? z <= 3 : dauer === 'mittel' ? z >= 4 && z <= 6 : z >= 7))
      && (alter === 'alle' || a <= +alter && (alter !== '2' || a <= 2))
      && (form === 'alle' || c.dataset.form === form)
      && (!s || c.dataset.suche.includes(s));
  };
  const apply = () => {
    let n = 0; cards.forEach(c => { const v = ok(c); c.hidden = !v; if (v) n++; });
    const e = document.querySelector('[data-gn-count]'); if (e) e.textContent = n + (n === 1 ? ' Geschichte' : ' Geschichten');
    const leer = document.querySelector('[data-gn-leer]'); if (leer) leer.hidden = n > 0;
  };
  f.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    for (const k of ['thema', 'dauer', 'alter', 'form']) if (b.dataset[k]) {
      if (k === 'thema') thema = b.dataset[k]; if (k === 'dauer') dauer = b.dataset[k]; if (k === 'alter') alter = b.dataset[k]; if (k === 'form') form = b.dataset[k];
      f.querySelectorAll(`[data-${k}]`).forEach(x => x.setAttribute('aria-pressed', x === b));
    }
    apply();
  });
  if (q) q.addEventListener('input', apply);
  /* Figuren: Klick sucht nach der Figur */
  document.querySelectorAll('[data-gn-figur]').forEach(b => b.addEventListener('click', () => {
    if (!q) return; q.value = b.dataset.gnFigur; apply();
    document.getElementById('ts-gn-alle').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }));
  apply();
})();
</script>'''


FAQ_GN = [
    ('Wie lang sind die Gute-Nacht-Geschichten?', 'Es gibt ganz kurze Geschichten mit 1–2 Minuten für die Kleinsten, die meisten dauern 4–5 Minuten, und für größere Kinder gibt es längere mit 7–9 Minuten. Mit dem Filter „Länge“ findest du die passende.'),
    ('Für welches Alter sind die Geschichten?', 'Für Kinder von etwa 2 bis 7 Jahren. Bei jeder Geschichte steht ein Alter. Alle sind ruhig, enden friedlich und kommen ohne Gruselmomente aus.'),
    ('Was ist der Nachtmodus?', 'Auf jeder Geschichten-Seite gibt es einen Nachtmodus: Die Seite wird dunkler und wärmer, auf Wunsch auch die Schrift größer – angenehm zum Vorlesen im abgedunkelten Kinderzimmer.'),
    ('Muss ich etwas herunterladen?', 'Nein. Alle Geschichten liest du direkt hier auf der Seite – am Handy, Tablet oder Computer. Wer mag, kann eine Geschichte über den Druck-Knopf auch auf Papier bringen.'),
    ('Gibt es die Geschichten auch zum Anhören?', 'Auf jeder Seite gibt es „Vorlesen lassen“ – dann liest die Computerstimme deines Geräts vor. Selbst eingesprochene Hörgeschichten sind in Planung.'),
    ('Sind die Geschichten kostenlos?', 'Ja, alle Geschichten sind kostenlos und ohne Anmeldung. Ihr dürft sie zu Hause, in der Kita und in der Schule vorlesen. Bitte teilt den Link, statt die Texte zu kopieren.'),
]

SEO_TEXT = [
    ('Warum Gute-Nacht-Geschichten so gut tun',
     'Eine Geschichte vor dem Schlafen ist mehr als Unterhaltung: Sie ist ein fester Moment, in dem der Tag leiser wird. Kinder kuscheln sich an, hören eine vertraute Stimme und kommen zur Ruhe. Ganz nebenbei wachsen Wortschatz, Fantasie und Konzentration – und die Bindung zwischen euch.'),
    ('Welche Themen passen zum Einschlafen?',
     'Am besten Geschichten mit kleinen, lösbaren Problemen und einem warmen Ende: Freundschaft, Mut, Gefühle, Tiere, Fahrzeuge oder ein bisschen Fantasie. Die meisten unserer Geschichten werden zum Schluss langsamer und leiser – wie ein Lied, das ausklingt. Andere enden mit einem Lacher oder mit Vorfreude auf morgen. Viele spielen im Hamburger Hafen, bei Möwe Mats und ihren Freunden.'),
    ('Für welches Alter sind welche Geschichten?',
     'Für 2-Jährige gibt es ganz kurze Geschichten mit Wiederholungen und Geräuschen zum Mitmachen. Ab 3 Jahren passen die meisten Geschichten mit 4–5 Minuten. Ab 5 Jahren dürfen es längere Abenteuer mit 7–9 Minuten sein.'),
    ('Wie lang sollte eine Gute-Nacht-Geschichte sein?',
     'So lang, wie euer Kind gut zuhören kann – und kurz genug, dass es noch gemütlich bleibt. An müden Tagen lieber eine kurze Geschichte, am Wochenende darf es eine längere sein. Der Filter oben hilft beim Aussuchen.'),
    ('Wer schreibt die Geschichten?',
     'Die Geschichten entstehen im Kreativhafen von Trutz, Papa aus Hamburg und Autor der Kritzelbücher und des Kinderkrimis „Maria Holm“. Zu jeder Geschichte gibt es ein passendes Ausmalbild – damit sie am nächsten Morgen weitergeht.'),
]


def karte_geschichte(g, r=-2):
    themen = ','.join(g['themen'])
    such = ' '.join([g['titel'], g['teaser'], themen, g.get('reihe', '')] + g['absaetze'][:3]).lower()
    return (f'<a class="ts-gn-card ts-glass" href="{GESCH_URL}{g["slug"]}" data-gn-card data-themen="{esc(themen)}" data-zeit="{g["lesezeit"]}" '
            f'data-alter="{g["alter"]}" data-form="{esc(g["form"])}" data-saison="{saison_von(g)}" data-suche="{esc(such)}" '
            f'data-titel="{esc(g["titel"])}" data-teaser="{esc(g["teaser"])}">'
            f'<div class="ts-gn-card__img"><img src="{BASIS}ausmalbilder/bilder/bunt/{g["motiv"]}.webp" alt="" loading="lazy" width="360" height="396" style="--r:{r}deg"></div>'
            f'<div class="ts-gn-card__body"><h3 class="ts-gn-card__t">{esc(g["titel"])}</h3><p class="ts-gn-card__s">{esc(g["teaser"])}</p>'
            f'<p class="ts-label ts-gn-card__m">{g["lesezeit"]} Min. · ab {g["alter"]} J. · {esc(g["form"])}</p></div></a>')


def seite_geschichten():
    themen = sorted({t for g in GESCHICHTEN for t in g['themen']})
    cards = ''.join(karte_geschichte(g, [-2, 1.5, -1, 2][i % 4]) for i, g in enumerate(GESCHICHTEN))
    zeiten = sorted({g['lesezeit'] for g in GESCHICHTEN})
    def chips(key, items):
        return ''.join(f'<button type="button" data-{key}="{v}" aria-pressed="{str(v == "alle").lower()}">{esc(t)}</button>' for v, t in items)
    fil = (chips('dauer', DAUER) + '<span style="width:100%;height:0"></span>' + chips('alter', ALTER) +
           '<span style="width:100%;height:0"></span>' + chips('form', [('alle', 'Jede Art')] + [(f_, f_) for f_ in sorted({g['form'] for g in GESCHICHTEN})]) +
           '<span style="width:100%;height:0"></span>' + chips('thema', [('alle', 'Alle Themen')] + [(t, t) for t in themen]))
    figuren = ''.join(f'<button type="button" class="ts-gn-fig" data-gn-figur="{esc(s)}"><img src="{BASIS}ausmalbilder/bilder/bunt/{m}.webp" alt="" loading="lazy" width="120" height="132">'
                      f'<b>{esc(n)}</b><span>{esc(t)}</span></button>' for n, m, t, s in FIGUREN)
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in FAQ_GN)
    seo = ''.join(f'<h3>{esc(h)}</h3><p>{esc(t)}</p>' for h, t in SEO_TEXT)
    ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Gute-Nacht-Geschichten zum Vorlesen – Kreativhafen',
          'itemListElement': [{'@type': 'ListItem', 'position': i, 'url': f'https://{KAT.DOMAIN}{GESCH_URL}{g["slug"]}', 'name': g['titel']}
                              for i, g in enumerate(GESCHICHTEN, 1)]}
    moon = '<svg width="16" height="16" class="ts-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>'
    return f'''<!-- =====================================================================
  KREATIVHAFEN – Seite /gute-nacht-geschichten (Übersicht)  ·  Code-Block, alles einfügen
  Die einzelnen Geschichten liegen als Blog-Beiträge unter {GESCH_URL}<name>.
====================================================================== -->
{KH_CSS}
<style>
  .ts-gn-search {{ display: flex; align-items: center; gap: .6rem; margin-top: 1.5rem; padding: .35rem .35rem .35rem 1.1rem; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); max-width: 34rem; }}
  .ts .ts-gn-search input {{ flex: 1; min-width: 0; padding: 11px 0; border: 0; background: transparent; color: var(--ts-text, #f6faf7); font: 500 15px/1 var(--ts-font-body, Inter, sans-serif); outline: none; }}
  .ts .ts-gn-search input::placeholder {{ color: var(--ts-muted, #9aaba3); }}
  .ts-gn-figs {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; margin-top: 2rem; }}
  .ts .ts-gn-fig {{ display: grid; grid-template-columns: 64px 1fr; grid-template-rows: auto auto; column-gap: .9rem; align-items: center; text-align: left; padding: .8rem; border-radius: 18px; border: 1px solid var(--ts-line, rgba(255,255,255,.08)); background: rgba(255,255,255,.02); color: inherit; cursor: pointer; transition: border-color .25s, transform .4s var(--ts-ease-out); }}
  .ts .ts-gn-fig:hover {{ border-color: rgba(110,231,183,.45); transform: translateY(-3px); }}
  .ts .ts-gn-fig img {{ grid-row: 1 / 3; width: 64px !important; height: 64px !important; object-fit: cover; object-position: top; border-radius: 50%; background: #fbf9f4; }}
  .ts .ts-gn-fig b {{ font: 700 15px/1.2 var(--ts-font-display, 'Syne', sans-serif); }}
  .ts .ts-gn-fig span {{ color: var(--ts-muted, #9aaba3); font-size: 13px; line-height: 1.4; }}
  .ts .ts-gn-seo {{ columns: 1; column-gap: 3rem; margin-top: 2rem; }}
  .ts .ts-gn-seo h3 {{ margin: 0 0 .5rem; font: 700 1.15rem/1.25 var(--ts-font-display, 'Syne', sans-serif); break-after: avoid; }}
  .ts .ts-gn-seo p {{ margin: 0 0 1.6rem; color: var(--tss-text, rgba(246,250,247,.72)); line-height: 1.7; break-inside: avoid; }}
  @media (min-width: 900px) {{ .ts-gn-figs {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }} .ts .ts-gn-seo {{ columns: 2; }} }}
</style>
{reiter_html()}
<div class="ts ts-am tss ts-bleed ts-kh2 ts-gn-page" style="padding-top:0">
  <div class="ts-am__orb" aria-hidden="true"></div>
  <section class="ts-container tss--top" aria-labelledby="ts-gn-title" style="padding-bottom:0">
    <div class="tss-kicker"><p class="ts-label ts-muted">[ Kreativhafen — Vorlesen ]</p><p class="ts-label ts-muted">Kostenlos · ohne Anmeldung</p></div>
    <div class="tss-head">
      <h1 id="ts-gn-title" class="tss-h1" data-ts-fit>Gute-Nacht-<br>Geschichten<i>.</i></h1>
      <div>
        <p class="tss-lead">{len(GESCHICHTEN)} kostenlose Gute-Nacht-Geschichten zum Vorlesen – ruhig, warm und mit einem leisen Ende, das müde macht. Von Möwe Mats im Hamburger Hafen bis zum kleinen Drachen Funki. Zu jeder Geschichte gibt es ein Ausmalbild für den nächsten Morgen.</p>
        <ul class="ts-am__chips"><li class="ts-label">Kostenlos</li><li class="ts-label">{min(zeiten)}–{max(zeiten)} Minuten</li><li class="ts-label">Ab 2 Jahren</li><li class="ts-label">Mit Nachtmodus</li></ul>
      </div>
    </div>
    <div class="ts-gn-today ts-glass ts-reveal" data-gn-today>
      <a data-href href="#" aria-hidden="true" tabindex="-1"><img src="" alt="" width="360" height="396"></a>
      <div>
        <p class="ts-label ts-muted">[ Für heute Abend ]</p>
        <h2 class="ts-am__h2" data-t>…</h2>
        <p class="ts-am__sub" data-s></p>
        <p class="ts-label" style="margin-top:1rem;color:#6ee7b7" data-m></p>
        <div class="ts-am__ctas">{btn('Jetzt vorlesen', '#', True, moon, ' data-href')}</div>
      </div>
    </div>
  </section>

  <section class="ts-container ts-am__block" data-gn-saison hidden aria-label="Passend zur Jahreszeit">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Passend zur Jahreszeit ]</p></div>
    <h2 class="ts-am__h2" data-t>Geschichten für die Saison<i>.</i></h2>
    <div class="ts-gn-grid"></div>
  </section>

  <section id="ts-gn-alle" class="ts-container ts-am__block" aria-labelledby="ts-gn-alle-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Alle Geschichten ]</p><p class="ts-label ts-muted" data-gn-count>{len(GESCHICHTEN)} Geschichten</p></div>
    <h2 id="ts-gn-alle-t" class="ts-am__h2">Welche soll es heute sein<i>?</i></h2>
    <label class="ts-gn-search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
      <input type="search" placeholder="Suchen: Möwe, Drache, Bagger …" aria-label="Geschichten durchsuchen" data-gn-q></label>
    <div class="ts-gn-filter" data-gn-filter role="group" aria-label="Filter">{fil}</div>
    <div class="ts-gn-grid">{cards}</div>
    <p class="ts-label ts-muted" data-gn-leer hidden style="margin-top:1.5rem">Keine Geschichte passt – probier einen anderen Filter.</p>
  </section>

  <section class="ts-container ts-am__block" aria-labelledby="ts-gn-fig-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Unsere Figuren ]</p><p class="ts-label ts-muted">Antippen zum Finden</p></div>
    <h2 id="ts-gn-fig-t" class="ts-am__h2">Wer wohnt im Kreativhafen<i>?</i></h2>
    <div class="ts-gn-figs">{figuren}</div>
  </section>

  <section class="ts-container ts-am__block" aria-labelledby="ts-gn-tipps-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Vorlese-Tipps ]</p><p class="ts-label ts-muted">01 / 03</p></div>
    <h2 id="ts-gn-tipps-t" class="ts-am__h2" style="margin-bottom:2rem">So wird’s gemütlich<i>.</i></h2>
    <div class="tss-steps">
      <div class="tss-step"><h3>Licht runter</h3><p>Nur noch eine kleine Lampe an – oder den Nachtmodus auf der Geschichten-Seite einschalten.</p></div>
      <div class="tss-step"><h3>Langsam lesen</h3><p>Ruhig und leise, mit Pausen. Gegen Ende darf die Stimme immer langsamer werden.</p></div>
      <div class="tss-step"><h3>Euer eigener Schluss</h3><p>Erfindet einen Gute-Nacht-Satz, den ihr nach jeder Geschichte gemeinsam sagt – so wird das Vorlesen zu eurem Ritual.</p></div>
    </div>
  </section>

  <section class="ts-container ts-am__block" aria-labelledby="ts-gn-seo-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Rund ums Vorlesen ]</p></div>
    <h2 id="ts-gn-seo-t" class="ts-am__h2">Du suchst eine Gute-Nacht-Geschichte<i>?</i></h2>
    <div class="ts-gn-seo">{seo}</div>
  </section>

  <section class="ts-container ts-am__block ts-am__end" aria-labelledby="ts-gn-faq-t">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Fragen &amp; Antworten ]</p></div>
    <h2 id="ts-gn-faq-t" class="ts-am__h2" style="margin-bottom:1.5rem">Gut zu wissen<i>.</i></h2>
    <div class="tss-faq">{faq}</div>
    <div class="ts-am-final ts-glass">
      <p>Morgen früh: Ausmalbild dazu?</p>
      {btn('Zu den Ausmalbildern', '/ausmalbilder')}
    </div>
  </section>
</div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{jsonld_faq(FAQ_GN)}
{heute_js()}'''


STORY_JS = r'''
<script>
/* Geschichte: Nachtmodus, Schriftgröße, Vorlesen lassen, Drucken, Ausmalbild drucken */
(() => {
  const root = document.querySelector('[data-gn-story]'); if (!root) return;
  const txt = root.querySelector('.ts-gn-text'), h = document.documentElement;
  const night = root.querySelector('[data-gn="night"]');
  const setNight = on => { h.classList.toggle('ts-gn-dark', on); night.setAttribute('aria-pressed', on); try { localStorage.setItem('ts-gn-night', on ? '1' : ''); } catch (e) {} };
  night.addEventListener('click', () => setNight(!h.classList.contains('ts-gn-dark')));
  try { if (localStorage.getItem('ts-gn-night')) setNight(true); } catch (e) {}
  let size = 19; try { size = +localStorage.getItem('ts-gn-size') || 19; } catch (e) {}
  const setSize = s => { size = Math.max(16, Math.min(28, s)); txt.style.setProperty('--gn-size', size + 'px'); try { localStorage.setItem('ts-gn-size', size); } catch (e) {} };
  setSize(size);
  root.querySelector('[data-gn="plus"]').addEventListener('click', () => setSize(size + 2));
  root.querySelector('[data-gn="minus"]').addEventListener('click', () => setSize(size - 2));
  root.querySelector('[data-gn="print"]').addEventListener('click', () => window.print());
  /* Vorlesen lassen (Computerstimme des Geräts, falls vorhanden) */
  const sp = root.querySelector('[data-gn="speak"]');
  if (!('speechSynthesis' in window)) sp.hidden = true;
  else sp.addEventListener('click', () => {
    if (speechSynthesis.speaking) { speechSynthesis.cancel(); sp.setAttribute('aria-pressed', 'false'); return; }
    const t = [...txt.querySelectorAll('p')].map(p => p.textContent).join(' ') + ' ' + ((root.querySelector('[data-gn-night]') || {}).textContent || '');
    const u = new SpeechSynthesisUtterance(t); u.lang = 'de-DE'; u.rate = .85; u.pitch = 1;
    const v = speechSynthesis.getVoices().find(v => /^de/i.test(v.lang)); if (v) u.voice = v;
    u.onend = () => sp.setAttribute('aria-pressed', 'false');
    speechSynthesis.speak(u); sp.setAttribute('aria-pressed', 'true');
  });
  const sh = root.querySelector('[data-gn="share"]');
  if (sh) sh.addEventListener('click', async () => {
    const data = { title: document.title, text: 'Eine Gute-Nacht-Geschichte zum Vorlesen:', url: location.href };
    try { if (navigator.share) await navigator.share(data); else { await navigator.clipboard.writeText(location.href); sh.textContent = 'Link kopiert ✓'; } } catch (e) {}
  });
  const mp = root.querySelector('[data-gn="motiv"]');
  if (mp) mp.addEventListener('click', () => window.tsKhPrint(root.querySelector('.ts-gn-motiv__img').innerHTML, mp.dataset.name, mp.dataset.titel));
})();
</script>'''


def geschichte_block(g):
    i = GESCHICHTEN.index(g)
    verwandt = sorted([x for x in GESCHICHTEN if x is not g], key=lambda x: -len(set(x['themen']) & set(g['themen'])))[:2]
    svg = WEB.mini(K.motif_svg(g['motiv'], with_name=True, w=1000, h=1100)).replace('<svg ', "<svg role='img' aria-label='Ausmalbild " + esc(name_von(g['motiv'])) + "' ", 1)
    absaetze = ''.join(f'<p>{esc(a)}</p>' for a in g['absaetze'])
    fragen = ''.join(f'<li>{esc(f)}</li>' for f in g['fragen'])
    moon = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>'
    ld = {'@context': 'https://schema.org', '@type': 'ShortStory', 'name': g['titel'], 'headline': g['titel'], 'description': g['teaser'],
          'inLanguage': 'de', 'author': {'@type': 'Person', 'name': 'Trutz Stähler', 'url': f'https://{KAT.DOMAIN}/ueber-mich'},
          'publisher': {'@type': 'Organization', 'name': 'Kreativhafen'}, 'isAccessibleForFree': True,
          'typicalAgeRange': f'{g["alter"]}-6', 'timeRequired': f'PT{g["lesezeit"]}M', 'genre': 'Gute-Nacht-Geschichte',
          'keywords': ', '.join(g['themen']), 'image': f'{BASIS}ausmalbilder/bilder/bunt/{g["motiv"]}.webp',
          'url': f'https://{KAT.DOMAIN}{GESCH_URL}{g["slug"]}', 'wordCount': sum(len(a.split()) for a in g['absaetze'])}
    ico = lambda d: f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">{d}</svg>'
    gn_html = f'<p class="ts-gn-night ts-glass" data-gn-night>{moon}<span>{esc(g["gute_nacht"])}</span></p>' if g['gute_nacht'] else ''
    fr_html = (f'<div class="ts-gn-ask ts-glass ts-gn-dim"><p class="ts-label ts-muted">[ Zum Reden danach ]</p><ul>{fragen}</ul></div>') if g['fragen'] else ''
    audio = (f'<div class="ts-gn-audio ts-glass ts-gn-noprint"><p class="ts-label ts-muted">[ Papa liest vor ]</p>'
             f'<audio controls preload="none" src="{esc(g["audio"])}"></audio></div>') if g.get('audio') else ''
    buch = ('/romane', 'Für Größere: Kinderkrimi „Maria Holm“') if g['alter'] >= 5 else ('/malbuecher', 'Die Kritzelbücher ansehen')
    reihe = [x for x in GESCHICHTEN if g.get('reihe') and x.get('reihe') == g['reihe'] and x is not g]
    reihe_html = ('<div class="ts-gn-reihe ts-gn-dim ts-gn-noprint"><p class="ts-label ts-muted">[ Mehr aus der Reihe „' + esc(g['reihe']) + '“ ]</p><ul>' +
                  ''.join(f'<li><a href="{GESCH_URL}{x["slug"]}">{esc(x["titel"])}</a><span class="ts-label">{x["lesezeit"]} Min.</span></li>' for x in reihe) +
                  '</ul></div>') if reihe else ''
    return f'''<!-- =====================================================================
  GUTE-NACHT-GESCHICHTE „{g['titel']}“  ·  Blog-Beitrag {GESCH_URL}{g['slug']}
  Einfügen: Beitrag öffnen → Inhalt löschen → Code-Block → alles einfügen.
====================================================================== -->
{KH_CSS}
{reiter_html()}
<article class="ts ts-am tss ts-bleed ts-kh2 ts-gn-page" style="padding-top:0" data-gn-story aria-labelledby="ts-gn-h">
  <div class="ts-am__orb ts-gn-dim" aria-hidden="true"></div>
  <div class="ts-container tss--top">
    <div class="ts-gn-story">
      <div class="tss-kicker ts-gn-dim"><p class="ts-label ts-muted"><a href="/gute-nacht-geschichten" style="color:inherit">← Alle Gute-Nacht-Geschichten</a></p><p class="ts-label ts-muted">Geschichte {i + 1:02d} / {len(GESCHICHTEN):02d}</p></div>
      <ul class="ts-gn-meta ts-gn-dim"><li class="ts-label">{esc(g['form'])}</li><li class="ts-label">Ab {g['alter']} Jahren</li><li class="ts-label">{g['lesezeit']} Min. Vorlesezeit</li>{''.join(f'<li class="ts-label">{esc(t)}</li>' for t in g['themen'])}</ul>
      <h1 id="ts-gn-h" class="ts-gn-h1">{esc(g['titel'])}<i>.</i></h1>
      <p class="ts-gn-lead ts-gn-dim">{esc(g['teaser'])}</p>
      <div class="ts-gn-tools" role="toolbar" aria-label="Lesehilfen">
        <button type="button" data-gn="night" aria-pressed="false">{ico('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/>')}Nachtmodus</button>
        <button type="button" data-gn="minus" aria-label="Schrift kleiner">A−</button>
        <button type="button" data-gn="plus" aria-label="Schrift größer">A+</button>
        <button type="button" data-gn="speak" aria-pressed="false">{ico('<path d="M11 5 6 9H2v6h4l5 4V5Z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>')}Vorlesen lassen</button>
        <button type="button" data-gn="print">{ico('<path d="M6 9V3h12v6"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/>')}Drucken</button>
      </div>
      {audio}
      <div class="ts-gn-text">{absaetze}</div>
      {gn_html}
      {fr_html}
      <div class="ts-gn-motiv ts-glass ts-gn-dim">
        <div class="ts-gn-motiv__img">{svg}</div>
        <div><p class="ts-label ts-muted">[ Das Ausmalbild zur Geschichte ]</p>
          <h2 class="ts-am__h2" style="font-size:clamp(1.5rem,3vw,2.2rem);margin-top:.8rem">Morgen früh: {esc(name_von(g['motiv']))} ausmalen<i>.</i></h2>
          <div class="ts-am__ctas ts-gn-noprint">
            <button type="button" class="ts-am-mini ts-am-mini--hi" data-gn="motiv" data-name="{esc(name_von(g['motiv']))}" data-titel="{esc(g['titel'])}">Ausmalbild drucken</button>
            <a class="ts-am-mini" href="/ausmalbilder?motiv={g['motiv']}#ts-am-malen">Online ausmalen</a>
          </div></div>
      </div>
      <div class="ts-gn-author ts-glass ts-gn-dim ts-gn-noprint">
        <img src="https://images.squarespace-cdn.com/content/v1/6869717aa7c996116c8c8a56/ffc25dc6-15ea-4d07-ab0d-6173fde95edf/IMG_3686.jpeg?format=300w" alt="Trutz Stähler" width="72" height="72" loading="lazy">
        <div><p class="ts-label ts-muted">[ Aus dem Kreativhafen ]</p>
          <p><b>Trutz Stähler</b> – Papa aus Hamburg, Autor der Kritzelbücher und des Kinderkrimis „Maria Holm“. Im Kreativhafen entstehen Geschichten zum Vorlesen und Ausmalbilder zum Weitermalen.</p>
          <div class="ts-am__ctas" style="margin-top:.9rem">
            <button type="button" class="ts-am-mini" data-gn="share">Mit Freunden teilen</button>
            <a class="ts-am-mini" href="{buch[0]}">{esc(buch[1])}</a>
          </div></div>
      </div>
      {reihe_html}
    </div>
  </div>
  <section class="ts-container ts-am__block ts-am__end ts-gn-noprint ts-gn-dim" aria-label="Weitere Geschichten">
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Noch eine? ]</p><p class="ts-label ts-muted"><a href="/gute-nacht-geschichten" style="color:inherit">Alle Geschichten →</a></p></div>
    <div class="ts-gn-grid" style="margin-top:1.5rem">{''.join(karte_geschichte(x, r) for x, r in zip(verwandt, (-2, 1.5)))}</div>
  </section>
</article>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script>{PRINT_JS}</script>
{STORY_JS}'''


# ======================================================================= Regal + Teaser
def regal_block():
    return f'''<!-- =====================================================================
  KREATIVHAFEN – Regal „Gratis im Hafen“ (Code-Block)
  Auf /kreativhafen direkt UNTER dem Regal „Bücher“ einfügen. Nutzt die Karten-Optik der Seite (ts-kh-card).
====================================================================== -->
<section class="ts ts-container ts-kh__shelf" aria-labelledby="ts-kh-gratis">
  <div class="ts-kh__shelf-head ts-reveal">
    <div><p class="ts-label ts-muted">[ Gratis im Hafen ]</p><h2 id="ts-kh-gratis" class="ts-kh__shelf-title" data-ts-fit>Zum Mitnehmen</h2></div>
    <p class="ts-kh__shelf-note">Ausmalbilder zum Ausdrucken und Gute-Nacht-Geschichten zum Vorlesen – kostenlos, ohne Anmeldung.</p>
  </div>
  <ul class="ts-kh__cards">
    <li class="ts-reveal">
      <a href="/ausmalbilder" class="ts-kh-card ts-glass ts-tilt">
        <div class="ts-kh-card__stage ts-kh-card__stage--art">
          <span class="ts-label ts-kh-card__num">03</span><span class="ts-label ts-kh-card__tag">Gratis</span>
          <img src="{BASIS}ausmalbilder/bilder/karte-hafen.webp" alt="Ausmalbilder aus dem Hamburger Hafen: Möwe, Containerschiff und Leuchtturm" loading="lazy">
        </div>
        <div class="ts-kh-card__body">
          <h3 class="ts-kh-card__title">Ausmalbilder zum Ausdrucken</h3>
          <p class="ts-kh-card__text">{N_MOTIVE} Motive in {N_PAKETE} Themen – vom Hamburger Hafen bis ins Weltall. Einzeln drucken, als PDF laden oder direkt im Browser ausmalen.</p>
          <div class="ts-kh-card__foot"><span class="ts-kh-card__more">Jetzt ausmalen</span><span class="ts-kh-card__go"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
        </div>
      </a>
    </li>
    <li class="ts-reveal">
      <a href="/gute-nacht-geschichten" class="ts-kh-card ts-glass ts-tilt">
        <div class="ts-kh-card__stage ts-kh-card__stage--art">
          <span class="ts-label ts-kh-card__num">04</span><span class="ts-label ts-kh-card__tag">Gratis</span>
          <img src="{BASIS}ausmalbilder/bilder/bunt/hf03.webp" alt="Möwe Mats aus den Gute-Nacht-Geschichten" loading="lazy" style="background:#fbf9f4;padding:8px;max-height:70% !important">
        </div>
        <div class="ts-kh-card__body">
          <h3 class="ts-kh-card__title">Gute-Nacht-Geschichten</h3>
          <p class="ts-kh-card__text">{len(GESCHICHTEN)} kurze Geschichten zum Vorlesen – ruhig, warm und mit einem Ausmalbild für den nächsten Morgen. Mit Nachtmodus.</p>
          <div class="ts-kh-card__foot"><span class="ts-kh-card__more">Jetzt vorlesen</span><span class="ts-kh-card__go"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
        </div>
      </a>
    </li>
  </ul>
</section>'''


def teaser_block():
    t = WEB.teaser()
    t = t.replace("Halloween, Laternenzeit, 24 Türchen zum Ausmalen und Winter: Ausmalbilder zum Ausdrucken – sofort als PDF. Drei Motive gibt es gratis.",
                  f"{N_MOTIVE} Ausmalbilder zum kostenlosen Ausdrucken und Gute-Nacht-Geschichten zum Vorlesen – frisch aus dem Kreativhafen.")
    t = t.replace("btn('Zu den Ausmalbildern', '/shop/ausmalbilder')", "")
    t = t.replace('href="/shop/ausmalbilder"', 'href="/ausmalbilder"').replace('href="/shop/ausmalbilder#ts-am-gratis"', 'href="/gute-nacht-geschichten"')
    t = t.replace('data-text="Gratis probieren">Gratis probieren', 'data-text="Gute-Nacht-Geschichten">Gute-Nacht-Geschichten')
    t = t.replace('[ Neu im Kreativhafen · Ausmalbilder ]', '[ Neu im Kreativhafen · kostenlos ]')
    t = t.replace('Malen durch die Saison<i>.</i>', 'Malen, vorlesen, träumen<i>.</i>')
    return t


# ======================================================================= Vorschau + main
def preview(name, block, title, basis_local):
    WEB.OUT = OUT
    os.makedirs(PREV, exist_ok=True)
    assets = os.path.join(HERE, 'vorschau-assets')
    gcss = open(os.path.join(assets, 'global.css'), encoding='utf-8').read()
    gcss += open(os.path.join(assets, 'kreativhafen-seite.css'), encoding='utf-8').read()   # Karten-Optik der Seite /kreativhafen
    gjs = open(os.path.join(assets, 'global.js'), encoding='utf-8').read()
    doc = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vorschau – {esc(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Syne:wght@600;700;800&display=swap" rel="stylesheet">
<style>{gcss}</style><style>body{{margin:0;background:#060608;color:#f6faf7;font-family:Inter,system-ui,sans-serif}}</style>
<script>window.KH_BASIS = {json.dumps(basis_local)};</script>
</head><body>
{block.replace(BASIS, basis_local)}
<script>{gjs}</script>
<script>document.querySelectorAll('.ts-reveal').forEach(e=>e.classList.add('is-in'));</script>
</body></html>'''
    open(os.path.join(PREV, name), 'w', encoding='utf-8').write(doc)


def main(basis_local='http://localhost:8765/kreativhafen/'):
    os.makedirs(os.path.join(OUT, 'geschichten'), exist_ok=True)
    files = {
        '01_reiter-leiste_fuer-kreativhafen-malbuecher-romane.html': reiter_block(),
        '02_regal-gratis-im-hafen_fuer-kreativhafen.html': regal_block(),
        '04_seite-gute-nacht-geschichten.html': seite_geschichten(),
        '05_teaser-startseite.html': teaser_block(),
    }
    am = seite_ausmalbilder()
    for i, t in enumerate(am, 1):
        files[f'03-{i}_seite-ausmalbilder_teil-{i}-von-{len(am)}.html'] = t
    for g in GESCHICHTEN:
        files[f'geschichten/{GESCHICHTEN.index(g) + 1:02d}_{g["slug"]}.html'] = geschichte_block(g)
    for n, c in files.items():
        open(os.path.join(OUT, n), 'w', encoding='utf-8').write(c)
        print(f'{n:78s} {len(c.encode()) / 1024:6.1f} KB')
    preview('ausmalbilder.html', '\n'.join(am), '/ausmalbilder', basis_local)
    preview('gute-nacht-geschichten.html', files['04_seite-gute-nacht-geschichten.html'], '/gute-nacht-geschichten', basis_local)
    g0 = GESCHICHTEN[0]
    preview('geschichte.html', files[f'geschichten/01_{g0["slug"]}.html'], g0['titel'], basis_local)
    preview('regal.html', reiter_block() + files['02_regal-gratis-im-hafen_fuer-kreativhafen.html'], 'Reiter + Regal', basis_local)


if __name__ == '__main__':
    main()

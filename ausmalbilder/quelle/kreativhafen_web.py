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
  /* Geschichten: Karten wie bei Zitronenbande/Zwergenstark – Bild, Titel, Alter · Dauer */
  .ts-gn-grid { display: grid; gap: clamp(.75rem, 2vw, 1.25rem); margin-top: 1.5rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .ts .ts-gn-card { display: flex; flex-direction: column; border-radius: 18px; overflow: hidden; color: inherit; text-decoration: none; border: 1px solid var(--ts-line, rgba(255,255,255,.08)); background: rgba(255,255,255,.025); transition: transform .5s var(--ts-ease-out), border-color .25s; }
  .ts .ts-gn-card:hover { transform: translateY(-4px); border-color: rgba(110,231,183,.45); }
  .ts-gn-card[hidden] { display: none !important; }
  .ts .ts-gn-card img { display: block; width: 100% !important; height: auto !important; aspect-ratio: 4 / 3; object-fit: cover; background: #1f2a44; }
  .ts-gn-card__body { display: flex; flex-direction: column; gap: .4rem; flex: 1; padding: .85rem 1rem 1rem; }
  .ts .ts-gn-card__t { margin: 0; font: 700 clamp(.98rem, 1.45vw, 1.18rem)/1.22 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.01em; }
  .ts .ts-gn-card__m { margin: auto 0 0; color: var(--ts-muted, #9aaba3); font: 500 13px/1.35 var(--ts-font-body, Inter, sans-serif); }
  /* Übersicht */
  .ts .ts-gn-intro { max-width: 46rem; margin: 1.25rem 0 0; color: var(--tss-text, rgba(246,250,247,.78)); font-size: clamp(16px, 1.35vw, 18px); line-height: 1.7; }
  .ts-gn-jump { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.5rem; }
  .ts .ts-gn-jump a { padding: 10px 15px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); color: var(--ts-text, #f6faf7); text-decoration: none; font: 600 13px/1 var(--ts-font-body, Inter, sans-serif); }
  .ts .ts-gn-jump a:hover { border-color: rgba(110,231,183,.5); }
  .ts .ts-gn-jump a:first-child { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts-gn-bar { display: flex; flex-wrap: wrap; align-items: center; gap: .75rem 1.25rem; margin-top: 1.5rem; }
  .ts-gn-filter { display: flex; flex-wrap: wrap; align-items: center; gap: .45rem; }
  .ts .ts-gn-filter b { margin-right: .25rem; font: 600 14px/1 var(--ts-font-body, Inter, sans-serif); }
  .ts .ts-gn-filter button { padding: 9px 14px; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); background: transparent; color: var(--ts-text, #f6faf7); font: 600 13px/1 var(--ts-font-body, Inter, sans-serif); cursor: pointer; }
  .ts .ts-gn-filter button[aria-pressed="true"] { background: #f6faf7; color: #060608; border-color: #f6faf7; }
  .ts-gn-search { display: flex; align-items: center; gap: .6rem; flex: 1 1 16rem; max-width: 24rem; padding: .2rem .2rem .2rem 1rem; border-radius: 999px; border: 1px solid var(--ts-line-strong, rgba(255,255,255,.14)); }
  .ts .ts-gn-search input { flex: 1; min-width: 0; padding: 10px 0; border: 0; background: transparent; color: var(--ts-text, #f6faf7); font: 500 15px/1 var(--ts-font-body, Inter, sans-serif); outline: none; }
  .ts .ts-gn-search input::placeholder { color: var(--ts-muted, #9aaba3); }
  .ts .ts-gn-state { margin: 1rem 0 0; color: var(--ts-muted, #9aaba3); font-size: 14px; }
  .ts .ts-gn-state button { margin-left: .5rem; padding: 0; border: 0; background: none; color: #6ee7b7; font: inherit; text-decoration: underline; cursor: pointer; }
  .ts-gn-morebtn { display: flex; justify-content: center; margin-top: 2rem; }
  .ts-gn-figs { display: grid; grid-template-columns: minmax(0, 1fr); gap: .8rem; margin-top: 2rem; }
  .ts-gn-page .ts-am__h2 { font-size: clamp(1.75rem, 4.6vw, 3.4rem); hyphens: auto; -webkit-hyphens: auto; overflow-wrap: break-word; }
  .ts .ts-gn-fig { display: grid; grid-template-columns: 64px 1fr; grid-template-rows: auto auto; column-gap: .9rem; align-items: center; text-align: left; padding: .8rem; border-radius: 18px; border: 1px solid var(--ts-line, rgba(255,255,255,.08)); background: rgba(255,255,255,.02); color: inherit; text-decoration: none; transition: border-color .25s, transform .4s var(--ts-ease-out); }
  .ts .ts-gn-fig:hover { border-color: rgba(110,231,183,.45); transform: translateY(-3px); }
  .ts .ts-gn-fig img { grid-row: 1 / 3; width: 64px !important; height: 64px !important; object-fit: cover; border-radius: 50%; }
  .ts .ts-gn-fig b { font: 700 15px/1.2 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-fig span { color: var(--ts-muted, #9aaba3); font-size: 13px; line-height: 1.4; }
  .ts .ts-gn-seo { margin-top: 2rem; max-width: 52rem; }
  .ts .ts-gn-seo h3 { margin: 2rem 0 .6rem; font: 700 1.2rem/1.25 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-seo h3:first-child { margin-top: 0; }
  .ts .ts-gn-seo p, .ts .ts-gn-seo li { color: var(--tss-text, rgba(246,250,247,.75)); line-height: 1.75; }
  .ts .ts-gn-seo p { margin: 0 0 1rem; }
  .ts .ts-gn-seo ul { margin: 0 0 1rem; padding-left: 1.2rem; }
  .ts .ts-gn-seo b { color: #f6faf7; }
  .ts .ts-gn-seo a { color: #6ee7b7; }
  /* Einzelne Geschichte */
  .ts-gn-story { max-width: 44rem; margin: 0 auto; }
  .ts .ts-gn-crumb { margin: 0; color: var(--ts-muted, #9aaba3); font-size: 13.5px; line-height: 1.5; }
  .ts .ts-gn-crumb a { color: inherit; text-decoration: none; }
  .ts .ts-gn-crumb a:hover { color: #6ee7b7; }
  .ts .ts-gn-crumb span { margin: 0 .4rem; opacity: .6; }
  .ts .ts-gn-h1 i { font-style: normal; color: #6ee7b7; }
  .ts .ts-gn-h1.ts-gn-h1--page { max-width: 18ch; margin-top: 2rem; font-size: clamp(2.3rem, 6.4vw, 5.4rem); }
  .ts .ts-gn-h1 { margin: 1rem 0 0; font: 800 clamp(2rem, 5.4vw, 3.8rem)/1.02 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.03em; }
  .ts-gn-by { display: flex; align-items: center; gap: .8rem; margin-top: 1.2rem; }
  .ts .ts-gn-by img { width: 46px !important; height: 46px !important; border-radius: 50%; object-fit: cover; }
  .ts .ts-gn-by p { margin: 0; font-size: 15px; line-height: 1.35; }
  .ts .ts-gn-by small { display: block; color: var(--ts-muted, #9aaba3); font-size: 13px; }
  .ts .ts-gn-facts { display: flex; flex-wrap: wrap; gap: .5rem 1.4rem; margin: 1.3rem 0 0; padding: .9rem 0; list-style: none; border-top: 1px solid var(--ts-line, rgba(255,255,255,.08)); border-bottom: 1px solid var(--ts-line, rgba(255,255,255,.08)); font-size: 15px; }
  .ts .ts-gn-facts a { color: inherit; }
  .ts .ts-gn-hero { display: block; width: 100% !important; height: auto !important; aspect-ratio: 4 / 3; margin-top: 1.5rem; border-radius: 22px; object-fit: cover; }
  .ts .ts-gn-about { margin-top: 1.5rem; padding: 1.2rem 1.4rem; border-radius: 18px; border-left: 3px solid #6ee7b7; background: rgba(110,231,183,.06); }
  .ts .ts-gn-about h2 { margin: 0 0 .5rem; font: 700 1.05rem/1.2 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-about p { margin: 0; color: var(--tss-text, rgba(246,250,247,.8)); line-height: 1.65; }
  .ts-gn-tools { position: sticky; top: calc(var(--ts-header-space, 96px) - 16px); z-index: 4; display: flex; flex-wrap: wrap; align-items: center; gap: .35rem; margin-top: 1.5rem; padding: .4rem; border-radius: 999px; border: 1px solid var(--ts-line, rgba(255,255,255,.08)); background: rgba(6,6,8,.85); backdrop-filter: blur(12px); width: max-content; max-width: 100%; }
  .ts .ts-gn-tools button { display: inline-flex; align-items: center; gap: .4rem; padding: 9px 13px; border-radius: 999px; border: 1px solid transparent; background: transparent; color: var(--ts-text, #f6faf7); font: 500 13.5px/1 var(--ts-font-body, Inter, sans-serif); cursor: pointer; }
  .ts .ts-gn-tools button:hover { border-color: var(--ts-line-strong, rgba(255,255,255,.14)); }
  .ts .ts-gn-tools button[aria-pressed="true"] { background: #f6faf7; color: #060608; }
  .ts .ts-gn-tools span { padding: 0 .2rem 0 .5rem; color: var(--ts-muted, #9aaba3); font-size: 13px; }
  .ts .ts-gn-tools i { width: 1px; height: 20px; margin: 0 .2rem; background: var(--ts-line-strong, rgba(255,255,255,.14)); }
  @media (max-width: 520px) { .ts-gn-tools { border-radius: 18px; } .ts .ts-gn-tools i { display: none; } }
  .ts-gn-text { --gn-size: 19px; margin-top: 2rem; }
  .ts .ts-gn-text > p { margin: 0 0 1.15em; font: 400 var(--gn-size)/1.85 var(--ts-font-body, Inter, sans-serif); color: #e7ece9; }
  .ts .ts-gn-tip { margin: 1.8em 0; padding: 1rem 1.2rem; border-radius: 14px; border: 1px dashed var(--ts-line-strong, rgba(255,255,255,.18)); font-size: 15px; line-height: 1.55; color: var(--tss-text, rgba(246,250,247,.8)); }
  .ts .ts-gn-tip b { margin-right: .5rem; padding: 3px 8px; border-radius: 6px; background: #6ee7b7; color: #060608; font: 700 11px/1 var(--ts-font-mono, monospace); letter-spacing: .1em; vertical-align: 1px; }
  .ts .ts-gn-tip a { color: #6ee7b7; }
  .ts .ts-gn-night { display: flex; align-items: center; gap: 1rem; margin: 2.25rem 0 0; padding: 1.3rem 1.5rem; border-radius: 22px; font: 700 clamp(1.1rem, 2vw, 1.4rem)/1.35 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-night svg { flex: none; color: #f7d046; }
  .ts .ts-gn-ask { margin-top: 1.25rem; padding: 1.3rem 1.5rem; border-radius: 22px; }
  .ts .ts-gn-ask h2 { margin: 0; font: 700 1.05rem/1.2 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-ask ul { margin: .8rem 0 0; padding: 0; list-style: none; display: grid; gap: .55rem; }
  .ts .ts-gn-ask li { position: relative; padding-left: 1.5rem; color: var(--tss-text, rgba(246,250,247,.8)); line-height: 1.55; }
  .ts .ts-gn-ask li::before { content: "?"; position: absolute; left: 0; top: 0; color: #6ee7b7; font-weight: 800; }
  .ts .ts-gn-end { margin: 2.5rem 0 0; text-align: center; color: var(--ts-muted, #9aaba3); font: 600 12px/1 var(--ts-font-mono, monospace); letter-spacing: .3em; }
  .ts-gn-more { display: flex; justify-content: center; margin-top: 2rem; }
  .ts .ts-gn-like { margin-top: 2.5rem; padding: clamp(1.3rem, 3vw, 2rem); border-radius: 22px; }
  .ts .ts-gn-like > h2 { margin: 0; font: 800 clamp(1.4rem, 2.6vw, 1.9rem)/1.1 var(--ts-font-display, 'Syne', sans-serif); letter-spacing: -0.02em; }
  .ts .ts-gn-book { display: grid; grid-template-columns: 72px 1fr; gap: 1rem; align-items: start; margin-top: 1.25rem; }
  .ts .ts-gn-book__ico { display: grid; place-items: center; width: 72px; height: 92px; border-radius: 6px 12px 12px 6px; background: linear-gradient(135deg, #2e9e6a, #1d4d3f); box-shadow: inset 6px 0 0 rgba(0,0,0,.25); font-size: 30px; }
  .ts .ts-gn-book h3 { margin: 0; font: 700 1.1rem/1.25 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-book p { margin: .4rem 0 0; color: var(--tss-text, rgba(246,250,247,.75)); line-height: 1.6; font-size: 15px; }
  .ts .ts-gn-share { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--ts-line, rgba(255,255,255,.08)); }
  .ts .ts-gn-share > span { margin-right: .4rem; font: 600 14px/1 var(--ts-font-body, Inter, sans-serif); }
  .ts .ts-gn-audio { margin-top: 1.5rem; padding: 1rem 1.2rem; border-radius: 18px; }
  .ts .ts-gn-audio audio { width: 100%; margin-top: .6rem; }
  .ts .ts-gn-reihe { margin-top: 2rem; }
  .ts .ts-gn-reihe h2 { margin: 0; font: 700 1.15rem/1.2 var(--ts-font-display, 'Syne', sans-serif); }
  .ts .ts-gn-reihe ul { margin: .8rem 0 0; padding: 0; list-style: none; border-top: 1px solid var(--ts-line, rgba(255,255,255,.08)); }
  .ts .ts-gn-reihe li { display: flex; justify-content: space-between; gap: 1rem; padding: .85rem 0; border-bottom: 1px solid var(--ts-line, rgba(255,255,255,.08)); }
  .ts .ts-gn-reihe a { color: #f6faf7; font: 600 1rem/1.3 var(--ts-font-body, Inter, sans-serif); text-decoration: none; }
  .ts .ts-gn-reihe a:hover { color: #6ee7b7; }
  .ts .ts-gn-reihe span { color: var(--ts-muted, #9aaba3); white-space: nowrap; font-size: 14px; }
  .ts-gn-glance { display: grid; gap: 1.5rem; margin-top: 1.75rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .ts .ts-gn-glance h3 { margin: 0 0 .7rem; color: var(--ts-muted, #9aaba3); font: 600 11px/1.3 var(--ts-font-mono, monospace); letter-spacing: .14em; text-transform: uppercase; }
  .ts .ts-gn-glance ul { margin: 0; padding: 0; list-style: none; display: grid; gap: .5rem; }
  .ts .ts-gn-glance a { color: var(--ts-text, #f6faf7); text-decoration: none; font-size: 15px; }
  .ts .ts-gn-glance a:hover { color: #6ee7b7; }
  /* Nachtmodus: dunkler, wärmer – zum Vorlesen im abgedunkelten Kinderzimmer */
  html.ts-gn-dark .ts-gn-page { background: #050505; }
  html.ts-gn-dark .ts .ts-gn-text > p { color: #e9dcc0; }
  html.ts-gn-dark .ts-gn-dim, html.ts-gn-dark .ts-gn-tip { opacity: .25; transition: opacity .4s; }
  html.ts-gn-dark .ts-gn-hero { filter: brightness(.45); }
  html.ts-gn-dark .ts-khr, html.ts-gn-dark .ts-header { opacity: .25; }
  @media (min-width: 640px) {
    .ts-am-gal { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ts-am-packs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .ts-gn-glance { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .ts-gn-figs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (min-width: 900px) {
    .ts-gn-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ts-gn-grid--4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .ts-gn-figs { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  }
  @media (min-width: 1024px) {
    .ts-am-gal { grid-template-columns: repeat(5, minmax(0, 1fr)); }
    .ts-am-packs { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  }
  @media print {
    .ts-khr, .ts-gn-tools, .ts-gn-noprint, .ts-gn-tip, .ts-gn-hero, header, footer, #footer-sections, .ts-header { display: none !important; }
    .ts .ts-gn-text > p { color: #111 !important; font-size: 13pt !important; }
    .ts .ts-gn-h1, .ts .ts-gn-night, .ts .ts-gn-ask, .ts .ts-gn-ask li, .ts .ts-gn-about, .ts .ts-gn-about p, .ts .ts-gn-facts { color: #111 !important; background: none !important; }
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
    gcards = ''.join(karte_geschichte(g_von(s), False) for s in LIEBLINGE[:3])
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
    <div class="ts-am__blockhead"><p class="ts-label ts-muted">[ Auch im Kreativhafen ]</p><p class="ts-label ts-muted">Gute-Nacht-Geschichten</p></div>
    <h2 id="ts-am-gn-t" class="ts-am__h2">Und abends: vorlesen<i>.</i></h2>
    <p class="ts-am__sub">Kostenlose Gute-Nacht-Geschichten – direkt auf der Seite lesen, ohne Download.</p>
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
# Aufbau nach dem Vorbild von zitronenbande.de und zwergenstark.de:
# Einleitung → Lieblingsgeschichten → passend zum Monat → alle Geschichten mit Vorlesedauer-Filter → Figuren → Ratgeber-Text → FAQ
SAISON_FENSTER = {'hw': (1001, 1031), 'lt': (1020, 1111), 'ad': (1112, 1224), 'wi': (1201, 228)}
DAUER = [('alle', 'Alle'), ('kurz', '1–3 Min.'), ('mittel', '4–6 Min.'), ('lang', 'ab 7 Min.')]
LIEBLINGE = ['moewe-mats-will-nicht-schlafen', 'funki-der-kleine-drache', 'bagger-bruno-macht-feierabend',
             'ella-fliegt-zum-mond', 'das-kleine-gespenst-huhu', 'teddy-haelt-wache']
FIGUREN = [
    ('Möwe Mats', 'moewe-mats-will-nicht-schlafen', 'Die neugierige Möwe vom Hamburger Hafen – mit eigener Reihe.', 'Mats'),
    ('Leuchtturm Lotte', 'leuchtturm-lotte-und-der-nebel', 'Ihr Licht ist klein, ihr Herz ist groß.', 'Lotte'),
    ('Fähre Frieda', 'die-faehre-frieda-faehrt-nach-hause', 'Bringt jeden Abend alle sicher nach Hause.', 'Frieda'),
    ('Kran Karl', 'ein-schlaflied-fuer-kran-karl', 'Der größte Kran im Hafen – und der müdeste.', 'Karl'),
    ('Funki', 'funki-der-kleine-drache', 'Der kleine Drache, der kein Feuer spucken kann.', 'Funki'),
    ('Bagger Bruno', 'bagger-bruno-macht-feierabend', 'Will nie Feierabend machen.', 'Bruno'),
    ('Wichtel Wilbur', 'wichtel-wilbur-und-das-warten', 'Bewacht im Advent jede Nacht ein Türchen.', 'Wilbur'),
    ('Gespenst Huhu', 'das-kleine-gespenst-huhu', 'Fürchtet sich vor allem – sogar vor sich selbst.', 'Huhu'),
]
# „Geschichten auf einen Blick“ (unter jeder Geschichte und als Sprungziele der Übersicht)
GLANCE = [
    ('Nach Dauer', [('Kurz (1–3 Minuten)', 'dauer=kurz'), ('Mittel (4–6 Minuten)', 'dauer=mittel'), ('Lang (ab 7 Minuten)', 'dauer=lang')]),
    ('Nach Alter', [('Für 2-Jährige', 'alter=2'), ('Für 3- bis 4-Jährige', 'alter=3'), ('Ab 5 Jahren', 'alter=5')]),
    ('Nach Thema', [('Hamburger Hafen', 'thema=Hafen'), ('Jahreszeiten', 'thema=Jahreszeiten'), ('Fahrzeuge', 'thema=Fahrzeuge'),
                    ('Weltraum', 'thema=Weltraum'), ('Mut & Gefühle', 'thema=Gefühle'), ('Freundschaft', 'thema=Freundschaft')]),
    ('Nach Figur', [('Möwe Mats', 'suche=Mats'), ('Funki, der Drache', 'suche=Funki'), ('Leuchtturm Lotte', 'suche=Lotte'), ('Bagger Bruno', 'suche=Bruno')]),
]
AUTOR_IMG = 'https://images.squarespace-cdn.com/content/v1/6869717aa7c996116c8c8a56/ffc25dc6-15ea-4d07-ab0d-6173fde95edf/IMG_3686.jpeg?format=300w'


def bild_url(g):
    return f'{BASIS}geschichten/bilder/{g["slug"]}.webp'


def g_von(slug):
    return next(g for g in GESCHICHTEN if g['slug'] == slug)


def saison_von(g):
    w = SAISON_FENSTER.get(g['motiv'][:2])
    return f'{w[0]}-{w[1]}' if w else ''


def glance_html():
    cols = ''.join(f'<div><h3>{esc(h)}</h3><ul>' + ''.join(f'<li><a href="/gute-nacht-geschichten?{q}#ts-gn-alle">{esc(t)}</a></li>' for t, q in links) + '</ul></div>'
                   for h, links in GLANCE)
    return f'<div class="ts-gn-glance">{cols}</div>'


def heute_js():
    return r'''
<script>
/* Gute-Nacht-Geschichten: Auswahl zum Monat, Vorlesedauer-Filter, Suche, „Mehr anzeigen“, Links ?dauer= ?alter= ?thema= ?suche= */
(() => {
  const all = document.getElementById('ts-gn-alle'); if (!all) return;
  const cards = [...all.querySelectorAll('[data-gn-card]')];
  const d = new Date(), md = (d.getMonth() + 1) * 100 + d.getDate();
  const inWin = s => { if (!s) return false; const [a, b] = s.split('-').map(Number); return a <= b ? md >= a && md <= b : md >= a || md <= b; };
  /* Beliebt im <Monat> */
  const MON = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  const TXT = { 9: 'Bunte Blätter, Kürbisse und die ersten dunklen Abende: Diese Geschichten passen jetzt perfekt.',
    10: 'Laternen, Nebel und Kerzenlicht: Geschichten für die ruhigen Novemberabende.',
    11: 'Die Zeit des Wartens: Geschichten für die Adventsabende – mit Wichtel Wilbur und Co.',
    0: 'Kalt draußen, warm im Bett: Wintergeschichten zum Einkuscheln.', 1: 'Kalt draußen, warm im Bett: Wintergeschichten zum Einkuscheln.' };
  const sb = document.querySelector('[data-gn-saison]'), saison = cards.filter(c => inWin(c.dataset.saison));
  if (sb && saison.length) {
    sb.querySelector('[data-t]').textContent = 'Beliebt im ' + MON[d.getMonth()];
    sb.querySelector('[data-s]').textContent = TXT[d.getMonth()] || 'Diese Geschichten passen gerade besonders gut.';
    sb.querySelector('.ts-gn-grid').append(...saison.slice(0, 4).map(c => { const k = c.cloneNode(true); k.removeAttribute('data-gn-card'); k.hidden = false; return k; }));
    sb.hidden = false;
  }
  /* Filter */
  const q = all.querySelector('[data-gn-q]'), more = all.querySelector('[data-gn-more]'), state = all.querySelector('[data-gn-state]');
  const P = new URLSearchParams(location.search);
  let dauer = P.get('dauer') || 'alle', alter = P.get('alter') || '', thema = P.get('thema') || '', offen = false;
  if (P.get('suche') && q) q.value = P.get('suche');
  const ALT = { 2: 'für 2-Jährige', 3: 'für 3- bis 4-Jährige', 5: 'ab 5 Jahren' };
  const ok = c => {
    const z = +c.dataset.zeit, a = +c.dataset.alter, s = (q && q.value || '').trim().toLowerCase();
    return (dauer === 'alle' || (dauer === 'kurz' ? z <= 3 : dauer === 'mittel' ? z >= 4 && z <= 6 : z >= 7))
      && (!alter || (alter === '2' ? a <= 2 : alter === '3' ? a >= 3 && a <= 4 : a >= 5))
      && (!thema || c.dataset.themen.split(',').includes(thema))
      && (!s || c.dataset.suche.includes(s));
  };
  const apply = () => {
    const aktiv = dauer !== 'alle' || alter || thema || (q && q.value.trim());
    let n = 0, shown = 0;
    cards.forEach(c => { const v = ok(c); if (v) n++; const zeig = v && (aktiv || offen || n <= 12); c.hidden = !zeig; if (zeig) shown++; });
    if (more) more.hidden = !!aktiv || offen || n <= 12;
    all.querySelectorAll('[data-dauer]').forEach(b => b.setAttribute('aria-pressed', b.dataset.dauer === dauer));
    const teile = []; if (thema) teile.push('Thema „' + thema + '“'); if (alter) teile.push(ALT[alter] || '');
    if (q && q.value.trim()) teile.push('Suche „' + q.value.trim() + '“');
    state.innerHTML = '';
    state.append(n + (n === 1 ? ' Geschichte' : ' Geschichten') + (teile.length ? ' · ' + teile.join(' · ') : ''));
    if (aktiv) { const r = document.createElement('button'); r.type = 'button'; r.textContent = 'Alle zeigen'; r.onclick = () => { dauer = 'alle'; alter = thema = ''; if (q) q.value = ''; history.replaceState(null, '', location.pathname + '#ts-gn-alle'); apply(); }; state.append(r); }
    if (!n) state.append(' – probier eine andere Länge oder ein anderes Wort.');
  };
  all.querySelectorAll('[data-dauer]').forEach(b => b.addEventListener('click', () => { dauer = b.dataset.dauer; apply(); }));
  if (q) q.addEventListener('input', apply);
  if (more) more.addEventListener('click', () => { offen = true; apply(); });
  /* Figuren und Sprunglinks auf derselben Seite: ohne Neuladen filtern */
  document.querySelectorAll('a[href^="/gute-nacht-geschichten?"]').forEach(a => a.addEventListener('click', e => {
    if (location.pathname.replace(/\/+$/, '') !== '/gute-nacht-geschichten') return;
    e.preventDefault(); const p = new URLSearchParams(a.getAttribute('href').split('?')[1].split('#')[0]);
    dauer = p.get('dauer') || 'alle'; alter = p.get('alter') || ''; thema = p.get('thema') || ''; if (q) q.value = p.get('suche') || '';
    apply(); all.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }));
  apply();
})();
</script>'''


FAQ_GN = [
    ('Warum sind Gute-Nacht-Geschichten so wichtig für Kinder?', 'Eine Geschichte vor dem Schlafen ist ein fester, ruhiger Moment am Ende des Tages. Kinder kommen zur Ruhe, fühlen sich geborgen und verarbeiten, was sie erlebt haben. Ganz nebenbei wachsen Wortschatz, Fantasie und Konzentration – und die Nähe zwischen euch.'),
    ('Wie lang sollte eine Gute-Nacht-Geschichte sein?', 'So lang, wie euer Kind gut zuhören kann. Für 2-Jährige reichen 1–2 Minuten, ab 3 Jahren passen 4–5 Minuten, größere Kinder mögen auch 7 Minuten und mehr. Mit dem Filter „Vorlesedauer“ findest du schnell die passende Länge.'),
    ('Welche Themen eignen sich zum Einschlafen?', 'Geschichten mit kleinen, lösbaren Problemen und einem warmen Ende: Freundschaft, Mut, Gefühle, Tiere, Fahrzeuge oder ein bisschen Fantasie. Spannung darf sein – aber am Schluss ist alles gut.'),
    ('Wie wird das Vorlesen am Abend besonders entspannt?', 'Licht runter, kuscheln, langsam und leise lesen. Gegen Ende darf die Stimme immer ruhiger werden. Auf jeder Geschichten-Seite gibt es einen Nachtmodus, der die Seite dunkel und die Schrift warm macht.'),
    ('Muss ich etwas herunterladen oder mich anmelden?', 'Nein. Alle Geschichten liest du direkt hier auf der Seite – am Handy, Tablet oder Computer. Kostenlos und ohne Anmeldung.'),
    ('Darf ich die Geschichten in der Kita oder Schule vorlesen?', 'Ja, sehr gern – zu Hause, in der Kita, in der Schule oder in der Bücherei. Bitte teilt den Link zur Geschichte, statt die Texte zu kopieren.'),
]


def seo_html():
    n = len(GESCHICHTEN)
    kurz = sum(g['lesezeit'] <= 3 for g in GESCHICHTEN)
    return f'''<h3>Du suchst eine Gute-Nacht-Geschichte zum Vorlesen?</h3>
<p>Dann bist du hier richtig. Im Kreativhafen findest du {n} kostenlose Gute-Nacht-Geschichten für Kinder von 2 bis 7 Jahren – alle selbst geschrieben und direkt hier lesbar. Ohne Download, ohne Anmeldung. Nutze den Filter „Vorlesedauer“, um die passende Einschlafgeschichte für heute Abend zu finden: kurz (1–3 Min.), mittel (4–6 Min.) oder etwas länger.</p>
<h3>Wovon handeln unsere Gute-Nacht-Geschichten?</h3>
<p>Je nachdem, was dein Kind gerade liebt, findest du hier die passende Geschichte:</p>
<ul>
<li><b>Hamburger Hafen:</b> Möwe Mats, Leuchtturm Lotte, Fähre Frieda und Kran Karl erleben kleine, ruhige Abenteuer zwischen Containern und Elbe. <a href="/gute-nacht-geschichten?thema=Hafen#ts-gn-alle">Zu den Hafengeschichten</a></li>
<li><b>Fahrzeuge:</b> Bagger, Auto und Flugzeug machen Feierabend – perfekt für kleine Fahrzeug-Fans.</li>
<li><b>Fantasie &amp; Märchen:</b> Drache Funki, Nixe Nele, ein Einhorn und ein Ritter, der sich vor dem Dunkeln fürchtet.</li>
<li><b>Jahreszeiten:</b> Ein kleines Gespenst im Herbst, eine Laterne im November, Wichtel Wilbur im Advent und ein Schneemann im Winter.</li>
</ul>
<h3>Kurze Gute-Nacht-Geschichten für müde Abende</h3>
<p>Manchmal ist schon die Zahnbürste zu viel. Für solche Abende gibt es {kurz} ganz kurze Geschichten mit 1–3 Minuten – mit Wiederholungen und Geräuschen zum Mitmachen, ideal schon für 2-Jährige. <a href="/gute-nacht-geschichten?dauer=kurz#ts-gn-alle">Kurze Geschichten anzeigen</a></p>
<h3>Wer schreibt die Geschichten?</h3>
<p>Die Geschichten entstehen im Kreativhafen von Trutz Stähler – Papa aus Hamburg und Autor der Kritzelbücher und des Kinderkrimis „Maria Holm“. Neue Geschichten kommen regelmäßig dazu.</p>'''


def karte_geschichte(g, haupt=True):
    themen = ','.join(g['themen'])
    such = ' '.join([g['titel'], g['teaser'], themen, g.get('reihe', '')] + g['absaetze'][:3]).lower()
    data = (f' data-gn-card data-themen="{esc(themen)}" data-zeit="{g["lesezeit"]}" data-alter="{g["alter"]}" '
            f'data-saison="{saison_von(g)}" data-suche="{esc(such)}"') if haupt else ''
    return (f'<a class="ts-gn-card" href="{GESCH_URL}{g["slug"]}"{data}>'
            f'<img src="{bild_url(g)}" alt="" loading="lazy" width="800" height="600">'
            f'<div class="ts-gn-card__body"><h3 class="ts-gn-card__t">{esc(g["titel"])}</h3>'
            f'<p class="ts-gn-card__m">ab {g["alter"]} Jahren · ca. {g["lesezeit"]} Min.</p></div></a>')


def seite_geschichten():
    n = len(GESCHICHTEN)
    lieblinge = ''.join(karte_geschichte(g_von(s), False) for s in LIEBLINGE)
    cards = ''.join(karte_geschichte(g) for g in GESCHICHTEN)
    dauer = ''.join(f'<button type="button" data-dauer="{v}" aria-pressed="{str(v == "alle").lower()}">{esc(t)}</button>' for v, t in DAUER)
    figuren = ''.join(f'<a class="ts-gn-fig" href="/gute-nacht-geschichten?suche={esc(s)}#ts-gn-alle"><img src="{bild_url(g_von(slug))}" alt="" loading="lazy" width="120" height="120">'
                      f'<b>{esc(nm)}</b><span>{esc(t)}</span></a>' for nm, slug, t, s in FIGUREN)
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in FAQ_GN)
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Gute-Nacht-Geschichten für Kinder zum Vorlesen',
          'url': f'https://{KAT.DOMAIN}/gute-nacht-geschichten', 'inLanguage': 'de', 'isAccessibleForFree': True,
          'mainEntity': {'@type': 'ItemList', 'numberOfItems': n,
                         'itemListElement': [{'@type': 'ListItem', 'position': i, 'url': f'https://{KAT.DOMAIN}{GESCH_URL}{g["slug"]}', 'name': g['titel']}
                                             for i, g in enumerate(GESCHICHTEN, 1)]}}
    return f'''<!-- =====================================================================
  KREATIVHAFEN – Seite /gute-nacht-geschichten (Übersicht)  ·  Code-Block, alles einfügen
  Die einzelnen Geschichten liegen als Blog-Beiträge unter {GESCH_URL}<name>.
====================================================================== -->
{KH_CSS}
{reiter_html()}
<div class="ts ts-am tss ts-bleed ts-kh2 ts-gn-page" style="padding-top:0">
  <div class="ts-am__orb" aria-hidden="true"></div>
  <section class="ts-container tss--top" aria-labelledby="ts-gn-title" style="padding-bottom:0">
    <div class="tss-kicker"><p class="ts-label ts-muted">[ Gratis Gute-Nacht-Geschichten lesen ]</p><p class="ts-label ts-muted">Ohne Download · ohne Anmeldung</p></div>
    <h1 id="ts-gn-title" class="ts-gn-h1 ts-gn-h1--page">Gute-Nacht-Geschichten für Kinder zum Vorlesen<i>.</i></h1>
    <p class="ts-gn-intro">Hier findest du {n} kostenlose Gute-Nacht-Geschichten für Kinder von 2 bis 7 Jahren. Alle selbst geschrieben und direkt hier zum Vorlesen. Entdecke die Reihe rund um Möwe Mats aus dem Hamburger Hafen oder filtere nach Vorlesedauer.</p>
    <nav class="ts-gn-jump" aria-label="Schnell finden"><a href="#ts-gn-alle">Alle Geschichten</a><a href="/gute-nacht-geschichten?dauer=kurz#ts-gn-alle">Kurze Geschichten</a><a href="/gute-nacht-geschichten?suche=Mats#ts-gn-alle">Möwe Mats</a><a href="/gute-nacht-geschichten?thema=Jahreszeiten#ts-gn-alle">Herbst &amp; Winter</a></nav>
  </section>

  <section class="ts-container ts-am__block" aria-labelledby="ts-gn-lieb-t">
    <h2 id="ts-gn-lieb-t" class="ts-am__h2">Unsere Lieblingsgeschichten</h2>
    <div class="ts-gn-grid">{lieblinge}</div>
  </section>

  <section class="ts-container ts-am__block" data-gn-saison hidden aria-labelledby="ts-gn-saison-t">
    <h2 id="ts-gn-saison-t" class="ts-am__h2" data-t>Passend zur Jahreszeit</h2>
    <p class="ts-am__sub" data-s></p>
    <div class="ts-gn-grid ts-gn-grid--4"></div>
  </section>

  <section id="ts-gn-alle" class="ts-container ts-am__block" aria-labelledby="ts-gn-alle-t" style="scroll-margin-top:110px">
    <h2 id="ts-gn-alle-t" class="ts-am__h2">Alle Gute-Nacht-Geschichten</h2>
    <p class="ts-am__sub">Hier findest du alle unsere Gute-Nacht-Geschichten – von den neuesten bis zu den kürzesten. Filtere nach Vorlesedauer, um die passende Geschichte für heute Abend zu finden.</p>
    <div class="ts-gn-bar">
      <div class="ts-gn-filter" role="group" aria-label="Vorlesedauer"><b>Vorlesedauer:</b>{dauer}</div>
      <label class="ts-gn-search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
        <input type="search" placeholder="Suchen: Möwe, Drache, Bagger …" aria-label="Geschichten durchsuchen" data-gn-q></label>
    </div>
    <p class="ts-gn-state" data-gn-state aria-live="polite">{n} Geschichten</p>
    <div class="ts-gn-grid">{cards}</div>
    <div class="ts-gn-morebtn"><button type="button" class="ts-am-mini" data-gn-more hidden>Mehr Geschichten anzeigen</button></div>
  </section>

  <section class="ts-container ts-am__block" aria-labelledby="ts-gn-fig-t">
    <h2 id="ts-gn-fig-t" class="ts-am__h2">Beliebte Figuren</h2>
    <div class="ts-gn-figs">{figuren}</div>
  </section>

  <section class="ts-container ts-am__block" aria-label="Rund ums Vorlesen">
    <div class="ts-gn-seo">{seo_html()}</div>
  </section>

  <section class="ts-container ts-am__block ts-am__end" aria-labelledby="ts-gn-faq-t">
    <h2 id="ts-gn-faq-t" class="ts-am__h2" style="margin-bottom:1.5rem">FAQ – Gute-Nacht-Geschichten im Kreativhafen</h2>
    <div class="tss-faq">{faq}</div>
    <div class="ts-am-final ts-glass">
      <p>Noch mehr zum Vorlesen und Malen: meine Bücher.</p>
      {btn('Zu den Büchern', '/malbuecher')}
    </div>
  </section>
</div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{jsonld_faq(FAQ_GN)}
{heute_js()}'''


STORY_JS = r'''
<script>
/* Geschichte: Vorlesen lassen, Schriftgröße, Nachtmodus, Teilen */
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
  /* Vorlesen lassen (Computerstimme des Geräts, falls vorhanden) */
  const sp = root.querySelector('[data-gn="speak"]');
  if (!('speechSynthesis' in window)) sp.hidden = true;
  else {
    addEventListener('pagehide', () => speechSynthesis.cancel());
    sp.addEventListener('click', () => {
      if (speechSynthesis.speaking) { speechSynthesis.cancel(); sp.setAttribute('aria-pressed', 'false'); return; }
      const t = root.querySelector('.ts-gn-h1').textContent + '. ' + [...txt.querySelectorAll(':scope > p')].map(p => p.textContent).join(' ') + ' ' + ((root.querySelector('[data-gn-night]') || {}).textContent || '');
      const u = new SpeechSynthesisUtterance(t); u.lang = 'de-DE'; u.rate = .85; u.pitch = 1;
      const v = speechSynthesis.getVoices().find(v => /^de/i.test(v.lang)); if (v) u.voice = v;
      u.onend = () => sp.setAttribute('aria-pressed', 'false');
      speechSynthesis.speak(u); sp.setAttribute('aria-pressed', 'true');
    });
  }
  const sh = root.querySelector('[data-gn="share"]');
  if (sh) sh.addEventListener('click', async () => {
    const data = { title: document.title, text: 'Eine Gute-Nacht-Geschichte zum Vorlesen:', url: location.href };
    try { if (navigator.share) await navigator.share(data); else { await navigator.clipboard.writeText(location.href); sh.textContent = 'Link kopiert ✓'; } } catch (e) {}
  });
  const wa = root.querySelector('[data-gn="wa"]');
  if (wa) wa.href = 'https://wa.me/?text=' + encodeURIComponent('Eine schöne Gute-Nacht-Geschichte zum Vorlesen: ' + location.href);
})();
</script>'''


def tipp(g, i):
    """TIPP-Kasten mitten im Text (wie bei Zitronenbande) – wechselt von Geschichte zu Geschichte."""
    if g.get('reihe'):
        return f'Diese Geschichte gehört zur Reihe <a href="/gute-nacht-geschichten?suche=Mats#ts-gn-alle">„{esc(g["reihe"])}“</a> – es gibt noch mehr Abenteuer mit der kleinen Möwe.'
    opts = [
        'Kennst du schon <a href="/gute-nacht-geschichten?suche=Mats#ts-gn-alle">Möwe Mats</a>? Die neugierige Möwe aus dem Hamburger Hafen hat eine eigene Geschichten-Reihe.',
        'Mit dem Mond-Knopf oben wird die Seite dunkel und die Schrift warm – angenehm zum Vorlesen im abgedunkelten Kinderzimmer.',
        'An müden Abenden: Unsere <a href="/gute-nacht-geschichten?dauer=kurz#ts-gn-alle">kurzen Gute-Nacht-Geschichten</a> dauern nur 1–3 Minuten.',
        'Lust auf mehr zum Lesen und Malen? Schau dir meine <a href="/malbuecher">Bücher im Kreativhafen</a> an.',
    ]
    if 'Mats' in ' '.join(g['absaetze']):        # Mats kommt schon vor → nicht auf Mats hinweisen
        opts = opts[1:]
    return opts[i % len(opts)]


def geschichte_block(g):
    i = GESCHICHTEN.index(g)
    # weitere Geschichten: erst gleiche Themen, dann ähnliches Alter (wie „Weitere Gute-Nacht-Geschichten“ bei Zitronenbande)
    weitere = sorted([x for x in GESCHICHTEN if x is not g],
                     key=lambda x: (-len(set(x['themen']) & set(g['themen'])), abs(x['alter'] - g['alter']), GESCHICHTEN.index(x)))[:4]
    abs_ = g['absaetze']
    mitte = max(2, len(abs_) // 2)
    absaetze = (''.join(f'<p>{esc(a)}</p>' for a in abs_[:mitte]) +
                f'<aside class="ts-gn-tip ts-gn-noprint"><b>TIPP</b>{tipp(g, i)}</aside>' +
                ''.join(f'<p>{esc(a)}</p>' for a in abs_[mitte:]))
    fragen = ''.join(f'<li>{esc(f)}</li>' for f in g['fragen'])
    moon = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>'
    ld = {'@context': 'https://schema.org', '@type': 'ShortStory', 'name': g['titel'], 'headline': g['titel'], 'description': g['teaser'],
          'inLanguage': 'de', 'author': {'@type': 'Person', 'name': 'Trutz Stähler', 'url': f'https://{KAT.DOMAIN}/ueber-mich'},
          'publisher': {'@type': 'Organization', 'name': 'Kreativhafen'}, 'isAccessibleForFree': True,
          'typicalAgeRange': f'{g["alter"]}-7', 'timeRequired': f'PT{g["lesezeit"]}M', 'genre': 'Gute-Nacht-Geschichte',
          'keywords': ', '.join(g['themen']), 'image': bild_url(g),
          'url': f'https://{KAT.DOMAIN}{GESCH_URL}{g["slug"]}', 'wordCount': sum(len(a.split()) for a in g['absaetze'])}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Kreativhafen', 'item': f'https://{KAT.DOMAIN}/kreativhafen'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Gute-Nacht-Geschichten', 'item': f'https://{KAT.DOMAIN}/gute-nacht-geschichten'},
        {'@type': 'ListItem', 'position': 3, 'name': g['titel']}]}
    ico = lambda d: f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">{d}</svg>'
    gn_html = f'<p class="ts-gn-night ts-glass" data-gn-night>{moon}<span>{esc(g["gute_nacht"])}</span></p>' if g['gute_nacht'] else ''
    fr_html = (f'<div class="ts-gn-ask ts-glass ts-gn-dim"><h2>Zum Reden danach</h2><ul>{fragen}</ul></div>') if g['fragen'] else ''
    audio = (f'<div class="ts-gn-audio ts-glass ts-gn-noprint"><p class="ts-label ts-muted">[ Zum Anhören ]</p>'
             f'<audio controls preload="none" src="{esc(g["audio"])}"></audio></div>') if g.get('audio') else ''
    if g['alter'] >= 5:
        buch = ('/romane', '🔎', 'Maria Holm – der Kinderkrimi', 'Spannend, aber nicht zu gruselig: Der Kinderkrimi von Trutz für Leseratten und Rätselfans.')
    else:
        buch = ('/malbuecher', '✏️', 'Die Kritzelbücher', 'Zum Kritzeln, Malen und Weiterdenken – die Malbücher von Trutz für kleine Künstlerinnen und Künstler.')
    reihe = [x for x in GESCHICHTEN if g.get('reihe') and x.get('reihe') == g['reihe']]
    reihe_html = ('<div class="ts-gn-reihe ts-gn-dim ts-gn-noprint"><h2>Alle Geschichten der Reihe „' + esc(g['reihe']) + '“</h2><ul>' +
                  ''.join((f'<li><b>{esc(x["titel"])}</b><span>du liest gerade</span></li>' if x is g else
                           f'<li><a href="{GESCH_URL}{x["slug"]}">{esc(x["titel"])}</a><span>ca. {x["lesezeit"]} Min.</span></li>') for x in reihe) +
                  '</ul></div>') if reihe else ''
    facts = f'<li>🎯 ab {g["alter"]} Jahren</li><li>🕔 ca. {g["lesezeit"]} Minuten Vorlesedauer</li>'
    if g.get('reihe'):
        facts += f'<li>📚 Reihe: <a href="/gute-nacht-geschichten?suche=Mats#ts-gn-alle">{esc(g["reihe"])}</a></li>'
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
      <nav class="ts-gn-crumb ts-gn-dim" aria-label="Brotkrumen"><a href="/kreativhafen">Kreativhafen</a><span>›</span><a href="/gute-nacht-geschichten">Gute-Nacht-Geschichten</a><span>›</span>{esc(g['titel'])}</nav>
      <h1 id="ts-gn-h" class="ts-gn-h1">{esc(g['titel'])}</h1>
      <div class="ts-gn-by ts-gn-dim"><img src="{AUTOR_IMG}" alt="" width="46" height="46" loading="lazy"><p>von <b>Trutz Stähler</b><small>Papa aus Hamburg · schreibt Kinderbücher</small></p></div>
      <ul class="ts-gn-facts ts-gn-dim">{facts}</ul>
      <img class="ts-gn-hero" src="{bild_url(g)}" alt="Illustration zur Gute-Nacht-Geschichte „{esc(g['titel'])}“" width="800" height="600">
      <div class="ts-gn-about ts-gn-dim"><h2>Darum geht’s</h2><p>{esc(g['teaser'])}</p></div>
      <div class="ts-gn-tools" role="toolbar" aria-label="Lesehilfen">
        <button type="button" data-gn="speak" aria-pressed="false">{ico('<path d="M11 5 6 9H2v6h4l5 4V5Z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>')}Vorlesen</button>
        <i aria-hidden="true"></i><span>Schrift</span>
        <button type="button" data-gn="minus" aria-label="Schrift kleiner">A−</button>
        <button type="button" data-gn="plus" aria-label="Schrift größer">A+</button>
        <i aria-hidden="true"></i>
        <button type="button" data-gn="night" aria-pressed="false">{ico('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/>')}Nachtmodus</button>
      </div>
      {audio}
      <div class="ts-gn-text">{absaetze}</div>
      {gn_html}
      {fr_html}
      <p class="ts-gn-end ts-gn-dim" aria-hidden="true">✦ ENDE ✦</p>
      <div class="ts-gn-more ts-gn-noprint">{btn('Mehr Geschichten lesen', '/gute-nacht-geschichten')}</div>
      <div class="ts-gn-like ts-glass ts-gn-dim ts-gn-noprint">
        <h2>Hat dir die Geschichte gefallen<i style="font-style:normal;color:#6ee7b7">?</i></h2>
        <div class="ts-gn-book"><span class="ts-gn-book__ico" aria-hidden="true">{buch[1]}</span>
          <div><h3>{esc(buch[2])}</h3><p>{esc(buch[3])}</p>
            <div class="ts-am__ctas" style="margin-top:.9rem"><a class="ts-am-mini ts-am-mini--hi" href="{buch[0]}">Mehr dazu</a></div></div></div>
        <div class="ts-gn-share"><span>Mit Freunden teilen</span>
          <button type="button" class="ts-am-mini" data-gn="share">Link teilen</button>
          <a class="ts-am-mini" data-gn="wa" href="https://wa.me/" target="_blank" rel="noopener">WhatsApp</a></div>
      </div>
      {reihe_html}
    </div>
  </div>
  <section class="ts-container ts-am__block ts-gn-noprint ts-gn-dim" aria-labelledby="ts-gn-weitere-t">
    <h2 id="ts-gn-weitere-t" class="ts-am__h2">Weitere Gute-Nacht-Geschichten</h2>
    <p class="ts-am__sub">Mehr Einschlafgeschichten findest du in unserer Sammlung: <a href="/gute-nacht-geschichten" style="color:#6ee7b7">Alle Gute-Nacht-Geschichten →</a></p>
    <div class="ts-gn-grid ts-gn-grid--4">{''.join(karte_geschichte(x, False) for x in weitere)}</div>
  </section>
  <section class="ts-container ts-am__block ts-am__end ts-gn-noprint ts-gn-dim" aria-labelledby="ts-gn-glance-t">
    <h2 id="ts-gn-glance-t" class="ts-am__h2">Geschichten auf einen Blick</h2>
    {glance_html()}
  </section>
</article>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>
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
          <img src="{BASIS}geschichten/bilder/moewe-mats-will-nicht-schlafen.webp" alt="Möwe Mats aus den Gute-Nacht-Geschichten" loading="lazy">
        </div>
        <div class="ts-kh-card__body">
          <h3 class="ts-kh-card__title">Gute-Nacht-Geschichten</h3>
          <p class="ts-kh-card__text">{len(GESCHICHTEN)} Gute-Nacht-Geschichten zum Vorlesen – direkt auf der Seite, ohne Download. Mit Vorlesedauer, Nachtmodus und Vorlese-Funktion.</p>
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

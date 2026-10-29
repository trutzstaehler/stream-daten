"""Produktbilder, Social-Media-Bilder und Vorschau-Grafiken im Look von trutzstaehler.de.

python3 bilder.py   -> ../02-bilder/...
"""
import os, sys, subprocess, glob, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel as K
import motive  # noqa
import katalog as KAT
import pdf as PDF

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '02-bilder')
SEITEN = os.path.join(HERE, 'build', 'seiten')
FONTS = 'file://' + os.path.join(HERE, 'fonts')
esc = html.escape

PDFNAME = dict(PDF.DATEINAMEN, probier='Probierpaket_3-Ausmalbilder-gratis')


def seiten(pid, dpi=110):
    """PDF-Seiten als PNG (Cache)."""
    d = os.path.join(SEITEN, pid)
    pdf = os.path.join(PDF.OUT, PDFNAME[pid] + '.pdf')
    have = glob.glob(os.path.join(d, 'p-*.png'))
    if not have or min(os.path.getmtime(x) for x in have) < os.path.getmtime(pdf):
        os.makedirs(d, exist_ok=True)
        subprocess.run(['pdftoppm', '-r', str(dpi), '-png', pdf, os.path.join(d, 'p')], check=True)
    return sorted(glob.glob(os.path.join(d, 'p-*.png')))


def css(w, h, acc):
    return f'''
@font-face {{ font-family: Syne; src: url({FONTS}/Syne.ttf); font-weight: 400 800; }}
@font-face {{ font-family: Inter; src: url({FONTS}/Inter.ttf); font-weight: 100 900; }}
@font-face {{ font-family: JBM; src: url({FONTS}/JetBrainsMono.ttf); font-weight: 100 800; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: {w}px; height: {h}px; overflow: hidden; position: relative; background: #060608; color: #f6faf7; font-family: Inter, sans-serif; }}
.glow {{ position: absolute; inset: 0; background:
  radial-gradient(circle at 74% 30%, rgba(46,140,108,.34), rgba(46,140,108,.12) 32%, transparent 62%),
  radial-gradient(circle at 12% 96%, {acc}26, transparent 45%); }}
.grid {{ position: absolute; inset: 0; background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px); background-size: {w / 12:.0f}px {w / 12:.0f}px; }}
.top {{ position: absolute; left: 6%; right: 6%; top: 5%; display: flex; justify-content: space-between;
  padding-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,.1); }}
.lbl {{ font: 600 13px/1 JBM, monospace; letter-spacing: .2em; text-transform: uppercase; color: #9aaba3; }}
.lbl b {{ color: {acc}; font-weight: 700; }}
.page {{ position: absolute; background: #fff; border-radius: 6px; box-shadow: 0 50px 80px -30px rgba(0,0,0,.9), 0 2px 10px rgba(0,0,0,.4); overflow: hidden; }}
.page img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
h1 {{ font: 800 76px/.92 Syne, sans-serif; letter-spacing: -.045em; }}
h1 i {{ font-style: normal; color: {acc}; }}
h2 {{ font: 700 26px/1.2 Syne, sans-serif; letter-spacing: -.015em; color: #c9d4cf; margin-top: 14px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 9px; margin-top: 22px; }}
.chips span {{ padding: 9px 15px; border-radius: 999px; border: 1px solid rgba(255,255,255,.16); font: 600 12.5px/1 JBM, monospace;
  letter-spacing: .14em; text-transform: uppercase; color: #f6faf7; }}
.chips span.acc {{ border-color: {acc}; color: {acc}; }}
.txt {{ position: absolute; left: 6%; right: 6%; bottom: 6%; }}
.zoo {{ position: absolute; display: grid; gap: 14px; }}
.zoo div {{ background: #fbf9f4; border-radius: 6px; padding: 8px; box-shadow: 0 24px 50px -28px rgba(0,0,0,.85); }}
.zoo svg {{ display: block; width: 100%; height: auto; }}
'''


def page_img(src, x, y, w, rot=0, z=1):
    h = w * 1.4142
    return (f'<div class="page" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<img src="file://{src}"></div>')


def render(body, out, w, h, acc, scale=2):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{css(w, h, acc)}</style></head><body><div class="glow"></div><div class="grid"></div>{body}</body></html>'
    tmp = out + '.html'
    open(tmp, 'w', encoding='utf-8').write(doc)
    subprocess.run(['node', os.path.join(HERE, 'render.js'), tmp, out, str(w), str(h), '0', str(scale)], check=True)
    os.remove(tmp)
    # als hochwertiges JPEG speichern (kleiner, gleiche Qualitaet fuer Fotos/Verlaeufe)
    from PIL import Image
    jpg = out[:-4] + '.jpg'
    Image.open(out).convert('RGB').save(jpg, 'JPEG', quality=90, subsampling=0, optimize=True, progressive=True)
    os.remove(out)
    out = jpg
    # als JPEG-freundliches PNG belassen; Squarespace komprimiert selbst
    print('BILD', os.path.relpath(out, BASE))


def chips(items, acc_first=True):
    return '<div class="chips">' + ''.join(f'<span class="{"acc" if acc_first and i == 0 else ""}">{esc(t)}</span>' for i, t in enumerate(items)) + '</div>'


def top(left='Kreativhafen — Ausmalbilder', right=KAT.DOMAIN):
    return f'<div class="top"><span class="lbl">[ {esc(left)} ]</span><span class="lbl">{esc(right)}</span></div>'


def fan(pages, cx, y, w, spread=0.62, rots=(-9, 0, 8)):
    """Drei (oder mehr) Seiten gefaechert; mittlere vorne."""
    n = len(pages)
    out = []
    order = list(range(n))
    mid = n // 2
    for i in order:
        off = (i - mid) * w * spread
        rot = rots[i] if n == 3 else (i - mid) * 6
        z = 10 - abs(i - mid)
        out.append(page_img(pages[i], cx - w / 2 + off, y + abs(i - mid) * 18, w, rot, z))
    return ''.join(out)


def info(p):
    pid = p['id']
    if pid == 'advent':
        return ['24 Motive', 'PDF · A4', 'Türchen-Plan', 'ab 2 Jahren']
    if pid == 'anhaenger':
        return ['16 Anhänger', '4 Karten', 'PDF · A4', 'ab 2 Jahren']
    if pid == 'laterne':
        return ['8 Motive', '+ Bastelvorlage', 'Liedblatt', 'ab 2 Jahren']
    return [f'{len(p["motive"])} Motive', 'PDF · A4', 'Sofort-Download', 'ab 2 Jahren']


def hero_pages(pid):
    s = seiten(pid)
    if pid == 'advent':
        return [s[1], s[0], s[13]]       # Tuerchenplan, Cover, Tuer 12
    if pid == 'anhaenger':
        return [s[1], s[0], s[3]]
    if pid == 'laterne':
        return [s[2], s[0], s[11]]       # Sonne, Cover, Bastelvorlage-Mantel
    return [s[1], s[0], s[3]]


def produkt_hero(p, out, w=1000, h=1000):
    body = top() + fan(hero_pages(p['id']), w * .5, h * .16, w * .33)
    body += (f'<div class="txt"><h1>{esc(p["name"])}<i>.</i></h1><h2>{esc(p["sub"])}</h2>{chips(info(p))}</div>')
    render(body, out, w, h, p['farbe'])


def produkt_motive(p, out, w=1000, h=1000):
    keys = p['motive']
    n = len(keys)
    cols = 6 if n > 12 else (5 if n == 10 else 4)
    rots = [-1.6, 1.2, -.7, 1.5, -1.1, .8]
    cells = ''.join(f'<div style="transform:rotate({rots[i % 6]}deg)">{K.motif_svg(k, with_name=True)}</div>' for i, k in enumerate(keys))
    gw = w * .88
    body = top(p['name'], f'{n} Motive')
    body += f'<div style="position:absolute;left:6%;top:12%"><h1 style="font-size:58px">{n} Motive<i>.</i></h1><h2 style="font-size:22px">Je eine Seite – mit Namen zum Mitlesen.</h2></div>'
    rows = (n + cols - 1) // cols
    cell_h = (gw - (cols - 1) * 14) / cols * 1.1 + 16
    gh = rows * cell_h + (rows - 1) * 14
    top_ = max(h * .26, (h * .25 + h * .97 - gh) / 2)
    body += f'<div class="zoo" style="left:6%;width:{gw:.0f}px;top:{top_:.0f}px;grid-template-columns:repeat({cols},1fr)">{cells}</div>'
    render(body, out, w, h, p['farbe'])


def produkt_extras(p, out, w=1000, h=1000):
    s = seiten(p['id'])
    pid = p['id']
    if pid == 'laterne':
        pg, txt = [s[10], s[11], s[12]], 'Bastelvorlage & Liedblatt'
    elif pid == 'advent':
        pg, txt = [s[1], s[25], s[26]], 'Türchen-Plan & Urkunde'
    elif pid == 'anhaenger':
        pg, txt = [s[1], s[3], s[2]], 'Anhänger & Karten'
    else:
        pg, txt = [s[0], s[-2], s[-1]], 'Deckblatt, Urkunde & Eltern-Seite'
    body = top(p['name'], 'Inklusive')
    body += fan(pg, w * .5, h * .14, w * .32)
    body += f'<div class="txt"><h1 style="font-size:54px">{esc(txt)}<i>.</i></h1>{chips(p["extras"][:4], False)}</div>'
    render(body, out, w, h, p['farbe'])


AUSGEMALT = os.path.join(BASE, 'motive-ausgemalt')
MOTIVPNG = os.path.join(BASE, 'motive')


def produkt_ausgemalt(p, out, key, w=1000, h=1000, titel='So sieht’s ausgemalt aus'):
    """Vorher/Nachher: Linien-Vorlage neben ausgemalter Version (ein grosses Paar)."""
    cards = ''
    cw = 372
    for i, (src, lab, rot) in enumerate([(MOTIVPNG, 'vorher', -1.6), (AUSGEMALT, 'nachher', 1.4)]):
        cards += (f'<div style="width:{cw}px;transform:rotate({rot}deg)">'
                  f'<div style="background:#fbf9f4;border-radius:8px;padding:12px;box-shadow:0 40px 70px -30px rgba(0,0,0,.9)">'
                  f'<img src="file://{os.path.join(src, key + ".png")}" style="display:block;width:100%"></div>'
                  f'<p class="lbl" style="margin-top:16px;text-align:center">{lab}</p></div>')
    body = top(p['name'], 'Beispiel')
    body += f'<div style="position:absolute;left:6%;top:12%"><h1 style="font-size:54px">{esc(titel)}<i>.</i></h1></div>'
    body += f'<div style="position:absolute;left:0;right:0;top:{h * .27:.0f}px;display:flex;gap:56px;justify-content:center;align-items:flex-start">{cards}</div>'
    body += ('<div class="txt"><h2 style="margin:0;color:#f6faf7">Grüner Nikolaus? Lila Kürbis? Ganz egal –</h2>'
             '<h2 style="margin-top:4px">beim Malen entscheiden die Kleinen selbst.</h2></div>')
    render(body, out, w, h, p['farbe'])


def alle_motive(p, out, w=1000, h=1000):
    """Alle 52 Motive auf einen Blick (Saisonpaket)."""
    keys = [k for q in KAT.PAKETE for k in q['motive']]
    cells = ''.join(f'<div style="background:#fbf9f4;border-radius:4px;padding:3px"><img src="file://{os.path.join(MOTIVPNG, k + ".png")}" style="display:block;width:100%"></div>' for k in keys)
    body = top(p['name'], f'{len(keys)} Motive')
    body += f'<div style="position:absolute;left:6%;top:12%"><h1 style="font-size:54px">{len(keys)} Motive<i>.</i></h1><h2 style="font-size:22px">Von Halloween bis Silvester – plus Bastelvorlage, Anhänger &amp; Karten.</h2></div>'
    body += f'<div style="position:absolute;left:6%;right:6%;top:{h * .27:.0f}px;display:grid;grid-template-columns:repeat(9,1fr);gap:8px">{cells}</div>'
    render(body, out, w, h, p['farbe'])


def kita_lizenz_bild(p, out, w=1000, h=1000):
    lz = os.path.join(SEITEN, 'lizenz.png')
    pdf = os.path.join(PDF.OUT, 'Kita-Lizenzurkunde.pdf')
    if not os.path.exists(lz):
        PDF.write_pdf([PDF.page_lizenz()], 'Kita-Lizenzurkunde')
        subprocess.run(['pdftoppm', '-r', '110', '-png', '-singlefile', pdf, lz[:-4]], check=True)
        os.remove(pdf)
    body = top(p['name'], 'Lizenzurkunde')
    body += page_img(lz, w * .5 - 190, h * .12, 380, -2, 5)
    body += ('<div class="txt"><h1 style="font-size:50px">Kopieren für alle Gruppen<i>.</i></h1>'
             + chips(['1 Einrichtung', 'alle Gruppen', 'ohne Ablaufdatum', 'mit Urkunde'], True) + '</div>')
    render(body, out, w, h, p['farbe'])


def bundle_hero(p, out, ids, w=1000, h=1000, extra_chip=None):
    covers = [seiten(i)[0] for i in ids]
    body = top()
    n = len(covers)
    pw = w * .25
    for i, c in enumerate(covers):
        off = (i - (n - 1) / 2) * pw * .62
        body += page_img(c, w / 2 - pw / 2 + off, h * .17 + abs(i - (n - 1) / 2) * 16, pw, (i - (n - 1) / 2) * 5, 10 - abs(i - n // 2))
    ch = ['5 Pakete', '52 Motive', 'Bastelvorlage', 'Anhänger & Karten']
    if extra_chip:
        ch = [extra_chip] + ch[:3]
    body += f'<div class="txt"><h1>{esc(p["name"])}<i>.</i></h1><h2>{esc(p["sub"])}</h2>{chips(ch)}</div>'
    render(body, out, w, h, p['farbe'])


def social(p, out, w, h, url_hint):
    pid = p['id']
    pages = hero_pages(pid) if pid in KAT.ALLE_IDS else [seiten('probier')[1], seiten('probier')[0], seiten('probier')[2]]
    body = top()
    tall = h / w > 1.4
    pw = w * (.42 if tall else .40)
    body += fan(pages, w * .5, h * (.1 if tall else .12), pw)
    if tall:
        bunt = {'halloween': ['hw01', 'hw04', 'hw09'], 'laterne': ['lt01', 'lt03', 'lt08'], 'advent': ['ad06', 'ad11', 'ad24'],
                'winter': ['wi01', 'wi05', 'wi08'], 'anhaenger': ['ad10', 'ad09', 'ad17'], 'probier': ['hw01', 'lt01', 'ad24']}[pid]
        cards = ''.join(f'<div style="width:{w * .25:.0f}px;transform:rotate({r}deg);background:#fbf9f4;border-radius:6px;padding:7px;'
                        f'box-shadow:0 30px 60px -30px rgba(0,0,0,.9)"><img src="file://{os.path.join(AUSGEMALT, k + ".png")}" style="display:block;width:100%"></div>'
                        for k, r in zip(bunt, (-3, 1.5, -1)))
        body += f'<div style="position:absolute;left:0;right:0;top:{h * .1 + pw * 1.414 + 50:.0f}px;display:flex;justify-content:center;gap:26px">{cards}</div>'
    body += (f'<div class="txt"><h1 style="font-size:{int(w * .078)}px">{esc(p["name"])}<i>.</i></h1><h2>{esc(p["sub"])}</h2>'
             f'{chips(info(p) if pid in KAT.ALLE_IDS else ["3 Motive", "gratis", "PDF · A4"])}'
             f'<p class="lbl" style="margin-top:26px;color:#f6faf7">→ {esc(url_hint)}</p></div>')
    render(body, out, w, h, p.get('farbe', '#6ee7b7'))


def tuerchen_stories():
    """24 Instagram-Stories (1080x1920) fuer den Advent: Tuerchen X mit Motiv des Tages."""
    p = KAT.paket('advent')
    for i, k in enumerate(p['motive'], 1):
        name = K.MOTIFS[k]['name'].title().replace('Ä', 'ä').replace('Ö', 'ö').replace('Ü', 'ü')
        body = top('24 Türchen', f'{i}. Dezember')
        body += (f'<div style="position:absolute;left:8%;top:9%"><p class="lbl" style="font-size:22px">[ Türchen {i} ]</p>'
                 f'<h1 style="font-size:150px;margin-top:18px">{i}<i>.</i></h1>'
                 f'<h2 style="font-size:46px;color:#f6faf7">Heute: {esc(name)}</h2></div>')
        body += (f'<div style="position:absolute;left:12%;right:12%;top:36%;transform:rotate(-1.5deg);background:#fbf9f4;border-radius:10px;padding:18px;'
                 f'box-shadow:0 60px 90px -40px rgba(0,0,0,.9)"><img src="file://{os.path.join(MOTIVPNG, k + ".png")}" style="display:block;width:100%"></div>')
        body += ('<div class="txt" style="bottom:5%"><h2 style="font-size:34px;color:#f6faf7;margin:0">Wer malt mit? ✏️</h2>'
                 '<p class="lbl" style="margin-top:22px;font-size:20px;color:#f6faf7">→ Ganzer Kalender: Link in der Bio</p></div>')
        render(body, os.path.join(BASE, 'social', 'stories-advent', f'tuerchen-{i:02d}.png'), 1080, 1920, p['farbe'], scale=1)


def og_image(out, w=1200, h=630):
    covers = [seiten(i)[0] for i in KAT.ALLE_IDS]
    body = top('Kreativhafen — Shop', KAT.DOMAIN)
    pw = 150
    for i, c in enumerate(covers):
        body += page_img(c, 640 + i * 95, 120 + (i % 2) * 26, pw, (i - 2) * 4, 10 - abs(i - 2))
    body += ('<div class="txt" style="right:52%"><h1 style="font-size:66px">Ausmal&shy;bilder<i>.</i></h1>'
             '<h2>Halloween, Laterne, Advent, Winter – zum Ausdrucken.</h2></div>')
    render(body, out, w, h, '#6ee7b7')


def motiv_pngs():
    """Einzelmotive fuer Website (Vorschau) und Ausmal-Widget."""
    d = os.path.join(BASE, 'motive')
    os.makedirs(d, exist_ok=True)
    keys = [k for k, m in K.MOTIFS.items() if m['pack'] != 'test']
    html_ = ''.join(f'<div id="{k}" style="width:1000px;height:1100px;background:#fff">{K.motif_svg(k, with_name=True, w=1000, h=1100)}</div>' for k in keys)
    tmp = os.path.join(d, '_alle.html')
    open(tmp, 'w').write(f'<html><body style="margin:0">{html_}</body></html>')
    js = os.path.join(HERE, 'build', 'shots.js')
    os.makedirs(os.path.dirname(js), exist_ok=True)
    open(js, 'w').write('''const {chromium}=require('playwright');(async()=>{const [inp,dir,...keys]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:1100}});
await p.goto('file://'+inp);for(const k of keys){await p.locator('#'+k).screenshot({path:dir+'/'+k+'.png'});}await b.close();})();''')
    subprocess.run(['node', js, os.path.abspath(tmp), d] + keys, check=True)
    os.remove(tmp)
    # verlustfrei auf Graustufen-Palette reduzieren (klein fuer Code-Bloecke)
    from PIL import Image
    for k in keys:
        f_ = os.path.join(d, k + '.png')
        Image.open(f_).convert('L').quantize(16).save(f_, optimize=True)
    print('MOTIVE', len(keys))


if __name__ == '__main__':
    what = sys.argv[1:] or ['motive', 'produkte', 'social', 'og']
    if 'motive' in what:
        motiv_pngs()
    if 'produkte' in what:
        for p in KAT.PAKETE:
            d = os.path.join(BASE, 'produkte', p['slug'])
            nr = iter(range(1, 9))
            produkt_hero(p, os.path.join(d, f'{next(nr)}-titel.png'))
            if p['motive']:
                produkt_motive(p, os.path.join(d, f'{next(nr)}-alle-motive.png'))
            produkt_extras(p, os.path.join(d, f'{next(nr)}-' + ('anhaenger-und-karten' if p['id'] == 'anhaenger' else 'extras') + '.png'))
            produkt_ausgemalt(p, os.path.join(d, f'{next(nr)}-ausgemalt.png'), {'halloween': 'hw04', 'laterne': 'lt03', 'advent': 'ad06', 'winter': 'wi01', 'anhaenger': 'ad10'}[p['id']])
        bundle_hero(KAT.BUNDLE, os.path.join(BASE, 'produkte', KAT.BUNDLE['slug'], '1-titel.png'), KAT.ALLE_IDS, extra_chip='Spare 7,60 €')
        alle_motive(KAT.BUNDLE, os.path.join(BASE, 'produkte', KAT.BUNDLE['slug'], '2-alle-motive.png'))
        produkt_ausgemalt(KAT.BUNDLE, os.path.join(BASE, 'produkte', KAT.BUNDLE['slug'], '3-ausgemalt.png'), 'ad11')
        bundle_hero(KAT.KITA, os.path.join(BASE, 'produkte', KAT.KITA['slug'], '1-titel.png'), KAT.ALLE_IDS, extra_chip='1 Einrichtung')
        kita_lizenz_bild(KAT.KITA, os.path.join(BASE, 'produkte', KAT.KITA['slug'], '2-lizenzurkunde.png'))
        alle_motive(KAT.KITA, os.path.join(BASE, 'produkte', KAT.KITA['slug'], '3-alle-motive.png'))
    if 'social' in what:
        for p in KAT.PAKETE + [dict(KAT.GRATIS, farbe='#6ee7b7')]:
            pid = p['id']
            social(p, os.path.join(BASE, 'social', f'pinterest-{pid}.png'), 1000, 1500, f'{KAT.DOMAIN}/shop/ausmalbilder')
            social(p, os.path.join(BASE, 'social', f'instagram-{pid}.png'), 1080, 1350, 'Link in der Bio')
    if 'stories' in what:
        tuerchen_stories()
    if 'og' in what:
        og_image(os.path.join(BASE, 'website', 'og-ausmalbilder.png'))

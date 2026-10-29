"""Baut die Download-PDFs (A4, druckfreundlich) fuer alle Pakete.

python3 pdf.py [paket-id ...]   -> ../01-produkte-pdf/*.pdf
"""
import os, sys, subprocess, html, zipfile, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel as K
import motive  # noqa: registriert alle Motive
import katalog as KAT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '01-produkte-pdf')
TMP = os.path.join(HERE, 'build')
FONTS = 'file://' + os.path.join(HERE, 'fonts')
GREY = '#8a8a8a'

CSS = f'''
@font-face {{ font-family: Syne; src: url({FONTS}/Syne.ttf); font-weight: 400 800; }}
@font-face {{ font-family: Inter; src: url({FONTS}/Inter.ttf); font-weight: 100 900; }}
@font-face {{ font-family: JBM; src: url({FONTS}/JetBrainsMono.ttf); font-weight: 100 800; }}
@font-face {{ font-family: Fredoka; src: url({FONTS}/Fredoka-Bold.ttf); font-weight: 700; }}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; color: #111; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.pg {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; }}
.pg:last-child {{ page-break-after: auto; break-after: auto; }}
.lbl {{ font: 600 7.2pt/1 JBM, monospace; letter-spacing: .16em; text-transform: uppercase; color: {GREY}; }}
.ft {{ position: absolute; left: 14mm; right: 14mm; bottom: 9mm; display: flex; justify-content: space-between; align-items: center;
       border-top: .25mm solid #e2e2e2; padding-top: 2.6mm; }}
.hd {{ position: absolute; left: 14mm; right: 14mm; top: 12mm; display: flex; justify-content: space-between; align-items: center; height: 24mm; }}
.name {{ font: 500 10pt Inter, sans-serif; color: #555; display: flex; align-items: flex-end; gap: 2mm; }}
.name i {{ display: inline-block; width: 52mm; border-bottom: .35mm solid #9a9a9a; height: 5mm; }}
.art {{ position: absolute; left: 14mm; right: 14mm; top: 40mm; bottom: 20mm; display: flex; align-items: center; justify-content: center; }}
.art svg {{ width: 100%; height: 100%; }}
.full {{ position: absolute; inset: 0; }}
.full svg {{ width: 100%; height: 100%; display: block; }}
h1, h2, h3 {{ margin: 0; font-family: Syne, sans-serif; font-weight: 800; letter-spacing: -.02em; }}
.txt {{ position: absolute; left: 20mm; right: 20mm; top: 20mm; bottom: 22mm; font: 400 10.5pt/1.6 Inter, sans-serif; color: #222; }}
.txt h1 {{ font-size: 30pt; line-height: 1; letter-spacing: -.035em; }}
.txt h1 em {{ font-style: normal; color: var(--acc); }}
.txt h2 {{ font-size: 13pt; line-height: 1.15; margin: 7mm 0 2.5mm; }}
.txt p {{ margin: 0 0 2.5mm; }}
.txt ul {{ margin: 0; padding: 0; list-style: none; }}
.txt li {{ position: relative; padding-left: 5mm; margin-bottom: 1.6mm; }}
.txt li::before {{ content: ""; position: absolute; left: 0; top: 2.1mm; width: 2mm; height: 2mm; border-radius: 50%; background: var(--acc); }}
.txt .k {{ display: block; margin-bottom: 6mm; }}
.txt .box {{ border: .3mm solid #ddd; border-radius: 4mm; padding: 5mm 6mm; margin-top: 6mm; }}
.txt .sig {{ font: 700 15pt Fredoka, sans-serif; margin-top: 3mm; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }}
.more {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2mm 6mm; font-size: 9.5pt; }}
.more b {{ font-family: Syne; }}
'''


def esc(s):
    return html.escape(s, quote=True)


def group(inner, x, y, s):
    """Motiv (1000er-Raster) an Position x,y mit Groesse s (Einheiten des Ziel-SVGs)."""
    return (f'<g transform="translate({K.f(x)} {K.f(y)}) scale({s / 1000:.5f})" stroke="{K.INK}" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</g>')


def draw(key):
    return K.MOTIFS[key]['draw']()


def footer(left, right=KAT.DOMAIN):
    return f'<div class="ft"><span class="lbl">{esc(left)}</span><span class="lbl">{esc(right)}</span></div>'


def ts_mark(x, y, s=1.0):
    """Kleines TS-Zeichen (Kreis + TS) fuer Deckblaetter."""
    return (f'<g transform="translate({K.f(x)} {K.f(y)}) scale({s})">'
            f'<circle cx="0" cy="0" r="30" fill="#fff" stroke="{K.INK}" stroke-width="3.5"/>'
            f'<text x="0" y="8.5" text-anchor="middle" font-family="Syne" font-weight="800" font-size="24" letter-spacing="-1" fill="{K.INK}">TS</text>'
            f'<circle cx="23" cy="-23" r="6" fill="#fff" stroke="{K.INK}" stroke-width="3"/></g>')


# ---------------------------------------------------------------- Seiten
def page_motif(p, key, i, n, num=None):
    badge = ''
    if num is not None:
        # Tuerchen-Nummer: Kreis mit hohler Zahl
        badge = (f'<svg viewBox="0 0 240 240" style="width:32mm;height:32mm;margin-top:6mm">'
                 f'<g stroke="{K.INK}" stroke-linejoin="round">{K.rounded_star(120, 124, 116, 80, 8, -90, w=7)}'
                 f'{K.lettering(str(num), 52, 66, 136, 116, outline=8)}</g></svg>')
    else:
        badge = f'<span class="lbl">{esc(p["name"])} · {i:02d} / {n:02d}</span>'
    return (f'<section class="pg"><div class="hd">{badge}<span class="name">Gemalt von: <i></i></span></div>'
            f'<div class="art">{K.motif_svg(key, with_name=True)}</div>'
            f'{footer(p["name"] + " · " + p["sub"], f"{i:02d} / {n:02d} · " + KAT.DOMAIN)}</section>')


def page_cover(p, label='Ausmalbilder · ab 2 Jahren'):
    a, b, c = p['cover']
    lines = p['titel_lettering']
    W, H = 1000, 1414
    o = []
    # Titel in hohlen Buchstaben
    o.append(K.lettering(lines[0], 90, 150, 820, 150, outline=11))
    o.append(K.lettering(lines[1], 60, 305, 880, 170, outline=12))
    # Motiv-Gruppe
    o.append(group(draw(a), 10, 640, 390))
    o.append(group(draw(c), 600, 640, 390))
    o.append(group(draw(b), 215, 480, 570))
    # Namensfeld
    o.append(K.rect(150, 1110, 700, 120, 60, w=7))
    o.append(f'<text x="200" y="1095" font-family="Inter" font-weight="600" font-size="26" fill="#555">Dieses Heft gehört:</text>')
    o.append(ts_mark(500, 1310, 1.0))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">'
           + ''.join(o) + '</g></svg>')
    head = (f'<div style="position:absolute;left:14mm;right:14mm;top:12mm;display:flex;justify-content:space-between">'
            f'<span class="lbl">[ Kreativhafen · {esc(label)} ]</span><span class="lbl">{esc(p["sub"])}</span></div>')
    return f'<section class="pg"><div class="full">{svg}</div>{head}{footer("Trutz Stähler · Hamburg")}</section>'


def medal(cx, cy, r):
    o = []
    # Baender
    o.append(K.path(f'M{cx - r * .55} {cy + r * .6} L{cx - r * .95} {cy + r * 1.75} L{cx - r * .55} {cy + r * 1.55} L{cx - r * .32} {cy + r * 1.95} L{cx - r * .05} {cy + r * .85} Z'))
    o.append(K.path(f'M{cx + r * .55} {cy + r * .6} L{cx + r * .95} {cy + r * 1.75} L{cx + r * .55} {cy + r * 1.55} L{cx + r * .32} {cy + r * 1.95} L{cx + r * .05} {cy + r * .85} Z'))
    o.append(K.rounded_star(cx, cy, r * 1.08, r * .92, 16, -90))
    o.append(K.circle(cx, cy, r * .78, w=K.LW_THIN))
    o.append(K.rounded_star(cx, cy - r * .05, r * .52, r * .24, 5, -90))
    return ''.join(o)


def page_urkunde(p):
    W, H = 1000, 1414
    o = [K.lettering('SUPER', 170, 150, 660, 170, outline=12), K.lettering('GEMACHT!', 90, 330, 820, 170, outline=12)]
    o.append(medal(500, 760, 190))
    for x, y, r in [(150, 640, 40), (850, 600, 32), (180, 900, 28), (840, 930, 44), (500, 520, 26)]:
        o.append(K.sparkle(x, y, r))
    o.append(f'<line x1="140" y1="1180" x2="860" y2="1180" stroke="#9a9a9a" stroke-width="3"/>')
    o.append(f'<text x="500" y="1225" text-anchor="middle" font-family="Inter" font-weight="500" font-size="26" fill="#555">hat alle Bilder aus „{esc(p["name"])}“ ausgemalt.</text>')
    o.append(f'<line x1="300" y1="1310" x2="700" y2="1310" stroke="#9a9a9a" stroke-width="3"/>')
    o.append(f'<text x="500" y="1350" text-anchor="middle" font-family="Inter" font-weight="500" font-size="22" fill="#888">Datum</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">' + ''.join(o) + '</g></svg>'
    head = '<div style="position:absolute;left:14mm;right:14mm;top:12mm"><span class="lbl">[ Mal-Urkunde ]</span></div>'
    return f'<section class="pg"><div class="full">{svg}</div>{head}{footer(p["name"] + " · Urkunde")}</section>'


def page_eltern(p, lizenz='privat', extra='', mehr=True):
    andere = [q for q in KAT.PAKETE if q['id'] != p['id']]
    more = ''.join(f'<div><b>{esc(q["name"])}</b><br>{esc(q["sub"])}</div>' for q in andere)
    if lizenz == 'kita':
        liz = ('<p><b>Kita-Lizenz:</b> Ihr dürft alle Seiten für die Kinder <b>einer Einrichtung</b> (ein Standort, alle Gruppen) '
               'beliebig oft ausdrucken und kopieren – ohne Ablaufdatum. Nicht erlaubt: Weitergabe an andere Einrichtungen, '
               'Veröffentlichung (z. B. im Netz oder in Elternbriefen als Datei) und Weiterverkauf. Die Lizenzurkunde liegt bei.</p>')
    else:
        liz = ('<p><b>Für eure Familie:</b> Druckt die Seiten so oft aus, wie ihr möchtet – für eure eigenen Kinder, Enkel, '
               'Patenkinder. Bitte nicht weitergeben, hochladen oder verkaufen. Für Kita, Schule, Hort oder Verein gibt es die '
               f'<b>Kita-Lizenz</b> auf {KAT.DOMAIN}/shop/ausmalbilder.</p>')
    mehr_html = (f'<h2>Mehr aus dem Kreativhafen</h2><div class="more">{more}</div>'
                 f'<p style="margin-top:4mm">Alle Pakete, die Kita-Lizenz und Bilder zum Ausmalen direkt im Browser: <b>{KAT.DOMAIN}/shop/ausmalbilder</b></p>') if mehr else ''
    body = f'''
<span class="lbl k">[ Für Eltern · Großeltern · Erzieher:innen ]</span>
<h1>Moin! Schön, dass<br>ihr <em>dabei</em> seid.</h1>
<p style="margin-top:6mm">Ich bin Trutz – Papa aus Hamburg und der Kopf hinter dem Kreativhafen. Wie in meinen Malbüchern gibt es
auch hier dicke Linien, große Flächen und zu jedem Bild den Namen zum Mitlesen – gemacht für kleine Hände ab etwa 2 Jahren
und für alle Großen, die einfach gern malen.</p>
{extra}
<div class="cols">
<div><h2>So druckt ihr am besten</h2><ul>
<li>A4, Hochformat, Größe <b>„Tatsächliche Größe“ / 100 %</b></li>
<li>Schwarzweiß reicht – spart Farbe</li>
<li>Etwas dickeres Papier (120–160 g/m²) verträgt auch Filzstifte</li>
<li>Wachsmaler und dicke Buntstifte sind ideal für die Kleinsten</li>
<li>Bild verkleckert? Einfach neu ausdrucken.</li></ul></div>
<div><h2>Lizenz</h2>{liz}</div>
</div>
<div class="box"><h2 style="margin-top:0">Zeigt mir eure Bilder!</h2>
<p>Ich freue mich riesig über eure Kunstwerke: auf Instagram mit <b>{KAT.INSTA}</b> markieren oder per Mail an <b>{KAT.MAIL}</b>.
(Bitte nur das Bild – ohne Namen oder Gesichter eurer Kinder.)</p>
<p class="sig">Viel Spaß beim Malen – euer Trutz</p></div>
{mehr_html}
'''
    acc = p.get('farbe', '#2e9e6a')
    return (f'<section class="pg" style="--acc:{acc}"><div class="txt">{body}</div>'
            f'{footer("Trutz Stähler · Hamburg · " + KAT.DOMAIN + "/impressum", "© " + str(datetime.date.today().year) + " Trutz Stähler")}</section>')


# ---------------------------------------------------------------- Extras Advent
def page_tuerchenplan(p):
    W, H = 1000, 1414
    o = [K.lettering('MEIN', 300, 120, 400, 110, outline=10), K.lettering('TÜRCHEN-PLAN', 70, 245, 860, 135, outline=11)]
    o.append(f'<text x="500" y="440" text-anchor="middle" font-family="Inter" font-weight="500" font-size="25" fill="#555">Jeden Tag ein Bild ausmalen – und danach hier das Türchen anmalen!</text>')
    cols, rows = 4, 6
    x0, y0, cw, ch, gap = 80, 490, 200, 132, 13
    for i in range(24):
        r, c = divmod(i, cols)
        x = x0 + c * (cw + gap); y = y0 + r * (ch + gap)
        o.append(K.rect(x, y, cw, ch, 22, w=7))
        o.append(K.circle(x + cw - 26, y + ch / 2, 7, w=5))  # Tuerknauf
        o.append(K.lettering(str(i + 1), x + 30, y + 26, cw - 80, ch - 52, outline=7))
        if i + 1 in (6, 24):
            o.append(K.sparkle(x + 24, y + 24, 14, w=4))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">' + ''.join(o) + '</g></svg>'
    head = '<div style="position:absolute;left:14mm;right:14mm;top:12mm;display:flex;justify-content:space-between"><span class="lbl">[ 1. – 24. Dezember ]</span><span class="name">Name: <i></i></span></div>'
    return f'<section class="pg"><div class="full">{svg}</div>{head}{footer(p["name"] + " · Türchen-Plan")}</section>'


# ---------------------------------------------------------------- Extras Laterne
LIED = [
    ('Laterne, Laterne,', 'Sonne, Mond und Sterne.', 'Brenne auf, mein Licht,', 'brenne auf, mein Licht,', 'aber nur meine liebe Laterne nicht!'),
    ('Laterne, Laterne,', 'Sonne, Mond und Sterne.', 'Sperrt ihn ein, den Wind,', 'sperrt ihn ein, den Wind,', 'er soll warten, bis wir alle zu Hause sind!'),
    ('Laterne, Laterne,', 'Sonne, Mond und Sterne.', 'Bleibe hell, mein Licht,', 'bleibe hell, mein Licht,', 'denn sonst strahlt meine liebe Laterne nicht!'),
]


def page_lied(p):
    W, H = 1000, 1414
    o = [K.lettering('LATERNE,', 120, 110, 760, 140, outline=11), K.lettering('LATERNE', 120, 260, 760, 140, outline=11)]
    # Rahmen aus kleinen Motiven
    pos = [(30, 470), (850, 470), (30, 1180), (850, 1180)]
    keys = ['lt02', 'lt03', 'lt04', 'lt01']
    for (x, y), k in zip(pos, keys):
        o.append(group(draw(k), x, y, 130))
    for x, y, r in [(70, 680, 22), (930, 700, 26), (80, 960, 26), (925, 990, 20), (500, 1370, 18)]:
        o.append(K.sparkle(x, y, r, w=5))
    y = 470
    for v, strophe in enumerate(LIED):
        o.append(f'<text x="500" y="{y}" text-anchor="middle" font-family="JBM" font-weight="600" font-size="18" letter-spacing="3" fill="{GREY}">STROPHE {v + 1}</text>')
        y += 46
        for z in strophe:
            o.append(f'<text x="500" y="{y}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="34" fill="{K.INK}">{esc(z)}</text>')
            y += 44
        y += 26
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">' + ''.join(o) + '</g></svg>'
    head = '<div style="position:absolute;left:14mm;right:14mm;top:12mm"><span class="lbl">[ Liedblatt zum Mitsingen · Volkslied ]</span></div>'
    return f'<section class="pg"><div class="full">{svg}</div>{head}{footer(p["name"] + " · Liedblatt")}</section>'


def scissors(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" fill="#fff" stroke="{K.INK}" stroke-width="4">'
            f'<circle cx="-14" cy="-9" r="8"/><circle cx="-14" cy="9" r="8"/>'
            f'<path d="M-7 -5 L22 8 M-7 5 L22 -8" fill="none"/></g>')


def page_bastel_mantel(p):
    """Laternen-Mantel 262 x 140 mm (+ Klebelasche), quer auf der Seite."""
    # Koordinaten in mm (Seite quer: 297 x 210)
    MW, MH, LA = 262, 138, 14
    x0, y0 = (297 - MW - LA) / 2, 46
    o = []
    # Klebelasche (schraffiert durch Streifen)
    o.append(f'<rect x="{x0 + MW}" y="{y0}" width="{LA}" height="{MH}" fill="#fff" stroke="{K.INK}" stroke-width=".5" stroke-dasharray="2 1.6"/>')
    o.append(f'<text transform="translate({x0 + MW + LA / 2 + 1.6} {y0 + MH / 2}) rotate(90)" text-anchor="middle" font-family="JBM" font-weight="600" font-size="3.4" letter-spacing=".8" fill="{GREY}">HIER KLEBEN</text>')
    # Mantel
    o.append(f'<rect x="{x0}" y="{y0}" width="{MW}" height="{MH}" fill="#fff" stroke="{K.INK}" stroke-width=".8"/>')
    # Unten: Wellen (Hafen) als ausmalbare Baender
    base = y0 + MH
    def wave(yy, amp, n):
        d = f'M{x0} {yy}'
        step = MW / n
        for i in range(n):
            xa = x0 + i * step
            d += f' Q{xa + step / 4:.2f} {yy - amp:.2f} {xa + step / 2:.2f} {yy:.2f} T{xa + step:.2f} {yy:.2f}'
        return d
    o.append(f'<path d="{wave(base - 30, 6, 9)} L{x0 + MW} {base} L{x0} {base} Z" fill="#fff" stroke="{K.INK}" stroke-width=".8"/>')
    o.append(f'<path d="{wave(base - 15, 5, 12)} L{x0 + MW} {base} L{x0} {base} Z" fill="#fff" stroke="{K.INK}" stroke-width=".8"/>')
    # Sonne, Mond und Sterne gross am Himmel
    inner = ''
    for k, x, y, s_ in [('lt02', x0 + 14, y0 + 12, 74), ('lt04', x0 + 104, y0 + 18, 58), ('lt03', x0 + 178, y0 + 8, 76)]:
        inner += f'<g transform="translate({x} {y}) scale({s_ / 1000:.5f})" stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">{draw(k)}</g>'
    o.append(inner)
    for sx, sy, r in [(x0 + 95, y0 + 14, 4), (x0 + 168, y0 + 16, 4.5), (x0 + 168, y0 + 78, 3.5), (x0 + 96, y0 + 84, 3.5), (x0 + 250, y0 + 92, 3.5), (x0 + 8, y0 + 96, 3.5)]:
        o.append(K.rounded_star(sx, sy, r * 1.6, r * .8, w=.55))
    for sx, sy, r in [(x0 + 60, y0 + 92, 3), (x0 + 140, y0 + 90, 3), (x0 + 215, y0 + 92, 2.6)]:
        o.append(K.sparkle(sx, sy, r, w=.45))
    # Schere + Hinweise
    o.append(scissors(x0 - 1, y0 - 4, .16))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 297 210" style="width:297mm;height:210mm">'
           f'<g stroke-linecap="round" stroke-linejoin="round">{"".join(o)}</g>'
           f'<text x="{x0}" y="22" font-family="Syne" font-weight="800" font-size="9" fill="{K.INK}">Meine Laterne – der Mantel</text>'
           f'<text x="{x0}" y="31" font-family="Inter" font-weight="500" font-size="3.8" fill="#555">1. Ausmalen  ·  2. Am Rand ausschneiden  ·  3. Zur Rolle biegen und an der Lasche festkleben</text>'
           f'<text x="{x0}" y="{y0 + MH + 12}" font-family="Inter" font-weight="500" font-size="3.4" fill="#777">Tipp: Wer mag, schneidet in Mond und Sterne kleine Fenster und klebt Transparentpapier dahinter.</text>'
           f'<text x="{x0}" y="{y0 + MH + 18}" font-family="Inter" font-weight="700" font-size="3.4" fill="#111">Bitte nur mit elektrischem Laternenstab (LED) – niemals mit einer echten Kerze.</text>'
           f'</svg>')
    rot = (f'<div style="position:absolute;left:0;top:0;width:297mm;height:210mm;transform-origin:0 0;'
           f'transform:translate(210mm,0) rotate(90deg)">{svg}</div>')
    return f'<section class="pg">{rot}</section>'


def page_bastel_boden(p):
    """Boden mit Klebezacken, Deckelring, Bauanleitung (Hochformat, Masse in mm)."""
    D = 83.4   # 262 mm Umfang
    o = []
    cx, cy = 60, 92
    # Zackenrand Boden
    n = 18; pts = []
    for i in range(n * 2):
        a = i * 3.14159 / n
        r = D / 2 + (10 if i % 2 == 0 else 0)
        pts.append((cx + r * __import__('math').cos(a), cy + r * __import__('math').sin(a)))
    o.append('<path d="M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + f' Z" fill="#fff" stroke="{K.INK}" stroke-width=".7"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{D / 2}" fill="#fff" stroke="{K.INK}" stroke-width=".5" stroke-dasharray="2 1.5"/>')
    o.append(f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-family="Syne" font-weight="800" font-size="6" fill="{K.INK}">BODEN</text>')
    o.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="Inter" font-size="3.2" fill="#555">Zacken nach oben knicken</text>')
    # Deckelring
    cx2, cy2 = 154, 92
    o.append(f'<circle cx="{cx2}" cy="{cy2}" r="{D / 2}" fill="#fff" stroke="{K.INK}" stroke-width=".7"/>')
    o.append(f'<circle cx="{cx2}" cy="{cy2}" r="{D / 2 - 11}" fill="#fff" stroke="{K.INK}" stroke-width=".7"/>')
    o.append(f'<text x="{cx2}" y="{cy2 + 1.5}" text-anchor="middle" font-family="Syne" font-weight="800" font-size="6" fill="{K.INK}">RING</text>')
    o.append(f'<text x="{cx2}" y="{cy2 + 8}" text-anchor="middle" font-family="Inter" font-size="3.2" fill="#555">oben aufkleben</text>')
    for a in range(0, 360, 45):
        import math
        o.append(K.rounded_star(cx2 + (D / 2 - 5.5) * math.cos(math.radians(a)), cy2 + (D / 2 - 5.5) * math.sin(math.radians(a)), 3.2, 1.6, w=.45))
    # Henkel-Streifen
    o.append(f'<rect x="20" y="146" width="170" height="14" rx="2" fill="#fff" stroke="{K.INK}" stroke-width=".7"/>')
    o.append(f'<text x="105" y="155" text-anchor="middle" font-family="Inter" font-size="3.4" fill="#555">Henkel (wer mag: alternativ Draht oder den Haken vom Laternenstab nutzen)</text>')
    steps = ['Mantel, Ring und Henkel bunt ausmalen.',
             'Alle Teile am Rand ausschneiden (Erwachsene helfen beim Ring).',
             'Mantel zur Rolle biegen, Lasche festkleben.',
             'Boden-Zacken nach oben knicken und innen in die Rolle kleben.',
             'Ring oben aufkleben, Henkel innen links und rechts festkleben.',
             'LED-Laternenstab einhängen – und los geht der Laternenumzug!']
    y = 182
    for i, s in enumerate(steps, 1):
        o.append(f'<circle cx="25" cy="{y - 1.3}" r="4" fill="#fff" stroke="{K.INK}" stroke-width=".6"/>')
        o.append(f'<text x="25" y="{y}" text-anchor="middle" font-family="Syne" font-weight="800" font-size="4.2" fill="{K.INK}">{i}</text>')
        o.append(f'<text x="33" y="{y}" font-family="Inter" font-weight="500" font-size="4.2" fill="#222">{esc(s)}</text>')
        y += 10
    o.append(f'<text x="20" y="{y + 6}" font-family="Inter" font-weight="700" font-size="3.8" fill="#111">Material: Schere, Klebestift oder Flüssigkleber, LED-Laternenstab. Tipp: auf 160 g/m² Papier drucken.</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297" style="width:210mm;height:297mm">'
           f'<text x="20" y="24" font-family="Syne" font-weight="800" font-size="8" fill="{K.INK}">Meine Laterne</text>'
           f'<text x="20" y="31" font-family="Inter" font-weight="500" font-size="4" fill="#555">Boden, Ring &amp; Henkel – ausmalen, ausschneiden, zusammenkleben</text>'
           f'<g stroke-linecap="round" stroke-linejoin="round">{"".join(o)}</g>'
           f'<text x="20" y="172" font-family="Syne" font-weight="800" font-size="7" fill="{K.INK}">So wird’s eine Laterne</text></svg>')
    return f'<section class="pg"><div class="full">{svg}</div>{footer(p["name"] + " · Bastelvorlage 2/2")}</section>'


# ---------------------------------------------------------------- Anhaenger & Karten
ANH_MOTIVE = ['ad10', 'ad24', 'ad07', 'ad09', 'ad04', 'ad11', 'ad08', 'ad15',
              'ad17', 'ad02', 'ad03', 'ad21', 'wi01', 'wi02', 'wi03', 'ad19']


def tag_svg(key):
    W, H = 880, 600
    o = [K.path('M110 30 L850 30 Q870 30 870 50 L870 550 Q870 570 850 570 L110 570 L20 470 L20 130 Z', w=8)]
    o.append(K.circle(80, 300, 26, w=7))
    o.append(group(draw(key), 95, 50, 500))
    o.append(f'<text x="600" y="235" font-family="Fredoka" font-weight="700" font-size="54" fill="{K.INK}" stroke="none">Für:</text>')
    o.append(f'<line x1="600" y1="320" x2="830" y2="320" stroke="#9a9a9a" stroke-width="5"/>')
    o.append(f'<text x="600" y="420" font-family="Fredoka" font-weight="700" font-size="54" fill="{K.INK}" stroke="none">Von:</text>')
    o.append(f'<line x1="600" y1="505" x2="830" y2="505" stroke="#9a9a9a" stroke-width="5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">'
            + ''.join(o) + '</g></svg>')


def page_anhaenger(p, keys, nr):
    cells = ''.join(f'<div style="width:88mm;height:60mm">{tag_svg(k)}</div>' for k in keys)
    grid = f'<div style="position:absolute;left:14mm;top:22mm;display:grid;grid-template-columns:88mm 88mm;gap:5mm 6mm">{cells}</div>'
    head = (f'<div style="position:absolute;left:14mm;right:14mm;top:12mm;display:flex;justify-content:space-between">'
            f'<span class="lbl">[ Geschenkanhänger {nr}/2 · ausmalen · ausschneiden · Band durchs Loch ]</span></div>')
    return f'<section class="pg">{head}{grid}{footer(p["name"] + " · Anhänger " + str(nr) + "/2")}</section>'


KARTEN = [('ad24', ['FROHE', 'WEIHNACHTEN']), ('ad11', ['FROHE', 'WEIHNACHTEN']),
          ('wi08', ['GUTES NEUES', 'JAHR!']), ('ad17', ['DANKE', 'SCHÖN!'])]


def card_svg(key, lines):
    W, H = 900, 1280
    o = [f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" rx="30" fill="#fff" stroke="{K.INK}" stroke-width="5" stroke-dasharray="22 16"/>']
    o.append(group(draw(key), 150, 60, 600))
    o.append(K.lettering(lines[0], 70, 700, 760, 170, outline=10))
    o.append(K.lettering(lines[1], 50, 880, 800, 170, outline=10))
    o.append(f'<text x="120" y="1180" font-family="Fredoka" font-weight="700" font-size="48" fill="{K.INK}" stroke="none">Für:</text>')
    o.append(f'<line x1="240" y1="1185" x2="780" y2="1185" stroke="#9a9a9a" stroke-width="5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">'
            + ''.join(o) + '</g></svg>')


def page_karten(p):
    cells = ''.join(f'<div style="width:88mm;height:125mm">{card_svg(k, l)}</div>' for k, l in KARTEN)
    grid = f'<div style="position:absolute;left:14mm;top:22mm;display:grid;grid-template-columns:88mm 88mm;gap:6mm 6mm">{cells}</div>'
    head = '<div style="position:absolute;left:14mm;right:14mm;top:12mm"><span class="lbl">[ 4 Karten · an der gestrichelten Linie ausschneiden ]</span></div>'
    return f'<section class="pg">{head}{grid}{footer(p["name"] + " · Karten")}</section>'


# ---------------------------------------------------------------- Kita-Lizenzurkunde
def page_lizenz():
    p = KAT.KITA
    W, H = 1000, 1414
    o = [K.lettering('LIZENZ', 70, 120, 640, 150, outline=10)]
    o.append(medal(845, 175, 62))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g stroke="{K.INK}" stroke-linecap="round" stroke-linejoin="round">' + ''.join(o) + '</g></svg>'
    alle = ''.join(f'<li>{esc(q["name"])} – {esc(q["sub"])}</li>' for q in KAT.PAKETE)
    txt = f'''<div style="position:absolute;left:22mm;right:22mm;top:76mm;bottom:22mm;font:400 10.2pt/1.55 Inter;color:#222;--acc:{p["farbe"]}" class="txt">
<h2 style="font-size:16pt;margin:0 0 5mm">Nutzungslizenz für eine Einrichtung</h2>
<p style="display:flex;gap:3mm;align-items:flex-end"><b>Einrichtung:</b><i style="flex:1;border-bottom:.35mm solid #9a9a9a;height:5mm"></i></p>
<p style="display:flex;gap:3mm;align-items:flex-end"><b>Ort / Standort:</b><i style="flex:1;border-bottom:.35mm solid #9a9a9a;height:5mm"></i></p>
<p style="display:flex;gap:3mm;align-items:flex-end"><b>Bestellnummer:</b><i style="flex:1;border-bottom:.35mm solid #9a9a9a;height:5mm"></i><b>Datum:</b><i style="width:35mm;border-bottom:.35mm solid #9a9a9a;height:5mm"></i></p>
<h2>Erlaubt</h2><ul>
<li>Alle enthaltenen Seiten für die Kinder dieser Einrichtung (ein Standort, alle Gruppen) ausdrucken und kopieren – so oft ihr wollt, ohne Ablaufdatum</li>
<li>Ausgemalte Bilder ausstellen, mitgeben, in Portfolios abheften</li>
<li>Speichern auf den Geräten der Einrichtung</li></ul>
<h2>Nicht erlaubt</h2><ul>
<li>Weitergabe der Dateien an andere Einrichtungen, Eltern oder Dritte</li>
<li>Veröffentlichung als Datei (Website, Cloud-Ordner für Eltern, soziale Netzwerke)</li>
<li>Weiterverkauf oder Verwendung in eigenen Produkten</li></ul>
<h2>Enthalten</h2><ul>{alle}</ul>
<p style="margin-top:5mm">Lizenzgeber: Trutz Stähler · {KAT.DOMAIN} · {KAT.MAIL}</p></div>'''
    head = '<div style="position:absolute;left:14mm;right:14mm;top:12mm"><span class="lbl">[ Kita- &amp; Schullizenz ]</span></div>'
    return f'<section class="pg"><div class="full">{svg}</div>{head}{txt}{footer("Kita-Lizenz · Lizenzurkunde")}</section>'


# ---------------------------------------------------------------- Pakete zusammenbauen
def pages_for(pid, lizenz='privat'):
    p = KAT.paket(pid)
    pg = [page_cover(p)]
    if pid == 'advent':
        pg.append(page_tuerchenplan(p))
        pg += [page_motif(p, k, i, 24, num=i) for i, k in enumerate(p['motive'], 1)]
    elif pid == 'anhaenger':
        pg += [page_anhaenger(p, ANH_MOTIVE[:8], 1), page_anhaenger(p, ANH_MOTIVE[8:], 2), page_karten(p)]
    else:
        n = len(p['motive'])
        pg += [page_motif(p, k, i, n) for i, k in enumerate(p['motive'], 1)]
    if pid == 'laterne':
        pg += [page_lied(p), page_bastel_mantel(p), page_bastel_boden(p)]
    if pid != 'anhaenger':
        pg.append(page_urkunde(p))
    pg.append(page_eltern(p, lizenz))
    return pg


def pages_gratis():
    g = dict(KAT.GRATIS, titel_lettering=['PROBIER', 'PAKET'], cover=['hw01', 'ad24', 'lt01'], farbe='#2e9e6a')
    pg = [page_cover(g, 'Gratis · 3 Ausmalbilder')]
    pg += [page_motif(g, k, i, 3) for i, k in enumerate(g['motive'], 1)]
    extra = ('<div class="box" style="margin:0 0 4mm"><b>Lust auf mehr?</b> Halloween, St. Martin mit Laternen-Bastelvorlage, '
             'ein Adventskalender mit 24 Türchen, Winter & Silvester und Geschenkanhänger zum Ausmalen – alles auf '
             f'<b>{KAT.DOMAIN}/shop/ausmalbilder</b>.</div>')
    pg.append(page_eltern(g, 'privat', extra, mehr=False))
    return pg


def write_pdf(pages, name):
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    doc = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{esc(name)}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    h = os.path.join(TMP, name + '.html')
    open(h, 'w', encoding='utf-8').write(doc)
    out = os.path.join(OUT, name + '.pdf')
    subprocess.run(['node', os.path.join(HERE, 'render.js'), h, out], check=True)
    meta(out, name)
    return out


def meta(path, name):
    """PDF-Metadaten (Titel, Autor, Stichworte) setzen."""
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(path); w = PdfWriter(clone_from=r)
    w.add_metadata({'/Title': TITEL.get(name, name.replace('_', ' – ').replace('-', ' ')), '/Author': 'Trutz Stähler',
                    '/Subject': 'Ausmalbilder aus dem Kreativhafen – ' + KAT.DOMAIN,
                    '/Keywords': 'Ausmalbilder, Malvorlagen, Kinder, Kreativhafen, Trutz Stähler',
                    '/Creator': KAT.DOMAIN})
    w.page_layout = '/SinglePage'
    with open(path, 'wb') as fh:
        w.write(fh)


DATEINAMEN = {
    'halloween': 'Kleine-Gruselfreunde_Halloween-Ausmalbilder',
    'laterne': 'Laterne-Laterne_St-Martin-Ausmalbilder',
    'advent': '24-Tuerchen_Adventskalender-zum-Ausmalen',
    'winter': 'Winterzeit_Winter-und-Silvester-Ausmalbilder',
    'anhaenger': 'Fuer-dich_Geschenkanhaenger-und-Karten',
}

TITEL = {
    'Kleine-Gruselfreunde_Halloween-Ausmalbilder': 'Kleine Gruselfreunde – Halloween-Ausmalbilder',
    'Laterne-Laterne_St-Martin-Ausmalbilder': 'Laterne, Laterne – Ausmalbilder zu St. Martin',
    '24-Tuerchen_Adventskalender-zum-Ausmalen': '24 Türchen – Adventskalender zum Ausmalen',
    'Winterzeit_Winter-und-Silvester-Ausmalbilder': 'Winterzeit – Ausmalbilder für Winter & Silvester',
    'Fuer-dich_Geschenkanhaenger-und-Karten': 'Für dich! – Geschenkanhänger & Karten zum Ausmalen',
    'Probierpaket_3-Ausmalbilder-gratis': 'Probierpaket – 3 Ausmalbilder gratis',
    'Kita-Lizenzurkunde': 'Kita-Lizenz – Lizenzurkunde',
}
TITEL.update({k + '_Kita': v + ' (Kita-Lizenz)' for k, v in list(TITEL.items())})

LIESMICH = '''Moin und danke für deinen Einkauf!

In diesem Paket stecken alle Ausmalbilder als PDF (A4):
{liste}

Drucken: A4, Hochformat, "Tatsächliche Größe" / 100 %.
Die Laternen-Bastelvorlage am besten auf 160 g/m² Papier drucken.

{lizenz}

Fragen? {mail}
Viel Spaß beim Malen – Trutz
{domain}
'''


def build(ids):
    built = {}
    for pid in ids:
        if pid in DATEINAMEN:
            built[pid] = write_pdf(pages_for(pid), DATEINAMEN[pid]); print('PDF', built[pid])
        elif pid == 'probier':
            print('PDF', write_pdf(pages_gratis(), 'Probierpaket_3-Ausmalbilder-gratis'))
        elif pid in ('bundle', 'kita'):
            liste = '\n'.join(f'- {DATEINAMEN[q]}.pdf' for q in DATEINAMEN)
            if pid == 'bundle':
                files = {q: write_pdf(pages_for(q), DATEINAMEN[q]) for q in DATEINAMEN}
                liz = 'Lizenz: für den privaten Gebrauch in deiner Familie. Bitte nicht weitergeben, hochladen oder verkaufen.'
                zname = 'Saisonpaket_Alle-Ausmalbilder-Herbst-Winter.zip'
            else:
                files = {q: write_pdf(pages_for(q, 'kita'), DATEINAMEN[q] + '_Kita') for q in DATEINAMEN}
                files['lizenz'] = write_pdf([page_lizenz()], 'Kita-Lizenzurkunde')
                liste = '\n'.join(f'- {DATEINAMEN[q]}_Kita.pdf' for q in DATEINAMEN) + '\n- Kita-Lizenzurkunde.pdf (bitte ausfüllen und abheften)'
                liz = 'Lizenz: Kita-Lizenz für eine Einrichtung (ein Standort, alle Gruppen) – Details in der Lizenzurkunde.'
                zname = 'Kita-Lizenz_Alle-Ausmalbilder-Herbst-Winter.zip'
            zp = os.path.join(OUT, zname)
            with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
                for f_ in files.values():
                    z.write(f_, os.path.basename(f_))
                z.writestr('Liesmich.txt', LIESMICH.format(liste=liste, lizenz=liz, mail=KAT.MAIL, domain=KAT.DOMAIN))
            # Kita-Einzel-PDFs nur im ZIP
            if pid == 'kita':
                for f_ in files.values():
                    os.remove(f_)
            print('ZIP', zp)


if __name__ == '__main__':
    ids = sys.argv[1:] or ['halloween', 'laterne', 'advent', 'winter', 'anhaenger', 'probier', 'bundle', 'kita']
    build(ids)

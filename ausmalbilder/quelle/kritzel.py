"""Zeichen-Bibliothek fuer die Ausmalbilder im Kritzelbuch-Stil.

Alle Motive werden in einem 1000x1000-Raster gezeichnet: dicke schwarze
Linien, weisse Flaechen, grosse glaenzende Augen. Ausgabe ist reines SVG
(ohne Schriften), damit es im PDF, im Browser und im Ausmal-Widget gleich aussieht.
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

INK = '#111111'
LW = 11          # Hauptlinie
LW_THIN = 7      # Details
HERE = os.path.dirname(os.path.abspath(__file__))
MOTIFS = {}      # key -> dict(name, pack, draw)


def motif(key, name, pack):
    def deco(fn):
        MOTIFS[key] = dict(key=key, name=name, pack=pack, draw=fn)
        return fn
    return deco


# ---------- Grundformen ----------
def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def path(d, fill='#fff', w=LW, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke-width="{w}" {extra}/>'


def line(d, w=LW_THIN):
    return f'<path d="{d}" fill="none" stroke-width="{w}"/>'


def circle(cx, cy, r, fill='#fff', w=LW):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke-width="{w}"/>'


def ellipse(cx, cy, rx, ry, fill='#fff', w=LW, rot=0):
    t = f' transform="rotate({f(rot)} {f(cx)} {f(cy)})"' if rot else ''
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" stroke-width="{w}"{t}/>'


def rect(x, y, w_, h, r=0, fill='#fff', w=LW, rot=0):
    t = f' transform="rotate({f(rot)} {f(x + w_ / 2)} {f(y + h / 2)})"' if rot else ''
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w_)}" height="{f(h)}" rx="{f(r)}" fill="{fill}" stroke-width="{w}"{t}/>'


def poly(pts, fill='#fff', w=LW, close=True):
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + (' Z' if close else '')
    return path(d, fill, w) if close else line(d, w)


def star_pts(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rounded_star(cx, cy, r_out, r_in, n=5, rot=-90, fill='#fff', w=LW):
    """Stern mit weichen Spitzen (wie gemalt)."""
    pts = star_pts(cx, cy, r_out, r_in, n, rot)
    d = ''
    m = len(pts)
    for i in range(m):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % m]
        a = (p1[0] + (p0[0] - p1[0]) * .12, p1[1] + (p0[1] - p1[1]) * .12)
        b = (p1[0] + (p2[0] - p1[0]) * .12, p1[1] + (p2[1] - p1[1]) * .12)
        d += (f'M{f(a[0])} {f(a[1])}' if i == 0 else f' L{f(a[0])} {f(a[1])}') + f' Q{f(p1[0])} {f(p1[1])} {f(b[0])} {f(b[1])}'
    return path(d + ' Z', fill, w)


def sparkle(cx, cy, r, w=LW_THIN):
    """Kleiner Glitzer-Stern (4 Zacken) als Fuellmotiv."""
    k = r * .28
    d = (f'M{f(cx)} {f(cy - r)} Q{f(cx + k * .4)} {f(cy - k * .4)} {f(cx + r)} {f(cy)} '
         f'Q{f(cx + k * .4)} {f(cy + k * .4)} {f(cx)} {f(cy + r)} Q{f(cx - k * .4)} {f(cy + k * .4)} {f(cx - r)} {f(cy)} '
         f'Q{f(cx - k * .4)} {f(cy - k * .4)} {f(cx)} {f(cy - r)} Z')
    return path(d, '#fff', w)


def heart(cx, cy, s, fill='#fff', w=LW_THIN):
    d = (f'M{f(cx)} {f(cy + s * .9)} C{f(cx - s * 1.3)} {f(cy + s * .1)} {f(cx - s * .9)} {f(cy - s * .95)} {f(cx)} {f(cy - s * .35)} '
         f'C{f(cx + s * .9)} {f(cy - s * .95)} {f(cx + s * 1.3)} {f(cy + s * .1)} {f(cx)} {f(cy + s * .9)} Z')
    return path(d, fill, w)


# ---------- Gesichter ----------
def eye(cx, cy, s=1.0, look=(0, 0)):
    rx, ry = 21 * s, 27 * s
    lx, ly = look
    return (ellipse(cx, cy, rx, ry, fill=INK, w=0) +
            f'<circle cx="{f(cx - 7 * s + lx)}" cy="{f(cy - 10 * s + ly)}" r="{f(8.5 * s)}" fill="#fff" stroke="none"/>' +
            f'<circle cx="{f(cx + 7 * s + lx)}" cy="{f(cy + 9 * s + ly)}" r="{f(4 * s)}" fill="#fff" stroke="none"/>')


def closed_eye(cx, cy, s=1.0):
    return line(f'M{f(cx - 18 * s)} {f(cy)} Q{f(cx)} {f(cy + 16 * s)} {f(cx + 18 * s)} {f(cy)}', LW_THIN * max(s, .8))


def face(cx, cy, s=1.0, gap=70, mouth='smile', blush=True, eyes='open', look=(0, 0)):
    """Kawaii-Gesicht: cx/cy = Mitte zwischen den Augen."""
    out = []
    for dx in (-gap * s, gap * s):
        out.append(eye(cx + dx, cy, s, look) if eyes == 'open' else closed_eye(cx + dx, cy, s))
    my = cy + 38 * s
    if mouth == 'smile':
        out.append(line(f'M{f(cx - 17 * s)} {f(my)} Q{f(cx)} {f(my + 20 * s)} {f(cx + 17 * s)} {f(my)}', LW_THIN * max(s, .8)))
    elif mouth == 'open':
        d = (f'M{f(cx - 22 * s)} {f(my - 4 * s)} Q{f(cx)} {f(my - 10 * s)} {f(cx + 22 * s)} {f(my - 4 * s)} '
             f'Q{f(cx + 20 * s)} {f(my + 30 * s)} {f(cx)} {f(my + 30 * s)} Q{f(cx - 20 * s)} {f(my + 30 * s)} {f(cx - 22 * s)} {f(my - 4 * s)} Z')
        out.append(path(d, '#fff', LW_THIN * max(s, .8)))
        out.append(line(f'M{f(cx - 10 * s)} {f(my + 21 * s)} Q{f(cx)} {f(my + 12 * s)} {f(cx + 10 * s)} {f(my + 21 * s)}', 5 * max(s, .8)))
    elif mouth == 'cat':
        out.append(line(f'M{f(cx - 20 * s)} {f(my)} Q{f(cx - 10 * s)} {f(my + 14 * s)} {f(cx)} {f(my)} Q{f(cx + 10 * s)} {f(my + 14 * s)} {f(cx + 20 * s)} {f(my)}', LW_THIN * max(s, .8)))
    elif mouth == 'o':
        out.append(ellipse(cx, my + 6 * s, 10 * s, 13 * s, '#fff', LW_THIN * max(s, .8)))
    if blush:
        for dx in (-(gap + 34) * s, (gap + 34) * s):
            out.append(ellipse(cx + dx, cy + 34 * s, 19 * s, 10 * s, '#fff', 5 * max(s, .8)))
    return ''.join(out)


# ---------- Schrift -> Pfade (hohle Buchstaben zum Ausmalen) ----------
_FONT = None


def _font():
    global _FONT
    if _FONT is None:
        _FONT = TTFont(os.path.join(HERE, 'fonts', 'Fredoka-Bold.ttf'))
    return _FONT


def text_path(text, tracking=0.04):
    """Liefert (svg_path_d, breite, ascent, descent) in Font-Einheiten."""
    font = _font()
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    hmtx = font['hmtx']
    x = 0; parts = []; minx = miny = 1e9; maxx = maxy = -1e9
    for ch in text:
        if ch == ' ':
            x += hmtx[cmap[32]][0]; continue
        gn = cmap.get(ord(ch))
        if gn is None:
            continue
        pen = SVGPathPen(gs)
        bp = BoundsPen(gs)
        gs[gn].draw(pen); gs[gn].draw(bp)
        d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({f(x)} 0)" d="{d}"/>')
        if bp.bounds:
            minx = min(minx, x + bp.bounds[0]); maxx = max(maxx, x + bp.bounds[2])
            miny = min(miny, bp.bounds[1]); maxy = max(maxy, bp.bounds[3])
        x += hmtx[gn][0] + tracking * upm
    return parts, (minx, miny, maxx, maxy)


def lettering(text, x, y, w, h, outline=13, fill='#fff', align='middle'):
    """Hohle Buchstaben, eingepasst in Box (x,y,w,h). Linienstaerke in Zielpixeln.
    Die Groesse richtet sich nach der Versalhoehe (inkl. Platz fuer Umlaute),
    damit alle Namen gleich gross wirken."""
    parts, (minx, miny, maxx, maxy) = text_path(text)
    cap = _font()['OS/2'].sCapHeight
    top = cap * 1.24                     # Platz fuer Umlaut-Punkte
    tw = maxx - minx
    sc = min(w / tw, h / top)
    ox = x + (w - tw * sc) / 2 if align == 'middle' else x
    base = y + (h + top * sc) / 2 - (top - cap) * sc * 0 - (top * sc - cap * sc) * 0
    base = y + h / 2 + cap * sc / 2 + (top - cap) * sc / 2   # Versalien mittig, Umlaute ragen nach oben
    tr = f'translate({f(ox - minx * sc)} {f(base)}) scale({sc:.5f} {-sc:.5f})'
    sw = outline * 2 / sc
    return (f'<g transform="{tr}" fill="{fill}" stroke="{INK}" stroke-width="{sw:.2f}" '
            f'stroke-linejoin="round" paint-order="stroke">' + ''.join(parts) + '</g>')


# ---------- Ausgabe ----------
def svg_doc(inner, vb='0 0 1000 1000', w=None, h=None):
    wh = f' width="{w}" height="{h}"' if w else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh}>'
            f'<g stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">{inner}</g></svg>')


def motif_svg(key, with_name=False, w=None, h=None):
    m = MOTIFS[key]
    inner = m['draw']()
    if not with_name:
        return svg_doc(inner, w=w, h=h)
    # Motiv + Name darunter (wie im Kritzelbuch)
    body = f'<g transform="translate(60 0) scale(.88)">{inner}</g>'
    return svg_doc(body + lettering(m['name'], 40, 905, 920, 150, outline=12), vb='0 0 1000 1100', w=w, h=h)

from kritzel import *
import math


def _round_poly(pts, k=.2, fill='#fff', w=LW):
    """Polygon mit weich abgerundeten Ecken."""
    d = ''
    m = len(pts)
    for i in range(m):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % m]
        a = (p1[0] + (p0[0] - p1[0]) * k, p1[1] + (p0[1] - p1[1]) * k)
        b = (p1[0] + (p2[0] - p1[0]) * k, p1[1] + (p2[1] - p1[1]) * k)
        d += (f'M{f(a[0])} {f(a[1])}' if i == 0 else f' L{f(a[0])} {f(a[1])}') + f' Q{f(p1[0])} {f(p1[1])} {f(b[0])} {f(b[1])}'
    return path(d + ' Z', fill, w)


def _cloud(cx, cy, s=1.0):
    d = (f'M{f(cx - 90 * s)} {f(cy + 30 * s)} C{f(cx - 130 * s)} {f(cy + 30 * s)} {f(cx - 130 * s)} {f(cy - 30 * s)} {f(cx - 85 * s)} {f(cy - 25 * s)} '
         f'C{f(cx - 80 * s)} {f(cy - 75 * s)} {f(cx - 10 * s)} {f(cy - 85 * s)} {f(cx + 10 * s)} {f(cy - 45 * s)} '
         f'C{f(cx + 40 * s)} {f(cy - 75 * s)} {f(cx + 100 * s)} {f(cy - 55 * s)} {f(cx + 90 * s)} {f(cy - 10 * s)} '
         f'C{f(cx + 135 * s)} {f(cy - 5 * s)} {f(cx + 130 * s)} {f(cy + 30 * s)} {f(cx + 95 * s)} {f(cy + 30 * s)} Z')
    return path(d, '#fff', LW_THIN)


@motif('lt01', 'LATERNE', 'laterne')
def laterne():
    o = []
    # Laternenstab (schraeg) mit Lämpchen-Griff
    o.append(rect(470, 70, 420, 34, 17, rot=-8))
    o.append(rect(840, 40, 70, 90, 22, rot=-8))
    o.append(circle(500, 132, 22))
    o.append(line('M500 154 L500 250', LW))
    # Henkeldraht
    o.append(line('M330 320 Q500 200 670 320', LW_THIN))
    # Deckel
    o.append(rect(360, 270, 280, 70, 18))
    # Kugel-Laterne
    o.append(path('M370 340 C190 380 150 530 175 620 C210 740 350 800 500 800 C650 800 790 740 825 620 C850 530 810 380 630 340 Z'))
    o.append(line('M285 380 C250 500 255 650 300 760', LW_THIN))
    o.append(line('M715 380 C750 500 745 650 700 760', LW_THIN))
    # Boden
    o.append(rect(370, 790, 260, 66, 18))
    o.append(face(500, 560, 1.35, gap=78, mouth='smile'))
    o.append(rounded_star(150, 220, 62, 30)); o.append(sparkle(250, 120, 30))
    o.append(sparkle(880, 360, 38)); o.append(rounded_star(870, 720, 44, 21)); o.append(sparkle(110, 760, 30))
    return ''.join(o)


@motif('lt02', 'SONNE', 'laterne')
def sonne():
    o = []
    cx, cy = 500, 500
    n = 12
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        r1 = 250
        r2 = 450 if i % 2 == 0 else 395
        half = math.radians(14 if i % 2 == 0 else 12)
        p1 = (cx + r1 * math.cos(a - half), cy + r1 * math.sin(a - half))
        p2 = (cx + r2 * math.cos(a), cy + r2 * math.sin(a))
        p3 = (cx + r1 * math.cos(a + half), cy + r1 * math.sin(a + half))
        o.append(_round_poly([p1, p2, p3], k=.3))
    o.append(circle(cx, cy, 285))
    o.append(face(cx, cy - 10, 1.6, gap=75, mouth='open'))
    return ''.join(o)


def _circ_inter(c1, r1, c2, r2):
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    xm, ym = c1[0] + a * dx / d, c1[1] + a * dy / d
    return ((xm + h * dy / d, ym - h * dx / d), (xm - h * dy / d, ym + h * dx / d))


@motif('lt03', 'MOND', 'laterne')
def mond():
    o = []
    c1, r1 = (460, 560), 340
    c2, r2 = (650, 450), 290
    p, q = _circ_inter(c1, r1, c2, r2)
    top, bot = (p, q) if p[1] < q[1] else (q, p)
    tx, ty = top
    # Muetzenzipfel (hinter dem Mond)
    o.append(path(f'M{f(tx - 150)} {f(ty + 40)} C{f(tx - 120)} {f(ty - 120)} {f(tx + 60)} {f(ty - 170)} {f(tx + 170)} {f(ty - 90)} '
                  f'C{f(tx + 230)} {f(ty - 45)} {f(tx + 250)} {f(ty + 20)} {f(tx + 245)} {f(ty + 90)} '
                  f'C{f(tx + 190)} {f(ty + 20)} {f(tx + 120)} {f(ty - 5)} {f(tx + 40)} {f(ty + 60)} Z'))
    o.append(circle(tx + 245, ty + 130, 44))
    # Sichel
    d = (f'M{f(top[0])} {f(top[1])} A{r1} {r1} 0 1 0 {f(bot[0])} {f(bot[1])} '
         f'A{r2} {r2} 0 0 1 {f(top[0])} {f(top[1])} Z')
    o.append(path(d))
    # Muetzenrand (vorne)
    o.append(rect(tx - 175, ty + 15, 240, 72, 36, rot=-22))
    # Gesicht (schlafend)
    o.append(closed_eye(260, 520, 1.7))
    o.append(line('M265 640 Q295 668 330 645', LW_THIN))
    o.append(ellipse(215, 590, 30, 15, '#fff', 5))
    # Sterne
    o.append(rounded_star(830, 790, 68, 33)); o.append(rounded_star(880, 560, 40, 19))
    o.append(sparkle(700, 940, 30)); o.append(sparkle(120, 140, 30))
    return ''.join(o)


@motif('lt04', 'STERN', 'laterne')
def stern():
    o = []
    o.append(rounded_star(500, 535, 450, 215))
    o.append(face(500, 545, 1.45, gap=72, mouth='open'))
    o.append(sparkle(120, 140, 40)); o.append(sparkle(880, 150, 32)); o.append(sparkle(890, 900, 30)); o.append(sparkle(110, 880, 26))
    return ''.join(o)


@motif('lt05', 'FLIEGENPILZ', 'laterne')
def fliegenpilz():
    o = []
    # Gras
    o.append(path('M150 900 C200 860 260 850 320 880 C380 840 470 840 520 880 C590 840 700 840 760 880 C800 860 850 865 870 900 Z', w=LW_THIN))
    # Stiel
    o.append(path('M340 520 C320 650 290 790 285 870 C285 885 300 890 320 890 L680 890 C700 890 715 885 715 870 C710 790 680 650 660 520 Z'))
    # Hut
    o.append(path('M110 520 C110 290 290 120 500 120 C710 120 890 290 890 520 C780 570 220 570 110 520 Z'))
    # Punkte (Flaechen)
    for cx, cy, rx, ry in [(500, 220, 70, 50), (300, 300, 62, 50), (700, 300, 62, 50), (200, 450, 45, 40), (800, 450, 45, 40), (420, 400, 48, 38), (590, 410, 52, 40)]:
        o.append(ellipse(cx, cy, rx, ry, '#fff', LW_THIN))
    o.append(face(500, 700, 1.3, gap=68, mouth='smile'))
    return ''.join(o)


@motif('lt06', 'KASTANIE', 'laterne')
def kastanie():
    o = []
    # Stacheln an der Schale (hinten)
    cx, cy, rx, ry = 500, 620, 385, 290
    for i in range(11):
        a = math.radians(6 + i * 168 / 10)
        bx, by = cx + rx * math.cos(a), cy + ry * math.sin(a)
        nx, ny = math.cos(a) * ry, math.sin(a) * rx
        nl = math.hypot(nx, ny); nx, ny = nx / nl, ny / nl
        tx, ty = -ny, nx
        o.append(_round_poly([(bx + tx * 34 - nx * 10, by + ty * 34 - ny * 10), (bx + nx * 78, by + ny * 78), (bx - tx * 34 - nx * 10, by - ty * 34 - ny * 10)], k=.15, w=LW_THIN))
    # Schale hinten (Innenseite)
    o.append(path('M115 620 C200 520 800 520 885 620 C800 700 200 700 115 620 Z', w=LW_THIN))
    # Kastanie
    o.append(path('M500 150 C540 170 800 270 800 500 C800 680 660 760 500 760 C340 760 200 680 200 500 C200 270 460 170 500 150 Z'))
    o.append(line('M320 300 C285 345 270 395 268 440', LW_THIN))
    # Schale vorne
    o.append(path('M115 620 C120 800 300 910 500 910 C700 910 880 800 885 620 C800 710 650 745 500 745 C350 745 200 710 115 620 Z'))
    o.append(face(500, 440, 1.4, gap=78, mouth='smile'))
    return ''.join(o)


@motif('lt07', 'HERBSTBLATT', 'laterne')
def herbstblatt():
    o = []
    right = [(500, 90), (585, 255), (690, 200), (670, 370), (880, 320), (800, 470), (920, 570), (730, 610), (755, 720), (585, 680), (515, 790)]
    left = [(1000 - x, y) for x, y in reversed(right[1:])]
    pts = right + [(500, 800)] + left[:-1] if False else right + left
    # Stiel (hinten)
    o.append(path('M480 760 C470 820 450 880 420 930 C440 945 460 945 470 935 C500 880 520 820 525 760 Z', w=LW))
    o.append(_round_poly(pts, k=.18))
    # Adern
    o.append(line('M500 790 L500 650', LW_THIN))
    o.append(line('M500 690 Q600 660 700 650', LW_THIN))
    o.append(line('M500 690 Q400 660 300 650', LW_THIN))
    o.append(line('M845 385 Q790 420 740 430', LW_THIN))
    o.append(line('M155 385 Q210 420 260 430', LW_THIN))
    o.append(line('M500 150 L500 300', LW_THIN))
    o.append(face(500, 450, 1.3, gap=75, mouth='smile'))
    return ''.join(o)


@motif('lt08', 'DRACHEN', 'laterne')
def drachen():
    o = []
    # Schwanz
    o.append(line('M470 700 C500 790 620 760 660 840 C700 910 820 870 930 950', LW_THIN))
    for bx, by, rot in [(575, 800, 20), (800, 905, 10)]:
        o.append(f'<g transform="rotate({rot} {bx} {by})">'
                 + path(f'M{bx} {by} L{bx - 72} {by - 46} C{bx - 88} {by - 12} {bx - 88} {by + 12} {bx - 72} {by + 46} Z', w=LW_THIN)
                 + path(f'M{bx} {by} L{bx + 72} {by - 46} C{bx + 88} {by - 12} {bx + 88} {by + 12} {bx + 72} {by + 46} Z', w=LW_THIN)
                 + circle(bx, by, 20, w=LW_THIN) + '</g>')
    # Drachen (Raute)
    o.append(_round_poly([(470, 60), (790, 330), (470, 710), (150, 330)], k=.08))
    o.append(line('M470 75 L470 200', LW_THIN)); o.append(line('M470 560 L470 695', LW_THIN))
    o.append(line('M170 330 L300 330', LW_THIN)); o.append(line('M640 330 L772 330', LW_THIN))
    o.append(face(470, 330, 1.3, gap=70, mouth='open'))
    o.append(_cloud(840, 120, .9)); o.append(_cloud(150, 820, .8))
    return ''.join(o)

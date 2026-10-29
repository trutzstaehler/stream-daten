from kritzel import *
import math


def _pt(cx, cy, a, d):
    """Punkt auf einer Achse (Winkel a in Grad, Bildschirmkoordinaten)."""
    r = math.radians(a)
    return cx + d * math.cos(r), cy + d * math.sin(r)


def _band(cx, cy, rx, ry, rx2, ry2, rot, t0, t1, n=40):
    """Ausschnitt eines Ellipsen-Rings (fuer Planetenring vorne)."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def p(rxx, ryy, t):
        x, y = rxx * math.cos(t), ryy * math.sin(t)
        return cx + x * c - y * s, cy + x * s + y * c
    outer = [p(rx, ry, t0 + (t1 - t0) * i / n) for i in range(n + 1)]
    inner = [p(rx2, ry2, t1 - (t1 - t0) * i / n) for i in range(n + 1)]
    return poly(outer + inner)


def _tail(p0, p1, p2, w0, w1, n=48):
    """Band entlang einer quadratischen Kurve p0->p2 (Kontrolle p1), Breite w0 -> w1, runde Enden."""
    def b(t):
        u = 1 - t
        return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = b(t); x2, y2 = b(min(1, t + .01)); x1, y1 = b(max(0, t - .01))
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in left)
    ex, ey = b(1)
    tx, ty = ex - b(.98)[0], ey - b(.98)[1]; tl = math.hypot(tx, ty) or 1
    d += f' Q{f(ex + tx / tl * w1 * .9)} {f(ey + ty / tl * w1 * .9)} {f(right[-1][0])} {f(right[-1][1])}'
    d += ' L' + ' L'.join(f'{f(x)} {f(y)}' for x, y in reversed(right)) + ' Z'
    return path(d)


def _swoosh(x0, y0, x1, y1, w, bend):
    """Geschwungener, spitz zulaufender Schweif von (x0,y0) (Breite w) nach (x1,y1)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    mx, my = (x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend
    a = (x0 + nx * w / 2, y0 + ny * w / 2); b = (x0 - nx * w / 2, y0 - ny * w / 2)
    return path(f'M{f(a[0])} {f(a[1])} Q{f(mx + nx * w * .3)} {f(my + ny * w * .3)} {f(x1)} {f(y1)} '
                f'Q{f(mx - nx * w * .3)} {f(my - ny * w * .3)} {f(b[0])} {f(b[1])} Z')


@motif('wr01', 'ASTRONAUT', 'weltraum')
def astronaut():
    o = []
    o.append(rounded_star(140, 190, 52, 25)); o.append(sparkle(860, 170, 36)); o.append(sparkle(150, 500, 30))
    o.append(rounded_star(870, 640, 42, 20)); o.append(sparkle(820, 860, 26))
    # Rucksack hinter dem Koerper
    o.append(rect(300, 520, 400, 230, 50))
    # Arme (links gesenkt, rechts winkt)
    o.append(path('M360 560 C300 560 240 610 215 690 C205 730 255 750 275 710 C292 668 325 645 365 640 Z'))
    o.append(path('M640 565 C705 545 765 480 775 405 C780 365 728 355 718 397 C708 448 680 492 640 505 Z'))
    o.append(circle(232, 728, 44)); o.append(circle(748, 385, 44))
    # Beine + Stiefel
    o.append(rect(372, 760, 112, 110, 30)); o.append(rect(516, 760, 112, 110, 30))
    o.append(rect(352, 850, 150, 62, 28)); o.append(rect(498, 850, 150, 62, 28))
    # Anzug
    o.append(path('M345 560 Q345 500 405 500 L595 500 Q655 500 655 560 L655 760 Q655 800 615 800 L385 800 Q345 800 345 760 Z'))
    o.append(rect(420, 600, 160, 110, 18))
    for x in (458, 500, 542):
        o.append(circle(x, 655, 17, w=LW_THIN))
    o.append(rect(405, 485, 190, 50, 22))
    # Helm
    o.append(circle(500, 300, 215))
    o.append(ellipse(500, 315, 168, 150))
    o.append(line('M378 230 Q410 190 460 178'))
    o.append(face(500, 320, 1.2, gap=68, mouth='open'))
    o.append(line('M500 85 L500 40', LW)); o.append(circle(500, 40, 18, w=LW_THIN))
    return ''.join(o)


@motif('wr02', 'RAUMSCHIFF', 'weltraum')
def raumschiff():
    o = []
    o.append(rounded_star(170, 230, 50, 24)); o.append(sparkle(830, 260, 38)); o.append(sparkle(190, 640, 30))
    o.append(rounded_star(820, 620, 40, 19)); o.append(circle(820, 820, 30, w=LW_THIN)); o.append(sparkle(160, 860, 24))
    # Flammen
    o.append(path('M420 760 C415 850 460 905 500 960 C540 905 585 850 580 760 Z'))
    o.append(path('M460 765 C458 825 480 862 500 895 C520 862 542 825 540 765 Z'))
    # Flossen
    o.append(path('M380 540 C315 585 280 650 280 770 L380 710 Z'))
    o.append(path('M620 540 C685 585 720 650 720 770 L620 710 Z'))
    o.append(path('M500 600 L540 760 L460 760 Z'))
    # Rumpf + Spitze
    o.append(path('M380 330 L620 330 L620 690 Q620 725 585 725 L415 725 Q380 725 380 690 Z'))
    o.append(path('M500 85 C585 150 620 240 620 330 L380 330 C380 240 415 150 500 85 Z'))
    o.append(path('M455 135 C475 118 525 118 545 135 C530 112 470 112 455 135 Z', w=LW_THIN))
    o.append(rect(380, 492, 240, 42, 0))
    # Bullauge
    o.append(circle(500, 410, 64)); o.append(circle(500, 410, 44, w=LW_THIN))
    o.append(line('M478 392 Q486 380 500 377'))
    # Duese
    o.append(rect(418, 718, 164, 52, 12))
    o.append(face(500, 610, 1.0, gap=62, mouth='smile'))
    return ''.join(o)


@motif('wr03', 'PLANET', 'weltraum')
def planet():
    o = []
    o.append(circle(150, 170, 52)); o.append(circle(135, 160, 14, w=LW_THIN))
    o.append(rounded_star(860, 160, 46, 22)); o.append(sparkle(880, 830, 32)); o.append(sparkle(110, 820, 28)); o.append(sparkle(250, 110, 24))
    cx, cy, rx, ry, rx2, ry2, rot = 500, 580, 440, 105, 330, 62, -12
    # Ring hinten (ganz), dann Planet, dann Ring vorne (untere Haelfte)
    o.append(ellipse(cx, cy, rx, ry, rot=rot)); o.append(ellipse(cx, cy, rx2, ry2, rot=rot))
    o.append(circle(500, 440, 255))
    o.append(circle(655, 300, 42, w=LW_THIN)); o.append(circle(352, 330, 26, w=LW_THIN)); o.append(circle(700, 450, 22, w=LW_THIN))
    o.append(_band(cx, cy, rx, ry, rx2, ry2, rot, 0, math.pi))
    o.append(face(500, 405, 1.25, gap=72, mouth='open'))
    return ''.join(o)


@motif('wr04', 'UFO', 'weltraum')
def ufo():
    o = []
    o.append(rounded_star(150, 180, 48, 23)); o.append(sparkle(860, 170, 36)); o.append(sparkle(120, 470, 28)); o.append(rounded_star(880, 450, 36, 17))
    # Lichtstrahl
    o.append(path('M420 650 L270 930 L730 930 L580 650 Z'))
    o.append(rounded_star(430, 830, 34, 16, w=LW_THIN)); o.append(sparkle(580, 780, 26, w=LW_THIN))
    # Unterteil
    o.append(ellipse(500, 628, 200, 46))
    # Kuppel
    o.append(line('M500 270 L500 205', LW)); o.append(circle(500, 190, 22, w=LW_THIN))
    o.append(path('M310 480 C310 210 690 210 690 480 Z'))
    o.append(line('M370 350 Q395 300 445 280'))
    o.append(face(500, 365, 1.0, gap=62, mouth='smile'))
    # Untertasse
    o.append(ellipse(500, 540, 395, 98))
    o.append(path('M140 560 Q500 650 860 560', fill='none', w=LW_THIN))
    for x, dy in ((250, 18), (375, 30), (500, 34), (625, 30), (750, 18)):
        o.append(circle(x, 540 + dy - 6, 24, w=LW_THIN))
    return ''.join(o)


@motif('wr05', 'ALIEN', 'weltraum')
def alien():
    o = []
    o.append(rounded_star(140, 200, 48, 23)); o.append(sparkle(860, 230, 34)); o.append(sparkle(150, 700, 30)); o.append(rounded_star(860, 700, 40, 19))
    # Antennen
    o.append(line('M430 240 Q400 170 370 130', LW)); o.append(line('M570 240 Q600 170 630 130', LW))
    o.append(circle(365, 120, 34)); o.append(circle(635, 120, 34))
    # Arme
    o.append(path('M392 640 C330 650 270 640 225 610 C200 593 222 560 250 576 C290 598 335 600 392 590 Z'))
    o.append(path('M608 640 C670 650 730 640 775 610 C800 593 778 560 750 576 C710 598 665 600 608 590 Z'))
    o.append(circle(226, 588, 34)); o.append(circle(774, 588, 34))
    # Fuesse + Koerper
    o.append(ellipse(420, 880, 75, 42)); o.append(ellipse(580, 880, 75, 42))
    o.append(path('M385 540 C360 680 350 790 368 870 L632 870 C650 790 640 680 615 540 Z'))
    o.append(ellipse(500, 735, 95, 95))
    # Kopf
    o.append(ellipse(500, 400, 235, 195))
    o.append(circle(345, 330, 26, w=LW_THIN)); o.append(circle(655, 330, 22, w=LW_THIN)); o.append(circle(390, 255, 16, w=LW_THIN))
    o.append(face(500, 405, 1.35, gap=75, mouth='open'))
    return ''.join(o)


@motif('wr06', 'ROBOTER', 'weltraum')
def roboter():
    o = []
    o.append(sparkle(130, 180, 38)); o.append(rounded_star(860, 180, 46, 22)); o.append(sparkle(130, 640, 30)); o.append(sparkle(880, 620, 30))
    # Antenne
    o.append(line('M500 175 L500 105', LW)); o.append(circle(500, 90, 26))
    # Arme
    o.append(rect(205, 470, 95, 230, 40)); o.append(rect(700, 470, 95, 230, 40))
    o.append(path('M215 690 C190 740 215 790 252 790 C290 790 312 740 288 690 Z'))
    o.append(path('M712 690 C688 740 710 790 748 790 C786 790 810 740 785 690 Z'))
    # Beine + Fuesse
    o.append(rect(375, 730, 90, 120, 18)); o.append(rect(535, 730, 90, 120, 18))
    o.append(rect(345, 835, 140, 70, 30)); o.append(rect(515, 835, 140, 70, 30))
    # Koerper
    o.append(rect(295, 440, 410, 310, 46))
    o.append(rect(365, 500, 270, 150, 22))
    o.append(heart(430, 575, 36))
    for i, x in enumerate((535, 595)):
        o.append(circle(x, 545, 22, w=LW_THIN))
    o.append(rect(520, 595, 100, 32, 14, w=LW_THIN))
    o.append(circle(350, 700, 16, w=LW_THIN)); o.append(circle(650, 700, 16, w=LW_THIN))
    # Hals + Kopf
    o.append(rect(445, 400, 110, 60, 12))
    o.append(rect(290, 245, 50, 100, 18)); o.append(rect(660, 245, 50, 100, 18))
    o.append(rect(320, 170, 360, 245, 50))
    o.append(face(500, 285, 1.25, gap=72, mouth='open'))
    return ''.join(o)


@motif('wr07', 'SATELLIT', 'weltraum')
def satellit():
    o = []
    o.append(rounded_star(140, 170, 46, 22)); o.append(sparkle(860, 150, 34)); o.append(sparkle(860, 850, 30)); o.append(rounded_star(150, 830, 40, 19))
    g = []
    # Solarpaneele
    for x0 in (85, 655):
        g.append(rect(x0, 420, 260, 160, 10))
        g.append(line(f'M{x0} 500 L{x0 + 260} 500'))
        for k in (1, 2, 3):
            xx = x0 + 65 * k
            g.append(line(f'M{xx} 420 L{xx} 580'))
    g.append(rect(345, 485, 70, 30, 6)); g.append(rect(585, 485, 70, 30, 6))
    # Schuessel + Antenne
    g.append(line('M500 345 L500 300', LW))
    g.append(path('M410 300 Q500 200 590 300 Q500 330 410 300 Z'))
    g.append(line('M500 290 L500 215', LW_THIN)); g.append(circle(500, 205, 16, w=LW_THIN))
    # Koerper
    g.append(rect(410, 340, 180, 300, 30))
    g.append(rect(440, 560, 120, 50, 12, w=LW_THIN))
    g.append(rect(460, 640, 80, 50, 10))
    g.append(face(500, 440, .95, gap=48, mouth='smile', blush=False))
    g.append(ellipse(452, 485, 15, 8, w=4)); g.append(ellipse(548, 485, 15, 8, w=4))
    o.append(f'<g transform="rotate(-14 500 500)">{"".join(g)}</g>')
    return ''.join(o)


@motif('wr08', 'STERNSCHNUPPE', 'weltraum')
def sternschnuppe():
    o = []
    o.append(sparkle(170, 170, 40)); o.append(rounded_star(860, 820, 44, 21)); o.append(sparkle(560, 860, 30)); o.append(circle(880, 120, 22, w=LW_THIN))
    # Schweif (drei Baender)
    o.append(_tail((560, 360), (330, 420), (110, 560), 92, 40))
    o.append(_tail((560, 470), (330, 580), (150, 760), 100, 44))
    o.append(_tail((620, 560), (470, 700), (370, 900), 92, 40))
    # Stern
    o.append(rounded_star(640, 410, 275, 135, 5, -100))
    o.append(face(640, 420, 1.3, gap=66, mouth='open'))
    return ''.join(o)


@motif('wr09', 'TELESKOP', 'weltraum')
def teleskop():
    o = []
    # Mond + Sterne, wohin das Teleskop zeigt
    o.append(path('M880 90 C800 95 750 160 755 235 C760 305 820 355 890 350 C840 330 810 285 810 225 C810 160 840 115 880 90 Z'))
    o.append(rounded_star(700, 130, 40, 19)); o.append(sparkle(860, 450, 30)); o.append(sparkle(140, 200, 34)); o.append(rounded_star(170, 470, 36, 17))
    # Stativ
    o.append(path('M505 500 L330 905 L370 915 L530 520 Z'))
    o.append(path('M495 500 L670 905 L630 915 L470 520 Z'))
    o.append(path('M485 520 L485 925 L515 925 L515 520 Z'))
    # Rohr entlang Achse
    cx, cy, a = 480, 400, -30
    ex, ey = _pt(cx, cy, a, -255)
    o.append(rect(ex - 45, ey - 38, 90, 76, 14, rot=a))
    o.append(rect(cx - 220, cy - 72, 440, 144, 44, rot=a))
    fx, fy = _pt(cx, cy, a, 250)
    o.append(rect(fx - 40, fy - 95, 80, 190, 22, rot=a))
    o.append(circle(500, 490, 42))
    o.append(face(470, 395, .9, gap=52, mouth='smile'))
    return ''.join(o)


@motif('wr10', 'MONDAUTO', 'weltraum')
def mondauto():
    o = []
    # Erde + Sterne
    o.append(circle(840, 160, 78))
    o.append(path('M800 110 C830 100 850 125 835 150 C820 172 790 160 785 140 C782 125 788 115 800 110 Z', w=LW_THIN))
    o.append(path('M860 185 C885 180 900 205 885 222 C868 238 845 225 848 205 Z', w=LW_THIN))
    o.append(rounded_star(140, 150, 46, 22)); o.append(sparkle(470, 120, 30)); o.append(sparkle(160, 470, 28))
    # Mondboden mit Kratern
    o.append(path('M60 770 Q260 730 500 765 T940 760 L940 935 L60 935 Z'))
    o.append(ellipse(200, 860, 70, 26, w=LW_THIN)); o.append(ellipse(800, 865, 85, 28, w=LW_THIN)); o.append(ellipse(520, 895, 50, 18, w=LW_THIN))
    # Antenne mit Schuessel
    o.append(line('M655 430 L700 300', LW))
    o.append(path('M650 300 Q700 220 760 290 Q710 320 650 300 Z'))
    # Kuppel
    o.append(path('M330 470 C330 300 600 300 600 470 Z'))
    o.append(path('M380 465 C380 360 550 360 550 465 Z', w=LW_THIN))
    # Raeder
    for x in (320, 680):
        o.append(circle(x, 720, 88)); o.append(circle(x, 720, 40, w=LW_THIN))
    # Karosserie
    o.append(path('M225 520 Q225 465 280 465 L720 465 Q785 465 790 525 L800 640 Q800 680 760 680 L260 680 Q225 680 225 645 Z'))
    o.append(rect(705, 520, 70, 50, 14, w=LW_THIN))
    o.append(face(470, 560, 1.0, gap=62, mouth='open'))
    return ''.join(o)

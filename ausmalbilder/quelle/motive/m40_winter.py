import math
from kritzel import *


def mirror(s):
    return f'<g transform="translate(1000 0) scale(-1 1)">{s}</g>'


def tube(d, w=46):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w - 2 * LW_THIN - 4}"/>')


def fluffy(cx, cy, r, n=10, bump=.22, w=LW):
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n
        c = (cx + r * (1 + bump * 2) * math.cos(a), cy + r * (1 + bump * 2) * math.sin(a))
        p = pts[(i + 1) % n]
        d += f' Q{f(c[0])} {f(c[1])} {f(p[0])} {f(p[1])}'
    return path(d + ' Z', w=w)


def clover(cx, cy, s, rot=0, w=LW):
    o = []
    for a in (90, 180, 270, 0):
        o.append(f'<g transform="rotate({a + rot} {f(cx)} {f(cy)})">'
                 + heart(cx, cy - .9 * s, s, w=w) + '</g>')
    return ''.join(o)


@motif('wi01', 'SCHNEEMANN', 'winter')
def schneemann():
    o = []
    o.append(tube('M330 600 L170 480')); o.append(tube('M215 515 L175 430')); o.append(tube('M235 530 L150 535'))
    o.append(mirror(tube('M330 600 L170 480'))); o.append(mirror(tube('M215 515 L175 430'))); o.append(mirror(tube('M235 530 L150 535')))
    o.append(circle(500, 710, 205))
    o.append(path('M560 520 L640 520 C660 600 650 680 640 720 L585 720 C590 660 580 590 560 520 Z'))
    o.append(line('M592 690 L640 690', LW_THIN))
    for y in (620, 720, 810):
        o.append(circle(500, y, 22))
    o.append(circle(500, 385, 155))
    o.append(path('M360 470 Q500 540 640 470 L650 520 Q500 590 350 520 Z'))
    o.append(rect(365, 220, 270, 42, 18))
    o.append(rect(400, 85, 200, 150, 14))
    o.append(rect(400, 180, 200, 40, 0, w=LW_THIN))
    o.append(eye(445, 360, 1.05)); o.append(eye(555, 360, 1.05))
    o.append(path('M495 392 L600 412 L495 425 Q482 408 495 392 Z', w=LW_THIN))
    o.append(line('M465 448 Q500 470 535 448', LW_THIN))
    o.append(ellipse(395, 412, 20, 10, w=5)); o.append(ellipse(605, 440, 20, 10, w=5))
    o.append(sparkle(150, 200, 34)); o.append(sparkle(850, 210, 28)); o.append(sparkle(860, 830, 30)); o.append(sparkle(140, 830, 26))
    return ''.join(o)


@motif('wi02', 'SCHNEEFLOCKE', 'winter')
def schneeflocke():
    o = []
    arm = (tube('M500 300 L420 215', 48) + tube('M500 300 L580 215', 48) +
           rect(468, 105, 64, 340, 32) + circle(500, 115, 34))
    for a in range(0, 360, 60):
        o.append(f'<g transform="rotate({a} 500 500)">{arm}</g>')
    o.append(circle(500, 500, 165))
    o.append(face(500, 485, 1.15, gap=65, mouth='smile'))
    return ''.join(o)


@motif('wi03', 'MÜTZE', 'winter')
def muetze():
    o = []
    o.append(fluffy(500, 185, 92, n=11, bump=.14))
    o.append(path('M215 700 C205 430 325 260 500 260 C675 260 795 430 785 700 Z'))
    o.append(line('M262 470 L330 420 L400 470 L470 420 L530 420 L600 470 L670 420 L738 470', LW_THIN))
    o.append(rect(170, 650, 660, 190, 70))
    for x in range(250, 760, 70):
        o.append(line(f'M{x} 675 L{x} 815', LW_THIN))
    o.append(face(500, 540, 1.15, gap=70, mouth='smile'))
    o.append(sparkle(130, 260, 34)); o.append(sparkle(860, 300, 28)); o.append(sparkle(880, 900, 26))
    return ''.join(o)


@motif('wi04', 'HANDSCHUH', 'winter')
def handschuh():
    o = []
    # Daumen (hinten), schraeg nach aussen
    o.append(ellipse(290, 520, 78, 128, rot=-28))
    o.append(line('M300 470 Q320 520 318 575', LW_THIN))
    # Hand
    o.append(path('M335 770 L335 390 C335 215 425 130 535 130 C655 130 735 225 735 390 L735 770 Z'))
    # Zickzack-Band als Muster
    zz1 = 'M335 545 ' + ' '.join(f'L{x} {525 if i % 2 == 0 else 565}' for i, x in enumerate(range(385, 735, 50))) + ' L735 545'
    zz2 = 'M335 615 ' + ' '.join(f'L{x} {595 if i % 2 == 0 else 635}' for i, x in enumerate(range(385, 735, 50))) + ' L735 615'
    o.append(line(zz1, LW_THIN)); o.append(line(zz2, LW_THIN))
    o.append(heart(535, 690, 40, w=LW_THIN))
    # Buendchen
    o.append(rect(295, 745, 480, 160, 55))
    for x in range(355, 740, 55):
        o.append(line(f'M{x} 770 L{x} 880', LW_THIN))
    o.append(face(535, 360, 1.15, gap=64, mouth='open'))
    o.append(sparkle(140, 200, 34)); o.append(sparkle(860, 220, 30)); o.append(sparkle(860, 620, 26))
    return ''.join(o)


@motif('wi05', 'EISBÄR', 'winter')
def eisbaer():
    o = []
    o.append(path('M330 560 C250 640 245 800 300 880 L700 880 C755 800 750 640 670 560 Z'))
    o.append(ellipse(500, 760, 120, 110, w=LW_THIN))
    o.append(ellipse(285, 700, 55, 95, rot=20)); o.append(ellipse(715, 700, 55, 95, rot=-20))
    o.append(ellipse(390, 880, 80, 45)); o.append(ellipse(610, 880, 80, 45))
    o.append(circle(305, 225, 72)); o.append(circle(305, 225, 34, w=LW_THIN))
    o.append(mirror(circle(305, 225, 72))); o.append(mirror(circle(305, 225, 34, w=LW_THIN)))
    o.append(ellipse(500, 400, 240, 200))
    o.append(eye(410, 370, 1.05)); o.append(eye(590, 370, 1.05))
    o.append(ellipse(500, 470, 92, 66))
    o.append(path('M470 440 Q500 425 530 440 Q520 470 500 472 Q480 470 470 440 Z', fill=INK, w=LW_THIN))
    o.append(line('M500 472 L500 492 M470 498 Q500 518 530 498', LW_THIN))
    o.append(ellipse(350, 445, 22, 11, w=5)); o.append(ellipse(650, 445, 22, 11, w=5))
    o.append(sparkle(140, 420, 32)); o.append(sparkle(870, 440, 28)); o.append(sparkle(860, 120, 26))
    return ''.join(o)


@motif('wi06', 'IGLU', 'winter')
def iglu():
    o = []
    o.append(path('M80 820 C250 790 750 790 920 820 L920 870 C750 845 250 845 80 870 Z'))
    o.append(path('M140 815 C140 500 300 320 500 320 C700 320 860 500 860 815 Z'))

    def edge_x(y):
        # linke Kuppelkante (kubische Bezier) bei Hoehe y
        P = [(140, 815), (140, 500), (300, 320), (500, 320)]
        best = None
        for i in range(2001):
            t = i / 2000
            mt = 1 - t
            bx = mt**3 * P[0][0] + 3 * mt * mt * t * P[1][0] + 3 * mt * t * t * P[2][0] + t**3 * P[3][0]
            by = mt**3 * P[0][1] + 3 * mt * mt * t * P[1][1] + 3 * mt * t * t * P[2][1] + t**3 * P[3][1]
            if best is None or abs(by - y) < abs(best[1] - y):
                best = (bx, by)
        return best[0]
    for y in (640, 730):
        xl = edge_x(y)
        o.append(line(f'M{f(xl)} {y} L{f(1000 - xl)} {y}', LW_THIN))
    xl = edge_x(560)
    o.append(line(f'M{f(xl)} 560 L330 560 M670 560 L{f(1000 - xl)} 560', LW_THIN))
    for x, y0, y1 in ((230, 640, 730), (340, 730, 815), (660, 730, 815), (770, 640, 730), (300, 560, 640), (700, 560, 640)):
        o.append(line(f'M{x} {y0} L{x} {y1}', LW_THIN))
    o.append(path('M380 815 L380 700 C380 600 620 600 620 700 L620 815 Z'))
    o.append(path('M425 815 L425 710 C425 650 575 650 575 710 L575 815 Z', w=LW_THIN))
    o.append(face(500, 470, 1.15, gap=72, mouth='smile'))
    o.append(sparkle(150, 230, 36)); o.append(sparkle(850, 200, 30)); o.append(rounded_star(820, 400, 40, 18))
    o.append(sparkle(170, 450, 24))
    return ''.join(o)


@motif('wi07', 'SCHLITTSCHUH', 'winter')
def schlittschuh():
    o = []
    o.append(rect(370, 735, 55, 85, 10)); o.append(rect(690, 735, 55, 85, 10))
    o.append(path('M200 790 L840 790 C880 790 895 830 860 840 L230 840 C190 840 170 820 175 800 Q140 790 150 760 Q175 740 200 790 Z'))
    o.append(path('M300 230 C300 200 315 185 340 185 L555 185 C565 305 580 420 640 470 C720 520 830 540 835 630 L835 690 L300 690 Z'))
    o.append(rect(285, 685, 565, 58, 24))
    o.append(rect(285, 150, 300, 70, 30))
    for y in (270, 340, 410):
        o.append(line(f'M380 {y} L520 {y + 50} M520 {y} L380 {y + 50}', LW_THIN))
    o.append(face(640, 600, .95, gap=60, mouth='smile'))
    o.append(sparkle(150, 300, 34)); o.append(sparkle(800, 250, 30)); o.append(sparkle(880, 420, 24))
    return ''.join(o)


@motif('wi08', 'GLÜCKSSCHWEIN', 'winter')
def gluecksschwein():
    o = []
    o.append(line('M720 760 C800 740 800 680 760 680 C730 680 740 720 770 720', LW_THIN))
    o.append(ellipse(500, 740, 240, 170))
    o.append(ellipse(390, 885, 55, 38)); o.append(ellipse(610, 885, 55, 38))
    o.append(ellipse(330, 780, 45, 60, rot=15)); o.append(ellipse(670, 780, 45, 60, rot=-15))
    ear = 'M330 290 C290 230 270 170 300 130 C350 150 400 190 430 245 Z'
    o.append(path(ear)); o.append(mirror(path(ear)))
    o.append(ellipse(500, 420, 245, 205))
    o.append(eye(400, 370, 1.05)); o.append(eye(600, 370, 1.05))
    o.append(ellipse(500, 490, 88, 62))
    o.append(ellipse(470, 490, 14, 22, fill=INK, w=0)); o.append(ellipse(530, 490, 14, 22, fill=INK, w=0))
    o.append(line('M465 572 Q500 595 535 572', LW_THIN))
    o.append(ellipse(330, 470, 24, 12, w=5)); o.append(ellipse(670, 470, 24, 12, w=5))
    o.append(line('M790 330 C770 270 790 230 810 210', LW_THIN))
    o.append(clover(820, 200, 42, rot=10, w=LW_THIN))
    o.append(sparkle(140, 230, 32)); o.append(sparkle(150, 640, 26)); o.append(sparkle(880, 520, 26))
    return ''.join(o)


@motif('wi09', 'KLEEBLATT', 'winter')
def kleeblatt():
    o = []
    cx, cy = 500, 420
    o.append(tube(f'M{cx} {cy + 60} C{cx + 20} {cy + 250} {cx + 110} {cy + 380} {cx + 210} {cy + 490}', 50))
    o.append(clover(cx, cy, 185, rot=0, w=LW))
    for a in (0, 90, 180, 270):
        r1, r2 = 105, 228
        ra = math.radians(a)
        o.append(line(f'M{f(cx + r1 * math.cos(ra))} {f(cy + r1 * math.sin(ra))} L{f(cx + r2 * math.cos(ra))} {f(cy + r2 * math.sin(ra))}', LW_THIN))
    o.append(circle(cx, cy, 100))
    o.append(face(cx, cy - 10, .85, gap=40, mouth='smile', blush=False))
    o.append(sparkle(130, 140, 34)); o.append(sparkle(870, 140, 30)); o.append(sparkle(860, 820, 28)); o.append(sparkle(150, 840, 26))
    return ''.join(o)


@motif('wi10', 'RAKETE', 'winter')
def rakete():
    o = []

    def burst(cx, cy, r, n=8, rr=None):
        g = []
        for i in range(n):
            a = 360 * i / n
            ra = math.radians(a)
            g.append(ellipse(cx + r * math.cos(ra), cy + r * math.sin(ra), r * .26, r * .55, w=LW_THIN + 1, rot=a + 90))
        g.append(circle(cx, cy, r * .42, w=LW_THIN + 1))
        return ''.join(g)
    # Feuerwerk
    o.append(burst(205, 230, 125))
    o.append(burst(800, 200, 95, 8))
    # Stab
    o.append(rect(478, 760, 44, 190, 20))
    # Flossen (hinten)
    o.append(path('M380 600 C330 640 290 700 285 790 L380 740 Z'))
    o.append(path('M620 600 C670 640 710 700 715 790 L620 740 Z'))
    # Koerper + Spitze
    o.append(rect(370, 360, 260, 400, 26))
    o.append(path('M362 380 C380 300 440 215 500 160 C560 215 620 300 638 380 Z'))
    # Baender (Flaechen)
    o.append(rect(355, 345, 290, 50, 20))
    o.append(rect(355, 690, 290, 50, 20))
    o.append(line('M370 470 L630 470', LW_THIN)); o.append(line('M370 620 L630 620', LW_THIN))
    o.append(rounded_star(445, 432, 26, 12, w=LW_THIN)); o.append(rounded_star(555, 432, 26, 12, w=LW_THIN))
    o.append(face(500, 530, 1.05, gap=58, mouth='open'))
    o.append(circle(440, 655, 16, w=LW_THIN)); o.append(circle(500, 655, 16, w=LW_THIN)); o.append(circle(560, 655, 16, w=LW_THIN))
    o.append(sparkle(800, 520, 34)); o.append(sparkle(170, 540, 30)); o.append(sparkle(800, 870, 30)); o.append(rounded_star(200, 860, 40, 19))
    return ''.join(o)

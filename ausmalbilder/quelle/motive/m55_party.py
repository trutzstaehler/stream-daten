from kritzel import *


def _icing(x0, x1, ytop, ybase, n, depth, r=26):
    """Zuckerguss-Band mit Tropfen: oben gerade (mit runden Ecken), unten wellig."""
    w = (x1 - x0) / n
    d = f'M{f(x0)} {f(ytop + r)} Q{f(x0)} {f(ytop)} {f(x0 + r)} {f(ytop)} L{f(x1 - r)} {f(ytop)} Q{f(x1)} {f(ytop)} {f(x1)} {f(ytop + r)} L{f(x1)} {f(ybase)}'
    for i in range(n):
        xa = x1 - i * w
        xb = xa - w
        deep = depth if i % 2 == 0 else depth * .55
        d += f' C{f(xa - w * .1)} {f(ybase + deep)} {f(xb + w * .1)} {f(ybase + deep)} {f(xb)} {f(ybase)}'
    d += ' Z'
    return path(d)


def _flame(x, y, s=1.0):
    return path(f'M{f(x)} {f(y - 60 * s)} Q{f(x + 34 * s)} {f(y - 10 * s)} {f(x + 24 * s)} {f(y + 18 * s)} '
                f'Q{f(x)} {f(y + 44 * s)} {f(x - 24 * s)} {f(y + 18 * s)} Q{f(x - 34 * s)} {f(y - 10 * s)} {f(x)} {f(y - 60 * s)} Z', w=LW_THIN)


def _bow(x, y, s=1.0):
    o = []
    o.append(path(f'M{f(x)} {f(y)} C{f(x - 30 * s)} {f(y - 50 * s)} {f(x - 90 * s)} {f(y - 40 * s)} {f(x - 85 * s)} {f(y)} '
                  f'C{f(x - 90 * s)} {f(y + 40 * s)} {f(x - 30 * s)} {f(y + 50 * s)} {f(x)} {f(y)} Z', w=LW_THIN))
    o.append(path(f'M{f(x)} {f(y)} C{f(x + 30 * s)} {f(y - 50 * s)} {f(x + 90 * s)} {f(y - 40 * s)} {f(x + 85 * s)} {f(y)} '
                  f'C{f(x + 90 * s)} {f(y + 40 * s)} {f(x + 30 * s)} {f(y + 50 * s)} {f(x)} {f(y)} Z', w=LW_THIN))
    o.append(circle(x, y, 16 * s, w=LW_THIN))
    return ''.join(o)


@motif('gb01', 'TORTE', 'party')
def torte():
    o = []
    o.append(ellipse(500, 845, 380, 48))                         # Teller
    o.append(rect(190, 560, 620, 290, 32))                        # untere Etage
    o.append(_icing(190, 810, 560, 625, 8, 50))
    o.append(rect(295, 380, 410, 200, 28))                        # obere Etage
    o.append(_icing(295, 705, 380, 435, 6, 40, 22))
    for x in (350, 650):
        o.append(circle(x, 515, 22, w=LW_THIN))
    o.append(heart(500, 515, 34))
    for x in (390, 500, 610):                                     # Kerzen
        o.append(rect(x - 21, 245, 42, 140, 10))
        o.append(line(f'M{x} 245 L{x} 222', LW_THIN))
        o.append(_flame(x, 180))
    o.append(face(500, 720, 1.15, gap=74, mouth='open'))
    o.append(sparkle(130, 300, 40)); o.append(sparkle(870, 280, 32)); o.append(sparkle(860, 520, 26))
    o.append(sparkle(140, 520, 24))
    return ''.join(o)


@motif('gb02', 'LUFTBALLONS', 'party')
def luftballons():
    o = []
    balloons = [(270, 290, 150, 180, .85), (730, 290, 150, 180, .85), (500, 410, 170, 200, 1.1)]
    # Schnuere zuerst (hinter den Ballons)
    for cx, cy, rx, ry, s in balloons:
        ky = cy + ry + 26
        o.append(line(f'M{cx} {ky} C{cx + (500 - cx) * .2 + 30} {ky + 120} {500 - (500 - cx) * .2 - 30} {800} 500 860', LW_THIN))
    for cx, cy, rx, ry, s in balloons:
        ky = cy + ry
        o.append(path(f'M{cx - 22} {ky + 28} L{cx} {ky - 4} L{cx + 22} {ky + 28} Q{cx} {ky + 18} {cx - 22} {ky + 28} Z', w=LW_THIN))
        o.append(ellipse(cx, cy, rx, ry))
        o.append(line(f'M{cx - rx * .6} {cy - ry * .25} Q{cx - rx * .55} {cy - ry * .65} {cx - rx * .2} {cy - ry * .78}', LW_THIN))
        o.append(face(cx, cy + 10 * s, s, gap=58, mouth='open' if s > 1 else 'smile'))
    o.append(_bow(500, 860, 1.1))
    o.append(sparkle(110, 620, 34)); o.append(sparkle(890, 620, 30)); o.append(sparkle(500, 110, 30))
    return ''.join(o)


@motif('gb03', 'PARTYHUT', 'party')
def partyhut():
    o = []
    top, bl, br, by = (500, 170), 255, 745, 790
    lx = lambda y: 500 - (y - top[1]) * (500 - bl) / (by - top[1])
    rx = lambda y: 500 + (y - top[1]) * (br - 500) / (by - top[1])
    o.append(path(f'M500 {top[1]} L{br} {by} Q500 {by + 70} {bl} {by} Z'))
    # Baender (Zickzack-Kanten von Rand zu Rand)
    for y in (360, 560):
        a, b = lx(y), rx(y)
        pts = [(a, y)]
        n = 6
        for i in range(1, n):
            pts.append((a + (b - a) * i / n, y + (24 if i % 2 else -24)))
        pts.append((b, y))
        o.append(line('M' + ' L'.join(f'{f(x)} {f(yy)}' for x, yy in pts), LW_THIN))
    # Punkte im oberen Band
    o.append(circle(500, 290, 24, w=LW_THIN))
    # Gesicht im mittleren Band
    o.append(face(500, 455, 1.0, gap=60, mouth='smile'))
    # Sterne im unteren Band
    o.append(rounded_star(400, 680, 40, 19, w=LW_THIN)); o.append(rounded_star(600, 680, 40, 19, w=LW_THIN))
    o.append(path(f'M{bl - 10} {by - 12} Q500 {by + 60} {br + 10} {by - 12} L{br + 4} {by + 36} Q500 {by + 115} {bl - 4} {by + 36} Z'))
    # Bommel
    d = ''
    for i in range(10):
        a1 = math.radians(i * 36); a2 = math.radians((i + 1) * 36); am = (a1 + a2) / 2
        x1, y1 = 500 + 62 * math.cos(a1), 140 + 62 * math.sin(a1)
        x2, y2 = 500 + 62 * math.cos(a2), 140 + 62 * math.sin(a2)
        xm, ym = 500 + 86 * math.cos(am), 140 + 86 * math.sin(am)
        d += (f'M{f(x1)} {f(y1)}' if i == 0 else '') + f' Q{f(xm)} {f(ym)} {f(x2)} {f(y2)}'
    o.append(path(d + ' Z'))
    o.append(sparkle(170, 300, 40)); o.append(sparkle(840, 290, 32)); o.append(sparkle(150, 640, 26)); o.append(sparkle(860, 620, 30))
    return ''.join(o)


@motif('gb04', 'MUFFIN', 'party')
def muffin():
    o = []
    o.append(path('M245 610 C205 530 265 455 330 470 C320 375 430 330 500 365 C570 330 680 375 670 470 '
                  'C735 455 795 530 755 610 Z'))
    for (x, y, rot) in [(360, 440, -30), (450, 410, 20), (600, 430, -15), (690, 520, 35), (300, 540, 25), (560, 380, 60)]:
        o.append(rect(x - 26, y - 10, 52, 20, 10, w=LW_THIN, rot=rot))
    # Kirsche
    o.append(line('M500 300 Q520 230 575 205', LW_THIN))
    o.append(circle(500, 315, 48))
    o.append(path('M290 575 L710 575 L655 880 L345 880 Z'))
    for t in (.2, .4, .6, .8):
        xt = 290 + 420 * t; xb = 345 + 310 * t
        o.append(line(f'M{f(xt)} 575 L{f(xb)} 880', LW_THIN))
    o.append(rect(270, 555, 460, 46, 23))
    o.append(face(500, 690, 1.0, gap=62, mouth='smile', blush=False))
    o.append(sparkle(150, 300, 38)); o.append(sparkle(860, 320, 30)); o.append(sparkle(840, 760, 30)); o.append(sparkle(160, 760, 26))
    return ''.join(o)


@motif('gb05', 'EISWAFFEL', 'party')
def eiswaffel():
    o = []
    L = lambda t: (365 + 135 * t, 540 + 380 * t)
    R = lambda t: (635 - 135 * t, 540 + 380 * t)
    o.append(path('M365 540 L635 540 L500 920 Z'))
    for a, b in ((0, .45), (.25, .75)):
        p, q = L(a), R(b)
        o.append(line(f'M{f(p[0])} {f(p[1])} L{f(q[0])} {f(q[1])}', LW_THIN))
        p, q = R(a), L(b)
        o.append(line(f'M{f(p[0])} {f(p[1])} L{f(q[0])} {f(q[1])}', LW_THIN))
    o.append(path('M365 540 L635 540 L500 920 Z', fill='none'))
    # untere Kugel mit Tropfkante
    o.append(path('M320 540 C285 400 380 300 500 300 C620 300 715 400 680 540 '
                  'C660 600 630 560 610 575 C590 640 555 600 540 585 C520 560 480 560 460 590 '
                  'C440 630 400 610 395 575 C380 560 350 600 320 540 Z'))
    # obere Kugel
    o.append(path('M360 330 C340 210 420 140 500 140 C580 140 660 210 640 330 C600 360 400 360 360 330 Z'))
    for (x, y, rot) in [(430, 220, -25), (560, 210, 30), (500, 270, 0), (600, 290, -40)]:
        o.append(rect(x - 22, y - 9, 44, 18, 9, w=LW_THIN, rot=rot))
    o.append(circle(500, 110, 40))
    o.append(line('M500 72 Q510 40 540 30', LW_THIN))
    o.append(face(500, 440, 1.05, gap=64, mouth='open'))
    o.append(sparkle(180, 260, 40)); o.append(sparkle(820, 250, 32)); o.append(sparkle(800, 640, 28)); o.append(sparkle(200, 660, 30))
    return ''.join(o)


@motif('gb06', 'LOLLI', 'party')
def lolli():
    o = []
    o.append(rect(478, 600, 44, 320, 18))
    o.append(circle(500, 360, 270))
    for i in range(6):
        a = math.radians(i * 60 - 90)
        x2, y2 = 500 + 270 * math.cos(a), 360 + 270 * math.sin(a)
        c = math.radians(i * 60 - 50)
        cx, cy = 500 + 190 * math.cos(c), 360 + 190 * math.sin(c)
        o.append(line(f'M500 360 Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}', LW_THIN))
    o.append(circle(500, 360, 270, fill='none'))
    o.append(circle(500, 360, 105))
    o.append(face(500, 345, .95, gap=48, mouth='smile', blush=False))
    o.append(_bow(500, 640, 1.2))
    o.append(sparkle(130, 140, 36)); o.append(sparkle(870, 150, 30)); o.append(sparkle(840, 760, 34)); o.append(sparkle(170, 780, 28))
    return ''.join(o)


@motif('gb07', 'TRÖTE', 'party')
def troete():
    o = []
    # Konfetti
    for (x, y, r) in [(860, 180, 22), (900, 470, 18), (860, 800, 24), (150, 250, 20)]:
        o.append(circle(x, y, r, w=LW_THIN))
    o.append(rounded_star(780, 130, 40, 19, w=LW_THIN)); o.append(rounded_star(900, 650, 34, 16, w=LW_THIN))
    o.append(rect(90, 455, 110, 90, 22))                            # Mundstueck
    o.append(path('M180 468 L540 430 C620 380 690 290 780 270 L780 730 C690 710 620 620 540 570 L180 532 Z'))
    top = lambda x: 468 - (x - 180) * 38 / 360
    bot = lambda x: 532 + (x - 180) * 38 / 360
    for x in (290, 410):
        o.append(line(f'M{x} {f(top(x))} Q{x + 18} 500 {x} {f(bot(x))}', LW_THIN))
    o.append(line('M540 430 Q560 500 540 570', LW_THIN))
    o.append(ellipse(780, 500, 50, 232))
    o.append(face(650, 500, .95, gap=52, mouth='open'))
    o.append(sparkle(250, 720, 34)); o.append(sparkle(300, 290, 28))
    return ''.join(o)


@motif('gb08', 'GIRLANDE', 'party')
def girlande():
    o = []

    def chain(p0, c, p2, ts, deco, drop):
        B = lambda t: ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p2[0],
                       (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p2[1])
        o.append(line(f'M{p0[0]} {p0[1]} Q{c[0]} {c[1]} {p2[0]} {p2[1]}', LW_THIN))
        for t, dco in zip(ts, deco):
            a, b = B(t - .085), B(t + .085)
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            tip = (mx, my + drop)
            o.append(path(f'M{f(a[0])} {f(a[1])} L{f(b[0])} {f(b[1])} L{f(tip[0] + 8)} {f(tip[1] - 12)} '
                          f'Q{f(tip[0])} {f(tip[1] + 6)} {f(tip[0] - 8)} {f(tip[1] - 12)} Z'))
            cx, cy = mx, my + drop * .36
            if dco == 'face':
                o.append(face(cx, cy - 6, .75, gap=46, mouth='smile', blush=False))
            elif dco == 'star':
                o.append(rounded_star(cx, cy, 38, 18, w=LW_THIN))
            elif dco == 'heart':
                o.append(heart(cx, cy, 30))
            elif dco == 'dot':
                o.append(circle(cx, cy, 26, w=LW_THIN))
        for (x, y) in (p0, p2):
            o.append(circle(x, y, 18, w=LW_THIN))

    chain((60, 110), (500, 400), (940, 110), [.12, .31, .5, .69, .88], ['star', 'face', 'heart', 'face', 'dot'], 250)
    chain((80, 540), (500, 770), (920, 540), [.2, .4, .6, .8], ['heart', 'dot', 'face', 'star'], 230)
    o.append(sparkle(500, 90, 30))
    return ''.join(o)


@motif('gb09', 'PIZZA', 'party')
def pizza():
    o = []
    o.append(path('M205 250 Q500 175 795 250 L520 895 Q500 925 480 895 Z'))
    o.append(path('M175 240 Q500 140 825 240 Q835 275 805 300 Q500 220 195 300 Q165 275 175 240 Z'))
    for (x, y, r) in [(330, 365, 48), (670, 365, 48), (500, 615, 58), (500, 790, 32)]:
        o.append(circle(x, y, r, w=LW_THIN))
        o.append(circle(x, y, r * .55, w=5))
    # Basilikumblaetter
    for (x, y, rot) in [(395, 520, -30), (610, 520, 30)]:
        o.append(ellipse(x, y, 34, 18, w=LW_THIN, rot=rot))
    o.append(face(500, 420, 1.0, gap=60, mouth='open'))
    o.append(sparkle(140, 520, 38)); o.append(sparkle(860, 520, 32)); o.append(sparkle(250, 800, 30)); o.append(sparkle(760, 790, 26))
    return ''.join(o)


@motif('gb10', 'POPCORN', 'party')
def popcorn():
    o = []
    def kernel(x, y, r, rot):
        d = ''
        n = 5
        for i in range(n):
            a1 = math.radians(rot + i * 360 / n); a2 = math.radians(rot + (i + 1) * 360 / n); am = (a1 + a2) / 2
            p1 = (x + r * .78 * math.cos(a1), y + r * .78 * math.sin(a1))
            p2 = (x + r * .78 * math.cos(a2), y + r * .78 * math.sin(a2))
            c = (x + r * 1.25 * math.cos(am), y + r * 1.25 * math.sin(am))
            d += (f'M{f(p1[0])} {f(p1[1])}' if i == 0 else '') + f' Q{f(c[0])} {f(c[1])} {f(p2[0])} {f(p2[1])}'
        return path(d + ' Z')
    for (x, y, r, rot) in [(325, 395, 80, 10), (675, 395, 80, 40), (415, 320, 84, 70), (585, 320, 84, 20), (500, 230, 86, 0),
                           (355, 240, 66, 50), (650, 240, 66, 30), (500, 400, 78, 15)]:
        o.append(kernel(x, y, r, rot))
    o.append(path('M270 440 L730 440 L670 905 L330 905 Z'))
    lx = lambda y: 270 + 60 * (y - 440) / 465
    rx = lambda y: 730 - 60 * (y - 440) / 465
    for t in (.2, .8):
        xt = lx(505) + (rx(505) - lx(505)) * t
        xb = lx(905) + (rx(905) - lx(905)) * t
        o.append(line(f'M{f(xt)} 505 L{f(xb)} 905', LW_THIN))
    o.append(rect(255, 440, 490, 68, 20))
    o.append(rounded_star(500, 474, 26, 12, w=5))
    o.append(face(500, 650, 1.05, gap=62, mouth='open'))
    o.append(sparkle(150, 220, 38)); o.append(sparkle(860, 210, 32)); o.append(sparkle(150, 760, 30)); o.append(sparkle(860, 760, 34))
    return ''.join(o)

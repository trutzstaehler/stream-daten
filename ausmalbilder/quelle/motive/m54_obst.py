from kritzel import *


def _cloud(cx, cy, rx, ry, n=9, bulge=1.32, rot=-90):
    """Wolken-/Brokkoli-Umriss: Punkte auf Ellipse, nach aussen gewoelbte Boegen."""
    pts = []
    for i in range(n):
        a = math.radians(rot + i * 360 / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        qx, qy = cx + (mx - cx) * bulge, cy + (my - cy) * bulge
        d += f' Q{f(qx)} {f(qy)} {f(p1[0])} {f(p1[1])}'
    return d + ' Z'


def _seed(x, y, rot=0):
    """Kern als kurzer Strich (keine Mini-Flaeche)."""
    a = math.radians(rot)
    dx, dy = 11 * math.sin(a), 11 * math.cos(a)
    return line(f'M{f(x - dx)} {f(y - dy)} L{f(x + dx)} {f(y + dy)}', LW_THIN)


@motif('og01', 'APFEL', 'obst')
def apfel():
    o = []
    o.append(path('M488 300 C486 240 496 185 526 140 L566 158 C540 200 528 248 530 300 Z'))
    o.append(path('M200 380 C150 540 220 760 360 805 C420 822 460 795 500 795 C540 795 580 822 640 805 '
                  'C780 760 850 540 800 380 C750 225 575 228 500 290 C425 228 250 225 200 380 Z'))
    o.append(path('M548 214 C600 128 718 118 772 168 C712 210 624 238 556 228 Z'))
    o.append(line('M570 222 C630 196 690 178 740 172'))
    o.append(ellipse(310, 420, 46, 26, rot=-40, w=LW_THIN))
    o.append(face(500, 540, 1.3, gap=72, mouth='open'))
    o.append(sparkle(140, 220, 34)); o.append(sparkle(860, 300, 26)); o.append(sparkle(880, 820, 30))
    return ''.join(o)


@motif('og02', 'BANANE', 'obst')
def banane():
    o = []
    # Stiel rechts, Spitze links
    o.append(path('M790 300 L852 282 L872 340 L816 372 Z'))
    o.append(path('M140 410 C170 360 205 352 228 372 C300 470 400 520 500 520 C620 520 720 460 800 350 '
                  'C830 330 860 350 862 380 C860 620 700 780 500 780 C300 780 160 640 140 410 Z'))
    o.append(path('M140 410 C150 380 170 365 190 368 C196 392 186 416 160 432 Z', w=LW_THIN))
    o.append(line('M260 470 C340 640 660 660 790 470', LW_THIN))
    o.append(face(510, 630, 1.05, gap=64, mouth='smile'))
    o.append(sparkle(200, 220, 36)); o.append(sparkle(560, 260, 26)); o.append(sparkle(860, 800, 30))
    return ''.join(o)


@motif('og03', 'ERDBEERE', 'obst')
def erdbeere():
    o = []
    o.append(rect(486, 150, 30, 130, 12))
    o.append(path('M500 850 C370 820 200 640 200 460 C200 345 320 300 500 332 C680 300 800 345 800 460 '
                  'C800 640 630 820 500 850 Z'))
    o.append(rounded_star(500, 335, 165, 92, 8, -90))
    for x, y, r in [(300, 450, -20), (700, 450, 20), (260, 580, -10), (740, 580, 10), (360, 700, -25),
                    (640, 700, 25), (500, 770, 0), (410, 790, -15), (590, 790, 15), (330, 520, -15), (670, 520, 15)]:
        o.append(_seed(x, y, r))
    o.append(face(500, 560, 1.2, gap=70, mouth='open'))
    o.append(sparkle(170, 200, 32)); o.append(sparkle(830, 210, 26)); o.append(sparkle(150, 820, 28))
    return ''.join(o)


@motif('og04', 'BIRNE', 'obst')
def birne():
    o = []
    o.append(path('M488 250 C486 200 494 160 518 120 L552 136 C530 172 524 210 526 250 Z'))
    o.append(path('M500 232 C430 232 396 300 396 380 C396 452 300 520 280 640 C258 770 380 852 500 852 '
                  'C620 852 742 770 720 640 C700 520 604 452 604 380 C604 300 570 232 500 232 Z'))
    o.append(path('M540 176 C590 110 690 104 736 150 C686 186 610 206 546 192 Z'))
    o.append(line('M560 186 C610 166 660 156 708 152'))
    o.append(ellipse(350, 640, 38, 22, rot=-60, w=LW_THIN))
    o.append(face(500, 640, 1.2, gap=70, mouth='smile'))
    o.append(sparkle(200, 300, 34)); o.append(sparkle(820, 330, 28)); o.append(sparkle(850, 780, 30))
    return ''.join(o)


@motif('og05', 'KAROTTE', 'obst')
def karotte():
    o = []
    # Kraut
    o.append(path('M478 300 C390 230 350 150 380 92 C440 120 482 210 506 296 Z'))
    o.append(path('M488 300 C462 200 470 118 506 62 C552 120 548 214 518 300 Z'))
    o.append(path('M498 300 C540 214 600 140 656 120 C672 186 600 260 526 304 Z'))
    o.append(line('M470 290 C440 220 410 160 390 112', LW_THIN))
    o.append(line('M502 290 C496 210 500 140 506 90', LW_THIN))
    o.append(line('M520 292 C560 230 600 180 640 142', LW_THIN))
    # Ruebe
    o.append(path('M320 330 C320 284 680 284 680 330 C680 460 568 770 512 872 C506 884 494 884 488 872 '
                  'C432 770 320 460 320 330 Z'))
    for y, side in [(560, -1), (650, 1), (740, -1)]:
        x0 = 500 + side * (150 - (y - 500) * .35)
        o.append(line(f'M{f(x0)} {y} L{f(x0 - side * 55)} {y + 12}', LW_THIN))
    o.append(face(500, 420, 1.15, gap=64, mouth='open'))
    o.append(sparkle(200, 380, 34)); o.append(sparkle(800, 420, 28)); o.append(sparkle(760, 760, 32))
    return ''.join(o)


@motif('og06', 'TOMATE', 'obst')
def tomate():
    o = []
    o.append(ellipse(500, 570, 340, 285))
    o.append(rounded_star(500, 300, 150, 52, 5, -90))
    o.append(rect(486, 186, 28, 104, 12))
    o.append(ellipse(300, 470, 50, 28, rot=-45, w=LW_THIN))
    o.append(face(500, 590, 1.35, gap=74, mouth='open'))
    o.append(sparkle(160, 200, 34)); o.append(sparkle(850, 210, 28)); o.append(sparkle(880, 900, 26))
    return ''.join(o)


@motif('og07', 'ANANAS', 'obst')
def ananas():
    o = []
    # Blaetterkrone (hinten nach vorn)
    o.append(path('M440 380 C380 300 330 230 300 170 C380 200 440 260 480 340 Z'))
    o.append(path('M560 380 C620 300 670 230 700 170 C620 200 560 260 520 340 Z'))
    o.append(path('M450 380 C420 280 410 190 430 110 C480 180 500 280 500 380 Z'))
    o.append(path('M550 380 C580 280 590 190 570 110 C520 180 500 280 500 380 Z'))
    o.append(path('M470 384 C470 270 480 140 500 60 C520 140 530 270 530 384 Z'))
    cx, cy, rx, ry = 500, 630, 240, 270
    o.append(ellipse(cx, cy, rx, ry))
    # Schuppen als eigene Rauten-Flaechen, Gesichtsfeld frei
    s = 44
    for row in range(-8, 9):
        for col in range(-8, 9):
            x = cx + col * 1.6 * s + (.8 * s if row % 2 else 0)
            y = cy + row * s * .9
            if 355 < x < 645 and 515 < y < 665:
                continue
            corners = [(x, y - s * .9), (x + s * .8, y), (x, y + s * .9), (x - s * .8, y)]
            if all(((px - cx) / (rx - 22)) ** 2 + ((py - cy) / (ry - 22)) ** 2 <= 1 for px, py in corners):
                o.append(poly(corners, w=LW_THIN))
    o.append(face(500, 580, 1.15, gap=66, mouth='smile'))
    o.append(sparkle(180, 420, 34)); o.append(sparkle(820, 430, 28)); o.append(sparkle(170, 820, 28))
    return ''.join(o)


@motif('og08', 'WASSERMELONE', 'obst')
def wassermelone():
    o = []
    # Keil: Rinde = ganzer Keil, Fruchtfleisch darueber mit hoeherem Bogen
    o.append(path('M500 120 L160 690 A380 380 0 0 0 840 690 Z'))
    o.append(path('M500 120 L178 660 A375 375 0 0 0 822 660 Z'))
    o.append(path('M500 120 L200 623 A360 360 0 0 0 800 623 Z'))
    for x, y, r in [(500, 270, 0), (430, 400, -15), (570, 400, 15), (300, 600, -20), (700, 600, 20), (500, 750, 0), (390, 700, -10), (610, 700, 10)]:
        a = math.radians(r)
        o.append(f'<path d="M{f(x)} {f(y - 22)} C{f(x + 16)} {f(y)} {f(x + 12)} {f(y + 22)} {f(x)} {f(y + 22)} '
                 f'C{f(x - 12)} {f(y + 22)} {f(x - 16)} {f(y)} {f(x)} {f(y - 22)} Z" fill="{INK}" stroke="none" '
                 f'transform="rotate({r} {f(x)} {f(y)})"/>')
    o.append(face(500, 540, 1.15, gap=66, mouth='open'))
    o.append(sparkle(170, 220, 34)); o.append(sparkle(830, 230, 30)); o.append(sparkle(860, 520, 24))
    return ''.join(o)


@motif('og09', 'BROKKOLI', 'obst')
def brokkoli():
    o = []
    o.append(path('M400 560 L600 560 L650 860 Q500 900 350 860 Z'))
    o.append(line('M440 640 L410 600', LW_THIN)); o.append(line('M560 650 L594 606', LW_THIN))
    o.append(path(_cloud(500, 420, 330, 250, 10, 1.3)))
    for x, y, r in [(300, 330, 60), (700, 330, 60), (500, 250, 70)]:
        o.append(line(f'M{x - r * .6} {y + r * .2} Q{x} {y - r * .7} {x + r * .6} {y + r * .2}', LW_THIN))
    o.append(face(500, 450, 1.25, gap=72, mouth='open'))
    o.append(sparkle(110, 700, 30)); o.append(sparkle(890, 700, 34)); o.append(sparkle(880, 140, 24))
    return ''.join(o)


@motif('og10', 'KIRSCHEN', 'obst')
def kirschen():
    o = []
    o.append(path('M548 168 C460 260 370 380 336 490 L356 496 C392 390 478 272 566 184 Z', w=LW_THIN))
    o.append(path('M556 172 C600 290 650 390 680 470 L700 462 C670 380 622 280 574 168 Z', w=LW_THIN))
    o.append(circle(320, 650, 175))
    o.append(circle(690, 625, 175))
    o.append(path('M562 172 C620 92 744 80 800 134 C740 186 642 204 568 178 Z'))
    o.append(line('M584 172 C640 148 704 136 770 134'))
    o.append(ellipse(240, 570, 34, 20, rot=-45, w=LW_THIN))
    o.append(ellipse(612, 545, 34, 20, rot=-45, w=LW_THIN))
    o.append(face(330, 670, .9, gap=60, mouth='open'))
    o.append(face(698, 645, .9, gap=60, mouth='smile'))
    o.append(sparkle(170, 250, 34)); o.append(sparkle(880, 300, 28)); o.append(sparkle(500, 900, 26))
    return ''.join(o)

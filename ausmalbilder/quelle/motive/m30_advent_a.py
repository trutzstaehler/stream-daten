from kritzel import *


# ---------- lokale Helfer ----------
def tube(ds, width, outline=LW):
    """Dicke Roehre (Geweih, Kufen, Stangen): schwarze Kontur + weisse Flaeche, mehrere Pfade verschmelzen."""
    if isinstance(ds, str):
        ds = [ds]
    blk = ''.join(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width + 2 * outline}"/>' for d in ds)
    wht = ''.join(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{width}"/>' for d in ds)
    return blk + wht


def leaf(cx, cy, length, width, angle=0, w=LW_THIN + 1):
    L, W = length / 2, width
    d = f'M{f(-L)} 0 Q{f(-L * .2)} {f(-W)} {f(L)} 0 Q{f(-L * .2)} {f(W)} {f(-L)} 0 Z'
    return (f'<g transform="translate({f(cx)} {f(cy)}) rotate({f(angle)})">'
            f'<path d="{d}" fill="#fff" stroke-width="{w}"/>'
            f'<path d="M{f(-L * .7)} 0 L{f(L * .65)} 0" fill="none" stroke-width="{LW_THIN - 2}"/></g>')


def holly(cx, cy, s=1.0, angle=0):
    """Zwei Stechpalmenblaetter mit drei Beeren."""
    return (leaf(cx - 70 * s, cy, 150 * s, 45 * s, angle - 20) + leaf(cx + 70 * s, cy, 150 * s, 45 * s, angle + 20) +
            circle(cx - 22 * s, cy - 12 * s, 24 * s, w=LW_THIN + 1) + circle(cx + 22 * s, cy - 12 * s, 24 * s, w=LW_THIN + 1) +
            circle(cx, cy + 22 * s, 24 * s, w=LW_THIN + 1))


def bow(cx, cy, s=1.0):
    """Schleife: zwei Schlaufen, zwei Baender, Knoten."""
    o = []
    o.append(path(f'M{f(cx - 12 * s)} {f(cy + 10 * s)} L{f(cx - 70 * s)} {f(cy + 120 * s)} L{f(cx - 35 * s)} {f(cy + 105 * s)} L{f(cx - 22 * s)} {f(cy + 140 * s)} L{f(cx + 10 * s)} {f(cy + 20 * s)} Z', w=LW_THIN + 2))
    o.append(path(f'M{f(cx + 12 * s)} {f(cy + 10 * s)} L{f(cx + 70 * s)} {f(cy + 120 * s)} L{f(cx + 35 * s)} {f(cy + 105 * s)} L{f(cx + 22 * s)} {f(cy + 140 * s)} L{f(cx - 10 * s)} {f(cy + 20 * s)} Z', w=LW_THIN + 2))
    o.append(path(f'M{f(cx)} {f(cy)} C{f(cx - 40 * s)} {f(cy - 70 * s)} {f(cx - 130 * s)} {f(cy - 60 * s)} {f(cx - 125 * s)} {f(cy)} C{f(cx - 120 * s)} {f(cy + 55 * s)} {f(cx - 40 * s)} {f(cy + 50 * s)} {f(cx)} {f(cy)} Z', w=LW_THIN + 2))
    o.append(path(f'M{f(cx)} {f(cy)} C{f(cx + 40 * s)} {f(cy - 70 * s)} {f(cx + 130 * s)} {f(cy - 60 * s)} {f(cx + 125 * s)} {f(cy)} C{f(cx + 120 * s)} {f(cy + 55 * s)} {f(cx + 40 * s)} {f(cy + 50 * s)} {f(cx)} {f(cy)} Z', w=LW_THIN + 2))
    o.append(ellipse(cx, cy, 30 * s, 26 * s, w=LW_THIN + 2))
    return ''.join(o)


def scallop_ellipse(cx, cy, rx, ry, n=26, bump=26, w=LW):
    """Ellipse mit gewellter Kante (Tannengruen-Kranz)."""
    pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n
        c = (cx + (rx + bump * 2) * math.cos(a), cy + (ry + bump * 2 * ry / rx + bump * .6) * math.sin(a))
        e = pts[(i + 1) % n]
        d += f' Q{f(c[0])} {f(c[1])} {f(e[0])} {f(e[1])}'
    return path(d + ' Z', w=w)


def flame(cx, base, h=210, w=85):
    top = base - h
    d = (f'M{f(cx)} {f(top)} C{f(cx + w * .5)} {f(top + h * .3)} {f(cx + w)} {f(top + h * .52)} {f(cx + w)} {f(top + h * .7)} '
         f'C{f(cx + w)} {f(base - h * .08)} {f(cx + w * .5)} {f(base)} {f(cx)} {f(base)} '
         f'C{f(cx - w * .5)} {f(base)} {f(cx - w)} {f(base - h * .08)} {f(cx - w)} {f(top + h * .7)} '
         f'C{f(cx - w)} {f(top + h * .52)} {f(cx - w * .5)} {f(top + h * .3)} {f(cx)} {f(top)} Z')
    h2, w2 = h * .5, w * .5
    t2 = base - h2 - h * .06
    d2 = (f'M{f(cx)} {f(t2)} C{f(cx + w2 * .6)} {f(t2 + h2 * .35)} {f(cx + w2)} {f(t2 + h2 * .55)} {f(cx + w2)} {f(t2 + h2 * .72)} '
          f'C{f(cx + w2)} {f(t2 + h2 * .95)} {f(cx + w2 * .5)} {f(t2 + h2)} {f(cx)} {f(t2 + h2)} '
          f'C{f(cx - w2 * .5)} {f(t2 + h2)} {f(cx - w2)} {f(t2 + h2 * .95)} {f(cx - w2)} {f(t2 + h2 * .72)} '
          f'C{f(cx - w2)} {f(t2 + h2 * .55)} {f(cx - w2 * .6)} {f(t2 + h2 * .35)} {f(cx)} {f(t2)} Z')
    return path(d) + path(d2, w=LW_THIN)


# ---------- Motive ----------
@motif('ad01', 'ADVENTSKRANZ', 'advent')
def adventskranz():
    o = []
    cx, cy = 500, 760
    # Kranz: ruhiger Ring aus Tannengruen
    o.append(scallop_ellipse(cx, cy, 395, 150, n=16, bump=24))
    o.append(ellipse(cx, cy - 22, 210, 62, w=LW_THIN + 1))
    # Kerzen: hinten zwei, vorne zwei (Reihenfolge hinten -> vorne)
    cands = [(385, 715, 260, False), (615, 715, 260, False), (215, 790, 280, True), (785, 790, 280, False)]
    for x, base, h, lit in cands:
        top = base - h
        hw = 64
        o.append(rect(x - hw, top, 2 * hw, h, 22))
        # Wachstropfen oben als eigene Flaeche
        o.append(path(f'M{f(x - hw)} {f(top + 52)} C{f(x - 40)} {f(top + 52)} {f(x - 36)} {f(top + 92)} {f(x - 14)} {f(top + 92)} '
                      f'C{f(x + 8)} {f(top + 92)} {f(x + 6)} {f(top + 58)} {f(x + 30)} {f(top + 58)} C{f(x + 50)} {f(top + 58)} {f(x + 52)} {f(top + 70)} {f(x + hw)} {f(top + 70)} '
                      f'L{f(x + hw)} {f(top + 22)} Q{f(x + hw)} {f(top)} {f(x + 42)} {f(top)} L{f(x - 42)} {f(top)} Q{f(x - hw)} {f(top)} {f(x - hw)} {f(top + 22)} Z', w=LW_THIN))
        o.append(line(f'M{f(x)} {f(top)} L{f(x)} {f(top - 24)}', LW_THIN))
        if lit:
            o.append(flame(x, top - 20, 170, 62))
        o.append(face(x, top + 150, .85, gap=30, mouth='open' if lit else 'smile', blush=False))
    # Schleife vorne + Beeren
    o.append(bow(500, 868, 1.0))
    o.append(circle(330, 890, 34, w=LW_THIN + 1)); o.append(circle(385, 905, 34, w=LW_THIN + 1))
    o.append(circle(670, 890, 34, w=LW_THIN + 1)); o.append(circle(615, 905, 34, w=LW_THIN + 1))
    o.append(sparkle(110, 300, 40)); o.append(sparkle(890, 290, 34)); o.append(sparkle(500, 230, 32))
    return ''.join(o)


@motif('ad02', 'KERZE', 'advent')
def kerze():
    o = []
    # Teller
    o.append(ellipse(500, 860, 290, 70))
    o.append(path('M770 850 C860 830 880 900 820 905', fill='none', w=LW))
    # Kerze mit Wachstropfen
    o.append(path('M350 450 Q350 400 400 400 L600 400 Q650 400 650 450 L650 840 Q650 875 615 875 L385 875 Q350 875 350 840 Z'))
    o.append(path('M350 470 C375 470 380 545 410 545 C440 545 438 480 465 480 C495 480 498 590 530 590 C562 590 560 488 592 488 '
                  'C622 488 628 515 650 515 L650 450 Q650 400 600 400 L400 400 Q350 400 350 450 Z', w=LW_THIN + 1))
    # Docht + Flamme
    o.append(line('M500 400 L500 360', LW))
    o.append(flame(500, 365, 230, 95))
    o.append(face(500, 690, 1.3, gap=72, mouth='smile'))
    o.append(holly(275, 840, .7, -10))
    o.append(sparkle(250, 230, 40)); o.append(sparkle(760, 270, 32)); o.append(sparkle(800, 560, 26))
    return ''.join(o)


@motif('ad03', 'PLÄTZCHEN', 'advent')
def plaetzchen():
    o = []
    # Teller
    o.append(ellipse(500, 760, 440, 150))
    o.append(ellipse(500, 750, 340, 105, w=LW_THIN))
    # Stern links hinten, Herz rechts hinten
    o.append(rounded_star(300, 520, 205, 100, rot=-100))
    o.append(rounded_star(300, 528, 130, 64, rot=-100, w=LW_THIN))
    o.append(heart(705, 515, 150, w=LW))
    o.append(heart(705, 515, 95, w=LW_THIN))
    # rundes Plaetzchen vorne mit Gesicht + Streuseln
    o.append(circle(500, 660, 175))
    o.append(circle(500, 660, 135, w=LW_THIN))
    o.append(face(500, 650, 1.05, gap=58, mouth='open'))
    for x, y, a in [(420, 560, 30), (580, 565, -30), (500, 545, 90), (575, 740, 20), (425, 740, -25)]:
        o.append(rect(x - 22, y - 9, 44, 18, 9, w=LW_THIN - 1, rot=a))
    o.append(sparkle(860, 250, 38)); o.append(sparkle(130, 260, 30)); o.append(sparkle(500, 300, 28))
    return ''.join(o)


@motif('ad04', 'LEBKUCHENMANN', 'advent')
def lebkuchenmann():
    o = []
    body = ('M440 395 L300 405 C225 410 195 450 200 490 C205 532 245 552 300 545 L372 535 L362 650 '
            'L282 790 C258 835 278 885 324 890 C364 895 390 868 404 838 L470 722 Q500 702 530 722 '
            'L596 838 C610 868 636 895 676 890 C722 885 742 835 718 790 L638 650 L628 535 L700 545 '
            'C755 552 795 532 800 490 C805 450 775 410 700 405 L560 395 Z')
    o.append(path(body))
    o.append(circle(500, 255, 165))
    # Zuckerguss
    for d in ['M248 440 Q266 458 248 476 Q230 494 248 512', 'M752 440 Q734 458 752 476 Q770 494 752 512',
              'M290 815 Q320 835 350 815', 'M650 815 Q680 835 710 815']:
        o.append(line(d, LW_THIN))
    for y in (480, 575, 655):
        o.append(circle(500, y, 26, w=LW_THIN + 1))
    # Fliege
    o.append(path('M500 410 L430 375 Q415 410 430 445 Z', w=LW_THIN + 1))
    o.append(path('M500 410 L570 375 Q585 410 570 445 Z', w=LW_THIN + 1))
    o.append(circle(500, 410, 20, w=LW_THIN + 1))
    o.append(face(500, 240, 1.2, gap=62, mouth='smile'))
    o.append(line('M405 135 Q440 115 470 128', LW_THIN)); o.append(line('M530 128 Q560 115 595 135', LW_THIN))
    o.append(sparkle(150, 220, 38)); o.append(sparkle(850, 230, 30)); o.append(sparkle(860, 660, 26))
    return ''.join(o)


@motif('ad05', 'STIEFEL', 'advent')
def stiefel():
    o = []
    # Suesses im Stiefel (hinten)
    o.append(line('M600 330 L620 170', LW))
    o.append(circle(625, 150, 80))
    o.append(line('M625 85 C680 100 690 160 650 180 C615 195 585 165 605 140 C620 122 645 135 638 150', LW_THIN))
    o.append(tube('M440 340 L440 190 C440 120 360 110 345 175', 50))
    for y in (300, 240):
        o.append(line(f'M415 {y + 16} L465 {y - 16}', LW_THIN))
    o.append(line('M367 140 L393 178', LW_THIN))
    o.append(rect(480, 210, 90, 110, 10, rot=-8)); o.append(line('M520 210 L512 322', LW_THIN))
    # Stiefel
    o.append(path('M320 380 L320 820 C320 860 350 880 395 880 L795 880 C850 880 872 845 860 800 '
                  'C848 750 795 728 720 718 L640 706 L640 380 Z'))
    o.append(line('M320 815 L866 815', LW_THIN + 1))
    o.append(heart(770, 790, 34, w=LW_THIN))
    # Fellrand
    o.append(path('M285 330 Q300 300 340 305 Q370 285 400 305 Q440 288 470 305 Q510 288 540 305 Q575 288 610 305 Q650 300 670 330 '
                  'L670 395 Q655 425 620 415 Q585 435 550 415 Q515 435 480 415 Q445 435 410 415 Q375 435 340 415 Q300 425 285 395 Z'))
    o.append(face(480, 570, 1.25, gap=66, mouth='open'))
    o.append(sparkle(170, 240, 38)); o.append(sparkle(830, 330, 32)); o.append(sparkle(180, 650, 28))
    return ''.join(o)


@motif('ad06', 'NIKOLAUS', 'advent')
def nikolaus():
    o = []
    # Mantel
    o.append(path('M200 965 C210 830 300 765 420 755 L580 755 C700 765 790 830 800 965 Z'))
    o.append(rect(465, 860, 70, 110, 8, w=LW_THIN + 1))
    # Muetze (Spitze faellt nach rechts)
    o.append(path('M300 330 C315 170 440 92 575 105 C705 118 790 230 812 400 C780 340 735 312 690 312 L705 330 Z'))
    # Gesicht
    o.append(circle(500, 470, 195))
    # Bart mit Wolkenkante
    pts = []
    n = 9
    for i in range(n + 1):
        a = math.radians(-12 + i * (204 / n))
        pts.append((500 + 212 * math.cos(a), 505 + 340 * math.sin(a)))
    d = f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(n):
        p, q = pts[i], pts[i + 1]
        am = math.radians(-12 + (i + .5) * (204 / n))
        c = (500 + 262 * math.cos(am), 505 + 392 * math.sin(am))
        d += f' Q{f(c[0])} {f(c[1])} {f(q[0])} {f(q[1])}'
    d += f' C{f(320)} {f(540)} {f(420)} {f(575)} {f(500)} {f(575)} C{f(580)} {f(575)} {f(680)} {f(540)} {f(pts[0][0])} {f(pts[0][1])} Z'
    o.append(path(d))
    o.append(line('M470 700 Q500 722 530 700', LW_THIN))
    # Schnurrbart + Nase
    o.append(path('M500 585 C470 556 400 556 378 600 C402 632 466 634 500 606 Z', w=LW_THIN + 2))
    o.append(path('M500 585 C530 556 600 556 622 600 C598 632 534 634 500 606 Z', w=LW_THIN + 2))
    o.append(circle(500, 552, 30, w=LW_THIN + 2))
    o.append(line('M478 660 Q500 676 522 660', LW_THIN))
    # Augen + Baeckchen
    o.append(eye(420, 452, 1.2)); o.append(eye(580, 452, 1.2))
    o.append(ellipse(352, 520, 24, 13, w=5)); o.append(ellipse(648, 520, 24, 13, w=5))
    o.append(line('M385 392 Q420 372 455 390', LW_THIN)); o.append(line('M545 390 Q580 372 615 392', LW_THIN))
    # Fellrand + Bommel
    o.append(path('M280 320 Q300 290 340 296 Q375 276 410 294 Q455 276 500 292 Q545 276 590 294 Q625 276 660 296 Q700 290 720 320 '
                  'L720 365 Q705 395 665 386 Q625 405 585 386 Q545 405 500 388 Q455 405 415 386 Q375 405 335 386 Q295 395 280 365 Z'))
    o.append(circle(812, 410, 62))
    o.append(sparkle(150, 200, 36)); o.append(sparkle(880, 200, 28)); o.append(sparkle(140, 640, 26))
    return ''.join(o)


@motif('ad07', 'ZUCKERSTANGE', 'advent')
def zuckerstange():
    o = []
    W = 132                       # Roehrenbreite (weiss)
    sx, acx, acy, r = 610, 455, 340, 155
    lx = acx - r                  # linkes Ende
    d = f'M{sx} 900 L{sx} {acy} A{r} {r} 0 0 0 {lx} {acy} L{lx} 455'
    o.append(tube(d, W))
    hw = W / 2
    # schraege Streifen am Schaft (Paare = Baender)
    for y in range(860, acy + 40, -95):
        o.append(line(f'M{f(sx - hw)} {f(y + 22)} L{f(sx + hw)} {f(y - 22)}', LW_THIN + 1))
        o.append(line(f'M{f(sx - hw)} {f(y - 20)} L{f(sx + hw)} {f(y - 64)}', LW_THIN + 1))
    # Streifen im Bogen
    for ang in (22, 85, 148):
        a1, a2 = math.radians(-ang), math.radians(-ang - 26)
        for a in (a1, a2):
            x1, y1 = acx + (r - hw) * math.cos(a), acy + (r - hw) * math.sin(a)
            x2, y2 = acx + (r + hw) * math.cos(a), acy + (r + hw) * math.sin(a)
            o.append(line(f'M{f(x1)} {f(y1)} L{f(x2)} {f(y2)}', LW_THIN + 1))
    # Schleife + Stechpalme
    o.append(holly(sx + 10, 640, .85, 0))
    o.append(bow(sx, 560, 1.15))
    o.append(sparkle(200, 640, 46)); o.append(sparkle(820, 240, 36)); o.append(sparkle(250, 860, 30)); o.append(sparkle(840, 820, 26))
    return ''.join(o)


@motif('ad08', 'GLOCKE', 'advent')
def glocke():
    o = []
    o.append(circle(500, 175, 42))
    o.append(circle(500, 820, 62))
    o.append(path('M500 200 C375 200 322 305 315 430 C306 575 285 655 205 725 L795 725 C715 655 694 575 685 430 C678 305 625 200 500 200 Z'))
    o.append(line('M300 610 Q500 660 700 610', LW_THIN + 1))
    o.append(rect(180, 705, 640, 80, 40))
    o.append(face(500, 450, 1.3, gap=78, mouth='open'))
    o.append(bow(500, 200, 1.3))
    for x, y, s in [(130, 380, 40), (870, 360, 34), (150, 650, 26), (860, 640, 30)]:
        o.append(sparkle(x, y, s))
    o.append(line('M120 520 Q100 470 120 420', LW_THIN)); o.append(line('M880 520 Q900 470 880 420', LW_THIN))
    return ''.join(o)


@motif('ad09', 'KUGEL', 'advent')
def kugel():
    o = []
    cx, cy, R = 500, 565, 330
    o.append(line('M500 60 L500 190', LW_THIN))
    o.append(circle(500, 175, 40))
    o.append(circle(cx, cy, R))
    def edge(y):
        dx = math.sqrt(R * R - (y - cy) ** 2)
        return cx - dx, cx + dx
    for y, amp in ((455, 30), (690, 30)):
        x1, x2 = edge(y)
        n = 6; seg = (x2 - x1) / n
        d = f'M{f(x1)} {f(y)}'
        for i in range(n):
            xm = x1 + seg * (i + .5); xe = x1 + seg * (i + 1)
            d += f' Q{f(xm)} {f(y + (amp if i % 2 else -amp))} {f(xe)} {f(y)}'
        o.append(line(d, LW_THIN + 1))
    o.append(face(cx, 560, 1.2, gap=72, mouth='smile'))
    for x, y, s in [(400, 340, 32), (500, 300, 26), (600, 340, 32)]:
        o.append(sparkle(x, y, s, w=LW_THIN - 1))
    for x, y in [(370, 790), (500, 820), (630, 790)]:
        o.append(circle(x, y, 26, w=LW_THIN))
    o.append(rect(425, 210, 150, 70, 12))
    o.append(line('M465 220 L465 270', LW_THIN - 1)); o.append(line('M535 220 L535 270', LW_THIN - 1))
    o.append(sparkle(140, 300, 40)); o.append(sparkle(870, 330, 32)); o.append(sparkle(860, 860, 26))
    return ''.join(o)


@motif('ad10', 'GESCHENK', 'advent')
def geschenk():
    o = []
    o.append(rect(230, 500, 540, 400, 16))
    o.append(rect(605, 500, 80, 400, 0, w=LW_THIN + 1))
    o.append(rect(190, 375, 620, 135, 18))
    o.append(rect(595, 375, 100, 135, 0, w=LW_THIN + 1))
    o.append(bow(645, 360, 1.45))
    o.append(face(410, 690, 1.3, gap=72, mouth='open'))
    for x, y, s in [(140, 260, 40), (380, 240, 28), (880, 560, 32), (130, 820, 26)]:
        o.append(sparkle(x, y, s))
    return ''.join(o)


@motif('ad11', 'RENTIER', 'advent')
def rentier():
    o = []
    # Geweih
    left = ['M410 330 C390 240 340 180 270 150', 'M372 238 C320 230 270 250 235 285', 'M335 190 C330 140 345 105 370 80']
    right = ['M590 330 C610 240 660 180 730 150', 'M628 238 C680 230 730 250 765 285', 'M665 190 C670 140 655 105 630 80']
    o.append(tube(left + right, 46))
    # Hals mit Schal
    o.append(path('M390 720 L378 850 L622 850 L610 720 Z'))
    # Ohren
    o.append(leaf(270, 410, 190, 55, 25, w=LW)); o.append(leaf(730, 410, 190, 55, -25, w=LW))
    # Kopf + Schnauze
    o.append(ellipse(500, 520, 215, 230))
    o.append(ellipse(500, 670, 150, 108))
    o.append(eye(420, 480, 1.05)); o.append(eye(580, 480, 1.05))
    o.append(ellipse(345, 560, 22, 12, w=5)); o.append(ellipse(655, 560, 22, 12, w=5))
    o.append(circle(500, 625, 50))
    o.append(line('M470 712 Q500 738 530 712', LW_THIN))
    # Schal
    o.append(path('M545 840 L520 965 L620 965 L625 830 Z'))
    o.append(line('M545 935 L612 935', LW_THIN))
    o.append(path('M345 785 Q500 835 655 785 L665 855 Q500 905 335 855 Z'))
    o.append(sparkle(140, 560, 36)); o.append(sparkle(860, 560, 30)); o.append(sparkle(500, 150, 30))
    return ''.join(o)


@motif('ad12', 'SCHLITTEN', 'advent')
def schlitten():
    o = ['<g transform="translate(-80 -120) scale(1.16)">']
    # Geschenke auf dem Schlitten
    o.append(rect(270, 390, 200, 175, 12)); o.append(rect(355, 390, 34, 175, 0, w=LW_THIN))
    o.append(bow(372, 385, .7))
    o.append(rect(495, 300, 200, 265, 12)); o.append(rect(495, 410, 200, 34, 0, w=LW_THIN))
    o.append(face(595, 510, .7, gap=42, mouth='smile', blush=False))
    o.append(sparkle(595, 350, 26, w=LW_THIN - 1))
    # Kufe
    o.append(tube('M150 800 L760 800 C850 800 880 720 830 680 C800 655 760 670 770 700', 40))
    o.append(rect(300, 660, 44, 140, 6)); o.append(rect(640, 660, 44, 140, 6))
    # Sitz
    o.append(path('M190 540 L800 540 Q830 540 822 570 L790 680 Q785 695 768 695 L235 695 Q218 695 212 680 L172 570 Q165 540 190 540 Z'))
    o.append(face(500, 600, .85, gap=54, mouth='open'))
    o.append(heart(290, 615, 30)); o.append(heart(710, 615, 30))
    o.append(line('M100 880 Q300 860 500 880 Q700 900 900 870', LW_THIN))
    o.append(sparkle(150, 300, 40)); o.append(sparkle(840, 290, 34)); o.append(sparkle(860, 480, 24))
    o.append('</g>')
    return ''.join(o)

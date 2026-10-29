from kritzel import *
import math


def _holly_leaf(cx, cy, length, width, ang, w=LW):
    """Stechpalmenblatt mit Zacken; lokal entlang x, dann gedreht (ang in Grad)."""
    ts = [0, .14, .3, .5, .7, .86, 1]
    prof = lambda t: math.sin(math.pi * t) ** .8
    def side(sign, seq):
        pts = [(-length / 2 + t * length, sign * width * prof(t)) for t in seq]
        d = ''
        for (x0, y0), (x1, y1), t0, t1 in zip(pts, pts[1:], seq, seq[1:]):
            tm = (t0 + t1) / 2
            d += f' Q{f((x0 + x1) / 2)} {f(sign * width * prof(tm) * .68)} {f(x1)} {f(y1)}'
        return d
    d = f'M{f(-length / 2)} 0' + side(1, ts) + side(-1, ts[::-1]) + ' Z'
    g = f'<g transform="translate({f(cx)} {f(cy)}) rotate({f(ang)})">'
    g += path(d, w=w) + line(f'M{f(-length * .4)} 0 L{f(length * .38)} 0', LW_THIN) + '</g>'
    return g


def _cloud(cx, cy, s, w=LW_THIN):
    d = (f'M{f(cx - 50 * s)} {f(cy + 20 * s)} C{f(cx - 80 * s)} {f(cy + 20 * s)} {f(cx - 80 * s)} {f(cy - 25 * s)} {f(cx - 45 * s)} {f(cy - 22 * s)} '
         f'C{f(cx - 40 * s)} {f(cy - 55 * s)} {f(cx + 10 * s)} {f(cy - 60 * s)} {f(cx + 20 * s)} {f(cy - 30 * s)} '
         f'C{f(cx + 55 * s)} {f(cy - 45 * s)} {f(cx + 80 * s)} {f(cy - 5 * s)} {f(cx + 55 * s)} {f(cy + 20 * s)} Z')
    return path(d, w=w)


@motif('ad13', 'WICHTEL', 'advent')
def wichtel():
    o = []
    # Koerper
    o.append(path('M330 640 C320 720 300 800 290 850 L710 850 C700 800 680 720 670 640 Z'))
    o.append(rect(305, 735, 390, 50, 20))
    o.append(rect(470, 728, 60, 64, 10))
    # Stiefel
    o.append(path('M300 850 C250 850 220 880 230 905 L420 905 C430 880 420 850 400 850 Z'))
    o.append(path('M600 850 C580 850 570 880 580 905 L770 905 C780 880 750 850 700 850 Z'))
    # Arme
    o.append(path('M335 660 C270 680 240 740 250 790 C280 800 300 780 310 760 C320 730 340 710 355 700 Z'))
    o.append(path('M665 660 C730 680 760 740 750 790 C720 800 700 780 690 760 C680 730 660 710 645 700 Z'))
    o.append(circle(258, 795, 30)); o.append(circle(742, 795, 30))
    # Bart
    o.append(path('M330 520 C300 620 380 710 500 710 C620 710 700 620 670 520 C600 560 400 560 330 520 Z'))
    # Gesicht
    o.append(ellipse(500, 480, 150, 115))
    o.append(face(500, 465, .95, gap=62, mouth='none', blush=True))
    o.append(circle(500, 528, 30))
    # Muetze (Spitze nach rechts gekippt)
    o.append(path('M320 370 C330 240 400 130 520 85 C600 55 690 85 740 145 C680 135 630 155 610 205 C600 270 650 320 680 370 Z'))
    o.append(rect(300, 345, 400, 66, 33))
    o.append(circle(760, 150, 45))
    o.append(sparkle(170, 250, 34)); o.append(sparkle(860, 400, 26))
    return ''.join(o)


@motif('ad14', 'LEBKUCHENHAUS', 'advent')
def lebkuchenhaus():
    o = []
    # Schornstein
    o.append(rect(610, 170, 80, 150, 8))
    o.append(rect(595, 150, 110, 40, 14))
    # Haus
    o.append(rect(240, 430, 520, 450, 18))
    # Dach
    o.append(path('M150 470 L500 160 L850 470 C850 510 800 520 780 490 C760 520 720 520 705 490 C690 520 650 520 635 490 '
                  'C620 520 580 520 565 490 C550 520 510 520 500 490 C490 520 450 520 435 490 C420 520 380 520 365 490 '
                  'C350 520 310 520 295 490 C280 520 240 520 220 490 C200 520 150 510 150 470 Z'))
    # Tuer
    o.append(path('M420 880 L420 720 C420 650 580 650 580 720 L580 880 Z'))
    o.append(circle(555, 790, 10, fill=INK, w=0))
    # Fenster
    for x in (290, 600):
        o.append(rect(x, 560, 110, 110, 16))
        o.append(line(f'M{x + 55} 560 L{x + 55} 670 M{x} 615 L{x + 110} 615'))
    # Gesicht ueber der Tuer
    o.append(face(500, 590, .8, gap=55, mouth='smile'))
    # Bonbons auf dem Dach
    for cx, cy in ((500, 300), (410, 390), (590, 390)):
        o.append(circle(cx, cy, 30))
    o.append(heart(500, 395, 30))
    # Zuckerguss-Punkte unten
    for x in (300, 370, 640, 710):
        o.append(circle(x, 840, 16))
    o.append(sparkle(140, 220, 34)); o.append(sparkle(860, 250, 28))
    return ''.join(o)


@motif('ad15', 'SOCKE', 'advent')
def socke():
    o = []
    # Aufhaenger
    o.append(path('M590 150 C590 70 690 70 690 150', fill='none', w=LW))
    # Socke
    o.append(path('M360 230 L660 230 L660 600 C660 700 640 760 560 820 C480 880 340 900 250 860 C170 825 160 730 230 690 '
                  'C290 655 350 640 360 590 Z'))
    # Ferse + Spitze
    o.append(path('M660 650 C660 720 640 770 580 815 C560 760 590 690 660 650 Z'))
    o.append(path('M245 862 C175 830 160 735 228 692 C270 730 280 820 245 862 Z'))
    # Bund
    o.append(rect(320, 120, 380, 140, 40))
    for x in (390, 510, 630):
        o.append(circle(x, 190, 22))
    # Gesicht
    o.append(face(510, 430, 1.05, gap=65, mouth='open'))
    o.append(rounded_star(430, 640, 45, 22))
    o.append(sparkle(170, 300, 34)); o.append(sparkle(820, 460, 28))
    return ''.join(o)


@motif('ad16', 'KAKAO', 'advent')
def kakao():
    o = []
    # Dampf
    o.append(line('M400 250 C360 210 440 170 400 120', LW))
    o.append(line('M500 230 C460 190 540 150 500 100', LW))
    o.append(line('M600 250 C560 210 640 170 600 120', LW))
    # Henkel
    o.append(path('M720 450 C860 440 880 640 720 660 L720 610 C810 600 800 500 720 505 Z'))
    # Untertasse
    o.append(ellipse(500, 845, 360, 55))
    # Tasse
    o.append(path('M250 350 L750 350 L730 740 C725 810 660 840 590 840 L410 840 C340 840 275 810 270 740 Z'))
    o.append(ellipse(500, 352, 250, 48))
    # Marshmallows
    o.append(rect(330, 290, 100, 80, 20, rot=-12))
    o.append(rect(450, 270, 100, 80, 20, rot=8))
    o.append(rect(565, 295, 100, 80, 20, rot=-6))
    # Gesicht
    o.append(face(500, 560, 1.15, gap=70, mouth='smile'))
    o.append(heart(500, 730, 38))
    o.append(sparkle(160, 400, 32)); o.append(sparkle(880, 300, 26))
    return ''.join(o)


@motif('ad17', 'TEDDY', 'advent')
def teddy():
    o = []
    # Beine
    o.append(ellipse(370, 815, 105, 95)); o.append(ellipse(630, 815, 105, 95))
    # Koerper
    o.append(ellipse(500, 690, 200, 190))
    o.append(ellipse(500, 720, 110, 110))
    # Arme
    o.append(ellipse(300, 640, 70, 110, rot=30)); o.append(ellipse(700, 640, 70, 110, rot=-30))
    o.append(ellipse(355, 850, 52, 45)); o.append(ellipse(645, 850, 52, 45))
    # Ohren
    o.append(circle(320, 210, 85)); o.append(circle(680, 210, 85))
    o.append(circle(320, 210, 45)); o.append(circle(680, 210, 45))
    # Kopf
    o.append(ellipse(500, 340, 230, 200))
    o.append(ellipse(500, 420, 95, 70))
    o.append(ellipse(500, 395, 30, 20, fill=INK, w=0))
    o.append(line('M500 412 L500 440 M470 450 Q500 470 530 450'))
    o.append(eye(420, 320, 1.0)); o.append(eye(580, 320, 1.0))
    o.append(ellipse(340, 390, 22, 12, w=5)); o.append(ellipse(660, 390, 22, 12, w=5))
    # Schleife
    o.append(path('M500 545 L400 495 C380 530 380 570 400 600 Z'))
    o.append(path('M500 545 L600 495 C620 530 620 570 600 600 Z'))
    o.append(circle(500, 548, 28))
    o.append(sparkle(140, 450, 34)); o.append(sparkle(870, 470, 28))
    return ''.join(o)


@motif('ad18', 'EISENBAHN', 'advent')
def eisenbahn():
    o = []
    # Rauchwolken
    o.append(_cloud(690, 200, 1.4)); o.append(_cloud(820, 110, 1.0))
    # Schornstein
    o.append(path('M620 380 L600 270 L740 270 L720 380 Z'))
    o.append(rect(585, 245, 170, 45, 16))
    # Kessel
    o.append(rect(440, 380, 380, 250, 40))
    # Kabine
    o.append(rect(130, 260, 340, 370, 24))
    o.append(rect(110, 220, 380, 60, 24))
    o.append(rect(190, 330, 200, 150, 20))
    # Gesicht im Fenster
    o.append(face(290, 400, .8, gap=50, mouth='smile', blush=False))
    # Gesicht am Kessel (Front)
    o.append(face(640, 490, 1.0, gap=70, mouth='open'))
    # Fahrwerk
    o.append(rect(110, 620, 760, 60, 20))
    o.append(path('M870 620 L940 690 L870 690 Z'))
    for cx, r in ((240, 110), (520, 85), (730, 85)):
        o.append(circle(cx, 730, r)); o.append(circle(cx, 730, r * .35))
    o.append(line('M240 730 L730 730', LW))
    o.append(sparkle(120, 140, 32))
    return ''.join(o)


@motif('ad19', 'ENGEL', 'advent')
def engel():
    o = []
    # Fluegel
    o.append(path('M440 520 C330 400 180 380 130 450 C100 520 180 560 230 570 C170 600 170 680 250 690 C330 700 400 640 440 600 Z'))
    o.append(path('M560 520 C670 400 820 380 870 450 C900 520 820 560 770 570 C830 600 830 680 750 690 C670 700 600 640 560 600 Z'))
    o.append(line('M230 570 C300 560 360 560 420 570'))
    o.append(line('M770 570 C700 560 640 560 580 570'))
    # Kleid
    o.append(path('M420 500 L580 500 C640 650 700 760 730 850 C620 890 380 890 270 850 C300 760 360 650 420 500 Z'))
    o.append(line('M300 800 C420 840 580 840 700 800'))
    # Arme mit Stern
    o.append(path('M440 560 C420 620 440 660 480 670 L520 670 C560 660 580 620 560 560 Z'))
    o.append(rounded_star(500, 660, 55, 26))
    # Kopf
    o.append(circle(500, 360, 150))
    o.append(path('M355 330 C360 220 440 200 500 205 C560 200 640 220 645 330 C600 290 560 270 500 290 C440 270 400 290 355 330 Z'))
    o.append(face(500, 380, 1.0, gap=60, mouth='smile'))
    # Heiligenschein
    o.append(ellipse(500, 175, 130, 35))
    o.append(ellipse(500, 175, 85, 16))
    o.append(sparkle(150, 230, 32)); o.append(sparkle(850, 220, 36)); o.append(sparkle(870, 820, 26))
    return ''.join(o)


@motif('ad20', 'NUSSKNACKER', 'advent')
def nussknacker():
    o = []
    # Beine + Stiefel
    o.append(rect(395, 700, 90, 150, 10)); o.append(rect(515, 700, 90, 150, 10))
    o.append(path('M380 840 L490 840 L490 900 L340 900 C330 870 350 840 380 840 Z'))
    o.append(path('M510 840 L620 840 C650 840 670 870 660 900 L510 900 Z'))
    # Arme
    o.append(rect(300, 470, 80, 230, 36)); o.append(rect(620, 470, 80, 230, 36))
    o.append(circle(340, 715, 36)); o.append(circle(660, 715, 36))
    # Jacke
    o.append(rect(360, 450, 280, 270, 30))
    o.append(rect(360, 630, 280, 45, 10))
    o.append(rect(470, 626, 60, 53, 8))
    for y in (500, 560):
        o.append(circle(500, y, 15))
    # Kopf
    o.append(rect(370, 250, 260, 220, 40))
    o.append(eye(445, 325, .9)); o.append(eye(555, 325, .9))
    o.append(ellipse(395, 375, 20, 11, w=5)); o.append(ellipse(605, 375, 20, 11, w=5))
    # Bart, Mund, Schnurrbart
    o.append(path('M370 410 C375 480 430 520 500 520 C570 520 625 480 630 410 C580 445 420 445 370 410 Z'))
    o.append(path('M465 425 L535 425 C535 465 465 465 465 425 Z', w=LW_THIN))
    o.append(path('M500 405 C470 370 420 375 405 410 C440 418 475 415 500 405 C525 415 560 418 595 410 C580 375 530 370 500 405 Z'))
    o.append(circle(500, 375, 20))
    # Hut
    o.append(rect(395, 100, 210, 160, 16))
    o.append(rect(370, 235, 260, 40, 14))
    o.append(line('M395 150 L605 150', LW_THIN))
    o.append(path('M560 100 C560 40 620 30 640 60 C610 60 590 80 590 100 Z'))
    o.append(rounded_star(500, 190, 34, 16))
    o.append(sparkle(170, 300, 34)); o.append(sparkle(840, 330, 28))
    return ''.join(o)


@motif('ad21', 'STECHPALME', 'advent')
def stechpalme():
    o = []
    o.append(_holly_leaf(700, 280, 450, 115, -38))
    o.append(_holly_leaf(300, 660, 470, 120, 140))
    o.append(_holly_leaf(700, 660, 470, 120, 40))
    # Beeren mit Gesichtern
    for cx, cy, s in ((415, 500, 1.0), (585, 500, 1.0), (500, 395, 1.0)):
        o.append(circle(cx, cy, 95))
        o.append(face(cx, cy - 5, .62, gap=50, mouth='smile'))
    o.append(sparkle(160, 230, 36)); o.append(sparkle(320, 130, 24)); o.append(sparkle(500, 880, 30))
    return ''.join(o)


@motif('ad22', 'SCHNEEKUGEL', 'advent')
def schneekugel():
    o = []
    # Kugel
    o.append(circle(500, 420, 330))
    # Boden-Schnee
    o.append(path('M205 560 C300 520 400 560 500 545 C600 530 700 520 795 560 C770 640 700 700 600 735 L400 735 C300 700 230 640 205 560 Z'))
    # kleiner Tannenbaum links
    o.append(path('M330 560 L250 560 L330 420 L270 420 L350 290 L430 420 L370 420 L450 560 Z'))
    # Schneemann
    o.append(circle(560, 520, 95)); o.append(circle(560, 380, 70))
    o.append(face(560, 375, .55, gap=36, mouth='smile', blush=False))
    o.append(path('M505 320 L615 320 L600 250 L520 250 Z'))
    o.append(rect(490, 312, 140, 22, 10))
    # Schneeflocken
    for cx, cy, r in ((330, 230, 26), (680, 230, 30), (710, 420, 24), (430, 190, 18)):
        o.append(sparkle(cx, cy, r))
    # Glanz
    o.append(line('M260 330 C270 260 310 200 360 170', LW_THIN))
    # Sockel
    o.append(path('M270 700 L730 700 L800 880 L200 880 Z'))
    o.append(rect(170, 860, 660, 60, 24))
    o.append(face(500, 770, .85, gap=70, mouth='open'))
    return ''.join(o)


@motif('ad23', 'WUNSCHZETTEL', 'advent')
def wunschzettel():
    o = []
    # Zettel (hinten, ragt oben heraus)
    o.append(rect(260, 140, 480, 500, 20, rot=-4))
    o.append(heart(500, 270, 70))
    o.append(rounded_star(350, 380, 40, 19)); o.append(rounded_star(650, 380, 40, 19))
    # Umschlag
    o.append(rect(150, 420, 700, 440, 30))
    o.append(path('M150 450 L500 700 L850 450', fill='none', w=LW))
    o.append(line('M170 845 L420 650'))
    o.append(line('M830 845 L580 650'))
    # Siegel
    o.append(circle(500, 700, 75))
    o.append(heart(500, 705, 34))
    o.append(sparkle(140, 230, 36)); o.append(sparkle(860, 260, 30))
    return ''.join(o)


@motif('ad24', 'TANNENBAUM', 'advent')
def tannenbaum():
    o = []
    # Stamm
    o.append(rect(450, 720, 100, 110, 10))
    # Ebenen (unten -> oben)
    def tier(top, bot, half):
        n = 4
        d = f'M500 {top} L{500 + half} {bot} '
        step = 2 * half / n
        for i in range(n):
            x0 = 500 + half - i * step
            x1 = x0 - step
            d += f'Q{f((x0 + x1) / 2)} {f(bot + 40)} {f(x1)} {bot} '
        return path(d + 'Z')
    o.append(tier(440, 740, 330))
    o.append(tier(300, 560, 260))
    o.append(tier(170, 400, 190))
    # Gesicht
    o.append(face(500, 470, 1.0, gap=62, mouth='open'))
    # Kugeln
    for cx, cy in ((420, 330), (590, 345), (385, 640), (620, 650), (500, 680)):
        o.append(circle(cx, cy, 30))
    # Stern
    o.append(rounded_star(500, 150, 85, 40))
    # Geschenke
    o.append(rect(150, 760, 200, 160, 12)); o.append(rect(140, 730, 220, 50, 12))
    o.append(rect(230, 730, 40, 190, 4))
    o.append(path('M250 730 C200 670 160 690 190 725 Z')); o.append(path('M250 730 C300 670 340 690 310 725 Z'))
    o.append(rect(650, 790, 220, 130, 12)); o.append(rect(640, 765, 240, 45, 12))
    o.append(rect(740, 765, 40, 155, 4))
    o.append(path('M760 765 C710 710 680 730 705 762 Z')); o.append(path('M760 765 C810 710 840 730 815 762 Z'))
    o.append(sparkle(170, 220, 34)); o.append(sparkle(840, 250, 28))
    return ''.join(o)

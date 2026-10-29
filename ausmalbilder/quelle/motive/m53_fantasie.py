from kritzel import *
import math


# ---------- lokale Helfer ----------
def _arc_band(cx, cy, r, fill='#fff', w=LW):
    """Halbkreis (oben) als geschlossene Flaeche."""
    return path(f'M{f(cx - r)} {f(cy)} A{f(r)} {f(r)} 0 0 1 {f(cx + r)} {f(cy)} Z', fill, w)


def _cloud(cx, cy, s=1.0, w=LW):
    d = (f'M{f(cx - 120 * s)} {f(cy + 50 * s)} '
         f'C{f(cx - 175 * s)} {f(cy + 50 * s)} {f(cx - 175 * s)} {f(cy - 30 * s)} {f(cx - 115 * s)} {f(cy - 25 * s)} '
         f'C{f(cx - 110 * s)} {f(cy - 85 * s)} {f(cx - 40 * s)} {f(cy - 95 * s)} {f(cx - 10 * s)} {f(cy - 55 * s)} '
         f'C{f(cx + 20 * s)} {f(cy - 110 * s)} {f(cx + 110 * s)} {f(cy - 95 * s)} {f(cx + 110 * s)} {f(cy - 25 * s)} '
         f'C{f(cx + 175 * s)} {f(cy - 25 * s)} {f(cx + 180 * s)} {f(cy + 50 * s)} {f(cx + 120 * s)} {f(cy + 50 * s)} Z')
    return path(d, '#fff', w)


def _gem_diamond(cx, cy, s, w=LW_THIN):
    return poly([(cx, cy - s), (cx + s * .8, cy), (cx, cy + s), (cx - s * .8, cy)], w=w)


# ---------- Motive ----------
@motif('mf01', 'EINHORN', 'fantasie')
def einhorn():
    o = []
    # Hals / Brust
    o.append(path('M380 690 C360 790 330 870 300 930 L700 930 C670 870 640 790 620 690 Z'))
    # Maehne hinten (Locken links + rechts)
    for (x, y, r) in [(300, 440, 70), (275, 545, 68), (300, 650, 66), (345, 745, 60)]:
        o.append(circle(x, y, r))
    for (x, y, r) in [(700, 440, 70), (725, 545, 68), (700, 650, 66), (655, 745, 60)]:
        o.append(circle(x, y, r))
    # Ohren
    o.append(path('M330 380 L300 230 L425 320 Z'))
    o.append(path('M670 380 L700 230 L575 320 Z'))
    o.append(path('M340 350 L322 268 L395 322 Z', w=LW_THIN))
    o.append(path('M660 350 L678 268 L605 322 Z', w=LW_THIN))
    # Kopf
    o.append(ellipse(500, 500, 215, 205))
    # Horn mit Streifen (Flaechen)
    o.append(path('M440 315 L500 85 L560 315 Q500 335 440 315 Z'))
    for (y, hw) in [(250, 44), (185, 27), (130, 13)]:
        o.append(line(f'M{500 - hw - 4} {y + 8} Q500 {y - 10} {500 + hw + 4} {y - 6}', LW_THIN))
    # Stirnlocke
    o.append(path('M430 330 C420 280 480 270 500 310 C520 270 590 285 570 335 C540 360 460 360 430 330 Z'))
    # Maul
    o.append(ellipse(500, 625, 128, 80))
    o.append(ellipse(458, 612, 12, 16, fill=INK, w=0))
    o.append(ellipse(542, 612, 12, 16, fill=INK, w=0))
    o.append(line('M470 655 Q500 677 530 655', LW_THIN))
    # Augen + Baeckchen
    o.append(eye(410, 470, 1.25)); o.append(eye(590, 470, 1.25))
    o.append(ellipse(340, 540, 24, 13, w=5)); o.append(ellipse(660, 540, 24, 13, w=5))
    # Glitzer
    o.append(sparkle(150, 230, 40)); o.append(sparkle(850, 210, 32)); o.append(rounded_star(860, 820, 48, 22))
    o.append(heart(140, 820, 36))
    return ''.join(o)


@motif('mf02', 'DRACHE', 'fantasie')
def drache():
    o = []
    # Schwanz (hinten rechts) mit Spitze
    o.append(path('M650 800 C780 820 870 760 860 650 C855 610 830 600 820 620 C840 700 770 750 640 730 Z'))
    o.append(path('M820 625 L800 545 L880 590 Z'))
    # Fluegel
    o.append(path('M330 520 C230 430 120 420 80 470 C130 480 140 520 120 560 C170 545 190 580 175 620 C230 600 270 620 300 650 Z'))
    o.append(path('M670 520 C770 430 880 420 920 470 C870 480 860 520 880 560 C830 545 810 580 825 620 C770 600 730 620 700 650 Z'))
    # Koerper
    o.append(ellipse(500, 700, 210, 200))
    # Bauch mit Streifen
    o.append(ellipse(500, 730, 130, 145))
    for y in (650, 715, 780, 840):
        hw = math.sqrt(max(0, 1 - ((y - 730) / 145) ** 2)) * 130
        o.append(line(f'M{f(500 - hw + 6)} {y} Q500 {y + 14} {f(500 + hw - 6)} {y}', LW_THIN))
    # Fuesse
    o.append(ellipse(390, 885, 85, 50)); o.append(ellipse(610, 885, 85, 50))
    for x in (350, 390, 430):
        o.append(line(f'M{x} 905 L{x} 925', LW_THIN))
    for x in (570, 610, 650):
        o.append(line(f'M{x} 905 L{x} 925', LW_THIN))
    # Arme
    o.append(ellipse(330, 690, 45, 70, rot=25)); o.append(ellipse(670, 690, 45, 70, rot=-25))
    # Stacheln auf dem Kopf
    o.append(path('M455 200 L480 130 L505 195 Z')); o.append(path('M500 195 L530 120 L555 200 Z'))
    # Hoerner
    o.append(path('M370 260 C340 200 340 160 360 130 C385 180 410 210 420 240 Z'))
    o.append(path('M630 260 C660 200 660 160 640 130 C615 180 590 210 580 240 Z'))
    # Kopf
    o.append(ellipse(500, 370, 200, 175))
    # Schnauze
    o.append(ellipse(500, 450, 110, 65))
    o.append(ellipse(465, 440, 10, 14, fill=INK, w=0)); o.append(ellipse(535, 440, 10, 14, fill=INK, w=0))
    o.append(line('M470 475 Q500 495 530 475', LW_THIN))
    o.append(eye(420, 345, 1.2)); o.append(eye(580, 345, 1.2))
    o.append(ellipse(345, 410, 24, 13, w=5)); o.append(ellipse(655, 410, 24, 13, w=5))
    o.append(sparkle(130, 250, 36)); o.append(sparkle(880, 260, 30)); o.append(sparkle(120, 820, 30))
    return ''.join(o)


@motif('mf03', 'BURG', 'fantasie')
def burg():
    o = []
    # Fahnen
    for x in (250, 750):
        o.append(line(f'M{x} 150 L{x} 70', LW_THIN))
        o.append(path(f'M{x} 72 L{x + 80} 95 L{x} 120 Z', w=LW_THIN))
    # Seitentuerme
    for x in (250,):
        o.append(rect(165, 300, 170, 600))
        o.append(path('M150 305 L250 150 L350 305 Z'))
        o.append(rect(215, 400, 70, 95, 35, w=LW_THIN))
    for x in (750,):
        o.append(rect(665, 300, 170, 600))
        o.append(path('M650 305 L750 150 L850 305 Z'))
        o.append(rect(715, 400, 70, 95, 35, w=LW_THIN))
    # Hauptgebaeude mit Zinnen
    zin = 'M300 420 '
    xs = [300, 360, 420, 480, 540, 600, 660, 700]
    d = 'M300 900 L300 360 '
    x = 300
    for i in range(6):
        d += f'L{x} 300 L{x + 50} 300 L{x + 50} 360 L{x + 67} 360 '
        x += 67
    d += 'L700 360 L700 900 Z'
    o.append(path('M300 900 L300 360 L330 360 L330 300 L385 300 L385 360 L420 360 L420 300 L475 300 L475 360 '
                  'L525 360 L525 300 L580 300 L580 360 L615 360 L615 300 L670 300 L670 360 L700 360 L700 900 Z'))
    # Tor
    o.append(path('M410 900 L410 730 C410 650 590 650 590 730 L590 900 Z'))
    o.append(line('M500 665 L500 900', LW_THIN))
    o.append(circle(470, 800, 9, fill=INK, w=0)); o.append(circle(530, 800, 9, fill=INK, w=0))
    # Gesicht oben am Hauptbau
    o.append(face(500, 470, 1.15, gap=80, mouth='smile'))
    # Steine
    o.append(rect(330, 580, 60, 35, 6, w=LW_THIN)); o.append(rect(610, 600, 60, 35, 6, w=LW_THIN))
    o.append(rect(200, 600, 60, 35, 6, w=LW_THIN)); o.append(rect(740, 640, 60, 35, 6, w=LW_THIN))
    # Boden
    o.append(line('M80 900 L920 900', LW))
    o.append(sparkle(100, 200, 36)); o.append(sparkle(900, 220, 30)); o.append(rounded_star(500, 160, 50, 24))
    return ''.join(o)


@motif('mf04', 'KRONE', 'fantasie')
def krone():
    o = []
    # Kronenkoerper mit 5 Zacken
    o.append(path('M170 720 L120 330 L300 500 L400 260 L500 450 L600 260 L700 500 L880 330 L830 720 Z'))
    # Kugeln auf den Spitzen
    for (x, y) in [(120, 310), (400, 235), (600, 235), (880, 310)]:
        o.append(circle(x, y, 34))
    o.append(rounded_star(500, 175, 70, 34))
    o.append(line('M500 245 L500 270', LW_THIN))
    # Band unten
    o.append(rect(150, 700, 700, 120, 30))
    # Edelsteine im Band
    o.append(circle(270, 760, 32, w=LW_THIN))
    o.append(_gem_diamond(500, 760, 42))
    o.append(circle(730, 760, 32, w=LW_THIN))
    o.append(ellipse(385, 760, 26, 18, w=LW_THIN)); o.append(ellipse(615, 760, 26, 18, w=LW_THIN))
    # Herzen-Edelsteine an den Zacken
    o.append(heart(230, 520, 34)); o.append(heart(770, 520, 34))
    # Gesicht
    o.append(face(500, 560, 1.3, gap=85, mouth='open'))
    o.append(sparkle(110, 140, 40)); o.append(sparkle(890, 150, 34)); o.append(sparkle(500, 900, 30))
    return ''.join(o)


@motif('mf05', 'ZAUBERHUT', 'fantasie')
def zauberhut():
    o = []
    # Zauberstab (hinten)
    o.append(path('M690 760 L870 360 L905 375 L725 775 Z'))
    o.append(rounded_star(888, 320, 75, 34))
    o.append(rect(696, 690, 52, 40, 8, w=LW_THIN, rot=24))
    # Hut-Kegel mit geknickter Spitze
    o.append(path('M240 780 C320 600 400 420 470 230 C490 170 540 120 610 110 C650 105 680 130 660 160 '
                  'C620 160 590 190 580 240 C600 420 660 610 740 780 Z'))
    # Krempe
    o.append(ellipse(490, 790, 380, 85))
    o.append(path('M150 790 C250 830 730 830 830 790 C760 845 220 845 150 790 Z', w=LW_THIN))
    # Hutband mit Schnalle
    o.append(path('M255 745 C400 785 590 785 725 745 L705 690 C580 725 400 725 278 690 Z'))
    o.append(rect(450, 692, 80, 70, 10, w=LW_THIN))
    o.append(rect(472, 712, 36, 30, 6, w=LW_THIN))
    # Sterne + Mond auf dem Hut
    o.append(rounded_star(430, 420, 44, 20, w=LW_THIN))
    o.append(rounded_star(560, 330, 32, 15, w=LW_THIN))
    o.append(path('M590 470 C540 470 520 530 560 560 C530 510 560 480 600 488 Z', w=LW_THIN))
    # Gesicht
    o.append(face(490, 600, 1.1, gap=75, mouth='smile'))
    o.append(sparkle(140, 300, 40)); o.append(sparkle(820, 200, 28)); o.append(sparkle(140, 610, 28)); o.append(sparkle(850, 640, 26))
    return ''.join(o)


@motif('mf06', 'FEE', 'fantasie')
def fee():
    o = []
    # Fluegel (hinten)
    o.append(ellipse(330, 470, 150, 95, rot=-30)); o.append(ellipse(670, 470, 150, 95, rot=30))
    o.append(ellipse(360, 640, 110, 65, rot=25)); o.append(ellipse(640, 640, 110, 65, rot=-25))
    # Beine
    o.append(rect(445, 800, 40, 90, 18)); o.append(rect(515, 800, 40, 90, 18))
    o.append(ellipse(455, 895, 48, 26)); o.append(ellipse(545, 895, 48, 26))
    # Kleid
    o.append(path('M440 500 L560 500 L680 820 C600 850 400 850 320 820 Z'))
    o.append(path('M320 820 C360 790 400 840 440 805 C470 840 530 840 560 805 C600 840 640 790 680 820 C600 850 400 850 320 820 Z', w=LW_THIN))
    o.append(rounded_star(500, 640, 38, 18, w=LW_THIN))
    # Arme
    o.append(path('M450 520 C400 560 360 600 330 610 C315 615 315 640 335 640 C370 630 420 590 465 560 Z'))
    o.append(path('M550 520 C600 540 650 520 690 470 C700 455 720 465 712 482 C680 540 620 575 545 565 Z'))
    # Zauberstab
    o.append(line('M705 470 L760 330', LW_THIN))
    o.append(rounded_star(765, 300, 48, 22))
    # Haare hinten
    o.append(ellipse(500, 350, 175, 165))
    # Dutt
    o.append(circle(500, 165, 55))
    # Kopf
    o.append(circle(500, 360, 135))
    # Pony
    o.append(path('M365 345 C370 250 440 215 500 220 C560 215 630 250 635 345 C600 300 560 290 530 305 C510 285 470 280 450 300 C420 290 390 310 365 345 Z'))
    o.append(face(500, 375, 1.0, gap=60, mouth='smile'))
    o.append(sparkle(120, 220, 36)); o.append(sparkle(880, 760, 32)); o.append(sparkle(140, 780, 28)); o.append(sparkle(870, 160, 26))
    return ''.join(o)


@motif('mf07', 'RITTER', 'fantasie')
def ritter():
    o = []
    # Beine + Stiefel
    o.append(rect(420, 760, 65, 120, 16)); o.append(rect(515, 760, 65, 120, 16))
    o.append(ellipse(440, 890, 62, 30)); o.append(ellipse(560, 890, 62, 30))
    # Koerper / Waffenrock
    o.append(path('M370 560 C370 520 400 500 440 500 L560 500 C600 500 630 520 630 560 L650 790 L350 790 Z'))
    o.append(rect(355, 690, 290, 40, 10, w=LW_THIN))
    o.append(rect(480, 692, 40, 36, 6, w=LW_THIN))
    # Arm rechts
    o.append(path('M625 540 C690 560 720 610 715 680 C715 700 690 705 685 685 C680 630 660 600 610 590 Z'))
    o.append(circle(700, 700, 30))
    # Federbusch
    o.append(path('M500 130 C470 60 560 40 600 70 C580 75 575 95 590 110 C560 110 540 125 535 150 Z'))
    # Helm
    o.append(path('M320 360 C320 220 400 150 500 150 C600 150 680 220 680 360 L680 480 C680 510 660 525 630 525 L370 525 C340 525 320 510 320 480 Z'))
    # Visier offen (Gesichtsfeld)
    o.append(path('M380 330 L620 330 C640 330 650 345 650 365 L650 470 C650 490 635 500 615 500 L385 500 C365 500 350 490 350 470 L350 365 C350 345 360 330 380 330 Z'))
    o.append(line('M500 160 L500 325', LW_THIN))
    o.append(face(500, 405, 1.05, gap=65, mouth='smile'))
    # Schild links
    o.append(path('M170 520 L420 520 L420 690 C420 790 330 850 295 870 C260 850 170 790 170 690 Z'))
    o.append(path('M200 550 L390 550 L390 690 C390 770 325 815 295 832 C265 815 200 770 200 690 Z', w=LW_THIN))
    o.append(line('M295 552 L295 830', LW_THIN)); o.append(line('M202 660 L388 660', LW_THIN))
    o.append(heart(248, 610, 26)); o.append(rounded_star(345, 745, 30, 14, w=LW_THIN))
    o.append(sparkle(140, 200, 36)); o.append(sparkle(860, 220, 32)); o.append(sparkle(860, 820, 28))
    return ''.join(o)


@motif('mf08', 'MEERJUNGFRAU', 'fantasie')
def meerjungfrau():
    o = []
    # Haare hinten (lang, wellig)
    o.append(path('M330 300 C300 420 300 560 260 640 C320 650 360 600 380 560 L620 560 C640 600 680 650 740 640 C700 560 700 420 670 300 C640 170 360 170 330 300 Z'))
    # Schwanzflosse
    o.append(path('M680 770 C760 660 880 640 940 690 C890 740 870 790 890 850 C810 850 740 830 690 820 Z'))
    o.append(path('M680 800 C740 870 800 920 900 935 C830 970 730 950 660 880 Z'))
    # Schwanz
    o.append(path('M390 600 L610 600 C640 700 620 780 700 800 C700 840 680 870 640 870 C520 870 400 830 380 720 C375 680 380 640 390 600 Z'))
    # Schuppen-Boegen (Flaechen)
    for (x, y) in [(445, 650), (520, 650), (595, 655), (445, 725), (520, 725), (595, 740)]:
        o.append(line(f'M{x - 35} {y} Q{x} {y + 45} {x + 35} {y}', LW_THIN))
    # Oberkoerper
    o.append(path('M405 470 C405 440 430 420 460 420 L540 420 C570 420 595 440 595 470 L610 610 L390 610 Z'))
    # Muschel-Oberteil
    for x in (450, 550):
        o.append(path(f'M{x - 45} 510 C{x - 45} 460 {x + 45} 460 {x + 45} 510 Z', w=LW_THIN))
        o.append(line(f'M{x} 470 L{x} 508', 5))
    # Arme
    o.append(path('M410 470 C360 520 345 580 360 620 C370 640 395 630 392 610 C385 570 400 530 440 500 Z'))
    o.append(path('M590 470 C640 520 655 580 640 620 C630 640 605 630 608 610 C615 570 600 530 560 500 Z'))
    # Kopf
    o.append(circle(500, 330, 130))
    # Pony
    o.append(path('M372 320 C375 230 440 195 500 198 C560 195 625 230 628 320 C600 280 560 270 520 285 C490 265 445 270 420 290 C400 290 385 300 372 320 Z'))
    # Seestern im Haar
    o.append(rounded_star(615, 225, 48, 22))
    o.append(face(500, 350, 1.0, gap=58, mouth='smile'))
    # Blasen
    o.append(circle(170, 300, 34)); o.append(circle(210, 220, 22)); o.append(circle(820, 380, 30)); o.append(circle(160, 820, 28))
    o.append(sparkle(860, 200, 30))
    return ''.join(o)


@motif('mf09', 'SCHATZKISTE', 'fantasie')
def schatzkiste():
    o = []
    # Deckel (offen, hinten)
    o.append(path('M220 470 L230 280 C240 180 760 180 770 280 L780 470 Z'))
    o.append(path('M245 450 L255 295 C265 215 735 215 745 295 L755 450 Z', w=LW_THIN))
    o.append(line('M400 205 L395 455', LW_THIN)); o.append(line('M600 205 L605 455', LW_THIN))
    # Schatz (Muenzen/Edelsteine) ueber dem Rand
    o.append(path('M220 520 C260 440 330 410 400 430 C450 380 560 380 600 430 C680 410 750 450 780 520 Z'))
    for (x, y, r) in [(330, 470, 40), (430, 445, 40), (560, 448, 40), (670, 470, 40)]:
        o.append(circle(x, y, r))
        o.append(circle(x, y, r * .55, w=LW_THIN))
    o.append(_gem_diamond(500, 410, 45, w=LW))
    o.append(rounded_star(770, 395, 38, 18, w=LW_THIN))
    # Kiste
    o.append(rect(200, 510, 600, 360, 30))
    # Baender
    o.append(rect(310, 510, 70, 360, 0, w=LW_THIN)); o.append(rect(620, 510, 70, 360, 0, w=LW_THIN))
    # Schloss
    o.append(rect(455, 560, 90, 100, 18))
    o.append(circle(500, 600, 14, fill=INK, w=0)); o.append(path('M492 605 L508 605 L512 640 L488 640 Z', fill=INK, w=0))
    # Gesicht
    o.append(face(500, 740, 1.15, gap=90, mouth='open'))
    o.append(sparkle(140, 220, 40)); o.append(sparkle(870, 210, 32)); o.append(sparkle(110, 760, 30)); o.append(sparkle(890, 760, 30))
    return ''.join(o)


@motif('mf10', 'REGENBOGEN', 'fantasie')
def regenbogen():
    o = []
    cx, cy = 500, 690
    for r in (430, 370, 310, 250):
        o.append(_arc_band(cx, cy, r))
    o.append(_arc_band(cx, cy, 190))
    # Sonne oben
    o.append(sparkle(500, 150, 40)); o.append(sparkle(170, 230, 32)); o.append(sparkle(830, 230, 32))
    # Wolken mit Gesichtern
    o.append(_cloud(205, 720, 1.25))
    o.append(face(205, 715, .85, gap=55, mouth='smile'))
    o.append(_cloud(795, 720, 1.25))
    o.append(face(795, 715, .85, gap=55, mouth='smile'))
    # Gesicht im Bogen-Inneren
    o.append(face(500, 600, 1.0, gap=55, mouth='open', blush=False))
    o.append(heart(500, 800, 34))
    return ''.join(o)

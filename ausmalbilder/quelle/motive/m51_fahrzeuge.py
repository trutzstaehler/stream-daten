from kritzel import *


def wheel(cx, cy, r):
    return circle(cx, cy, r) + circle(cx, cy, r * .45, w=LW_THIN) + circle(cx, cy, r * .14, w=LW_THIN)


def ground(y=880, x0=90, x1=910):
    return line(f'M{x0} {y} L{x1} {y}', LW_THIN)


@motif('fz01', 'AUTO', 'fahrzeuge')
def auto():
    o = [ground(860)]
    # Dach / Kabine
    o.append(path('M290 520 L350 360 Q365 325 405 325 L610 325 Q645 325 665 355 L760 520 Z'))
    # Fenster
    o.append(path('M335 505 L385 375 Q392 360 410 360 L495 360 L495 505 Z', w=LW_THIN))
    o.append(path('M530 505 L530 360 L605 360 Q625 360 637 378 L715 505 Z', w=LW_THIN))
    # Karosserie
    o.append(path('M120 700 L120 590 Q120 520 200 515 L800 515 Q880 520 885 600 L885 700 Q885 740 845 740 L160 740 Q120 740 120 700 Z'))
    # Lichter
    o.append(ellipse(850, 590, 24, 34, w=LW_THIN))
    o.append(rect(122, 575, 34, 55, 12, w=LW_THIN))
    # Stossstangen
    o.append(rect(840, 680, 70, 34, 14, w=LW_THIN))
    o.append(rect(95, 680, 70, 34, 14, w=LW_THIN))
    # Tuer-Linie + Griff
    o.append(line('M512 520 L512 735', LW_THIN))
    o.append(rect(545, 560, 60, 18, 9, w=5))
    o.append(face(340, 610, 1.15, gap=62, mouth='open'))
    # Raeder
    o.append(wheel(275, 750, 105))
    o.append(wheel(725, 750, 105))
    o.append(sparkle(150, 300, 34)); o.append(sparkle(860, 280, 28)); o.append(sparkle(740, 200, 20))
    return ''.join(o)


@motif('fz02', 'FEUERWEHR', 'fahrzeuge')
def feuerwehr():
    o = [ground(865)]
    # Leiter (auf dem Dach)
    o.append(path('M300 330 L820 260 L828 300 L308 370 Z'))
    for i in range(1, 9):
        x = 300 + i * 58
        y = 330 - i * 7.8
        o.append(line(f'M{x} {y} L{x + 5} {y + 38}', LW_THIN))
    # Aufbau hinten
    o.append(rect(380, 395, 500, 345, 26))
    # Rolllaeden
    o.append(rect(420, 440, 190, 170, 16, w=LW_THIN))
    o.append(rect(640, 440, 200, 170, 16, w=LW_THIN))
    for y in (480, 520, 560):
        o.append(line(f'M430 {y} L600 {y}', 5)); o.append(line(f'M650 {y} L830 {y}', 5))
    # Kabine
    o.append(path('M110 740 L110 470 Q110 420 160 410 L300 395 Q350 392 380 420 L400 440 L400 740 Z'))
    # Fenster
    o.append(path('M150 560 L150 470 Q150 448 175 445 L300 432 Q335 430 345 455 L355 560 Z', w=LW_THIN))
    # Blaulicht
    o.append(rect(170, 360, 110, 40, 16))
    o.append(path('M190 360 Q190 315 225 315 Q260 315 260 360 Z'))
    # Streifen
    o.append(rect(110, 640, 770, 40, 0, w=LW_THIN))
    o.append(face(255, 505, .85, gap=48, mouth='smile', blush=False))
    o.append(ellipse(122, 600, 18, 26, w=LW_THIN))
    o.append(wheel(250, 752, 98))
    o.append(wheel(720, 752, 98))
    o.append(sparkle(120, 260, 30)); o.append(sparkle(900, 180, 26)); o.append(sparkle(100, 340, 18))
    return ''.join(o)


@motif('fz03', 'BAGGER', 'fahrzeuge')
def bagger():
    o = [ground(870)]
    # Ausleger
    o.append(path('M440 575 L655 290 Q670 268 697 278 L718 288 Q740 303 724 325 L495 600 Z'))
    # Stiel
    o.append(path('M690 300 L738 282 L870 565 L822 585 Z'))
    o.append(circle(708, 296, 30, w=LW_THIN))
    # Schaufel
    o.append(path('M790 560 L905 545 Q930 543 930 570 L920 645 Q912 690 868 692 L792 692 Q758 692 764 660 Z'))
    o.append(line('M790 600 L915 590', LW_THIN))
    # Kette
    o.append(rect(130, 700, 560, 140, 70))
    o.append(rect(170, 730, 480, 80, 40, w=LW_THIN))
    for x in (210, 300, 390, 480, 570):
        o.append(circle(x + 15, 770, 26, w=LW_THIN))
    # Oberwagen
    o.append(rect(150, 560, 520, 140, 24))
    # Kabine
    o.append(path('M190 560 L190 330 Q190 300 220 300 L420 300 Q450 300 455 330 L480 560 Z'))
    o.append(path('M230 470 L230 345 L410 345 L430 470 Z', w=LW_THIN))
    o.append(face(330, 405, .95, gap=52, mouth='open'))
    # Warnleuchte
    o.append(rect(290, 265, 70, 36, 12))
    o.append(sparkle(110, 240, 30)); o.append(sparkle(560, 180, 24)); o.append(sparkle(900, 420, 24))
    return ''.join(o)


@motif('fz04', 'TRAKTOR', 'fahrzeuge')
def traktor():
    o = [ground(870)]
    # Auspuff
    o.append(rect(560, 300, 34, 160, 14))
    o.append(path('M550 300 Q577 255 605 300 Z', w=LW_THIN))
    # Motorhaube
    o.append(path('M480 470 L820 470 Q860 470 860 510 L860 650 L480 650 Z'))
    for y in (520, 560, 600):
        o.append(line(f'M800 {y} L845 {y}', 5))
    # Kabine
    o.append(path('M200 650 L200 290 Q200 260 230 260 L470 260 Q500 260 500 290 L500 650 Z'))
    o.append(path('M240 470 L240 305 L460 305 L460 470 Z', w=LW_THIN))
    o.append(rect(170, 235, 360, 40, 18))
    o.append(face(350, 390, 1.0, gap=55, mouth='smile'))
    # Raeder
    o.append(circle(330, 700, 170)); o.append(circle(330, 700, 95, w=LW_THIN)); o.append(circle(330, 700, 32, w=LW_THIN))
    o.append(wheel(760, 760, 95))
    o.append(sparkle(110, 220, 30)); o.append(sparkle(880, 300, 28)); o.append(sparkle(700, 190, 20))
    return ''.join(o)


@motif('fz05', 'BUS', 'fahrzeuge')
def bus():
    o = [ground(860)]
    o.append(path('M110 740 L110 310 Q110 250 170 250 L820 250 Q890 250 890 320 L890 740 Z'))
    # Fenster
    for x in (150, 330, 510):
        o.append(rect(x, 300, 150, 140, 18, w=LW_THIN))
    o.append(path('M690 300 L800 300 Q845 300 845 345 L845 470 L690 470 Z', w=LW_THIN))
    # Tuer
    o.append(rect(150, 490, 120, 230, 12, w=LW_THIN))
    o.append(line('M210 495 L210 715', 5))
    # Streifen
    o.append(rect(290, 520, 600, 50, 0, w=LW_THIN))
    o.append(ellipse(860, 650, 20, 28, w=LW_THIN))
    o.append(rect(860, 700, 50, 32, 12, w=LW_THIN))
    o.append(face(560, 400 + 240, .95, gap=60, mouth='open'))
    o.append(wheel(320, 745, 95))
    o.append(wheel(720, 745, 95))
    # Schild
    o.append(rect(380, 195, 240, 56, 16))
    o.append(sparkle(120, 170, 30)); o.append(sparkle(870, 170, 26))
    return ''.join(o)


@motif('fz06', 'FLUGZEUG', 'fahrzeuge')
def flugzeug():
    o = []
    # hinterer Fluegel
    o.append(path('M560 470 L640 260 Q650 240 672 245 L700 252 Q718 258 712 280 L660 470 Z'))
    # Leitwerk
    o.append(path('M170 470 L120 290 Q115 270 135 268 L175 268 Q195 268 205 290 L300 460 Z'))
    # Rumpf
    o.append(path('M150 470 Q150 410 230 410 L770 410 Q900 410 920 500 Q900 590 770 590 L230 590 Q150 590 150 530 Z'))
    # Fenster
    for x in (330, 420, 510):
        o.append(circle(x, 470, 30, w=LW_THIN))
    o.append(path('M800 440 Q860 445 885 490 L800 490 Z', w=LW_THIN))
    # vorderer Fluegel
    o.append(path('M420 560 L560 780 Q572 800 595 795 L625 788 Q645 782 638 760 L560 560 Z'))
    # Hoehenleitwerk
    o.append(path('M170 530 L95 610 Q85 625 102 630 L140 632 Q160 632 172 615 L240 545 Z'))
    o.append(face(680, 520, .75, gap=48, mouth='smile'))
    # Wolken
    for cx, cy, s in [(240, 760, 1.0), (800, 230, .8)]:
        o.append(path(f'M{cx - 90 * s} {cy} Q{cx - 90 * s} {cy - 45 * s} {cx - 45 * s} {cy - 45 * s} Q{cx - 30 * s} {cy - 95 * s} {cx + 15 * s} {cy - 80 * s} '
                      f'Q{cx + 60 * s} {cy - 95 * s} {cx + 70 * s} {cy - 45 * s} Q{cx + 110 * s} {cy - 40 * s} {cx + 105 * s} {cy} Z', w=LW_THIN))
    o.append(sparkle(110, 160, 28)); o.append(sparkle(900, 700, 30)); o.append(sparkle(470, 190, 22))
    return ''.join(o)


@motif('fz07', 'HUBSCHRAUBER', 'fahrzeuge')
def hubschrauber():
    o = []
    # Rotor
    o.append(rect(170, 205, 620, 36, 18))
    o.append(rect(455, 235, 50, 70, 10))
    # Heck
    o.append(path('M600 470 L860 430 L870 490 L620 560 Z'))
    o.append(path('M840 420 L880 330 Q890 310 910 318 L925 325 Q938 335 930 352 L895 450 Z'))
    o.append(circle(895, 470, 38, w=LW_THIN))
    # Kabine
    o.append(path('M480 300 Q700 300 700 500 Q700 650 520 650 L320 650 Q200 650 200 520 Q200 300 480 300 Z'))
    o.append(path('M250 500 Q255 345 470 345 L470 500 Z', w=LW_THIN))
    o.append(face(560, 500, 1.0, gap=55, mouth='open'))
    # Kufen
    o.append(rect(330, 650, 30, 90, 10, w=LW_THIN)); o.append(rect(560, 650, 30, 90, 10, w=LW_THIN))
    o.append(path('M220 740 L700 740 Q745 740 745 760 Q745 780 700 780 L220 780 Q190 780 190 760 Q190 740 220 740 Z'))
    o.append(sparkle(120, 400, 30)); o.append(sparkle(860, 650, 28)); o.append(sparkle(140, 760, 22))
    return ''.join(o)


@motif('fz08', 'POLIZEI', 'fahrzeuge')
def polizei():
    o = [ground(860)]
    # Blaulicht
    o.append(rect(440, 255, 130, 50, 18))
    o.append(path('M465 255 Q465 210 505 210 Q545 210 545 255 Z'))
    # Kabine
    o.append(path('M290 520 L345 340 Q358 305 395 305 L615 305 Q650 305 668 338 L760 520 Z'))
    o.append(path('M335 505 L382 360 Q390 340 410 340 L495 340 L495 505 Z', w=LW_THIN))
    o.append(path('M530 505 L530 340 L605 340 Q625 340 637 360 L715 505 Z', w=LW_THIN))
    # Karosserie
    o.append(path('M120 700 L120 590 Q120 520 200 515 L800 515 Q880 520 885 600 L885 700 Q885 740 845 740 L160 740 Q120 740 120 700 Z'))
    # Streifen
    o.append(rect(122, 610, 760, 50, 0, w=LW_THIN))
    o.append(ellipse(850, 575, 22, 30, w=LW_THIN))
    o.append(rect(840, 685, 70, 34, 14, w=LW_THIN))
    o.append(rect(95, 685, 70, 34, 14, w=LW_THIN))
    o.append(face(512, 560, .8, gap=52, mouth='smile'))
    o.append(wheel(275, 750, 105))
    o.append(wheel(725, 750, 105))
    for x, y, r in [(260, 230, 30), (760, 230, 30)]:
        o.append(sparkle(x, y, r))
    return ''.join(o)


@motif('fz09', 'MÜLLAUTO', 'fahrzeuge')
def muellauto():
    o = [ground(865)]
    # Behaelter
    o.append(path('M380 300 L760 300 Q840 300 870 380 L910 560 Q925 640 870 680 L870 740 L380 740 Z'))
    o.append(path('M760 330 Q820 340 845 420 L870 560 Q878 620 840 640 L760 640 Z', w=LW_THIN))
    for x in (480, 580, 680):
        o.append(line(f'M{x} 330 L{x} 600', LW_THIN))
    o.append(rect(380, 600, 380, 40, 0, w=LW_THIN))
    # Recycling-Pfeile als Kreis
    o.append(circle(810, 520, 44, w=LW_THIN))
    o.append(heart(810, 522, 20, w=5))
    # Kabine
    o.append(path('M110 740 L110 470 Q110 420 160 410 L300 395 Q350 392 380 420 L400 440 L400 740 Z'))
    o.append(path('M150 570 L150 470 Q150 448 175 445 L300 432 Q335 430 345 455 L355 570 Z', w=LW_THIN))
    o.append(face(250, 515, .8, gap=45, mouth='open', blush=False))
    o.append(ellipse(122, 625, 18, 26, w=LW_THIN))
    o.append(rect(170, 360, 90, 36, 14))
    o.append(wheel(250, 752, 98))
    o.append(wheel(720, 752, 98))
    o.append(sparkle(120, 260, 30)); o.append(sparkle(620, 200, 26)); o.append(sparkle(900, 220, 22))
    return ''.join(o)


@motif('fz10', 'FAHRRAD', 'fahrzeuge')
def fahrrad():
    o = [ground(860)]
    # Raeder
    for cx in (250, 750):
        o.append(circle(cx, 690, 165)); o.append(circle(cx, 690, 125, w=LW_THIN)); o.append(circle(cx, 690, 26, w=LW_THIN))
    # Rahmen (als Rohre mit Flaeche)
    o.append(path('M250 690 L420 450 L455 465 L292 700 Z'))
    o.append(path('M420 450 L700 450 L700 490 L440 490 Z'))
    o.append(path('M440 490 L520 690 L480 705 L405 505 Z'))
    o.append(path('M250 690 L500 690 L500 725 L250 725 Z'))
    o.append(path('M680 460 L750 690 L712 702 L645 470 Z'))
    # Sattel
    o.append(path('M360 410 Q360 380 410 380 L490 380 Q520 380 520 405 Q520 425 490 428 L390 432 Q360 432 360 410 Z'))
    o.append(rect(420, 425, 28, 40, 6, w=LW_THIN))
    # Lenker
    o.append(rect(655, 360, 30, 110, 10, w=LW_THIN))
    o.append(path('M640 340 L760 340 Q790 340 790 365 Q790 385 760 385 L640 385 Z'))
    # Korb
    o.append(path('M670 180 L920 180 Q935 180 932 196 L905 380 Q902 395 886 395 L705 395 Q690 395 687 380 L660 196 Q657 180 670 180 Z'))
    o.append(rect(650, 165, 290, 40, 18))
    o.append(face(796, 285, .85, gap=48, mouth='open'))
    o.append(circle(505, 690, 34, w=LW_THIN))
    o.append(sparkle(120, 300, 30)); o.append(sparkle(500, 230, 26)); o.append(sparkle(930, 500, 22))
    return ''.join(o)

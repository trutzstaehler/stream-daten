from kritzel import *


@motif('test_kuerbis', 'KÜRBIS', 'test')
def kuerbis():
    o = []
    # Stiel + Blatt (hinten)
    o.append(path('M480 250 C470 200 470 160 500 120 L548 136 C528 170 524 210 530 252 Z'))
    o.append(path('M545 200 C600 140 690 150 720 190 C670 200 620 230 585 260 C570 240 556 222 545 200 Z'))
    o.append(line('M560 215 C610 190 650 185 690 190'))
    o.append(line('M520 165 C560 120 610 110 650 120 C660 135 650 150 630 150', LW_THIN))
    # Segmente: aussen nach innen
    # aeussere Segmente
    o.append(path('M330 300 C140 300 90 500 130 630 C175 770 330 800 430 770 L430 310 C400 302 365 300 330 300 Z'))
    o.append(path('M670 300 C860 300 910 500 870 630 C825 770 670 800 570 770 L570 310 C600 302 635 300 670 300 Z'))
    # mittlere Segmente
    o.append(path('M390 300 C280 310 240 420 240 540 C240 680 310 780 420 780 L580 780 C690 780 760 680 760 540 C760 420 720 310 610 300 C560 292 440 292 390 300 Z'))
    o.append(line('M400 305 C330 380 320 690 410 778', LW_THIN))
    o.append(line('M600 305 C670 380 680 690 590 778', LW_THIN))
    o.append(face(500, 540, 1.25, gap=72, mouth='open'))
    return ''.join(o)


@motif('test_gespenst', 'GESPENST', 'test')
def gespenst():
    o = []
    d = ('M500 140 C330 140 250 280 250 450 L250 760 C250 800 290 820 320 790 C350 760 380 760 405 795 '
         'C430 830 470 830 500 795 C530 760 570 760 595 795 C620 830 660 830 690 795 C720 760 750 770 750 760 L750 450 C750 280 670 140 500 140 Z')
    o.append(path(d))
    # Aermchen
    o.append(path('M255 470 C200 470 160 520 175 560 C190 590 230 570 255 545 Z'))
    o.append(path('M745 470 C800 450 845 490 835 530 C825 565 780 560 745 540 Z'))
    o.append(face(500, 420, 1.3, gap=70, mouth='o'))
    o.append(sparkle(170, 250, 36)); o.append(sparkle(830, 230, 26)); o.append(sparkle(860, 690, 30))
    return ''.join(o)


@motif('test_laterne', 'LATERNE', 'test')
def laterne():
    o = []
    # Stab + Draht
    o.append(path('M120 120 L880 120 L880 160 L120 160 Z', w=LW))
    o.append(line('M500 160 L500 210', LW))
    o.append(line('M330 330 Q500 180 670 330', LW_THIN))
    # Kugel-Laterne
    o.append(rect(380, 280, 240, 60, 14))
    o.append(path('M380 340 C230 380 200 520 220 600 C245 710 360 770 500 770 C640 770 755 710 780 600 C800 520 770 380 620 340 Z'))
    o.append(line('M300 400 C320 520 320 640 330 730', LW_THIN))
    o.append(line('M700 400 C680 520 680 640 670 730', LW_THIN))
    o.append(rect(380, 770, 240, 60, 14))
    o.append(face(500, 520, 1.25, gap=75, mouth='smile'))
    o.append(rounded_star(170, 330, 50, 24)); o.append(sparkle(850, 330, 34)); o.append(sparkle(160, 720, 26))
    return ''.join(o)

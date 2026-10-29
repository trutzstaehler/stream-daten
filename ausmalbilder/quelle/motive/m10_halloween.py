from kritzel import *


def mirror(s):
    return f'<g transform="translate(1000 0) scale(-1 1)">{s}</g>'


def tube(d, w=46):
    """Dicker Strang mit Umriss (fuellbar), z. B. Beine, Arme."""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w - 2 * LW_THIN - 4}"/>')


@motif('hw01', 'KÜRBIS', 'halloween')
def kuerbis():
    o = []
    o.append(line('M560 225 C600 170 650 150 700 160 C730 168 735 200 705 205 C690 207 680 195 690 185', LW_THIN))
    o.append(path('M478 270 C468 215 470 170 500 125 L552 142 C530 180 525 225 532 272 Z'))
    o.append(path('M548 230 C600 170 690 175 725 215 C680 225 630 250 595 285 C578 265 562 250 548 230 Z'))
    o.append(path('M330 300 C140 300 90 500 130 630 C175 770 330 800 430 770 L430 310 C400 302 365 300 330 300 Z'))
    o.append(path('M670 300 C860 300 910 500 870 630 C825 770 670 800 570 770 L570 310 C600 302 635 300 670 300 Z'))
    o.append(path('M390 300 C280 310 240 420 240 540 C240 680 310 780 420 780 L580 780 C690 780 760 680 760 540 C760 420 720 310 610 300 C560 292 440 292 390 300 Z'))
    o.append(line('M400 305 C330 380 320 690 410 778', LW_THIN))
    o.append(line('M600 305 C670 380 680 690 590 778', LW_THIN))
    o.append(face(500, 530, 1.25, gap=72, mouth='open'))
    o.append(sparkle(150, 220, 34)); o.append(sparkle(870, 860, 28))
    return ''.join(o)


@motif('hw02', 'GESPENST', 'halloween')
def gespenst():
    o = []
    d = ('M500 130 C330 130 245 270 245 450 L245 770 C245 815 290 830 322 800 C352 770 382 770 407 805 '
         'C432 840 470 840 500 805 C530 770 570 770 595 805 C620 840 660 840 690 805 C718 772 755 790 755 760 L755 450 C755 270 670 130 500 130 Z')
    o.append(path('M255 480 C195 470 150 520 168 565 C185 600 228 580 255 552 Z'))
    o.append(path('M745 480 C805 455 852 495 840 540 C828 578 780 572 745 548 Z'))
    o.append(path(d))
    o.append(face(500, 420, 1.3, gap=72, mouth='o'))
    o.append(sparkle(150, 250, 38)); o.append(sparkle(850, 220, 28)); o.append(sparkle(880, 700, 32))
    o.append(rounded_star(140, 760, 46, 22))
    return ''.join(o)


@motif('hw03', 'FLEDERMAUS', 'halloween')
def fledermaus():
    o = []
    wing = ('M420 430 C320 330 190 290 70 340 C115 380 120 425 105 470 C160 445 210 470 215 525 '
            'C260 495 315 510 330 565 C360 535 395 545 415 580 Z')
    o.append(path(wing)); o.append(mirror(path(wing)))
    o.append(line('M380 430 C300 400 220 395 160 410', LW_THIN))
    o.append(mirror(line('M380 430 C300 400 220 395 160 410', LW_THIN)))
    ear = 'M385 410 L365 235 C365 220 380 215 390 225 L470 330 Z'
    o.append(path(ear)); o.append(mirror(path(ear)))
    o.append(ellipse(450, 675, 38, 30)); o.append(ellipse(550, 675, 38, 30))
    o.append(ellipse(500, 500, 165, 170))
    o.append(ellipse(500, 590, 80, 55, w=LW_THIN))
    o.append(face(500, 470, 1.1, gap=60, mouth='smile'))
    o.append(sparkle(170, 200, 34)); o.append(sparkle(830, 190, 26)); o.append(rounded_star(820, 780, 48, 22))
    o.append(sparkle(180, 760, 28))
    return ''.join(o)


@motif('hw04', 'KATZE', 'halloween')
def katze():
    o = []
    o.append(path('M640 845 C790 860 880 770 860 660 C850 600 800 585 780 630 C800 700 780 785 640 795 Z'))
    o.append(path('M375 540 C295 630 285 790 325 870 L675 870 C715 790 705 630 625 540 Z'))
    o.append(line('M450 700 C440 780 450 830 460 868', LW_THIN)); o.append(line('M550 700 C560 780 550 830 540 868', LW_THIN))
    o.append(ellipse(420, 875, 62, 36)); o.append(ellipse(580, 875, 62, 36))
    o.append(path('M370 560 Q500 610 630 560 L632 600 Q500 652 368 600 Z'))
    ear = 'M300 320 L285 150 C285 130 305 122 320 133 L430 225 Z'
    o.append(path(ear)); o.append(mirror(path(ear)))
    o.append(ellipse(500, 390, 225, 190))
    o.append(line('M320 290 L313 195 L385 250', LW_THIN)); o.append(mirror(line('M320 290 L313 195 L385 250', LW_THIN)))
    o.append(circle(500, 640, 30))
    o.append(line('M478 640 L522 640', LW_THIN))
    o.append(face(500, 390, 1.15, gap=78, mouth='cat'))
    for y0, y1 in ((440, 420), (468, 478)):
        o.append(line(f'M330 {y0} L220 {y1}', LW_THIN)); o.append(mirror(line(f'M330 {y0} L220 {y1}', LW_THIN)))
    o.append(sparkle(150, 180, 32)); o.append(sparkle(860, 200, 26))
    return ''.join(o)


@motif('hw05', 'SPINNE', 'halloween')
def spinne():
    o = []
    o.append(line('M500 60 L500 300', LW_THIN))
    legs = ['M390 410 Q240 300 160 400', 'M350 470 Q190 440 120 560', 'M355 545 Q210 600 180 730', 'M400 610 Q300 720 320 850']
    for d in legs:
        o.append(tube(d)); o.append(mirror(tube(d)))
    o.append(circle(500, 500, 195))
    o.append(face(500, 480, 1.25, gap=72, mouth='open'))
    o.append(sparkle(200, 170, 32)); o.append(sparkle(800, 170, 32)); o.append(rounded_star(830, 880, 44, 20))
    return ''.join(o)


@motif('hw06', 'HEXENHUT', 'halloween')
def hexenhut():
    o = []
    o.append(ellipse(500, 765, 410, 95))
    o.append(path('M265 745 C335 600 365 400 425 265 C455 195 525 125 610 112 C655 106 672 142 640 162 '
                  'C590 192 575 262 585 322 C605 482 680 622 735 745 Q500 800 265 745 Z'))
    o.append(path('M295 655 Q500 700 705 655 L738 745 Q500 800 262 745 Z'))
    o.append(rect(450, 668, 100, 92, 18))
    o.append(rect(477, 693, 46, 42, 8, w=LW_THIN))
    o.append(face(505, 480, 0.95, gap=58, mouth='smile'))
    o.append(rounded_star(170, 330, 55, 26)); o.append(sparkle(830, 330, 36)); o.append(sparkle(150, 580, 26))
    o.append(sparkle(860, 560, 24))
    return ''.join(o)


@motif('hw07', 'HEXENKESSEL', 'halloween')
def hexenkessel():
    o = []
    o.append(rect(640, 130, 44, 330, 22, rot=22))
    o.append(circle(390, 370, 52)); o.append(circle(520, 320, 66)); o.append(circle(640, 385, 40))
    o.append(circle(455, 215, 30)); o.append(circle(590, 225, 24))
    o.append(rect(290, 800, 80, 80, 26)); o.append(rect(630, 800, 80, 80, 26))
    o.append(path('M235 470 C150 600 195 800 330 855 L670 855 C805 800 850 600 765 470 Z'))
    o.append(rect(185, 410, 630, 85, 42))
    o.append(face(500, 640, 1.2, gap=78, mouth='open'))
    o.append(sparkle(150, 230, 32)); o.append(sparkle(860, 250, 28))
    return ''.join(o)


@motif('hw08', 'BONBONS', 'halloween')
def bonbons():
    o = []
    # Lolli (hinten)
    o.append(rect(285, 260, 40, 300, 20, rot=-35))
    o.append(circle(225, 225, 118))
    o.append(line('M225 225 C250 215 255 245 228 255 C195 262 185 220 205 200 C235 172 280 195 282 235 '
                  'C285 285 225 310 190 290 C150 268 140 210 170 175', LW_THIN))
    # grosses Bonbon
    wr = 'M290 470 L120 360 Q85 500 120 640 L290 530 Z'
    o.append(path(wr)); o.append(mirror(path(wr)))
    o.append(line('M150 405 L255 485', LW_THIN)); o.append(line('M150 595 L255 515', LW_THIN))
    o.append(mirror(line('M150 405 L255 485', LW_THIN))); o.append(mirror(line('M150 595 L255 515', LW_THIN)))
    o.append(ellipse(500, 500, 230, 170))
    o.append(face(500, 480, 1.15, gap=70, mouth='open'))
    # kleines Bonbon
    sw = 'M690 805 L610 755 Q595 805 610 855 L690 830 Z'
    o.append(path(sw)); o.append(path('M830 805 L910 755 Q925 805 910 855 L830 830 Z'))
    o.append(ellipse(760, 815, 85, 62))
    o.append(line('M720 760 C700 800 710 840 735 872', LW_THIN)); o.append(line('M790 758 C770 800 780 840 805 870', LW_THIN))
    o.append(sparkle(820, 190, 36)); o.append(sparkle(170, 820, 30))
    return ''.join(o)


@motif('hw09', 'MONSTER', 'halloween')
def monster():
    o = []
    horn = 'M310 290 C270 200 280 140 315 95 C340 150 380 190 430 215 Z'
    o.append(path(horn)); o.append(mirror(path(horn)))
    o.append(ellipse(200, 560, 70, 45, rot=-35)); o.append(ellipse(800, 560, 70, 45, rot=35))
    o.append(ellipse(400, 840, 75, 45)); o.append(ellipse(600, 840, 75, 45))
    pts = []
    xs = [790 - i * (580 / 10) for i in range(11)]
    zz = ' '.join(f'L{f(x)} {800 if i % 2 else 760}' for i, x in enumerate(xs))
    d = f'M500 170 C690 170 790 310 790 500 {zz} L210 500 C210 310 310 170 500 170 Z'
    o.append(path(d))
    o.append(circle(500, 400, 112))
    o.append(eye(500, 410, 2.4))
    o.append(path('M375 560 Q500 690 625 560 Q500 590 375 560 Z', w=LW_THIN))
    o.append(rect(445, 568, 42, 40, 8, w=LW_THIN)); o.append(rect(515, 568, 42, 40, 8, w=LW_THIN))
    o.append(ellipse(330, 560, 22, 12, w=5)); o.append(ellipse(670, 560, 22, 12, w=5))
    o.append(circle(300, 680, 34, w=LW_THIN)); o.append(circle(690, 690, 28, w=LW_THIN)); o.append(circle(640, 250, 26, w=LW_THIN))
    o.append(sparkle(130, 200, 32)); o.append(sparkle(880, 230, 28))
    return ''.join(o)


@motif('hw10', 'SPUKHAUS', 'halloween')
def spukhaus():
    o = []
    o.append(rect(625, 170, 85, 200, 10))
    o.append(rect(608, 150, 119, 42, 14))
    o.append(rect(240, 460, 520, 420, 18))
    o.append(path('M170 470 L500 170 L830 470 Q842 505 800 505 L200 505 Q158 505 170 470 Z'))
    o.append(circle(500, 375, 52)); o.append(line('M500 323 L500 427 M448 375 L552 375', LW_THIN))
    # Fenster mit Augen
    for x in (295, 595):
        o.append(path(f'M{x} 690 L{x} 600 C{x} 535 {x + 110} 535 {x + 110} 600 L{x + 110} 690 Z'))
        o.append(eye(x + 55, 625, 1.45))
    o.append(ellipse(368, 728, 28, 14, w=5)); o.append(ellipse(632, 728, 28, 14, w=5))
    o.append(line('M468 720 Q500 748 532 720', LW_THIN))
    o.append(path('M425 880 L425 810 C425 755 575 755 575 810 L575 880 Z'))
    o.append(circle(550, 835, 10, fill=INK, w=0))
    # kleiner Kuerbis vor dem Haus
    o.append(rect(860, 745, 20, 38, 8, w=LW_THIN))
    o.append(ellipse(838, 835, 44, 50)); o.append(ellipse(902, 835, 44, 50)); o.append(ellipse(870, 835, 42, 52))
    o.append(rounded_star(150, 240, 52, 25)); o.append(sparkle(860, 160, 34)); o.append(sparkle(870, 600, 28))
    o.append(sparkle(130, 650, 30))
    return ''.join(o)

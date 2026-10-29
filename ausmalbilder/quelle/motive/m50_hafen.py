import math
from kritzel import *


def waves(y, x0=80, x1=920, n=6, amp=26, w=LW_THIN):
    """Wellenlinie (offen) als Wasser-Andeutung."""
    step = (x1 - x0) / n
    d = f'M{f(x0)} {f(y)}'
    for i in range(n):
        xa = x0 + i * step
        d += f' Q{f(xa + step / 4)} {f(y - amp)} {f(xa + step / 2)} {f(y)} T{f(xa + step)} {f(y)}'
    return line(d, w)


def water(y, x0=60, x1=940, n=7, amp=22, bottom=None):
    """Geschlossene Wasserflaeche mit gewellter Oberkante."""
    step = (x1 - x0) / n
    d = f'M{f(x0)} {f(y)}'
    for i in range(n):
        xa = x0 + i * step
        d += f' Q{f(xa + step / 4)} {f(y - amp)} {f(xa + step / 2)} {f(y)} T{f(xa + step)} {f(y)}'
    b = bottom if bottom is not None else y + 70
    d += f' L{f(x1)} {f(b)} Q{f((x0 + x1) / 2)} {f(b + 18)} {f(x0)} {f(b)} Z'
    return path(d)


# ------------------------------------------------------------------ hf01
@motif('hf01', 'SCHIFF', 'hafen')
def schiff():
    o = []
    # Container (hinten)
    cont = [(250, 360, 130, 95), (380, 360, 130, 95), (510, 360, 130, 95),
            (250, 265, 130, 95), (380, 265, 130, 95), (315, 170, 130, 95)]
    for x, y, w_, h in cont:
        o.append(rect(x, y, w_, h, 6))
        for k in range(1, 4):
            xx = x + w_ * k / 4
            o.append(line(f'M{f(xx)} {f(y + 18)} L{f(xx)} {f(y + h - 18)}', LW_THIN))
    # Bruecke / Aufbau
    o.append(rect(670, 230, 150, 225, 10))
    o.append(rect(650, 205, 190, 40, 10))
    o.append(rect(700, 270, 40, 40, 6, w=LW_THIN)); o.append(rect(760, 270, 40, 40, 6, w=LW_THIN))
    o.append(rect(735, 120, 40, 90, 6))
    o.append(rect(722, 105, 66, 26, 8))
    # Rumpf
    o.append(path('M120 455 L900 455 L850 640 Q500 670 175 640 Z'))
    o.append(path('M150 545 L875 545 L850 640 Q500 670 175 640 Z'))
    o.append(face(500, 505, 1.05, gap=72, mouth='smile'))
    # Bullaugen
    o.append(circle(250, 500, 22, w=LW_THIN)); o.append(circle(760, 500, 22, w=LW_THIN))
    # Wasser
    o.append(water(690, 60, 940, 7, 22, 800))
    o.append(waves(760, 160, 840, 5, 16))
    o.append(sparkle(140, 220, 34)); o.append(sparkle(880, 300, 26))
    return ''.join(o)


# ------------------------------------------------------------------ hf02
@motif('hf02', 'LEUCHTTURM', 'hafen')
def leuchtturm():
    o = []
    o.append(path('M430 185 L110 100 L110 290 Z'))
    o.append(path('M570 185 L890 100 L890 290 Z'))
    top_y, bot_y = 300, 790
    tl, tr, bl, br = 385, 615, 320, 680

    def xl(y): return tl + (bl - tl) * (y - top_y) / (bot_y - top_y)

    def xr(y): return tr + (br - tr) * (y - top_y) / (bot_y - top_y)
    o.append(path(f'M{tl} {top_y} L{tr} {top_y} L{br} {bot_y} L{bl} {bot_y} Z'))
    for ya, yb in ((450, 530), (630, 700)):
        o.append(path(f'M{f(xl(ya))} {ya} L{f(xr(ya))} {ya} L{f(xr(yb))} {yb} L{f(xl(yb))} {yb} Z', w=LW_THIN))
    o.append(path('M465 790 L465 745 Q500 710 535 745 L535 790 Z', w=LW_THIN))
    o.append(face(500, 370, 1.0, gap=62, mouth='smile'))
    o.append(rect(350, 270, 300, 36, 12))
    o.append(rect(420, 150, 160, 122, 14))
    o.append(line('M473 155 L473 268', LW_THIN)); o.append(line('M527 155 L527 268', LW_THIN))
    o.append(path('M400 155 L500 72 L600 155 Z'))
    o.append(circle(500, 60, 18))
    o.append(path('M220 790 Q280 750 360 772 L640 772 Q720 750 780 790 L800 835 L200 835 Z'))
    o.append(water(835, 70, 930, 6, 20, 915))
    o.append(sparkle(170, 460, 30)); o.append(sparkle(840, 470, 34)); o.append(sparkle(830, 650, 24)); o.append(sparkle(170, 650, 24))
    return ''.join(o)


# ------------------------------------------------------------------ hf03
@motif('hf03', 'MÖWE', 'hafen')
def moewe():
    o = []
    # Poller
    o.append(rect(380, 690, 240, 60, 20))
    o.append(path('M405 750 L595 750 L585 900 L415 900 Z'))
    o.append(rect(360, 885, 280, 40, 16))
    # Schwanz
    o.append(path('M650 560 L870 520 L840 590 L880 640 L650 640 Z'))
    # Koerper
    o.append(path('M330 520 C330 380 450 330 560 360 C700 400 720 520 680 620 C640 700 420 710 360 650 C330 620 330 580 330 520 Z'))
    # Fluegel
    o.append(path('M520 470 C620 440 720 480 760 560 C700 600 600 610 540 580 C500 560 495 500 520 470 Z'))
    o.append(line('M600 520 Q660 530 700 560', LW_THIN))
    o.append(line('M580 555 Q630 575 680 585', LW_THIN))
    # Kopf
    o.append(circle(400, 330, 130))
    # Schnabel (gelb mit Punkt)
    o.append(path('M270 330 L170 360 L270 390 Q290 360 270 330 Z'))
    o.append(line('M195 360 L268 360', LW_THIN))
    o.append(circle(250, 372, 9, w=LW_THIN))
    o.append(eye(360, 300, 1.0)); o.append(eye(450, 300, 1.0))
    o.append(ellipse(330, 345, 18, 9, w=5)); o.append(ellipse(480, 345, 18, 9, w=5))
    # Fuesse
    o.append(path('M440 690 L420 700 L470 700 Z', w=LW_THIN))
    o.append(path('M450 680 L430 694 L405 694 L420 680 Z', w=LW_THIN))
    o.append(path('M540 680 L520 694 L495 694 L510 680 Z', w=LW_THIN))
    o.append(sparkle(140, 170, 30)); o.append(sparkle(820, 230, 34))
    return ''.join(o)


# ------------------------------------------------------------------ hf04
@motif('hf04', 'ANKER', 'hafen')
def anker():
    o = []
    # Tau: haengt vom Ring in einem Bogen nach rechts (hinter dem Anker)
    o.append(path('M545 150 C760 120 860 260 790 360 C740 430 650 420 640 380 '
                  'L672 360 C690 385 735 380 760 340 C810 270 740 175 560 190 Z'))
    o.append(line('M640 158 Q648 175 640 192', LW_THIN)); o.append(line('M730 175 Q725 195 708 205', LW_THIN))
    o.append(line('M790 255 Q772 265 755 262', LW_THIN)); o.append(line('M770 345 Q755 340 742 330', LW_THIN))
    # Ring
    o.append(circle(500, 165, 72)); o.append(circle(500, 165, 32))
    # Bogen mit Spitzen
    o.append(path('M150 545 L270 500 L262 590 Q300 750 500 775 Q700 750 738 590 L730 500 L850 545 L790 585 '
                  'Q770 830 500 860 Q230 830 210 585 Z'))
    # Querbalken
    o.append(rect(320, 265, 360, 62, 31))
    # Schaft
    o.append(rect(435, 225, 130, 580, 60))
    o.append(circle(500, 805, 52))
    o.append(eye(470, 470, .85)); o.append(eye(530, 470, .85))
    o.append(line('M482 512 Q500 528 518 512', LW_THIN))
    o.append(ellipse(452, 505, 14, 7, w=5)); o.append(ellipse(548, 505, 14, 7, w=5))
    o.append(sparkle(200, 200, 34)); o.append(sparkle(180, 380, 26)); o.append(sparkle(860, 760, 28)); o.append(sparkle(140, 760, 26))
    return ''.join(o)


# ------------------------------------------------------------------ hf05
@motif('hf05', 'KRAN', 'hafen')
def kran():
    o = []
    # Beine (Portal)
    o.append(path('M250 880 L310 470 L370 470 L330 880 Z'))
    o.append(path('M670 880 L630 470 L690 470 L750 880 Z'))
    o.append(rect(220, 870, 140, 40, 14)); o.append(rect(640, 870, 140, 40, 14))
    o.append(rect(300, 640, 400, 40, 10))
    # Haus
    o.append(rect(280, 330, 440, 160, 18))
    o.append(rect(520, 360, 150, 90, 10, w=LW_THIN))
    o.append(face(380, 395, .85, gap=55, mouth='smile'))
    # Ausleger
    o.append(path('M240 300 L900 180 L900 225 L240 345 Z'))
    o.append(line('M300 330 L340 300 L380 318 L420 284 L460 302 L500 268 L540 286 L580 252 L620 270 L660 236 L700 254 L740 220 L780 238 L820 205 L860 222', LW_THIN))
    o.append(path('M120 270 L250 300 L250 345 L120 330 Z'))
    o.append(rect(90, 300, 90, 90, 10))
    # Seil + Haken
    o.append(line('M820 220 L820 450', LW_THIN))
    o.append(line('M760 470 L820 450 L880 470', LW_THIN))
    # Container
    o.append(rect(700, 470, 240, 140, 8))
    for k in range(1, 5):
        xx = 700 + 240 * k / 5
        o.append(line(f'M{f(xx)} 490 L{f(xx)} 590', LW_THIN))
    o.append(sparkle(560, 110, 30)); o.append(sparkle(140, 520, 28)); o.append(sparkle(860, 760, 32))
    return ''.join(o)


# ------------------------------------------------------------------ hf06
@motif('hf06', 'FÄHRE', 'hafen')
def faehre():
    o = []
    # Schornstein
    o.append(rect(600, 170, 80, 120, 10))
    o.append(rect(590, 150, 100, 36, 10))
    o.append(circle(680, 110, 34)); o.append(circle(740, 80, 26))
    # Oberdeck
    o.append(rect(270, 270, 470, 130, 24))
    for i in range(4):
        o.append(rect(300 + i * 110, 300, 80, 66, 14, w=LW_THIN))
    # Unterdeck
    o.append(rect(170, 390, 680, 150, 26))
    for i in range(5):
        o.append(rect(200 + i * 120, 420, 90, 70, 16, w=LW_THIN))
    # Rumpf
    o.append(path('M110 530 L900 530 L850 680 Q500 710 160 680 Z'))
    o.append(path('M140 600 L880 600 L850 680 Q500 710 160 680 Z'))
    o.append(face(500, 560, .95, gap=70, mouth='smile', blush=False))
    o.append(ellipse(380, 590, 20, 10, w=5)); o.append(ellipse(620, 590, 20, 10, w=5))
    # Rettungsring
    o.append(circle(240, 465, 30, w=LW_THIN)); o.append(circle(240, 465, 13, w=LW_THIN))
    # Wasser
    o.append(water(735, 60, 940, 7, 22, 840))
    o.append(waves(800, 160, 840, 5, 14))
    o.append(sparkle(150, 220, 30)); o.append(sparkle(880, 300, 32))
    return ''.join(o)


# ------------------------------------------------------------------ hf07
@motif('hf07', 'FISCHBRÖTCHEN', 'hafen')
def fischbroetchen():
    o = []
    # Unteres Broetchen
    o.append(path('M130 560 L870 560 Q880 700 740 740 L260 740 Q120 700 130 560 Z'))
    # Salat (Wellenblatt)
    d = 'M120 540'
    for i in range(8):
        x = 120 + i * 95
        d += f' Q{x + 47} 610 {x + 95} 540'
    d += ' L880 585 L120 585 Z'
    o.append(path(d))
    # Fisch
    o.append(path('M170 470 C260 380 620 380 720 470 C620 560 260 560 170 470 Z'))
    o.append(path('M700 470 L860 390 L830 470 L860 550 Z'))
    o.append(line('M560 420 Q590 470 560 520', LW_THIN))
    o.append(eye(270, 455, .8))
    o.append(line('M215 495 Q235 505 255 497', LW_THIN * .8))
    # Zwiebelringe
    o.append(ellipse(390, 418, 50, 22, w=LW_THIN)); o.append(ellipse(390, 418, 28, 11, w=LW_THIN))
    o.append(ellipse(510, 412, 48, 21, w=LW_THIN)); o.append(ellipse(510, 412, 26, 10, w=LW_THIN))
    # Oberes Broetchen
    o.append(path('M140 380 Q150 170 500 160 Q850 170 860 380 Q830 410 780 400 L220 400 Q170 410 140 380 Z'))
    for x, y in ((330, 230), (430, 205), (560, 210), (660, 240), (480, 270)):
        o.append(ellipse(x, y, 14, 7, w=5, rot=-20))
    o.append(face(500, 320, .95, gap=75, mouth='open'))
    o.append(sparkle(120, 140, 32)); o.append(sparkle(880, 150, 28)); o.append(sparkle(880, 820, 30))
    return ''.join(o)


# ------------------------------------------------------------------ hf08
@motif('hf08', 'RETTUNGSRING', 'hafen')
def rettungsring():
    o = []
    cx, cy, R, r = 500, 500, 330, 170
    # Seil aussen (Schlaufen)
    o.append(circle(cx, cy, R + 20, fill='none', w=LW_THIN))
    o.append(circle(cx, cy, R))
    o.append(circle(cx, cy, r))
    # Segmente: 4 Baender
    for a in (45, 135, 225, 315):
        o.append(f'<g transform="rotate({a} {cx} {cy})">' +
                 path(f'M{cx - 52} {cy - R + 2} L{cx + 52} {cy - R + 2} L{cx + 34} {cy - r - 2} L{cx - 34} {cy - r - 2} Z', w=LW_THIN) + '</g>')
    # Seilbefestigungen
    for a in (0, 90, 180, 270):
        x = cx + (R + 20) * math.cos(math.radians(a)); y = cy + (R + 20) * math.sin(math.radians(a))
        o.append(f'<g transform="rotate({a} {f(x)} {f(y)})">' + rect(x - 14, y - 26, 28, 52, 10, w=LW_THIN) + '</g>')
    # Gesicht im Loch-Rand oben
    o.append(face(cx, cy - 25, 1.1, gap=62, mouth='smile'))
    o.append(sparkle(140, 140, 34)); o.append(sparkle(870, 150, 28)); o.append(sparkle(860, 870, 32)); o.append(sparkle(140, 860, 26))
    return ''.join(o)


# ------------------------------------------------------------------ hf09
@motif('hf09', 'KAPITÄN', 'hafen')
def kapitaen():
    o = []
    # Oberkoerper (Jacke)
    o.append(path('M190 900 Q200 690 380 650 L620 650 Q800 690 810 900 Z'))
    o.append(path('M440 650 L500 760 L560 650 Z', w=LW_THIN))
    o.append(path('M500 760 L500 900', fill='none', w=LW_THIN))
    for y in (790, 850):
        o.append(circle(470, y, 13, w=LW_THIN)); o.append(circle(530, y, 13, w=LW_THIN))
    o.append(rect(240, 720, 90, 26, 8, w=LW_THIN, rot=-18)); o.append(rect(670, 720, 90, 26, 8, w=LW_THIN, rot=18))
    # Kopf
    o.append(ellipse(330, 460, 36, 50)); o.append(ellipse(670, 460, 36, 50))
    o.append(circle(500, 450, 175))
    # Bart (Wolkenkante) unten
    d = 'M335 470 Q340 650 500 680 Q660 650 665 470 Q640 560 600 545 Q560 600 500 590 Q440 600 400 545 Q360 560 335 470 Z'
    o.append(path(d))
    o.append(path('M420 520 Q460 495 500 515 Q540 495 580 520 Q545 545 500 532 Q455 545 420 520 Z', w=LW_THIN))
    o.append(eye(440, 430, 1.0)); o.append(eye(560, 430, 1.0))
    o.append(ellipse(380, 480, 18, 9, w=5)); o.append(ellipse(620, 480, 18, 9, w=5))
    o.append(circle(500, 488, 22, w=LW_THIN))
    # Muetze
    o.append(path('M290 320 Q300 170 500 160 Q700 170 710 320 Z'))
    o.append(rect(300, 300, 400, 60, 22))
    o.append(path('M330 360 Q500 400 670 360 L690 385 Q500 430 310 385 Z'))
    o.append(path('M500 215 L520 255 L563 258 L530 285 L540 325 L500 302 L460 325 L470 285 L437 258 L480 255 Z', w=LW_THIN))
    o.append(sparkle(140, 220, 32)); o.append(sparkle(860, 230, 28))
    return ''.join(o)


# ------------------------------------------------------------------ hf10
@motif('hf10', 'MICHEL', 'hafen')
def michel():
    o = []
    # Kirchenschiff unten
    o.append(rect(170, 690, 660, 200, 10))
    o.append(path('M150 700 L500 600 L850 700 Z'))
    for x in (220, 330, 610, 720):
        o.append(path(f'M{x} 860 L{x} 760 Q{x + 30} 725 {x + 60} 760 L{x + 60} 860 Z', w=LW_THIN))
    # Turm unten
    o.append(rect(395, 400, 210, 490, 8))
    o.append(path('M450 890 L450 800 Q500 750 550 800 L550 890 Z', w=LW_THIN))
    # Uhr mit Gesicht
    o.append(circle(500, 520, 82))
    o.append(eye(470, 505, .7)); o.append(eye(530, 505, .7))
    o.append(line('M480 548 Q500 562 520 548', LW_THIN * .8))
    o.append(line('M500 452 L500 470', LW_THIN)); o.append(line('M500 572 L500 590', LW_THIN))
    o.append(line('M432 520 L450 520', LW_THIN)); o.append(line('M550 520 L568 520', LW_THIN))
    # Turmstufen
    o.append(rect(410, 330, 180, 80, 8))
    o.append(rect(380, 315, 240, 30, 8))
    o.append(rect(430, 250, 140, 70, 8))
    o.append(line('M470 260 L470 310', LW_THIN)); o.append(line('M530 260 L530 310', LW_THIN))
    # Kupferhaube (gruen)
    o.append(path('M420 252 Q430 180 500 160 Q570 180 580 252 Z'))
    o.append(path('M465 165 Q470 120 500 105 Q530 120 535 165 Z'))
    o.append(rect(488, 50, 24, 60, 6))
    o.append(path('M500 20 L512 50 L488 50 Z', w=LW_THIN))
    o.append(sparkle(200, 300, 34)); o.append(sparkle(810, 320, 30)); o.append(sparkle(120, 560, 24)); o.append(sparkle(880, 540, 26))
    return ''.join(o)

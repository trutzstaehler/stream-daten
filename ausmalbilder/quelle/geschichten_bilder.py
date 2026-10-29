"""Illustrationen fuer die Gute-Nacht-Geschichten (bunt, ohne Schriftzug, auf ruhigem Abendhimmel).

python3 geschichten_bilder.py -> /kreativhafen/geschichten/bilder/<slug>.webp (800x600)
Quelle sind die Linienbilder der Motive, gefärbt passend zum Text (FARBEN); der Name unter dem Motiv wird abgeschnitten.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geschichten import ALLE
import ausgemalt as AM

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(HERE, '..', '02-bilder', 'motive')
OUT = os.path.join(REPO, 'kreativhafen', 'geschichten', 'bilder')
W, H = 800, 600

# Abendhimmel je Thema (oben, unten) – ruhig, damit die bunte Figur leuchtet
HIMMEL = {
    'Hafen': ('#1f3b5c', '#3f6f8f'), 'Weltraum': ('#15183a', '#38306b'), 'Fantasie': ('#2b2350', '#6a4c86'),
    'Fahrzeuge': ('#243a52', '#7a6a8f'), 'Jahreszeiten': ('#2a2440', '#8a5a5a'), 'Mut': ('#1f2a44', '#4b5d82'),
    'Familie': ('#2a3050', '#7a6080'), 'Gefühle': ('#2c2a4f', '#6f5f95'), 'Tiere': ('#1e3a4a', '#4f7f7a'),
    'Freundschaft': ('#283456', '#6a7aa0'), 'Einschlafen': ('#1a2140', '#45507a'),
}


# Farben passend zum Text der Geschichte („Mats hat weiße Federn, graue Flügel“ …)
# gross: Farbe der grössten Fläche(n) · pal: übrige Flächen · klein: Flächen unter 2500 px (Knöpfe, Wangen, Schnabel …)
# fest: {(y, x): Farbe} – die Fläche an diesem Punkt der Vorlage (1000x1100) bekommt genau diese Farbe
WEISS, GRAU, HGRAU = '#f7f6f2', '#b9c1c8', '#dde2e6'
FARBEN = {
    'moewe-mats-will-nicht-schlafen': dict(gross=WEISS, pal=[WEISS, GRAU, HGRAU], klein=['#f7d046']),
    'mats-sucht-ihre-lieblingsfeder': dict(gross=WEISS, pal=[WEISS, GRAU, HGRAU, '#cfd8de'], klein=['#f7d046']),
    'mats-und-das-schietwetter': dict(pal=[GRAU, HGRAU, '#8fa3b3', '#f7d046']),
    'leuchtturm-lotte-und-der-nebel': dict(pal=['#e8505b', WEISS], klein=['#f7d046']),
    'die-faehre-frieda-faehrt-nach-hause': dict(gross=WEISS, pal=[WEISS, '#4cb782', '#8bc34a'], klein=['#5ec8e5']),
    'ein-schlaflied-fuer-kran-karl': dict(gross='#3f7fd9', pal=['#3f7fd9', '#5ec8e5', '#e8505b', '#4cb782', '#f7d046']),
    'das-kleine-gespenst-huhu': dict(gross=WEISS, pal=[WEISS, HGRAU], klein=['#f29bc4']),
    'die-laterne-die-sich-vor-dem-wind-fuerchtete': dict(gross='#f6a33b', pal=['#f6a33b', '#f7d046']),
    'wichtel-wilbur-und-das-warten': dict(pal=['#2e9e6a', '#a0683f', '#e8505b'], klein=['#f29bc4'], fest={(194, 508): '#e8505b', (332, 499): WEISS, (400, 499): '#f6c9a8', (550, 430): WEISS, (719, 499): '#a0683f'}),
    'der-schneemann-der-die-sterne-sehen-wollte': dict(gross=WEISS, pal=[WEISS, '#e8505b', '#5ec8e5'], klein=['#f6a33b'], fest={(117, 499): '#3a3a40', (333, 497): WEISS, (644, 485): WEISS, (456, 499): '#e8505b'}),
    'bagger-bruno-macht-feierabend': dict(gross='#f7d046', pal=['#f7d046', '#f6a33b', GRAU, '#5ec8e5']),
    'teddy-haelt-wache': dict(gross='#a0683f', pal=['#a0683f', '#c99a6b'], klein=['#e8505b']),
    'gute-nacht-obstkorb': dict(gross='#e8505b', pal=['#e8505b', '#8bc34a'], klein=['#2e9e6a']),
    'die-luftballons-wollen-noch-nicht-schlafen': dict(pal=['#e8505b', '#f7d046', '#8bc34a'], fest={(246, 283): '#e8505b', (358, 500): '#f7d046', (246, 717): '#8bc34a'}),
    'robo-lernt-traeumen': dict(gross=GRAU, pal=[GRAU, HGRAU, '#9aa6b0'], klein=['#e8505b', '#f7d046', '#8bc34a', '#5ec8e5']),
    'das-einhorn-das-seinen-regenbogen-verlor': dict(gross=WEISS, pal=[WEISS, '#e8505b', '#f6a33b', '#f7d046', '#8bc34a', '#3f7fd9', '#9b6ad6']),
}


def faerben(g):
    """Wie ausgemalt.colorize, aber mit Farben aus der Geschichte. Gibt ein RGB-Array zurück."""
    f = FARBEN.get(g['slug'])
    a = np.array(Image.open(os.path.join(SRC, g['motiv'] + '.png')).convert('L'))
    wall = a < 140
    lab, n = ndimage.label(~wall)
    sizes = ndimage.sum(np.ones_like(lab), lab, index=np.arange(1, n + 1))
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    rng = np.random.default_rng(sum(map(ord, g['slug'])))
    pal = [AM.soften(c) for c in (f['pal'] if f else AM.SAISON.get(g['motiv'][:2], AM.BASE))]
    klein = [AM.soften(c) for c in f.get('klein', [])] if f else []
    innen = [i for i in range(1, n + 1) if i not in border and sizes[i - 1] >= 260]
    groesste = max((sizes[i - 1] for i in innen), default=0)
    lut = np.full((n + 1, 3), 255, np.uint8)
    for i in innen:
        s = sizes[i - 1]
        if f and f.get('gross') and s >= .6 * groesste:
            lut[i] = AM.soften(f['gross'])
        elif klein and s < 2500:
            lut[i] = klein[rng.integers(len(klein))]
        else:
            lut[i] = pal[rng.integers(len(pal))]
    for (y, x), c in (f.get('fest', {}) if f else {}).items():
        lut[lab[y, x]] = AM.soften(c)
    rgb = np.where(wall[..., None], np.array([17, 17, 17], np.uint8), lut[lab]).astype(np.int16)
    noise = rng.normal(0, 5, a.shape).astype(np.int16)
    colored = (~wall) & (lut[lab].sum(-1) < 765)
    rgb[colored] = np.clip(rgb[colored] + noise[colored][:, None], 0, 255)
    shade = (a.astype(np.float32) / 255)[..., None]
    return (rgb.astype(np.float32) * np.where(wall[..., None], 1, np.clip(shade * 1.04, 0, 1))).astype(np.uint8), lab, border


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


def freistellen(g):
    """Gefärbtes Motiv ohne Namen, Hintergrund transparent."""
    rgb, lab, border = faerben(g)
    im, bg = rgb[0:880, 60:940], np.isin(lab, list(border))[0:880, 60:940]
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # Kante weich, damit kein weisser Saum bleibt
    alpha = np.array(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.8)))
    rgba = np.dstack([im, alpha])
    img = Image.fromarray(rgba, 'RGBA')
    return img.crop(img.getbbox())


def bild(g, out):
    top, bot = HIMMEL.get(g['themen'][0], HIMMEL['Einschlafen'])
    t = np.linspace(0, 1, H)[:, None, None]
    sky = (hexrgb(top) * (1 - t) + hexrgb(bot) * t) * np.ones((1, W, 1))
    img = Image.fromarray(sky.astype(np.uint8), 'RGB').convert('RGBA')
    rng = np.random.default_rng(sum(map(ord, g['slug'])))
    d = ImageDraw.Draw(img)
    # Sterne
    for _ in range(46):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H * .62), rng.choice([1, 1, 1.5, 2, 2.5])
        a = int(rng.uniform(90, 230))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 246, 214, a))
    # Mond oben rechts (Sichel)
    mx, my, mr = W - 110 + rng.uniform(-20, 20), 95, 38
    moon = Image.new('L', (W, H), 0); md = ImageDraw.Draw(moon)
    md.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=255)
    md.ellipse((mx - mr + 18, my - mr - 8, mx + mr + 18, my + mr - 8), fill=0)
    glow = moon.filter(ImageFilter.GaussianBlur(18)).point(lambda v: v * .5)
    img.paste((255, 236, 170, 255), (0, 0), glow); img.paste((255, 239, 186, 255), (0, 0), moon)
    # weicher Lichtkreis hinter der Figur + Hügel
    halo = Image.new('L', (W, H), 0)
    ImageDraw.Draw(halo).ellipse((W / 2 - 230, 70, W / 2 + 230, 530), fill=95)
    img.paste((255, 255, 255, 255), (0, 0), halo.filter(ImageFilter.GaussianBlur(60)))
    hill = Image.new('L', (W, H), 0)
    ImageDraw.Draw(hill).ellipse((-180, 470, W + 180, 900), fill=255)
    img.paste(tuple(int(c) for c in hexrgb(bot) * .62) + (255,), (0, 0), hill.filter(ImageFilter.GaussianBlur(2)))
    # Figur
    fig = freistellen(g)
    s = min(430 / fig.height, 520 / fig.width)
    fig = fig.resize((round(fig.width * s), round(fig.height * s)), Image.LANCZOS)
    x, y = (W - fig.width) // 2, 545 - fig.height
    sh = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sh).ellipse((W / 2 - fig.width * .38, 528, W / 2 + fig.width * .38, 560), fill=110)
    img.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(10)))
    img.alpha_composite(fig, (x, y))
    img.convert('RGB').save(out, 'WEBP', quality=82, method=6)


def main():
    os.makedirs(OUT, exist_ok=True)
    for g in ALLE:
        bild(g, os.path.join(OUT, g['slug'] + '.webp'))
    tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print('BILDER', len(ALLE), f'{tot / 1e3:.0f} KB')


if __name__ == '__main__':
    main()

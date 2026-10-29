"""Ausgemalte Beispielversionen der Motive (wie mit dem Farbeimer, sanfte Palette).

python3 ausgemalt.py  -> ../02-bilder/motive-ausgemalt/<key>.png
"""
import os, glob, colorsys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '02-bilder', 'motive')
OUT = os.path.join(HERE, '..', '02-bilder', 'motive-ausgemalt')

# Farben aus dem Ausmal-Widget, leicht aufgehellt (wirkt wie Wachsmaler)
BASE = ['#e8505b', '#f6a33b', '#f7d046', '#8bc34a', '#2e9e6a', '#5ec8e5', '#3f7fd9', '#9b6ad6', '#f29bc4', '#a0683f']
SAISON = {
    'hw': ['#f6a33b', '#9b6ad6', '#8bc34a', '#f7d046', '#5ec8e5', '#e8505b'],
    'lt': ['#f7d046', '#f6a33b', '#e8505b', '#5ec8e5', '#8bc34a', '#9b6ad6'],
    'ad': ['#e8505b', '#2e9e6a', '#f7d046', '#a0683f', '#5ec8e5', '#f29bc4'],
    'wi': ['#5ec8e5', '#3f7fd9', '#f29bc4', '#f7d046', '#8bc34a', '#9b6ad6'],
}


def soften(hexc, k=.18):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = l + (1 - l) * k
    r, g, b = colorsys.hls_to_rgb(h, l, s * .92)
    return np.array([r * 255, g * 255, b * 255], np.uint8)


def colorize(path, out):
    key = os.path.basename(path)[:-4]
    pal = [soften(c) for c in SAISON.get(key[:2], BASE)]
    a = np.array(Image.open(path).convert('L'))
    wall = a < 140
    lab, n = ndimage.label(~wall)
    sizes = ndimage.sum(np.ones_like(lab), lab, index=np.arange(1, n + 1))
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    rng = np.random.default_rng(sum(map(ord, key)))
    lut = np.zeros((n + 1, 3), np.uint8)
    H = a.shape[0]
    for i in range(1, n + 1):
        s = sizes[i - 1]
        if i in border or s < 260:      # Hintergrund + Glanzpunkte bleiben weiss
            lut[i] = (255, 255, 255); continue
        lut[i] = pal[rng.integers(len(pal))]
    # weiche "Wachsmaler"-Struktur: leichte Helligkeitsschwankung
    rgb = np.where(wall[..., None], np.array([17, 17, 17], np.uint8), lut[lab])
    noise = (rng.normal(0, 5, a.shape)).astype(np.int16)
    colored = (~wall) & (lut[lab].sum(-1) < 765)
    rgb = rgb.astype(np.int16)
    rgb[colored] = np.clip(rgb[colored] + noise[colored][:, None], 0, 255)
    # Linien weich halten: Kantenpixel aus der Vorlage multiplizieren
    shade = (a.astype(np.float32) / 255)[..., None]
    rgb = (rgb.astype(np.float32) * np.where(wall[..., None], 1, np.clip(shade * 1.04, 0, 1))).astype(np.uint8)
    Image.fromarray(rgb).save(out, optimize=True)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    fs = sorted(glob.glob(os.path.join(SRC, '*.png')))
    for f in fs:
        colorize(f, os.path.join(OUT, os.path.basename(f)))
    print('AUSGEMALT', len(fs))

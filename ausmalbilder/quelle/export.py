"""Exportiert die Daten fuer die kostenlosen Kreativhafen-Seiten nach /kreativhafen im Repo.

Die Seiten laden sie wie helden.json ueber raw.githubusercontent.com:
  kreativhafen/ausmalbilder/daten/katalog.json      Pakete + Motivliste
  kreativhafen/ausmalbilder/daten/motive-<id>.json  SVG je Motiv (mit Namen, kompakt)
  kreativhafen/ausmalbilder/bilder/karte-<id>.webp  Kartenbild je Paket
  kreativhafen/ausmalbilder/bilder/bunt/<key>.webp  ausgemalte Vorschau je Motiv
  kreativhafen/ausmalbilder/pdf/…                   (gratis_pdf.py)
"""
import os, sys, json, re, io, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel as K
import motive  # noqa
import katalog as KAT
import gratis_pdf as GP
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
KH = os.path.join(REPO, 'kreativhafen')
AM = os.path.join(KH, 'ausmalbilder')
BUNT = os.path.join(HERE, '..', '02-bilder', 'motive-ausgemalt')


def mini(svg):
    """SVG verkleinern: nur Pfad-/Formkoordinaten runden (nie Transformationen!), Leerraum sparen."""
    rnd = lambda m: str(round(float(m.group(0))))
    svg = re.sub(r'(\s(?:d|points|cx|cy|r|rx|ry|x|y|width|height|x1|y1|x2|y2)=")([^"]*)(")',
                 lambda m: m.group(1) + re.sub(r'-?\d+\.\d+', rnd, m.group(2)) + m.group(3), svg)
    return re.sub(r'\s+', ' ', svg).replace('> <', '><')


def anzeigename(key):
    n = K.MOTIFS[key]['name']
    return n[0] + n[1:].lower()


def webp(src, dst, w):
    im = Image.open(src).convert('RGB')
    im = im.resize((w, round(w * im.size[1] / im.size[0])), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=78, method=6)


def karte(p, dst):
    """Kartenbild 1200x800: drei ausgemalte Motive auf dunklem Grund mit Paketfarbe."""
    W, H = 1200, 800
    bg = Image.new('RGB', (W, H), (11, 16, 14))
    acc = tuple(int(p['farbe'][i:i + 2], 16) for i in (1, 3, 5))
    # weicher Farbschein
    glow = Image.new('L', (W, H), 0)
    import PIL.ImageDraw as D, PIL.ImageFilter as F
    D.Draw(glow).ellipse((W * .2, H * .25, W * .8, H * 1.2), fill=120)
    glow = glow.filter(F.GaussianBlur(120))
    bg = Image.composite(Image.new('RGB', (W, H), acc), bg, glow.point(lambda v: v * .45))
    teile = []
    for k, x, y, w, rot in [(p['cover'][0], 120, 210, 330, -7), (p['cover'][2], 750, 220, 330, 6), (p['cover'][1], 400, 120, 400, 0)]:
        m = Image.open(os.path.join(BUNT, k + '.png')).convert('RGB')
        m = m.resize((w, round(w * 1.1)), Image.LANCZOS)
        card = Image.new('RGB', (w + 24, round(w * 1.1) + 24), (251, 249, 244)); card.paste(m, (12, 12))
        mask = Image.new('L', card.size, 255)
        card = card.rotate(rot, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
        mask = mask.rotate(rot, expand=True, resample=Image.BICUBIC)
        teile.append((card, mask, x, y))
    # erst alle Schatten (nur auf den Hintergrund), dann die Karten
    for card, mask, x, y in teile:
        sh = Image.new('L', (W, H), 0); sh.paste(mask.point(lambda v: v * .55), (x + 8, y + 30))
        bg.paste((0, 0, 0), (0, 0), sh.filter(F.GaussianBlur(30)))
    for card, mask, x, y in teile:
        bg.paste(card, (x, y), mask)
    bg.save(dst, 'WEBP', quality=80, method=6)


def main():
    os.makedirs(os.path.join(AM, 'daten'), exist_ok=True)
    os.makedirs(os.path.join(AM, 'bilder', 'bunt'), exist_ok=True)
    kat = []
    for p in KAT.ALLE_PAKETE:
        keys = p['motive'] or []
        data = {k: mini(K.motif_svg(k, with_name=True, w=1000, h=1100)) for k in keys}
        if pid_has := keys:
            with open(os.path.join(AM, 'daten', f'motive-{p["id"]}.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        for k in keys:
            webp(os.path.join(BUNT, k + '.png'), os.path.join(AM, 'bilder', 'bunt', k + '.webp'), 360)
        karte(p, os.path.join(AM, 'bilder', f'karte-{p["id"]}.webp'))
        pdfname = GP.DATEI[p['id']] + '.pdf'
        pdfpath = os.path.join(GP.OUT, pdfname)
        kat.append(dict(id=p['id'], nr=p['nr'], name=p['name'], sub=p['sub'], farbe=p['farbe'], saison=p.get('saison', ''),
                        kurz=p['kurz'], extras=p.get('extras', []),
                        anzahl=len(keys), seiten=None,
                        pdf='ausmalbilder/pdf/' + pdfname,
                        pdf_mb=round(os.path.getsize(pdfpath) / 1e6, 1) if os.path.exists(pdfpath) else None,
                        karte=f'ausmalbilder/bilder/karte-{p["id"]}.webp',
                        motive=[dict(key=k, name=anzeigename(k)) for k in keys]))
    zp = os.path.join(GP.OUT, GP.ZIPNAME)
    out = dict(stand=__import__('datetime').date.today().isoformat(), basis=KAT.GRATIS_URL_BASIS,
               alle_zip='ausmalbilder/pdf/' + GP.ZIPNAME, alle_zip_mb=round(os.path.getsize(zp) / 1e6, 1) if os.path.exists(zp) else None,
               pakete=kat)
    with open(os.path.join(AM, 'daten', 'katalog.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    tot = sum(os.path.getsize(os.path.join(dp, x)) for dp, _, fs in os.walk(KH) for x in fs)
    print('EXPORT', len(kat), 'Pakete,', sum(len(p['motive']) for p in kat), 'Motive,', f'{tot / 1e6:.1f} MB gesamt in kreativhafen/')


if __name__ == '__main__':
    main()

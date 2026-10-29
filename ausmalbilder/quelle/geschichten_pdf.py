"""Vorlese-PDFs: Geschichte (A4, ruhig gesetzt) + passendes Ausmalbild.

python3 geschichten_pdf.py -> /kreativhafen/geschichten/pdf/<slug>.pdf
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel as K
import motive  # noqa
import katalog as KAT
import pdf as PDF
from geschichten import ALLE

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(REPO, 'kreativhafen', 'geschichten', 'pdf')
esc = html.escape

CSS = PDF.CSS + '''
.story { position: relative; padding: 0 22mm; }
.story h1 { font: 800 28pt/1.02 Syne; letter-spacing: -.03em; margin: 5mm 0 3mm; }
.story h1 em { font-style: normal; color: #2e9e6a; }
.story .meta { font: 600 7.5pt/1 JBM; letter-spacing: .16em; text-transform: uppercase; color: #8a8a8a; }
.story .lead { font: 500 11pt/1.6 Inter; color: #555; margin: 0 0 7mm; }
.story p.t { font: 400 12pt/1.75 Inter; color: #1a1a1a; margin: 0 0 3.2mm; }
.story p.first::first-letter { float: left; font: 800 34pt/.8 Syne; margin: 1mm 2mm 0 0; color: #2e9e6a; }
.story .night { margin: 7mm 0 5mm; padding: 5mm 6mm; border: .3mm solid #ddd; border-radius: 4mm; font: 700 13pt/1.4 Syne; }
.story .ask { padding: 4mm 6mm; border-radius: 4mm; background: #f4f6f5; font: 400 10.5pt/1.6 Inter; }
.story .ask b { display: block; font: 600 7.5pt/1 JBM; letter-spacing: .16em; text-transform: uppercase; color: #8a8a8a; margin-bottom: 2mm; }
.flow { width: 210mm; }
@page { size: A4; margin: 16mm 0 20mm; }
'''


def build():
    os.makedirs(OUT, exist_ok=True)
    PDF.OUT = OUT
    for i, g in enumerate(ALLE, 1):
        # Text fliesst ueber so viele Seiten wie noetig (Chromium bricht selbst um)
        txt = ''.join(f'<p class="t{" first" if j == 0 else ""}">{esc(a)}</p>' for j, a in enumerate(g['absaetze']))
        fr = ''.join(f'<div>• {esc(f)}</div>' for f in g['fragen'])
        story = f'''<div class="flow"><div class="story">
<div class="meta">Kreativhafen · Gute-Nacht-Geschichte · ab {g["alter"]} Jahren · {g["lesezeit"]} Min.</div>
<h1>{esc(g["titel"])}<em>.</em></h1><p class="lead">{esc(g["teaser"])}</p>{txt}
<div class="night">☾ {esc(g["gute_nacht"])}</div>
<div class="ask"><b>Zum Reden danach</b>{fr}</div>
<p class="meta" style="margin-top:8mm">Text: Trutz Stähler · {KAT.DOMAIN}/gute-nacht-geschichten · kostenlos zum Vorlesen</p>
</div></div>'''
        p = dict(name=g['titel'], sub='Ausmalbild zur Geschichte')
        motiv = PDF.page_motif(p, g['motiv'], 1, 1).replace('01 / 01 · ', '')
        name = g['slug']
        PDF.TITEL[name] = f'{g["titel"]} – Gute-Nacht-Geschichte zum Vorlesen'
        doc = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{esc(g["titel"])}</title><style>{CSS}</style></head><body>{story}</body></html>'
        h = os.path.join(PDF.TMP, name + '.html'); os.makedirs(PDF.TMP, exist_ok=True)
        open(h, 'w', encoding='utf-8').write(doc)
        import subprocess
        tmp_story = os.path.join(PDF.TMP, name + '_text.pdf')
        subprocess.run(['node', os.path.join(HERE, 'render.js'), h, tmp_story], check=True)
        PDF.OUT = PDF.TMP
        tmp_motiv = PDF.write_pdf([motiv], name + '_motiv')
        from pypdf import PdfWriter
        w = PdfWriter()
        for f_ in (tmp_story, tmp_motiv):
            w.append(f_)
        out = os.path.join(OUT, name + '.pdf')
        with open(out, 'wb') as fh:
            w.write(fh)
        PDF.meta(out, name)
        print('PDF', os.path.relpath(out, REPO), f'{os.path.getsize(out) / 1e3:.0f} KB')


if __name__ == '__main__':
    build()

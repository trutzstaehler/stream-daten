"""Druckfertiger Kita-Flyer (A4) mit QR-Code.  python3 flyer.py -> ../07-werbematerial/Kita-Flyer_Ausmalbilder.pdf"""
import os, sys, io, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segno
import kritzel as K
import motive  # noqa
import katalog as KAT
import pdf as PDF

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '07-werbematerial')


def qr_svg(url):
    b = io.BytesIO(); segno.make(url, error='m').save(b, kind='svg', scale=4, border=0, dark='#111', xmldecl=False, svgns=True)
    return b.getvalue().decode().replace('<svg ', '<svg style="width:34mm;height:34mm" ', 1)


def flyer():
    motive_ = ['hw01', 'lt01', 'ad11', 'ad24', 'wi01', 'ad10']
    tiles = ''.join(f'<div style="border:.3mm solid #ddd;border-radius:3mm;padding:2mm">{K.motif_svg(k, with_name=True)}</div>' for k in motive_)
    body = f'''
<section class="pg" style="--acc:#2e9e6a">
  <div style="position:absolute;left:16mm;right:16mm;top:13mm;display:flex;justify-content:space-between"><span class="lbl">[ Kreativhafen · Für Kitas &amp; Schulen ]</span><span class="lbl">{KAT.DOMAIN}</span></div>
  <div style="position:absolute;left:16mm;right:16mm;top:24mm">
    <svg viewBox="0 0 1000 300" style="width:100%;display:block"><g stroke="#111" stroke-linejoin="round">{K.lettering('AUSMALBILDER', 0, 10, 1000, 140, outline=11)}{K.lettering('FÜR DIE GANZE GRUPPE', 60, 175, 880, 100, outline=9)}</g></svg>
    <p style="font:500 11.5pt/1.55 Inter;color:#222;margin:4mm 0 0">Laternenfest, Adventszeit, Weihnachten: 52 Ausmalbilder mit dicken Linien und dem Namen zum Mitlesen – gemacht für Kinder ab 2 Jahren. Mit der <b>Kita-Lizenz</b> kopiert ihr alle Seiten für alle Gruppen eurer Einrichtung.</p>
  </div>
  <div style="position:absolute;left:16mm;right:16mm;top:103mm;display:grid;grid-template-columns:repeat(6,1fr);gap:3mm">{tiles}</div>
  <div class="txt" style="left:16mm;right:16mm;top:146mm;bottom:auto">
    <div class="cols">
      <div><h2 style="margin-top:0">Das ist drin</h2><ul>
        <li><b>Laterne, Laterne:</b> 8 Motive, Laternen-Bastelvorlage, Liedblatt</li>
        <li><b>24 Türchen:</b> Adventskalender – ein Bild pro Tag für die Gruppe</li>
        <li><b>Für dich!:</b> 16 Geschenkanhänger + 4 Karten</li>
        <li><b>Halloween</b> und <b>Winter &amp; Silvester:</b> je 10 Motive</li></ul></div>
      <div><h2 style="margin-top:0">Kita-Lizenz · {KAT.KITA["preis"]}</h2><ul>
        <li>Eine Einrichtung, alle Gruppen</li>
        <li>Kopieren, so oft ihr wollt</li>
        <li>Ohne Ablaufdatum</li>
        <li>Mit Lizenzurkunde für Leitung &amp; Träger</li>
        <li>Rechnung an den Träger möglich</li></ul></div>
    </div>
  </div>
  <div style="position:absolute;left:16mm;right:16mm;bottom:22mm;display:flex;gap:8mm;align-items:center;border:.35mm solid #ddd;border-radius:5mm;padding:6mm">
    {qr_svg('https://' + KAT.DOMAIN + '/ausmalbilder')}
    <div style="font:500 11pt/1.5 Inter;color:#222">
      <div style="font:800 17pt/1.1 Syne;letter-spacing:-.02em;margin-bottom:2mm">3 Motive gratis ausprobieren</div>
      <b>{KAT.DOMAIN}/ausmalbilder</b><br>Fragen &amp; Rechnungen: {KAT.MAIL}<br>
      <span style="color:#666">Trutz Stähler · Papa aus Hamburg · Kreativhafen</span>
    </div>
  </div>
  {PDF.footer('Kreativhafen · Ausmalbilder für Kita & Schule')}
</section>'''
    os.makedirs(OUT, exist_ok=True)
    doc = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{PDF.CSS}</style></head><body>{body}</body></html>'
    h = os.path.join(PDF.TMP, 'flyer.html'); open(h, 'w', encoding='utf-8').write(doc)
    out = os.path.join(OUT, 'Kita-Flyer_Ausmalbilder.pdf')
    subprocess.run(['node', os.path.join(HERE, 'render.js'), h, out], check=True)
    print(out)
    return h


if __name__ == '__main__':
    flyer()

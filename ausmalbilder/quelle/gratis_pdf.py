"""Kostenlose Variante: alle 11 Pakete als PDF (+ Gesamt-ZIP) fuer den Kreativhafen.

python3 gratis_pdf.py [paket-id ...]  -> /kreativhafen/ausmalbilder/pdf/ im Repo
"""
import os, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdf as PDF
import katalog as KAT

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(REPO, 'kreativhafen', 'ausmalbilder', 'pdf')

DATEI = {
    'halloween': 'Halloween-Ausmalbilder_Kleine-Gruselfreunde',
    'laterne': 'St-Martin-Ausmalbilder_Laterne-Laterne',
    'advent': 'Adventskalender-zum-Ausmalen_24-Tuerchen',
    'winter': 'Winter-Ausmalbilder_Winterzeit',
    'anhaenger': 'Geschenkanhaenger-zum-Ausmalen_Fuer-dich',
    'hafen': 'Hafen-Ausmalbilder_Moin-Hafen',
    'fahrzeuge': 'Fahrzeuge-Ausmalbilder_Brumm-brumm',
    'weltraum': 'Weltraum-Ausmalbilder_Ab-ins-All',
    'fantasie': 'Maerchen-Ausmalbilder_Es-war-einmal',
    'obst': 'Obst-und-Gemuese-Ausmalbilder_Knackig-und-bunt',
    'party': 'Geburtstag-Ausmalbilder_Hurra-Party',
}
ZIPNAME = 'Alle-Ausmalbilder_Kreativhafen.zip'


def build(ids=None):
    ids = ids or [p['id'] for p in KAT.ALLE_PAKETE]
    PDF.OUT = OUT
    os.makedirs(OUT, exist_ok=True)
    for pid in ids:
        name = DATEI[pid]
        p = KAT.paket(pid)
        PDF.TITEL[name] = f'{p["name"]} – {p["sub"]} (kostenlos)'
        out = PDF.write_pdf(PDF.pages_for(pid, 'gratis'), name)
        print('PDF', os.path.relpath(out, REPO), f'{os.path.getsize(out) / 1e6:.2f} MB')
    if set(ids) == {p['id'] for p in KAT.ALLE_PAKETE}:
        zp = os.path.join(OUT, ZIPNAME)
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for pid in ids:
                z.write(os.path.join(OUT, DATEI[pid] + '.pdf'), DATEI[pid] + '.pdf')
            z.writestr('Liesmich.txt',
                       'Moin!\n\nHier sind alle Ausmalbilder aus dem Kreativhafen als PDF (A4).\n'
                       'Drucken: A4, Hochformat, "Tatsächliche Größe" / 100 %.\n\n'
                       'Kostenlos für Familien, Kitas, Schulen und Vereine. Bitte teile den Link\n'
                       f'{KAT.DOMAIN}/ausmalbilder statt der Dateien und verkaufe die Bilder nicht.\n\n'
                       f'Viel Spaß beim Malen – Trutz\n{KAT.DOMAIN}\n')
        print('ZIP', os.path.relpath(zp, REPO), f'{os.path.getsize(zp) / 1e6:.2f} MB')


if __name__ == '__main__':
    build(sys.argv[1:] or None)

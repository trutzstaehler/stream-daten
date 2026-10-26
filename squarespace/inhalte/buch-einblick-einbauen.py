"""Baut den Bereich „Blick ins Buch“ mit den Illustrations-Adressen in die Maria-Holm-Seite (Datei 10) ein.

Aufruf:  python3 inhalte/buch-einblick-einbauen.py URL1 URL2 … URL6
Die Bilder liegen in bilder/buch/ und werden bei Squarespace unter „Benutzerdefinierte Dateien“ hochgeladen.
Jede Adresse wird über ihren Dateinamen zugeordnet; die Reihenfolge ist egal.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = ['maria-detektivin', 'kapitel-01-fahrrad', 'kapitel-02-spurensuche', 'kapitel-05-lagebesprechung', 'kapitel-06-speicherstadt', 'kapitel-09-anker']

urls = {}
for u in sys.argv[1:]:
    name = u.split('?')[0].rstrip('/').split('/')[-1].rsplit('.', 1)[0]
    if name not in NAMES:
        sys.exit(f'Unbekannte Datei: {u}')
    urls[name] = u
missing = [n for n in NAMES if n not in urls]
if missing:
    sys.exit('Es fehlen Adressen für: ' + ', '.join(missing))

block = open(os.path.join(HERE, 'maria-holm-einblick.html')).read().rstrip('\n')
for n, u in urls.items():
    block = block.replace(f'__BUCH_{n}__', u)
if '__BUCH_' in block:
    sys.exit('Nicht alle Bildstellen ersetzt')

p = os.path.join(ROOT, '10-maria-holm-codeblock.html')
s = open(p).read()
s, n = re.subn(r'\n<!-- ============ BLICK INS BUCH ============ -->.*?<!-- /BLICK INS BUCH -->', lambda m: '\n' + block, s, flags=re.S)
if not n:
    s = s.rstrip('\n') + '\n\n' + block + '\n'
open(p, 'w').write(s)
print('Fertig.')

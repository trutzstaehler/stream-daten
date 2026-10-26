"""Stellt die Website von Google Fonts auf selbst gehostete Schriften (Squarespace „Benutzerdefinierte Dateien“) um.

Aufruf:  python3 inhalte/schriften-einbauen.py URL1 URL2 … URL6
Die Reihenfolge ist egal – jede Adresse wird über ihren Dateinamen zugeordnet.
Ändert: 01 (Header), den Twitch-Generator samt 12–17 und den Rechtstexte-Generator samt 18–20.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FILES = {
    'syne-latin-wght-normal.woff2': ("'Syne'", '400 800'),
    'inter-latin-wght-normal.woff2': ("'Inter'", '100 900'),
    'jetbrains-mono-latin-wght-normal.woff2': ("'JetBrains Mono'", '100 800'),
    'cinzel-latin-wght-normal.woff2': ("'Cinzel'", '400 900'),
    'asul-latin-400-normal.woff2': ("'Asul'", '400'),
    'asul-latin-700-normal.woff2': ("'Asul'", '700'),
}
URANGE = 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD'

urls = {}
for u in sys.argv[1:]:
    name = u.split('?')[0].rstrip('/').split('/')[-1]
    if name not in FILES:
        sys.exit(f'Unbekannte Datei: {u}')
    urls[name] = u
missing = [n for n in FILES if n not in urls]
if missing:
    sys.exit('Es fehlen Adressen für: ' + ', '.join(missing))

faces = '\n'.join(
    f"  @font-face {{ font-family: {fam}; font-style: normal; font-weight: {w}; font-display: swap; src: url('{urls[n]}') format('woff2'); unicode-range: {URANGE}; }}"
    for n, (fam, w) in FILES.items())
block = ('<style>\n  /* Schriften – selbst gehostet bei Squarespace (keine Verbindung zu Google) */\n'
         + faces + '\n</style>')

# 1) Header 01: Google-Links durch @font-face ersetzen
p = os.path.join(ROOT, '01-code-injection-header.html')
s = open(p).read()
old = re.search(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">', s)
if old:
    s = s.replace(old.group(0), block)
else:
    s, n = re.subn(r'<style>\n  /\* Schriften – selbst gehostet.*?</style>', lambda m: block, s, count=1, flags=re.S)
    if not n:
        sys.exit('01: Schrift-Bereich nicht gefunden')
s = s.replace('Enthält: Fonts, Design-Tokens', 'Enthält: Schriften (selbst gehostet), Design-Tokens')
open(p, 'w').write(s)

# 2) Twitch: Google-Link aus den Code-Blöcken entfernen (Cinzel/Asul kommen jetzt aus 01)
g = os.path.join(ROOT, 'twitch-vorlage', 'umbau-generator.py')
t = open(g).read()
t = re.sub(r"FONTS = '''<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">\n<link href=\"https://fonts\.googleapis\.com/css2[^']*'''",
           "FONTS = '<!-- Schriften (Cinzel, Asul) kommen selbst gehostet aus Datei 01 -->'", t)
open(g, 'w').write(t)
subprocess.run([sys.executable, g], check=True, stdout=subprocess.DEVNULL)

# 3) Datenschutz: Abschnitt Schriftarten ohne Google
r = os.path.join(HERE, 'rechtstexte-generator.py')
t = open(r).read()
t = re.sub(r"\('schriften','Schriftarten \(Google Fonts &amp; Adobe Fonts\)', '''        <p>Für eine einheitliche Darstellung nutzt.*?</p>\n        <p>Rechtsgrundlage ist mein berechtigtes Interesse.*?</p>\n",
           "('schriften','Schriftarten', '''        <p>Die Schriften dieser Website (Syne, Inter, JetBrains Mono, Cinzel und Asul) liegen auf den Servern von Squarespace und werden von dort geladen. Eine Verbindung zu Google Fonts findet nicht statt.</p>\n",
           t, flags=re.S)
open(r, 'w').write(t)
subprocess.run([sys.executable, r], check=True, stdout=subprocess.DEVNULL)

left = subprocess.run(['grep', '-l', 'fonts.googleapis', *[os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.endswith('.html')]], capture_output=True, text=True).stdout.strip()
print('Fertig.' if not left else 'Achtung, noch Google-Links in:\n' + left)

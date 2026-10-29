"""Einrichtungsanleitung fuer den kostenlosen Kreativhafen.  python3 kh_doku.py -> ../08-kreativhafen-gratis/EINRICHTUNG.md"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geschichten import ALLE
import katalog as KAT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '08-kreativhafen-gratis')
N = sum(len(p['motive']) for p in KAT.ALLE_PAKETE)

zeilen = []
for i, g in enumerate(ALLE, 1):
    zeilen.append(f"| {i:02d} | {g['titel']} | `{g['slug']}` | `geschichten/{i:02d}_{g['slug']}.html` | `{g['slug']}.jpg` | {g['teaser']} |")

doc = f'''# Kreativhafen gratis: Einrichtung

**Aufbau:** Kreativhafen (Hauptkategorie) → **Gute-Nacht-Geschichten** (direkt auf der Seite lesen) · **Ausmalbilder** (kostenlos herunterladen) · **Malbücher** und **Romane** (deine Bücher zum Kaufen).

Alle Code-Blöcke liegen in diesem Ordner (`08-kreativhafen-gratis/`). Die Reihenfolge unten ist die beste Reihenfolge zum Einrichten. Zeitbedarf: etwa 2 Stunden, davon die meiste Zeit für die 24 Geschichten.

---

## Schritt 0: Daten auf GitHub ✓ erledigt

Ausmalbilder, PDFs und Bilder lädt die Seite, wie deine Twitch-Seite die Datei `helden.json`, aus deinem Repo:
`{KAT.GRATIS_URL_BASIS}`

Der Ordner `kreativhafen/` ist seit Pull Request #2 in **`main`** und online abrufbar. Test: `{KAT.GRATIS_URL_BASIS}ausmalbilder/daten/katalog.json` zeigt Text, kein „404“.

---

## Schritt 1: Kreativhafen-Seite (`/kreativhafen`)

1. **Ganz oben** einen Code-Block einfügen mit dem Inhalt von `01_reiter-leiste_fuer-kreativhafen-malbuecher-romane.html`. Das ist die Reiter-Leiste: Übersicht · Gute-Nacht-Geschichten · Ausmalbilder · Malbücher · Romane.
2. **Direkt unter dem Regal „Bücher“** einen Code-Block mit `02_regal-gratis-im-hafen_fuer-kreativhafen.html` einfügen. Das neue Regal „Gratis im Hafen“ mit den Karten 03 Ausmalbilder und 04 Gute-Nacht-Geschichten nutzt dieselbe Karten-Optik wie deine Bücher.

## Schritt 2: Malbücher und Romane (`/malbuecher`, `/romane`)

Auf beiden Seiten ganz oben denselben Reiter-Block (`01_…`) einfügen. Dann ist der Kreativhafen von jeder Unterseite aus erreichbar.

## Schritt 3: Seite „Ausmalbilder“ (`/ausmalbilder`)

1. Neue Seite anlegen (nicht in der Hauptnavigation; sie ist über den Kreativhafen erreichbar), URL-Slug `ausmalbilder`.
2. Zwei Code-Blöcke untereinander: `03-1_seite-ausmalbilder_teil-1-von-2.html`, darunter `03-2_…teil-2-von-2.html`.
3. SEO-Titel: `Ausmalbilder kostenlos zum Ausdrucken – {N} Motive für Kinder | Kreativhafen`
4. SEO-Beschreibung: `{N} kostenlose Ausmalbilder für Kinder ab 2: Hamburger Hafen, Fahrzeuge, Weltraum, Halloween, Laterne, Adventskalender und mehr. Einzeln drucken oder als PDF laden.`
5. Social-Bild: `../02-bilder/website/og-ausmalbilder.jpg`

## Schritt 4: Seite „Gute-Nacht-Geschichten“ (`/gute-nacht-geschichten`)

1. Neue Seite, URL-Slug `gute-nacht-geschichten`, ein Code-Block: `04_seite-gute-nacht-geschichten.html`.
2. SEO-Titel: `Gute-Nacht-Geschichten zum Vorlesen – kostenlos | Kreativhafen`
3. SEO-Beschreibung: `{len(ALLE)} kostenlose Gute-Nacht-Geschichten zum Vorlesen für Kinder von 2 bis 7: direkt online lesen, mit Vorlesedauer und Nachtmodus. Von Möwe Mats aus dem Hamburger Hafen bis zum Drachen Funki.`

## Schritt 5: Die {len(ALLE)} Geschichten (Blog „Geschichten“)

Jede Geschichte bekommt ihre eigene Seite. So findet Google jede einzelne, genau wie bei Zitronenbande und Zwergenstark.

**Ausführliche Schritt-für-Schritt-Anleitung mit Steckbrief für jede Geschichte: `ANLEITUNG_BLOG-GESCHICHTEN.md`.**

Kurz: Blog „Geschichten“ unter „Nicht verlinkt“ anlegen, URL-Slug `geschichten`. Für jede Geschichte einen Beitrag mit Titel, URL-Slug, Code-Block, Auszug, Beitragsbild und SEO-Texten. Squarespaces eigener Titel und das Datum werden vom Code-Block automatisch ausgeblendet.

| # | Titel | URL-Slug | Code-Block | Vorschaubild | Teaser (Auszug/SEO) |
|---|---|---|---|---|---|
{chr(10).join(zeilen)}

## Schritt 6: Startseite

`05_teaser-startseite.html` als Code-Block auf der Startseite einfügen, z. B. unter „Bücher aus dem Kreativhafen“. Die Überschrift wechselt mit der Saison.

## Schritt 7: Testen

- `/kreativhafen`: Reiter oben, darunter die Regale Bücher und „Gratis im Hafen“
- `/ausmalbilder`:
  - Pakete mit Bild
  - „PDF“ lädt die Datei
  - „Drucken“ öffnet die Druckansicht
  - „Ausmalen“ holt das Motiv ins Mal-Werkzeug
- `/gute-nacht-geschichten`:
  - Lieblingsgeschichten und „Beliebt im <Monat>“ mit Bildern
  - Filter „Vorlesedauer“ und Suche funktionieren, „Mehr Geschichten anzeigen“ klappt die Liste auf
  - Links wie `/gute-nacht-geschichten?dauer=kurz` filtern direkt
- eine Geschichte öffnen und prüfen:
  - Nachtmodus
  - A−/A+
  - „Vorlesen“
  - Brotkrumen, „Weitere Gute-Nacht-Geschichten“ und „Geschichten auf einen Blick“ am Ende
- alles auch am Handy

---

## Wichtig: Datenschutz und Texte

1. **Datenschutzerklärung:** Die Seiten laden Bilder und Daten von **GitHub** (`raw.githubusercontent.com`, GitHub Inc., USA). Dabei wird die IP-Adresse der Besucher an GitHub übertragen. Deine Twitch-Seite macht das schon heute mit `helden.json`. Prüfe, ob GitHub in deiner Datenschutzerklärung steht, und ergänze sonst einen Absatz. Dazu ein Satz zum Mal-Werkzeug und zum Nachtmodus: *„Das Mal-Werkzeug und die Leseeinstellungen speichern Daten ausschließlich lokal in deinem Browser (localStorage); es wird nichts an uns übertragen.“*
2. **Die Geschichten und Motive habe ich als KI geschrieben bzw. gezeichnet.** Lies jede Geschichte vor dem Veröffentlichen einmal selbst und passe sie an deine Art zu erzählen an. Dann sind es wirklich deine Geschichten. Rein KI-generierte Texte und Bilder sind nach deutschem Recht wahrscheinlich nicht urheberrechtlich geschützt. Durch deine Überarbeitung wird deine Position stärker.
3. **„Vorlesen lassen“** nutzt die eingebaute Computerstimme des Geräts. Die Qualität hängt vom Gerät ab. Eigene Aufnahmen („Papa liest vor“) lassen sich später einfach ergänzen: In `quelle/geschichten/*.py` bei der Geschichte `audio='https://…/datei.mp3'` eintragen und neu erzeugen. Dann erscheint ein Audio-Player über dem Text.
4. **Aufbau der Geschichten** folgt Zitronenbande und Zwergenstark: Brotkrumen → Titel → Autor → Alter und Vorlesedauer → Bild → „Darum geht’s“ → Vorlesen/Schrift/Nachtmodus → Text mit TIPP-Kasten → „Mehr Geschichten lesen“ → „Hat dir die Geschichte gefallen?“ mit Buch-Tipp und Teilen → weitere Geschichten → „Geschichten auf einen Blick“. Kein Ausmalbild, kein Download.

## Neu erzeugen nach Änderungen

```bash
cd ausmalbilder/quelle
python3 export.py             # Motive/Bilder für GitHub (Ordner kreativhafen/)
python3 geschichten_bilder.py # Illustrationen der Geschichten (Farben passend zum Text)
python3 gratis_pdf.py         # PDFs + ZIP der Ausmalbilder
python3 kreativhafen_web.py   # alle Code-Blöcke + Vorschau
python3 kh_doku.py            # diese Anleitung
python3 blog_anleitung.py     # Anleitung + Steckbriefe für den Blog
```
'''
open(os.path.join(OUT, 'EINRICHTUNG.md'), 'w', encoding='utf-8').write(doc)
print('ok')

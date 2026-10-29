"""Schreibt die Einrichtungs-Anleitung und die Produkttexte (zum Kopieren in Squarespace).

python3 doku.py -> ../04-shop-einrichtung.md, ../04-produkttexte/*.txt
"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import katalog as KAT
import pdf as PDF

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..')
TXT = os.path.join(BASE, '04-produkttexte')

GUT_ZU_WISSEN_PRIVAT = [
    'Lizenz für den privaten Gebrauch in deiner Familie – für Kita, Schule & Verein gibt es die Kita-Lizenz',
    'Digitaler Inhalt: Mit Beginn des Downloads erlischt das Widerrufsrecht (siehe Widerrufsbelehrung)',
    f'Alle 5 Pakete zusammen gibt es als Saisonpaket für {KAT.BUNDLE["preis"]}',
]
SO_BEKOMMST = lambda groesse, typ='PDF-Datei (A4)': [
    f'Sofort nach dem Kauf per Download-Link – eine {typ}, ca. {groesse}',
    'Drucken, so oft du willst – Schwarzweiß reicht, A4 Hochformat in „Tatsächlicher Größe“',
    'Kein Versand, kein Abo, kein Konto nötig',
]


def mb(path):
    return f'{os.path.getsize(path) / 1e6:.1f} MB'.replace('.', ',')


def datei(pid):
    if pid == 'bundle':
        return 'Saisonpaket_Alle-Ausmalbilder-Herbst-Winter.zip'
    if pid == 'kita':
        return 'Kita-Lizenz_Alle-Ausmalbilder-Herbst-Winter.zip'
    return PDF.DATEINAMEN[pid] + '.pdf'


def texte():
    T = {}
    f = lambda pid: mb(os.path.join(PDF.OUT, datei(pid)))
    T['halloween'] = dict(
        drin=['10 Halloween-Motive, je eine A4-Seite: Kürbis, Gespenst, Fledermaus, Katze, Spinne, Hexenhut, Hexenkessel, Bonbons, Monster und Spukhaus',
              'Zu jedem Bild der Name in Buchstaben, die man mit ausmalen kann', 'Deckblatt zum Ausmalen („Dieses Heft gehört …“)',
              'Mal-Urkunde zum Schluss', 'Eine Seite für Eltern mit Drucktipps'],
        wen=['Für Kinder ab etwa 2 Jahren – dicke Linien, große Flächen', 'Freundliche Gesichter statt Grusel: auch für die Kleinsten',
             'Perfekt für die Halloween-Party, den Kindergeburtstag oder einen verregneten Herbstnachmittag'],
        bekommst=SO_BEKOMMST(f('halloween')), gut=GUT_ZU_WISSEN_PRIVAT)
    T['laterne'] = dict(
        drin=['8 Motive für die Laternenzeit: Laterne, Sonne, Mond, Stern, Fliegenpilz, Kastanie, Herbstblatt und Drachen',
              'Bastelvorlage für eine eigene Laterne: Mantel mit Sonne, Mond und Sternen, Boden, Ring und Henkel – mit Schritt-für-Schritt-Anleitung',
              'Liedblatt „Laterne, Laterne“ mit drei Strophen zum Mitsingen und Ausmalen',
              'Deckblatt zum Ausmalen, Mal-Urkunde und eine Seite für Eltern'],
        wen=['Für Kinder ab etwa 2 Jahren – die Bastelvorlage mit etwas Hilfe von Großen',
             'Ideal für die Wochen vor dem Laternenumzug zu St. Martin (11. November)'],
        bekommst=SO_BEKOMMST(f('laterne')) + ['Tipp: Die Bastelvorlage auf 160 g/m² Papier drucken. Bitte nur mit LED-Laternenstab verwenden.'],
        gut=GUT_ZU_WISSEN_PRIVAT)
    T['advent'] = dict(
        drin=['24 Weihnachtsmotive – eins für jeden Tag vom 1. bis 24. Dezember, jede Seite mit Türchen-Nummer',
              'Vom Adventskranz am 1. über den Nikolaus am 6. bis zum geschmückten Tannenbaum an Heiligabend',
              'Türchen-Plan zum Abhaken: Jeden Tag ein Türchen anmalen', 'Deckblatt zum Ausmalen und Mal-Urkunde für Heiligabend',
              'Eine Seite für Eltern mit Drucktipps'],
        wen=['Für Kinder ab etwa 2 Jahren – dicke Linien, große Flächen, Name zum Mitlesen',
             'Der Adventskalender, der nicht schmilzt: ganz ohne Schokolade, dafür mit 24 Malmomenten',
             'Auch als Gruppen-Adventskalender für Kita und Schule (mit der Kita-Lizenz)'],
        bekommst=SO_BEKOMMST(f('advent')) + ['Tipp: Alle 24 Seiten vorab ausdrucken, falten und jeden Tag eine „öffnen“'],
        gut=GUT_ZU_WISSEN_PRIVAT)
    T['winter'] = dict(
        drin=['10 Wintermotive: Schneemann, Schneeflocke, Mütze, Handschuh, Eisbär, Iglu, Schlittschuh, Glücksschwein, Kleeblatt und Rakete',
              'Glücksbringer für Silvester und Neujahr', 'Deckblatt zum Ausmalen, Mal-Urkunde und eine Seite für Eltern'],
        wen=['Für Kinder ab etwa 2 Jahren', 'Für die Zeit zwischen den Jahren, Schneetage und Schietwetter bis Februar'],
        bekommst=SO_BEKOMMST(f('winter')), gut=GUT_ZU_WISSEN_PRIVAT)
    T['anhaenger'] = dict(
        drin=['16 Geschenkanhänger mit „Für“ und „Von“ – mit Tannenbaum, Rentier, Teddy, Schneemann und vielen mehr',
              '4 Karten zum Ausmalen: zweimal „Frohe Weihnachten“, einmal „Gutes neues Jahr!“ und ein großes „Danke schön!“',
              'Deckblatt und eine Seite für Eltern'],
        wen=['Für Kinder ab etwa 2 Jahren – Großeltern lieben selbst gemalte Anhänger',
             'Ausmalen, ausschneiden, Band durchs Loch – fertig ist das persönliche Geschenk'],
        bekommst=SO_BEKOMMST(f('anhaenger')) + ['Tipp: Auf 160 g/m² Papier drucken, dann halten die Anhänger besser'],
        gut=GUT_ZU_WISSEN_PRIVAT)
    T['bundle'] = dict(
        drin=['Alle 5 Pakete in einem Download:', 'Kleine Gruselfreunde – 10 Halloween-Motive', 'Laterne, Laterne – 8 Motive + Laternen-Bastelvorlage + Liedblatt',
              '24 Türchen – Adventskalender mit 24 Motiven + Türchen-Plan', 'Winterzeit – 10 Motive für Winter & Silvester',
              'Für dich! – 16 Geschenkanhänger und 4 Karten', 'Zusammen 52 Motive, jedes Paket mit Deckblatt und Mal-Urkunde'],
        wen=['Für Familien, die von Halloween bis Silvester durchmalen wollen', f'Einzeln kosten die Pakete {KAT.euro(KAT.einzelsumme())} – im Saisonpaket sparst du 7,60 €'],
        bekommst=SO_BEKOMMST(f('bundle'), 'ZIP-Datei mit allen PDFs (A4)'),
        gut=['Lizenz für den privaten Gebrauch in deiner Familie – für Kita, Schule & Verein gibt es die Kita-Lizenz',
             'Digitaler Inhalt: Mit Beginn des Downloads erlischt das Widerrufsrecht (siehe Widerrufsbelehrung)',
             'Die ZIP-Datei lässt sich am Handy und Computer ohne Zusatzprogramm öffnen'])
    T['kita'] = dict(
        drin=['Das komplette Saisonpaket: alle 5 Pakete mit 52 Motiven, Laternen-Bastelvorlage, Liedblatt, Türchen-Plan, 16 Anhängern und 4 Karten',
              'Lizenzurkunde zum Ausfüllen und Abheften'],
        wen=['Für Kita, Krippe, Tagespflege, Grundschule, Hort, OGS und Vereine',
             'Saisonfertig: Laternenfest, Adventskalender für die Gruppe, Weihnachtsgeschenke der Kinder für die Eltern'],
        lizenz=['Gilt für eine Einrichtung (ein Standort) mit allen Gruppen', 'Drucken und kopieren, so oft ihr wollt – ohne Ablaufdatum',
                'Nicht erlaubt: Weitergabe der Dateien an andere Einrichtungen, Eltern oder Dritte, Veröffentlichung und Weiterverkauf',
                'Mehrere Standorte? Schreib mir, dann machen wir ein faires Angebot'],
        bekommst=SO_BEKOMMST(f('kita'), 'ZIP-Datei mit allen PDFs (A4)') + [f'Rechnung auf den Träger? Kein Problem – schreib mir an {KAT.MAIL}'],
        gut=['Digitaler Inhalt: Mit Beginn des Downloads erlischt das Widerrufsrecht (siehe Widerrufsbelehrung)'])
    return T


SEO = {
    'halloween': ('Halloween-Ausmalbilder für Kinder ab 2 – PDF | Kreativhafen', 'Kürbis, Gespenst & Co.: 10 freundliche Halloween-Ausmalbilder zum Ausdrucken – dicke Linien, Name zum Mitlesen. Sofort als PDF.'),
    'laterne': ('St. Martin Ausmalbilder + Laternen-Bastelvorlage – PDF', 'Laterne, Laterne: 8 Ausmalbilder, Bastelvorlage für die eigene Laterne und Liedblatt – für Kinder ab 2. Sofort als PDF zum Ausdrucken.'),
    'advent': ('Adventskalender zum Ausmalen – 24 Motive als PDF', '24 Türchen, 24 Ausmalbilder: vom Adventskranz bis zum Tannenbaum, mit Türchen-Plan. Für Kinder ab 2 – sofort als PDF zum Ausdrucken.'),
    'winter': ('Winter- & Silvester-Ausmalbilder für Kinder – PDF', 'Schneemann, Eisbär, Glücksschwein: 10 Winter- und Silvester-Ausmalbilder zum Ausdrucken. Dicke Linien, für Kinder ab 2. Sofort als PDF.'),
    'anhaenger': ('Geschenkanhänger & Karten zum Ausmalen – PDF', '16 Geschenkanhänger und 4 Weihnachts-, Neujahrs- und Dankeskarten zum Ausmalen. Kinder malen, die Geschenke werden persönlich.'),
    'bundle': ('Ausmalbilder-Saisonpaket Herbst & Winter – 52 Motive', 'Halloween, St. Martin, Adventskalender, Winter und Geschenkanhänger: alle 5 Pakete mit 52 Motiven als PDF – du sparst 7,60 €.'),
    'kita': ('Ausmalbilder Kita-Lizenz – kopieren für alle Gruppen', 'Alle Ausmalbilder der Saison für eure Kita oder Schule: 52 Motive, Bastelvorlage, Adventskalender – mit Lizenz für eine Einrichtung.'),
}


def produkttext(p, t):
    out = [p['intro'], '', 'DAS IST DRIN'] + ['• ' + x for x in t['drin']]
    out += ['', 'FÜR WEN'] + ['• ' + x for x in t['wen']]
    if 'lizenz' in t:
        out += ['', 'DIE LIZENZ'] + ['• ' + x for x in t['lizenz']]
    out += ['', 'SO BEKOMMST DU ES'] + ['• ' + x for x in t['bekommst']]
    out += ['', 'GUT ZU WISSEN'] + ['• ' + x for x in t['gut']]
    return '\n'.join(out)


def main():
    os.makedirs(TXT, exist_ok=True)
    T = texte()
    alle = KAT.PAKETE + [KAT.BUNDLE, KAT.KITA]
    md = []
    md.append('# Shop-Einrichtung: Ausmalbilder\n')
    md.append('Diese Anleitung führt dich Schritt für Schritt durch die Einrichtung in Squarespace. '
              'Alle Texte zum Kopieren liegen zusätzlich einzeln im Ordner `04-produkttexte/`.\n')
    md.append('**Reihenfolge:** Produkte anlegen → Kategorieseite → TS_SHOP ergänzen → Gratis-PDF → Weiterleitung → Teaser → Testkauf.\n')
    md.append('**Zeitbedarf:** etwa 2–3 Stunden für alles.\n')
    md.append('## 1. Produkte anlegen (7 digitale Produkte)\n')
    md.append('In Squarespace: **Commerce → Produkte → Shop-Seite „Shop“ (/store) → + → Digitales Produkt.** '
              'Für jedes Produkt die Felder unten ausfüllen. Wichtig ist der **Titel mit Gedankenstrich** („Name – Untertitel“): '
              'Dein Produktseiten-Skript macht daraus automatisch die kleine Überzeile und den großen Namen.\n')
    md.append('Die Beschreibung genau so einfügen, wie sie ist: Zeilen in GROSSBUCHSTABEN werden automatisch zu Zwischenüberschriften, '
              'Zeilen mit „• “ zu Aufzählungen, der erste Absatz wird zur Einleitung – wie bei deinen Stream-Widgets.\n')
    for i, p in enumerate(alle, 1):
        pid = p['id']
        t = produkttext(p, T[pid])
        open(os.path.join(TXT, f'{i:02d}_{p["slug"]}.txt'), 'w', encoding='utf-8').write(
            f'TITEL:\n{p["name"]} – {p["sub"]}\n\nPREIS:\n{p["preis"]}\n\nURL-SLUG:\n{p["slug"]}\n\nBESCHREIBUNG:\n{t}\n\n'
            f'SEO-TITEL:\n{SEO[pid][0]}\n\nSEO-BESCHREIBUNG:\n{SEO[pid][1]}\n')
        bilder = sorted(glob.glob(os.path.join(BASE, '02-bilder', 'produkte', p['slug'], '*.jpg')))
        md.append(f'### 1.{i} {p["name"]} – {p["sub"]}\n')
        md.append('| Feld | Eintrag |\n|---|---|')
        md.append(f'| Produkttyp | Digitales Produkt |')
        md.append(f'| Titel | `{p["name"]} – {p["sub"]}` |')
        md.append(f'| Preis | **{p["preis"]}** |')
        md.append(f'| Datei (Download) | `01-produkte-pdf/{datei(pid)}` ({mb(os.path.join(PDF.OUT, datei(pid)))}) |')
        md.append(f'| Bilder (in dieser Reihenfolge) | ' + '<br>'.join(f'`02-bilder/produkte/{p["slug"]}/{os.path.basename(b)}`' for b in bilder) + ' |')
        md.append(f'| Produkt-URL (Slug) | `{p["slug"]}` → ergibt `/store/p/{p["slug"]}` |')
        md.append(f'| SEO-Titel | {SEO[pid][0].replace("|", "\\|")} |')
        md.append(f'| SEO-Beschreibung | {SEO[pid][1]} |')
        if pid in KAT.ALLE_IDS:
            teile = sorted(os.path.basename(x) for x in glob.glob(os.path.join(BASE, '03-website', f'02-*_{p["slug"]}_teil-*.html')))
            md.append(f'| Zusätzliche Informationen | Code-Blöcke untereinander: ' + '<br>'.join(f'`03-website/{x}`' for x in teile) + ' |')
        md.append(f'| Text zum Kopieren | `04-produkttexte/{i:02d}_{p["slug"]}.txt` |\n')
        md.append('<details><summary>Beschreibung anzeigen</summary>\n\n```\n' + t + '\n```\n</details>\n')
    md.append('''## 2. Kategorieseite `/shop/ausmalbilder` anlegen

1. **Seiten → deine Seite `/shop/buecher` duplizieren** (drei Punkte → Duplizieren). So übernimmst du Layout und Abschnittsfarben.
2. Neue Seite umbenennen in **Ausmalbilder**, URL-Slug: **`/shop/ausmalbilder`**. Die Seite wie `/shop/buecher` aus der Navigation heraushalten.
3. Den vorhandenen Code-Block öffnen und den Inhalt komplett durch **`03-website/01-1_kategorieseite_…_teil-1-von-3.html`** ersetzen.
4. Darunter zwei weitere **Code-Blöcke** einfügen: Teil 2 und Teil 3. (Teil 1 enthält das CSS für alle drei Teile, deshalb immer zuerst.)
5. **Seiteneinstellungen → SEO:**
   - SEO-Titel: `Ausmalbilder zum Ausdrucken – Halloween, Laterne, Advent | Kreativhafen`
   - SEO-Beschreibung: `52 Ausmalbilder für Kinder ab 2: Halloween, St. Martin mit Laternen-Bastelvorlage, Adventskalender zum Ausmalen, Winter & Geschenkanhänger. Sofort als PDF – 3 Motive gratis.`
6. **Seiteneinstellungen → Social-Bild:** `02-bilder/website/og-ausmalbilder.jpg`.

> Falls Squarespace einen Code-Block nicht speichern will (sehr große Blöcke), sag Bescheid. Dann teile ich ihn weiter auf.

## 3. TS_SHOP ergänzen (Kachel auf /shop + Produktkacheln)

Öffne **Einstellungen → Erweitert → Code-Injection** (dort, wo `window.TS_SHOP` steht) und folge den drei Schritten in **`03-website/03_ts-shop-ergaenzung.js`**:

1. Kategorie-Zeile in `kategorien: [ … ]` ergänzen → auf `/shop` erscheint die dritte Kachel **„03 — Ausmalbilder“** (inklusive Zahl der Produkte).
2. Sieben Produkt-Zeilen in `produkte: [ … ]` ergänzen → die Kacheln auf `/shop/ausmalbilder` erscheinen, die Bilder holt sich dein Skript automatisch vom Produkt.
3. Eine Zeile im Brotkrumen-Skript ergänzen → auf den Produktseiten steht oben „Ausmalbilder › Kleine Gruselfreunde“ statt „Shop › …“.

**Hinweis:** Auf der Shop-Seite steht bei Bücher noch „02 — Bald“. Nach dem Einfügen steht Ausmalbilder als „03 — 7 Produkte“ daneben.

## 4. Gratis-Probierpaket hochladen

1. Auf einer beliebigen Seite einen Textblock öffnen, Text markieren → **Link → Datei → Datei hochladen** → `01-produkte-pdf/Probierpaket_3-Ausmalbilder-gratis.pdf`.
2. Squarespace erzeugt eine Adresse wie **`/s/Probierpaket_3-Ausmalbilder-gratis.pdf`**. Diese Adresse ist in Teil 3 der Kategorieseite schon eingetragen. Weicht sie ab, ersetze sie dort (Suche nach `/s/Probierpaket`).
3. Den Hilfs-Link im Textblock danach wieder entfernen, die Datei bleibt erhalten.

## 5. Kurze Adresse `/ausmalbilder`

**Einstellungen → Erweitert → URL-Zuordnungen**, neue Zeile:

```
/ausmalbilder -> /shop/ausmalbilder 301
/adventskalender-ausmalen -> /store/p/ausmalbilder-adventskalender 301
/laterne -> /store/p/ausmalbilder-laterne 301
```

Damit kannst du in Instagram-Posts und auf Flyern kurze Links nutzen: **trutzstaehler.de/ausmalbilder**.

## 6. Teaser auf Startseite und im Kreativhafen

`03-website/04_teaser_startseite-oder-kreativhafen.html` als Code-Block einfügen:
- **Startseite:** zwischen „Bücher aus dem Kreativhafen“ und dem Kontakt-Abschnitt.
- **Kreativhafen:** unter den Büchern.

Die Überschrift wechselt automatisch mit der Saison: „Halloween kann kommen.“ → „Laterne, Laterne.“ → „24 Türchen zum Ausmalen.“ → „Malen, wenn’s draußen schneit.“

## 7. Download-Mail prüfen

**Commerce → Kundenbenachrichtigungen → „Bestellung bestätigt“ und „Digitale Produkte“**. Vorschlag für den Text der Download-Mail:

```
Moin {Vorname}!

Danke für deine Bestellung – deine Ausmalbilder warten schon. Über den Button unten
lädst du die Datei herunter (der Link ist begrenzt gültig, also am besten gleich speichern).

Drucktipp: A4, Hochformat, „Tatsächliche Größe“ / 100 %. Schwarzweiß reicht.
Die Laternen-Bastelvorlage hält am besten auf 160 g/m² Papier.

Ich freu mich über eure Kunstwerke: auf Instagram mit @trutzstaehler markieren
(bitte nur das Bild, ohne Namen oder Gesichter der Kinder).

Viel Spaß beim Malen!
Trutz
```

## 8. Testkauf (wichtig!)

1. **Commerce → Rabatte → neuer Rabattcode** `TEST100`: 100 % auf ein Produkt, auf 1 Nutzung begrenzt.
2. Jedes Produkt einmal kaufen oder mindestens Halloween, Saisonpaket und Kita-Lizenz. Prüfe dabei:
   - Kommt die Mail an?
   - Lädt die Datei?
   - Stimmt der Hinweis zum Widerrufsrecht?
3. Rabattcode danach löschen.
4. Auf dem Handy prüfen:
   - `/shop` zeigt die Kachel „03 — Ausmalbilder“.
   - `/shop/ausmalbilder` zeigt alle 7 Kacheln mit Bild.
   - Das Ausmal-Widget funktioniert.
   - Auf jeder Produktseite stehen die Brotkrumen „Ausmalbilder › …“.

## 9. Black Friday (Fr, 27. November) – optional

Rabattcode **`MALZEIT`**: 20 % auf alle Ausmalbilder, gültig 27.–30. November. Details stehen im Marketing-Plan (`06-marketing.md`).
''')
    open(os.path.join(BASE, '04-shop-einrichtung.md'), 'w', encoding='utf-8').write('\n'.join(md))
    print('ok', len(os.listdir(TXT)), 'Texte')


if __name__ == '__main__':
    main()

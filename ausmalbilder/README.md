# Kreativhafen: Geschichten, Ausmalbilder, Bücher

> **Aktueller Stand (gilt):** Die Ausmalbilder sind **kostenlos**, die **Gute-Nacht-Geschichten** stehen direkt auf der Website, deine **Malbücher und Romane** bleiben zum Kaufen.
> **Start hier: `08-kreativhafen-gratis/EINRICHTUNG.md`**

| Bereich | Adresse | Inhalt |
|---|---|---|
| Kreativhafen (Hauptkategorie) | `/kreativhafen` | Reiter-Leiste + neues Regal „Gratis im Hafen“ unter den Büchern |
| Gute-Nacht-Geschichten | `/gute-nacht-geschichten` + `/geschichten/…` | 24 Geschichten direkt zum Lesen: Suche, Filter (Länge, Alter, Art, Thema), Saison-Block, Figuren, Nachtmodus, Vorlesen lassen, Ausmalbild zur Geschichte |
| Ausmalbilder | `/ausmalbilder` | 112 Motive in 11 Themen, PDF je Paket + Gesamt-ZIP, jedes Motiv einzeln drucken, Mal-Werkzeug im Browser |
| Bücher | `/malbuecher`, `/romane` | deine bestehenden Seiten, jetzt mit Reiter-Leiste |

**Daten:** Der Ordner `kreativhafen/` im Repo (PDFs, Motive, Bilder) wird wie `helden.json` über GitHub geladen. Dafür muss er nach `main`, siehe Anleitung, Schritt 0.

---

## Archiv: frühere Variante „Verkauf im Shop“ (nicht mehr aktiv)

Die folgenden Abschnitte beschreiben die erste Variante mit kostenpflichtigen Paketen. Sie wird nicht mehr genutzt. Die Dateien (`01-` bis `07-`) bleiben als Vorlage, falls du später doch etwas verkaufen möchtest.

# Ausmalbilder-Saison 2026: alles für den Kreativhafen-Shop

Moin Trutz! Hier ist alles, was du für den Verkauf der Ausmalbilder brauchst: Produkte, Bilder, Webseiten, Texte und Plan. **Fang mit `04-shop-einrichtung.md` an**, dort steht Schritt für Schritt, was wohin gehört.

## Die Produkte

| # | Produkt | Inhalt | Preis | Saison |
|---|---|---|---|---|
| 01 | **Kleine Gruselfreunde** – Halloween-Ausmalbilder | 10 Motive, Deckblatt, Urkunde, Elternseite | 3,90 € | bis 31. Oktober |
| 02 | **Laterne, Laterne** – Ausmalbilder zu St. Martin | 8 Motive + Laternen-Bastelvorlage + Liedblatt | 3,90 € | bis 11. November |
| 03 | **24 Türchen** – Adventskalender zum Ausmalen | 24 Motive mit Türchen-Nummer + Türchen-Plan | 5,90 € | 1.–24. Dezember |
| 04 | **Winterzeit** – Winter & Silvester | 10 Motive inkl. Glücksbringer | 3,90 € | Dezember – Februar |
| 05 | **Für dich!** – Geschenkanhänger & Karten | 16 Anhänger + 4 Karten | 2,90 € | bis Heiligabend |
| 06 | **Saisonpaket** – alle 5 Pakete | 52 Motive + alle Extras (ZIP) | 12,90 € (statt einzeln 20,50 €) | ganze Saison |
| 07 | **Kita-Lizenz** – für eine Einrichtung | Saisonpaket + Lizenzurkunde (ZIP) | 29,00 € | ganze Saison |
| – | **Probierpaket** (gratis) | Kürbis, Laterne, Tannenbaum | 0 € | Lockangebot |

Alle Motive haben dicke Linien, große Flächen, ein kawaii-Gesicht wie in deinen Kritzelbüchern und den Namen in hohlen Buchstaben zum Mitausmalen.

## Ordner

| Ordner / Datei | Was drin ist |
|---|---|
| `01-produkte-pdf/` | Die Download-Dateien: 5 Paket-PDFs, Probierpaket, 2 ZIPs (Saisonpaket, Kita-Lizenz) |
| `02-bilder/produkte/` | Produktbilder je Produkt (3–4 Stück, quadratisch 2000 px, Reihenfolge = Dateiname) |
| `02-bilder/social/` | Pinterest- (1000×1500) und Instagram-Bilder (1080×1350), dazu 24 Advents-Stories (1080×1920) |
| `02-bilder/motive/` · `motive-ausgemalt/` | Alle 52 Motive einzeln, als Vorlage und ausgemalt (für Posts, Stories, Etsy …) |
| `02-bilder/website/` | Social-Vorschaubild für die Kategorieseite |
| `03-website/` | Code-Blöcke: Kategorieseite (3 Teile), Zusatzinfos je Produkt, TS_SHOP-Ergänzung, Teaser |
| `03-website/vorschau/` | Lokale Vorschau der Code-Blöcke mit deinem echten Seiten-CSS (im Browser öffnen) |
| `04-shop-einrichtung.md` | **Start hier:** Schritt-für-Schritt-Anleitung für Squarespace |
| `04-produkttexte/` | Titel, Preis, Beschreibung und SEO je Produkt zum Kopieren |
| `05-rechtliches.md` | Widerruf, Lizenz-Baustein für die AGB, Urheberrecht, Preise, Datenschutz |
| `06-marketing.md` | Fahrplan bis Silvester, Instagram- und Pinterest-Texte, Kita-Brief, Black Friday |
| `07-werbematerial/` | Druckfertiger Kita-Flyer mit QR-Code |
| `quelle/` | Der Generator: Damit lässt sich alles neu erzeugen, wenn du etwas ändern willst |

## Was die Webseite kann

- **Kategorieseite `/shop/ausmalbilder`** im Design deines Shops:
  - Saison-Leiste, die automatisch „Jetzt dran · noch 2 Tage“, „Heute: Türchen 10“ oder „Fürs nächste Jahr“ anzeigt, auch nächstes Jahr
  - Produktkacheln über dein `TS_SHOP`
  - Saisonpaket-Angebot
  - Gratis-Download
  - Kita-Bereich, Schritte, FAQ
- **Ausmal-Widget wie auf deiner Tiere-Kritzelbuch-Seite:**
  - fünf Motive zur Auswahl
  - zeigt automatisch das Motiv der aktuellen Saison
  - Farbeimer, Pinsel, Radierer, Zurück, Speichern, Drucken
- **Produktseiten:** Zusatzinfos mit Widget und allen Motiven. Beim Adventskalender mit Türchen-Nummern, bei den Anhängern mit den echten Seiten.
- **Teaser** für Startseite oder Kreativhafen. Die Überschrift wechselt mit der Saison.
- **Für Google:** strukturierte Daten (Produkte mit Preis, FAQ) und SEO-Texte für jede Seite.

## Geprüft

- **Farbeimer-Test:** Alle 52 Motive automatisch durchgefärbt. Keine Fläche „läuft aus“, auch die Buchstaben lassen sich einzeln ausmalen.
- **PDFs:** Jede Seite durchgesehen. Automatischer Check: kein Text läuft über. Titel und Autor stehen in den Metadaten.
- **Webseiten:**
  - mit deinem echten Seiten-CSS auf Desktop (1440 px) und Handy (390 px) gerendert
  - kein seitliches Überlaufen, keine Skriptfehler
  - das Widget füllt per Klick
  - die Saison-Logik an 8 Daten zwischen Oktober und Juni getestet

## Ehrliche Hinweise und offene Punkte

1. **KI-Motive und Urheberrecht:** Die Motive habe ich erzeugt. Rein KI-generierte Bilder sind in Deutschland wahrscheinlich nicht urheberrechtlich geschützt (Details in `05-rechtliches.md`). Verkaufen darfst du sie, deine Lizenzbedingungen gelten vertraglich. Je mehr du selbst überarbeitest, desto stärker wird deine Position.
2. **Nur in Chromium getestet:** Das Widget nutzt die Motive als SVG. Bitte einmal auf einem iPhone (Safari) antippen und prüfen, ob die Fläche sich füllt.
3. **Code-Block-Größe:** Die Blöcke sind 26–79 KB groß, deine Malbuchseite hat einen mit rund 90 KB. Falls Squarespace beim Speichern meckert, teile ich weiter auf.
4. **Gratis-PDF-Link:** Die Adresse `/s/Probierpaket_3-Ausmalbilder-gratis.pdf` entsteht erst beim Hochladen. Weicht sie ab, musst du sie in Teil 3 der Kategorieseite anpassen.
5. **Checkout-Zustimmung zum Widerrufsrecht:** Prüfe, ob sie bei deinen Widgets schon aktiv ist (siehe `05-rechtliches.md`).
6. **Halloween ist übermorgen:** Wenn du nur Zeit für das Nötigste hast, stell heute Halloween + Probierpaket online und den Rest am Wochenende. Für die Laternenzeit reicht der Start Anfang November.
7. **Preise:** Preise im Stil deiner Widgets (x,90 €). Zum Ändern einfach `quelle/katalog.py` anpassen und neu erzeugen.

## Etwas ändern und neu erzeugen

```bash
cd quelle
pip install fonttools pypdf scipy segno pillow   # einmalig; Node + Playwright werden zum Rendern gebraucht
python3 pdf.py          # PDFs + ZIPs  → 01-produkte-pdf/
python3 bilder.py       # Produkt-, Social- und Motivbilder → 02-bilder/
python3 ausgemalt.py    # ausgemalte Beispielmotive
python3 website.py      # Code-Blöcke + Vorschau → 03-website/
python3 doku.py         # Shop-Anleitung + Produkttexte
python3 flyer.py        # Kita-Flyer
```

- **Texte und Preise:** `quelle/katalog.py`
- **Motive:** `quelle/motive/*.py`. Jedes Motiv ist eine kleine Zeichenfunktion, `python3 vorschau.py bogen.png hw` zeigt einen Kontaktbogen.

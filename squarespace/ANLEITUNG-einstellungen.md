# Squarespace-Einstellungen – Klick-Anleitung

Diese Punkte lassen sich nicht per Code setzen, sondern nur im Squarespace-Backend.
Die Menünamen können je nach Version leicht anders heißen. Falls du etwas nicht findest, hilft die Suche oben im Einstellungs-Menü.

---

## 1. Weiterleitungen alter Adressen (URL-Zuordnungen)

Damit alte Links (Google, Instagram, Lesezeichen) nicht ins Leere laufen.

**Einstellungen → Entwicklertools → URL-Zuordnungen (URL Mappings)**: diesen Text 1:1 einfügen und speichern:

```
/running/hella-half-marathon-2025 -> /hella-half-marathon-2025 301
/running2/hella-half-marathon-2025 -> /hella-half-marathon-2025 301
/running2 -> /running 301
/running2/category/[cat] -> /running 301
/maria-holmmaria-holm-und-das-geheimnis-der-verschwundenen-perle -> /maria-holm-und-das-geheimnis-der-verschwundenen-perle 301
/malbucher -> /malbuecher 301
/datenschutzerklrung -> /datenschutzerklaerung 301
/datenschutz -> /datenschutzerklaerung 301
/shop -> /kreativhafen 301
```

Weiterleitungen greifen nur, wenn unter der alten Adresse **keine Seite mehr existiert**. Deshalb vorher:
- den alten Blog **„Eventblog“ (`/running2`)** löschen. Er ist noch öffentlich und doppelt den Hella-Bericht im alten Design.
- ~~die leere Seite „Shop“ löschen~~ ✓ erledigt
- ~~Datenschutz-Adresse korrigieren~~ ✓ erledigt, jetzt `/datenschutzerklaerung`. Alle Links im Code zeigen direkt dorthin.

Danach testen: `trutzstaehler.de/running2` und `trutzstaehler.de/malbucher` aufrufen. Du solltest jeweils auf der neuen Seite landen.

---

## 2. Eigene 404-Seite

1. **Seiten → „Nicht verlinkt“ → +** → leere Seite, Titel `404`, Adresse `/404`.
2. Einzige Sektion → Code-Block über die volle Breite → Inhalt von `21-404-codeblock.html` einfügen.
3. Seiten-Einstellungen (Zahnrad) → **SEO** → „Seite in Suchergebnissen ausblenden“ aktivieren.
4. **Einstellungen → Website → 404-Seite** (ältere Versionen: Einstellungen → Erweitert → 404-Seite) → `404` auswählen → Speichern.

Testen: `trutzstaehler.de/gibtsnicht` aufrufen.

---

## 3. SEO-Titel und -Beschreibungen

Für jede Seite: **Seiten → Zahnrad neben der Seite → SEO** → „SEO-Titel“ und „SEO-Beschreibung“ eintragen.
Die Titel haben höchstens etwa 60 Zeichen, die Beschreibungen höchstens etwa 155 Zeichen. So schneidet Google nichts ab.

| Seite | SEO-Titel | SEO-Beschreibung |
|---|---|---|
| Startseite `/` | Trutz Stähler – Papa, Autor, Läufer & Streamer aus Hamburg | Echt sein statt perfekt wirken: Kinderbücher aus dem Kreativhafen, Laufberichte aus Hamburg und WoW-Forever-Streams auf Twitch. |
| Über mich `/ueber-mich` | Über mich – Trutz Stähler aus Hamburg | Papa, Autor, Läufer und Streamer: wer hinter trutzstaehler.de steckt und warum hier echt sein mehr zählt als perfekt wirken. |
| Kreativhafen `/kreativhafen` | Kreativhafen – Kinderbücher & Malbücher von Trutz Stähler | Geschichten und Malbücher für Kinder aus Hamburg: Romane wie „Maria Holm“ und liebevoll gestaltete Malbücher zum Ausmalen. |
| Romane `/romane` | Kinderromane aus dem Kreativhafen – Trutz Stähler | Spannende Kinderbücher aus Hamburg. Entdecke „Maria Holm und das Geheimnis der verschwundenen Perle“ – als Buch und Kindle-E-Book. |
| Maria Holm `/maria-holm-und-das-geheimnis-der-verschwundenen-perle` | Maria Holm und das Geheimnis der verschwundenen Perle | Ein Kinderkrimi ab 8 Jahren, Tatort Hamburg: Maria Holm jagt eine verschwundene Perle. Mit Leseprobe – als Buch und Kindle-E-Book. |
| Malbücher `/malbuecher` | Malbücher aus dem Kreativhafen – Trutz Stähler | Malbücher für Kinder zum Entspannen und Kreativsein – jetzt auf Amazon erhältlich. |
| Running `/running` | Running – Laufberichte von Trutz Stähler | Halbmarathon, Puls 201 und ein Franzbrötchen im Ziel: ehrliche Laufberichte aus Hamburg, mit Splits, Bildern und ganz viel Herz. |
| Hella Half `/hella-half-marathon-2025` | Hella Half Marathon 2025 – mein Rennbericht | Party, Kampf & großes Herz: mein Hella Halbmarathon 2025 in Hamburg – Race-Day-Routine, die Wand bei km 14 und der Weg ins Ziel. |
| Twitch-Start `/twitch-startseite` | Trutz Stahl auf Twitch – WoW Forever & Stream-Zentrale | World of Warcraft Forever live auf Twitch: spiel im Chat mit, erstell deinen Helden und kämpf dich in die Bestenliste. |
| Live `/live` | Live & Stream-Plan – Trutz Stahl auf Twitch | Wann ich live bin: der Wochenplan für WoW-Forever-Streams auf Twitch, mit Stream und Chat direkt hier auf der Seite. |
| Mitspielen `/mitspielen` | Mitspielen im Stream – alle Chat-Befehle | So spielst du im Twitch-Chat mit: Schritt-für-Schritt-Anleitung, alle Befehle, Völker, Klassen und Ruf-Stufen. |
| Charakter `/charakter` | Charakter – dein Held aus dem Stream | Dein Chat-Held im Charakterfenster wie im Spiel: Stufe, Ausrüstung, Talente, Ruf und Erfolge auf einen Blick. |
| Bestenliste `/bestenliste` | Bestenliste – die stärksten Chat-Helden | Wer führt? Die Bestenliste der Chat-Helden nach Stufe, Ruf, Bossen, Angeln, Quiz, Duellen und mehr – Allianz gegen Horde. |
| Statistiken `/statistiken` | Statistiken – Zahlen aus dem Stream | Stream, Kanal, Spiele, Bosse und Glücksrad: alle Statistiken aus der Stream-Zentrale von Trutz Stahl. |
| Kontakt `/kontakt` | Kontakt – Trutz Stähler | Schreib mir per E-Mail, auf Instagram oder LinkedIn: moin@trutzstaehler.de. Ich melde mich fix zurück. |
| Impressum `/impressum` | Impressum – Trutz Stähler | Impressum von trutzstaehler.de. |
| Datenschutz | Datenschutzerklärung – Trutz Stähler | Datenschutzerklärung von trutzstaehler.de: welche Daten verarbeitet werden und welche Rechte du hast. |

**Live geprüft:** Alle Beschreibungen sind eingetragen. Zwei Kleinigkeiten fehlen noch:
- **Startseite:** Der SEO-Titel fehlt, im Browser-Tab steht nur „trutzstaehler.de“. Bitte den Titel aus der Tabelle eintragen.
- **Impressum:** Im SEO-Titel fehlt das „I“: „mpressum – Trutz Stähler“.

Für Impressum, Datenschutz und 404 außerdem „Seite in Suchergebnissen ausblenden“ aktivieren. Das ist optional, für die 404-Seite aber empfohlen.

**Website-weit:** **Einstellungen → SEO** (bzw. Marketing → SEO):
- **Format für Seitentitel:** nur `%p`. **Live geprüft:** Derzeit hängt Squarespace „ — trutzstaehler.de“ an jeden Titel. Zusammen mit den Titeln oben wird das zu lang und doppelt sich.
- **Website-Beschreibung:** den Text der Startseite von oben verwenden.

Am Ende **Marketing → SEO → Google Search Console** verbinden und die Sitemap `https://trutzstaehler.de/sitemap.xml` einreichen.

---

## 4. Bild für Social-Media-Vorschau und Favicon

Die fertigen Bilder liegen im Ordner `bilder/`.

**Bild für die Social-Media-Vorschau** (erscheint, wenn jemand den Link in WhatsApp, Instagram oder LinkedIn teilt):
- **Einstellungen → Website → Teilen in sozialen Medien → Social-Sharing-Bild** → `social-sharing-1200x630.png` hochladen.
- Für die sechs Twitch-Seiten jeweils: Seiten-Einstellungen (Zahnrad) → **Social-Bild** → `social-sharing-twitch-1200x630.png`.

**Favicon** (Symbol im Browser-Tab):
- **Einstellungen → Website → Browsersymbol (Favicon)** → `favicon-512.png` hochladen.

Testen: Link `https://trutzstaehler.de` in WhatsApp an dich selbst schicken. WhatsApp merkt sich alte Vorschauen, deshalb notfalls `https://trutzstaehler.de/?v=2` probieren.

---

## 5. Sprache auf Deutsch

**Einstellungen → Sprache und Region**:
- **Website-Sprache:** Deutsch
- **Land/Region:** Deutschland
- **Zeitzone:** Europa/Berlin

Damit kennzeichnet der Browser die Seite als deutsch. Das hilft bei Google und Vorlese-Programmen und sorgt für deutsche Squarespace-Texte, etwa im Cookie-Banner.

---

## 6. Cookie-Banner prüfen

**Einstellungen → Cookies & Besucherdaten** (bzw. Datenschutz & Sicherheit → Cookie-Banner):
1. **Cookie-Banner** einschalten.
2. **Banner-Typ:** „Opt-in und Opt-out“. Dann ist erst einmal nichts erlaubt, und Besucher wählen selbst.
3. **„Nicht notwendige Cookies einschränken“ / „Restrict non-essential cookies“** aktivieren. Das ist der wichtigste Haken: Analyse-Cookies laufen erst nach Zustimmung.
4. Texte und Buttons auf Deutsch prüfen. Der Link zur Datenschutzerklärung im Banner sollte auf deine Datenschutzseite zeigen.

Testen:
1. Seite in einem privaten Fenster öffnen.
2. Entwicklertools öffnen → Anwendung/Speicher → Cookies.
3. Vor dem Klick auf „Akzeptieren“ dürfen dort keine Analyse-Cookies stehen, zum Beispiel `ss_cvr` oder `ss_cvt`.

Die Pille „Cookie-Einstellungen“ ist im Design ausgeblendet. Besucher erreichen die Einstellungen über den Link „Cookie-Einstellungen“ unten im Footer.

---

## 7. Schriften selbst hosten statt Google Fonts (schneller und besser für den Datenschutz)

Derzeit lädt die Seite die Schriften von Google. Selbst gehostet fällt diese Verbindung weg: Die Seite lädt schneller, und es gehen keine IP-Adressen mehr an Google.

Die Schriften liegen fertig im Ordner `schriften/`. Es sind nur 6 Dateien, weil vier davon alle Stärken in einer Datei enthalten:

| Datei | Schrift |
|---|---|
| `syne-latin-wght-normal.woff2` | Syne (Überschriften) |
| `inter-latin-wght-normal.woff2` | Inter (Text) |
| `jetbrains-mono-latin-wght-normal.woff2` | JetBrains Mono (kleine Labels) |
| `cinzel-latin-wght-normal.woff2` | Cinzel (Twitch-Überschriften) |
| `asul-latin-400-normal.woff2` | Asul normal (Twitch-Text) |
| `asul-latin-700-normal.woff2` | Asul fett (Twitch-Text) |

Alle Schriften stehen unter der SIL Open Font License und dürfen frei verwendet werden.

1. **Website → Website-Werkzeuge → Benutzerdefiniertes CSS → „Benutzerdefinierte Dateien verwalten“** → die 6 Dateien hochladen.
2. Im CSS-Fenster nacheinander auf jede Datei klicken. Squarespace fügt dann ihre Adresse ein, etwa `https://static1.squarespace.com/static/…/syne-latin-wght-normal.woff2`.
3. **Schick mir diese 6 Adressen.** Das eingefügte CSS kannst du danach wieder löschen.
4. Ich tausche dann die Google-Links in Datei 01 und in den Twitch-Code-Blöcken gegen eigene `@font-face`-Regeln aus und passe die Datenschutzerklärung an: Der Abschnitt „Google Fonts“ entfällt.

---

## 8. Ladezeit messen

1. **https://pagespeed.web.dev** öffnen → `https://trutzstaehler.de` eingeben → **Analysieren**.
2. Den Reiter **Mobil** ansehen und mir Screenshots von diesen Teilen schicken:
   - die vier Kreise
   - „Leistung“ mit LCP, CLS und TBT
   - die Liste „Diagnose“
3. Das am besten für die Startseite, `/running` und `/twitch-startseite` machen.

Squarespace selbst bringt eigene Skripte mit, die ich nicht entfernen kann. Alles aus den Code-Blöcken kann ich aber gezielt verbessern.

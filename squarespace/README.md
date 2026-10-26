# Squarespace-Einbau · trutzstaehler.de

Design: Dark Editorial · Hintergrund `#060608` · Nebenfarbe Markengrün `#1d4d3f` · Akzente in Grüntönen: Mint `#6ee7b7`, Hellgrün `#4ade80`, Blassgrün `#a7f3d0` · Text `#f6faf7`, Muted `#9aaba3`.

| Datei | Wohin in Squarespace |
|---|---|
| `01-code-injection-header.html` | Website → Seiten → Benutzerdefinierter Code → Code Injection → **Header** |
| `02-code-injection-footer.html` | dieselbe Stelle → **Footer** |
| `03-startseite-hero-codeblock.html` | Startseite → oberste Sektion → **Code-Block** über die volle Rasterbreite |
| `04-startseite-neuerscheinung-codeblock.html` | Startseite → Sektion unter der Hero → **Code-Block** über die volle Rasterbreite |
| `05-kreativhafen-codeblock.html` | Seite `/kreativhafen` → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `06-ueber-mich-codeblock.html` | Seite `/ueber-mich` → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `07-running-codeblock.html` | Seite `/running` → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `08-hella-half-marathon-2025-codeblock.html` | Seite `/hella-half-marathon-2025` (nicht verlinkt) → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `09-romane-codeblock.html` | Seite `/romane` → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `10-maria-holm-codeblock.html` | Seite `/maria-holm-und-das-geheimnis-der-verschwundenen-perle` → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `11-malbuecher-codeblock.html` | Seite `/malbuecher` → einzige Sektion → **Code-Block** über die volle Rasterbreite |

### Kontakt & Rechtliches

| Datei | Wohin in Squarespace |
|---|---|
| `18-kontakt-codeblock.html` | Seite `/kontakt` → einzige Sektion → Code-Block (ohne Formular: E-Mail, 2× Instagram, LinkedIn) |
| `19-impressum-codeblock.html` | Seite `/impressum` → einzige Sektion → Code-Block |
| `20-datenschutz-codeblock.html` | Seite Datenschutzerklärung → einzige Sektion → Code-Block (Abschnitt „Cookies & Statistik“ mit den Squarespace-Einstellungen abgleichen) |

### Twitch-Bereich (World of Warcraft Forever)

Alle Seiten tragen die Klasse `tsw`: Navigation, Buttons und Footer werden dort automatisch golden, unter der Navigation erscheint die Twitch-Unternavigation mit „← Homepage“. Die Daten kommen weiter aus `helden.json` (Stream-Zentrale); die Skripte sind unverändert übernommen.

| Datei | Wohin in Squarespace |
|---|---|
| `12-twitch-startseite-codeblock.html` | Seite `/twitch-startseite` |
| `13-live-codeblock.html` | Seite `/live` (Wochenplan im Skript bei `CONFIG.schedule`) |
| `14-mitspielen-codeblock.html` | Seite `/mitspielen` |
| `15-charakter-codeblock.html` | Seite `/charakter` |
| `16-bestenliste-codeblock.html` | Seite `/bestenliste` |
| `17-statistiken-codeblock.html` | Seite `/statistiken` |

Jeweils: einzige Sektion → **Code-Block** über die volle Rasterbreite. Die Seiten `/live` bis `/statistiken` unter „Nicht verlinkt“ anlegen.
Die Originale liegen in `twitch-vorlage/`, `umbau-generator.py` erzeugt daraus die Seiten neu.

Die Datei 01 ist das globale Design-System und wird nur einmal eingefügt. Die Datei 02 enthält Navigation und JavaScript für alle Seiten.
Jede neue Sektion kommt später als eigener Code-Block dazu.

Seiten-URLs in der Navigation (in Datei 02 und 03 anpassen, falls deine anders lauten):
`/ueber-mich`, `/kreativhafen`, `/running`, `/twitch-startseite`, `/kontakt`

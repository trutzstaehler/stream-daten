# Twitch-Bereich – Teil 1 (gespeichert, noch nicht umgesetzt)

Gestaltung: eigener Stil im Look von **World of Warcraft Forever**, bewusst anders als das grüne Dark-Editorial-Design der übrigen Seiten.
Teil 2 folgt.

## Gelieferte Code-Blöcke (unverändert in `squarespace/twitch-vorlage/`)

| Datei | Inhalt |
|---|---|
| `kopfzeile-codeblock.html` | Eigene Navigation „Trutz Stahl“ mit Wappen, Menü und Button „Zum Stream“ |
| `fusszeile-codeblock.html` | Eigene Fußzeile mit Seiten, Twitch, Instagram, Impressum und Blizzard-Hinweis |
| `mitspielen-codeblock.html` | Anleitung zum Mitspielen im Chat: Schritte, alle Befehle mit Suche, Völker & Klassen, Ruf-Stufen |
| `bestenliste-codeblock.html` | Bestenliste der Chat-Helden mit Reitern (Stufe, Ruf, Rang, Vermächtnis, Darkspear-Inseln, Bosse, Gegner, Angeln, Quiz, Duelle, Berufe) und Filter Allianz/Horde |
| `charaktere-codeblock.html` | Charakterfenster wie im Spiel; Suche nur über den vollständigen Namen oder Link (`/charakter#login`) |

## Eckdaten aus den Dateien

- **Markenname im Twitch-Bereich:** „Trutz Stahl“ (Streamer-Name), Kanal `einfach_trutz`, Gilde/Ruf „bei Stahlgarde“
- **Seiten laut Navigation:** `/` (Start), `/live`, `/mitspielen`, `/charakter`, `/bestenliste`, `/statistiken`
- **Schriften:** Cinzel (Überschriften), Asul (Text)
- **Farben:** Gold `#ffd100`, Text `#f3eee2`, gedämpft `#b8ad94`, Messing `#8c713c`, Linien `#4a4a4a`, Hintergrund `#120e0b`
- **Daten:** `https://raw.githubusercontent.com/trutzstaehler/stream-daten/main/helden.json` (dieses Repo, wird von der Stream-Zentrale aktualisiert); ohne Daten erscheinen Beispieldaten
- **Icons:** Wowhead (`wow.zamimg.com`)
- **Rechtlicher Hinweis in der Fußzeile:** World of Warcraft ist eine Marke von Blizzard Entertainment; Fan-Projekt ohne Verbindung zu Blizzard

## Offene Fragen für die Umsetzung

- Liegen `/live`, `/mitspielen`, `/charakter`, `/bestenliste`, `/statistiken` auf trutzstaehler.de neben den übrigen Seiten? Dann zeigt „Start“ (`/`) auf die neue Startseite – eventuell soll er auf `/twitch-startseite` zeigen.
- Sollen auf diesen Seiten die globale grüne Navigation und der Footer ausgeblendet und durch Kopf- und Fußzeile im WoW-Stil ersetzt werden?
- Für `/statistiken` und `/live` fehlen noch Code-Blöcke (eventuell in Teil 2).
- In der Fußzeile ist der Datenschutz-Link auskommentiert; auf der übrigen Seite gibt es eine Datenschutzerklärung.

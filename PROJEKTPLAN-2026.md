# Projekt: trutzstaehler.de zur „besten Homepage 2026“ machen

## Ausgangslage
- Website: https://trutzstaehler.de (Squarespace, eigenes Design mit Custom-Code)
- Person: Trutz Stähler – Papa, Autor, Läufer & Streamer aus Hamburg
- Motto/Leitsatz: „Echt sein statt perfekt wirken.“
- Drei Welten:
  1. Kreativhafen – Kinderkrimi „Maria Holm und das Geheimnis der verschwundenen Perle“ (ab 8, spielt in Speicherstadt/Hafen), „Mein erstes Tiere-Kritzelbuch“ und „Große Dinomotive zum Ausmalen“ (ab 1 Jahr)
  2. Running – Laufberichte (Alster, Niendorfer Gehege, Halbmarathon)
  3. Twitch – „einfach_trutz“ / „Trutz Stahl“, World of Warcraft Forever, Chat-Spiel mit Helden, Ruf-Stufen („Stahlgarde“) und Bestenliste
- Unterseiten: /ueber-mich, /kreativhafen, /running, /twitch-startseite, /shop (OBS-Stream-Widgets + Bücher), /kontakt, Buchseiten, Rechtliches
- Stream-Daten liegen als JSON im GitHub-Repo trutzstaehler/stream-daten (Datei helden.json) mit: updated, streamer, channel, repBei, ladder (Neutral 0 → Freundlich 3000 → Wohlwollend 9000 → Respektvoll 21000 → Ehrfürchtig 42000), totals (aktuell 1 Held, 0 Bosse, 1 Gegner), commands (Chat-Befehle wie !rad, !quest, !umfrage), characters, items, achievements
- Ziel: Award-tauglich werden (z. B. Awwwards; Bewertung nach meinem Kenntnisstand ca. Design 40 %, Bedienbarkeit 30 %, Kreativität 20 %, Inhalt 10 % – vor Einreichung aktuelle Kriterien prüfen)

## Was schon gut ist
- Starkes, eigenständiges dunkles Design (Grün-Akzent), große Typo-Headline mit ausgehöhltem „perfekt“
- Scrollgesteuerte „Drei Welten“-Strecke: 3D-Buch, animierte Alster-Karte mit km-Zähler, WoW-Siegel – jede Welt mit eigener Farbe
- Saubere Seitentitel, Meta-Beschreibungen und Vorschaubilder für Social Media auf allen Unterseiten, Person-Schema, Alt-Texte, Skip-Link, Rücksicht auf „weniger Bewegung“, kein Layout-Springen, eigene 404-Seite
- robots.txt lässt Suchmaschinen und KI-Crawler zu (sperrt nur Systemordner)

## Gemessene Probleme (Okt. 2026)
- Handy: Überschrift „Bücher aus dem Kreativhafen.“ bricht hässlich um zu „Kreativhaf / en.“
- Cookie-Banner verdeckt beim ersten Besuch die Hero-Buttons (Desktop) bzw. den halben Bildschirm (Handy), Text zu lang
- Startseite: ca. 1,5 MB, 42 Requests, 39 Skripte (Squarespace lädt auch Commerce-/Account-CSS). Größtes Element nach 1,2 s (Handy-Ansicht) bzw. 2,6 s (Desktop), gemessen über schnelle Leitung
- og:image und twitter:image mit http:// statt https://
- twitter:card = „summary“ statt „summary_large_image“
- WebSite-Schema hat leere description
- Einige Links/Buttons kleiner als 24 px (schwer zu tippen)
- Keine llms.txt

---

## AUF JEDEN FALL umsetzen

### A) Grundlagen reparieren (Pflicht, sonst raus bei der Jury)
1. Handy-Umbruch „Kreativhafen“ fixen (Schriftgröße per clamp() verkleinern oder gezielte Trennstelle „Kreativ-hafen“)
2. Cookie-Banner als schmale Leiste unten, kurzer Text, verdeckt keine Buttons
3. Ladezeit: Ziel PageSpeed 90+ am Handy – Hauptschrift vorladen (preload), Animations-Skripte verzögert laden, Bilder als WebP/AVIF, Effekte erst nach dem Inhalt laden
4. Meta-Fixes: og:image auf https, twitter:card auf summary_large_image, WebSite-Beschreibung in den Squarespace-SEO-Einstellungen füllen
5. Barrierefreiheit: Touch-Flächen mind. 24 px (besser 44 px), Scroll-Strecke mit Tastatur und Screenreader testen
6. Handy gleichwertig zum Desktop: jede besondere Funktion braucht eine durchdachte Handy-Version

### B) Ideen, die die Seite unverwechselbar machen
7. HAMBURGER HAFEN ALS KARTE (Leitidee): gezeichnete, interaktive Karte als „Entdecken“-Modus – Speicherstadt = Kreativhafen, Alster = Running, Taverne/Leuchtturm = Twitch. Normale Navigation bleibt daneben bestehen. Gezeichnete 2D-Karte reicht, kein aufwendiges 3D nötig. (Inspiration: Bruno Simon Portfolio, „Messenger“ von abeto)
8. DEINE HANDSCHRIFT: Kritzel-Striche im Stil der Malbücher, handgeschriebene Randnotizen, echte Fotos statt Stockbildern. (Inspiration: Lando-Norris-Website mit eigenen Kritzeleien)
9. „MOIN“-GRUSS: 10-Sekunden-Audio oder -Video von Trutz auf der Über-mich-Seite
10. HAMBURG IN ECHTZEIT: Tag/Nacht nach Hamburger Uhrzeit, bei Regen in Hamburg leichter Regen-Effekt, während des Streams gehen im Hafen die Lichter an
11. LIVE-STATUS: „Jetzt live“ bzw. „Nächster Stream: …“ auf der Startseite + grüner Punkt im Browser-Tab (Favicon), wenn live
12. PERLENJAGD: 5 schwarze Perlen (Bezug zu „Maria Holm“) auf den Unterseiten versteckt; wer alle findet, bekommt eine exklusive Leseprobe oder ein Ausmalbild
13. 3D-BUCH AUFSCHLAGEN: das vorhandene Buch auf der Startseite klickbar machen und 2–3 Seiten der Leseprobe durchblättern lassen
14. RUF-LEISTE & HELDEN aus helden.json: WoW-Rufleiste (Neutral → Ehrfürchtig) und Helden-Karten mit Items/Erfolgen. Solange es wenige Helden gibt (aktuell 1): „Werde der erste Held“ statt leerer Bestenliste
15. WEICHE SEITENÜBERGÄNGE: View Transitions API (per CSS @view-transition auch auf Squarespace möglich), Logo/Überschrift gleiten beim Seitenwechsel
16. TAB-TITEL beim Verlassen: „Maria braucht deine Hilfe!“
17. STRUKTURIERTE DATEN FÜR BÜCHER: Schema „Book“ mit ISBN, Preis, Bewertungen (für Sterne/Preis in Google)
18. „WIE DIESE SEITE ENTSTAND“: Bericht mit Ideen, Skizzen und Technik – auch auf Englisch (internationale Jury). Wird für die Award-Einreichung gebraucht; dazu gute Bilder und ein kurzes Video der Scroll-Strecke

---

## SPÄTER, wenn Zeit bleibt
- Ausmalen im Browser: ein Motiv aus dem Malbuch online ausmalen und als PDF drucken
- Echte Laufdaten: GPX-Strecke auf der Alster-Karte, Jahreskilometer, Zwischenzeiten-Diagramme
- „Jetzt“-Seite: was Trutz gerade schreibt, läuft, spielt
- Lesungen buchen: Angebot für Schulen, Kitas, Buchhandlungen + Pressemappe
- Newsletter „Hafenpost“
- Druckansicht für Ausmalbilder und Leseproben (ohne dunklen Hintergrund)
- Barrierefreiheitserklärung (als Kleinstunternehmen vermutlich nicht Pflicht, wirkt aber gut)
- Statistik ohne Cookies (Plausible/Fathom) – evtl. kann das Cookie-Banner dann wegfallen (prüfen, ob Squarespace selbst Cookies setzt)
- llms.txt für KI-Suchmaschinen
- Sound zum Einschalten (Möwen/Schiffshorn, Schritte, Taverne), standardmäßig aus
- Live-Anwesenheit: andere Besucher als kleine Boote, Zuschauer-Helden laufen während des Streams über die Seite
- Spickzettel der Chat-Befehle aus helden.json

## BEWUSST WEGLASSEN
- Easter Egg (Konami-Code) – die Perlenjagd erfüllt den Zweck besser
- Intro-/Ladebildschirm – kostet Zeit, nervt viele
- Chatbot „Frag Trutz“ – bei Kinderpublikum zu viel Risiko (Datenschutz) für wenig Nutzen
- „Lauf mit mir“-Termine und Galerie mit Kinderbildern – schön, aber nicht für die Website bzw. hoher Datenschutz-Aufwand

## OFFENE ENTSCHEIDUNG (vor der Hafenkarte klären)
- Option 1: Bei Squarespace bleiben, interaktive Teile als Code-Blöcke einbetten → einfacher, aber begrenzt (Ladezeit, Kontrolle)
- Option 2: Eigene Hauptseite (z. B. Astro), Squarespace nur noch für Shop/Zahlung → mehr Aufwand, volle Kontrolle, meist schneller

## REIHENFOLGE
1. Grundlagen reparieren (Punkte 1–6), ca. 1–2 Tage
2. Schnelle Treffer: Seitenübergänge, Tab-Titel, Buch-Schema, Live-Status + Favicon (Punkte 15, 16, 17, 11)
3. Ruf-Leiste & Helden, Buch aufschlagen, Perlenjagd (Punkte 14, 13, 12)
4. Hafenkarte + Hamburg in Echtzeit + Handschrift + Moin-Gruß (Punkte 7, 10, 8, 9) – vorher Technik-Entscheidung treffen
5. Entstehungsbericht (DE/EN) schreiben, Bilder/Video erstellen, einreichen (Punkt 18)

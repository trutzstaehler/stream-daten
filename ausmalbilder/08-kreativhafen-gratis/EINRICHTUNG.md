# Kreativhafen gratis: Einrichtung

**Aufbau:** Kreativhafen (Hauptkategorie) → **Gute-Nacht-Geschichten** (direkt auf der Seite lesen) · **Ausmalbilder** (kostenlos herunterladen) · **Malbücher** und **Romane** (deine Bücher zum Kaufen).

Alle Code-Blöcke liegen in diesem Ordner (`08-kreativhafen-gratis/`). Die Reihenfolge unten ist die beste Reihenfolge zum Einrichten. Zeitbedarf: etwa 2 Stunden, davon die meiste Zeit für die 24 Geschichten.

---

## Schritt 0: Daten auf GitHub freischalten (einmalig, wichtig!)

Ausmalbilder, PDFs und Vorschaubilder lädt die Seite, wie deine Twitch-Seite die Datei `helden.json`, aus deinem Repo:
`https://raw.githubusercontent.com/trutzstaehler/stream-daten/main/kreativhafen/`

Die Dateien liegen im Ordner `kreativhafen/` im Branch **`ausmalbilder-saison-2026`**. Damit die Adresse oben funktioniert, muss der Ordner in **`main`** liegen:

1. Auf GitHub `trutzstaehler/stream-daten` öffnen → „Compare & pull request“ für `ausmalbilder-saison-2026` → Pull Request erstellen → **Merge**. (Ich kann den Pull Request auch für dich anlegen.)
2. Kurz testen: `https://raw.githubusercontent.com/trutzstaehler/stream-daten/main/kreativhafen/ausmalbilder/daten/katalog.json` im Browser öffnen. Es muss Text erscheinen, kein „404“.

Solange das nicht passiert ist, zeigen die Ausmalbilder-Seite und die Bilder „konnten nicht geladen werden“.

---

## Schritt 1: Kreativhafen-Seite (`/kreativhafen`)

1. **Ganz oben** einen Code-Block einfügen mit dem Inhalt von `01_reiter-leiste_fuer-kreativhafen-malbuecher-romane.html`. Das ist die Reiter-Leiste: Übersicht · Gute-Nacht-Geschichten · Ausmalbilder · Malbücher · Romane.
2. **Direkt unter dem Regal „Bücher“** einen Code-Block mit `02_regal-gratis-im-hafen_fuer-kreativhafen.html` einfügen. Das neue Regal „Gratis im Hafen“ mit den Karten 03 Ausmalbilder und 04 Gute-Nacht-Geschichten nutzt dieselbe Karten-Optik wie deine Bücher.

## Schritt 2: Malbücher und Romane (`/malbuecher`, `/romane`)

Auf beiden Seiten ganz oben denselben Reiter-Block (`01_…`) einfügen. Dann ist der Kreativhafen von jeder Unterseite aus erreichbar.

## Schritt 3: Seite „Ausmalbilder“ (`/ausmalbilder`)

1. Neue Seite anlegen (nicht in der Hauptnavigation; sie ist über den Kreativhafen erreichbar), URL-Slug `ausmalbilder`.
2. Zwei Code-Blöcke untereinander: `03-1_seite-ausmalbilder_teil-1-von-2.html`, darunter `03-2_…teil-2-von-2.html`.
3. SEO-Titel: `Ausmalbilder kostenlos zum Ausdrucken – 112 Motive für Kinder | Kreativhafen`
4. SEO-Beschreibung: `112 kostenlose Ausmalbilder für Kinder ab 2: Hamburger Hafen, Fahrzeuge, Weltraum, Halloween, Laterne, Adventskalender und mehr. Einzeln drucken oder als PDF laden.`
5. Social-Bild: `../02-bilder/website/og-ausmalbilder.jpg`

## Schritt 4: Seite „Gute-Nacht-Geschichten“ (`/gute-nacht-geschichten`)

1. Neue Seite, URL-Slug `gute-nacht-geschichten`, ein Code-Block: `04_seite-gute-nacht-geschichten.html`.
2. SEO-Titel: `Gute-Nacht-Geschichten zum Vorlesen – kostenlos | Kreativhafen`
3. SEO-Beschreibung: `24 kostenlose Gute-Nacht-Geschichten zum Vorlesen für Kinder von 2 bis 7: kurz, ruhig und mit Ausmalbild. Von Möwe Mats aus dem Hamburger Hafen bis zum Drachen Funki.`

## Schritt 5: Die 24 Geschichten (Blog „Geschichten“)

Jede Geschichte bekommt ihre eigene Seite. So findet Google jede einzelne, genau wie bei Zitronenbande und Zwergenstark.

1. **Seiten → + → Blog** anlegen, Name „Geschichten“, URL-Slug **`geschichten`**, nicht in der Navigation anzeigen (die Übersicht ist `/gute-nacht-geschichten`).
2. Für jede Geschichte einen **Beitrag** anlegen:
   - **Titel** = Titel der Geschichte
   - **URL** (Beitragseinstellungen → Inhalt) = Slug aus der Tabelle
   - **Inhalt:** alles löschen → Code-Block → Inhalt der Datei aus der Tabelle einfügen
   - **Auszug / SEO-Beschreibung** = Teaser aus der Tabelle
   - **Vorschaubild** = Bild aus der Tabelle (für Google und Social Media)
   - **Autor:** Trutz Stähler
3. Wenn dein Blog-Layout Titel und Datum über dem Beitrag anzeigt, im Blog-Design „Titel/Datum/Autor ausblenden“ wählen. Die Geschichte bringt ihre eigene Überschrift mit.

| # | Titel | URL-Slug | Code-Block | Vorschaubild | Teaser (Auszug/SEO) |
|---|---|---|---|---|---|
| 01 | Möwe Mats will nicht schlafen | `moewe-mats-will-nicht-schlafen` | `geschichten/01_moewe-mats-will-nicht-schlafen.html` | `02-bilder/motive-ausgemalt/hf03.png` | Im Hafen ist abends noch so viel los – da kann Möwe Mats doch unmöglich schlafen gehen! Oder leuchtet der Hafen vielleicht auch ohne sie weiter? |
| 02 | Leuchtturm Lotte und der Nebel | `leuchtturm-lotte-und-der-nebel` | `geschichten/02_leuchtturm-lotte-und-der-nebel.html` | `02-bilder/motive-ausgemalt/hf02.png` | Leuchtturm Lotte findet ihr Licht viel zu klein. Doch in einer nebligen Nacht braucht ein kleines Boot genau dieses Licht, um nach Hause zu finden. |
| 03 | Die Fähre Frieda fährt nach Hause | `die-faehre-frieda-faehrt-nach-hause` | `geschichten/03_die-faehre-frieda-faehrt-nach-hause.html` | `02-bilder/motive-ausgemalt/hf06.png` | Es ist die letzte Fahrt des Tages: Hafenfähre Frieda bringt alle nach Hause – müde Menschen, einen schnarchenden Hund und ein Kind mit einer roten Mütze. |
| 04 | Ein Schlaflied für Kran Karl | `ein-schlaflied-fuer-kran-karl` | `geschichten/04_ein-schlaflied-fuer-kran-karl.html` | `02-bilder/motive-ausgemalt/hf05.png` | Kran Karl ist der größte Kran im Hafen – und heute Abend ist er so müde wie noch nie. Zum Glück hat ein Kind am Ufer eine Idee. |
| 05 | Das kleine Gespenst Huhu | `das-kleine-gespenst-huhu` | `geschichten/05_das-kleine-gespenst-huhu.html` | `02-bilder/motive-ausgemalt/hw02.png` | Huhu ist ein Gespenst – und fürchtet sich vor allem. Sogar vor sich selbst im Spiegel. Doch in der Halloween-Nacht klopft jemand an seine Tür. |
| 06 | Die Laterne, die sich vor dem Wind fürchtete | `die-laterne-die-sich-vor-dem-wind-fuerchtete` | `geschichten/06_die-laterne-die-sich-vor-dem-wind-fuerchtete.html` | `02-bilder/motive-ausgemalt/lt01.png` | Lina die Laterne soll beim Laternenumzug leuchten. Doch draußen weht der Novemberwind – und Lina hat Angst, dass er ihr Licht auspustet. |
| 07 | Wichtel Wilbur und das Warten | `wichtel-wilbur-und-das-warten` | `geschichten/07_wichtel-wilbur-und-das-warten.html` | `02-bilder/motive-ausgemalt/ad13.png` | Jede Nacht bewacht der kleine Wichtel Wilbur ein Türchen im Adventskalender. Doch das Warten fällt ihm so schwer – bis er entdeckt, wie schön es sein kann. |
| 08 | Der Schneemann, der die Sterne sehen wollte | `der-schneemann-der-die-sterne-sehen-wollte` | `geschichten/08_der-schneemann-der-die-sterne-sehen-wollte.html` | `02-bilder/motive-ausgemalt/wi01.png` | Schneemann Kalle steht im Garten und schaut jede Nacht zu den Sternen hinauf. Wie gern würde er sie einmal von Nahem sehen! Zum Glück hat er gute Freunde. |
| 09 | Funki, der kleine Drache | `funki-der-kleine-drache` | `geschichten/09_funki-der-kleine-drache.html` | `02-bilder/motive-ausgemalt/mf02.png` | Alle Drachen im Tal können Feuer spucken – nur Funki nicht. Aus seinem Maul kommt bloß warme Luft. Doch in einer eisigen Nacht wird genau das zu etwas ganz Besonderem. |
| 10 | Ella fliegt zum Mond | `ella-fliegt-zum-mond` | `geschichten/10_ella-fliegt-zum-mond.html` | `02-bilder/motive-ausgemalt/wr01.png` | Ella kann nicht einschlafen – also baut sie aus ihrem Bett eine Rakete. Gemeinsam mit Kuschelhase Momo fliegt sie bis zum Mond, um ihm persönlich gute Nacht zu sagen. |
| 11 | Bagger Bruno macht Feierabend | `bagger-bruno-macht-feierabend` | `geschichten/11_bagger-bruno-macht-feierabend.html` | `02-bilder/motive-ausgemalt/fz03.png` | Bagger Bruno liebt seine Baustelle so sehr, dass er abends einfach nicht aufhören will zu baggern. Bis ein alter Kran ihm verrät, was Bagger in der Nacht Schönes erleben. |
| 12 | Teddy hält Wache | `teddy-haelt-wache` | `geschichten/12_teddy-haelt-wache.html` | `02-bilder/motive-ausgemalt/ad17.png` | Jede Nacht, wenn Noah schläft, öffnet sein Teddy Brummel ganz leise die Augen. Denn er hat eine wichtige Aufgabe: Er hält Wache. Und dabei entdeckt er, wie friedlich die Nacht sein kann. |
| 13 | Mats und das Schietwetter | `mats-und-das-schietwetter` | `geschichten/13_mats-und-das-schietwetter.html` | `02-bilder/motive-ausgemalt/hf08.png` | Regen, Wind und graue Wolken über dem Hafen – Möwe Mats findet das Wetter doof. Bis sie merkt, wie gemütlich Regen klingen kann. |
| 14 | Mats sucht ihre Lieblingsfeder | `mats-sucht-ihre-lieblingsfeder` | `geschichten/14_mats-sucht-ihre-lieblingsfeder.html` | `02-bilder/motive-ausgemalt/hf04.png` | Mats hat eine ganz besondere Feder mit einem silbernen Glanz – und plötzlich ist sie weg! Der ganze Hafen hilft beim Suchen. |
| 15 | Mats hat Geburtstag | `mats-hat-geburtstag` | `geschichten/15_mats-hat-geburtstag.html` | `02-bilder/motive-ausgemalt/gb01.png` | Heute ist Mats’ Geburtstag! Am Hamburger Hafen wird gefeiert – mit Fischbrötchen-Torte, Hupkonzert und einem Lichtgeschenk von Lotte. |
| 16 | Mats und die Sternschnuppe | `mats-und-die-sternschnuppe` | `geschichten/16_mats-und-die-sternschnuppe.html` | `02-bilder/motive-ausgemalt/wr08.png` | In einer klaren Nacht saust eine Sternschnuppe über den Hafen. Mats darf sich etwas wünschen – aber was nur? |
| 17 | Das kleine Auto fährt nach Hause | `das-kleine-auto-faehrt-nach-hause` | `geschichten/17_das-kleine-auto-faehrt-nach-hause.html` | `02-bilder/motive-ausgemalt/fz01.png` | Den ganzen Tag ist das kleine Auto gefahren. Jetzt wird es dunkel – Zeit, nach Hause zu fahren und allen gute Nacht zu sagen. |
| 18 | Gute Nacht, Obstkorb | `gute-nacht-obstkorb` | `geschichten/18_gute-nacht-obstkorb.html` | `02-bilder/motive-ausgemalt/og01.png` | In der Küche steht ein Obstkorb. Apfel, Banane und die zwei Kirschen sind schon ganz müde – und sagen sich gute Nacht. |
| 19 | Das Flugzeug landet am Abend | `das-flugzeug-landet-am-abend` | `geschichten/19_das-flugzeug-landet-am-abend.html` | `02-bilder/motive-ausgemalt/fz06.png` | Hoch über den Wolken fliegt ein kleines Flugzeug. Jetzt geht die Sonne unter – und das Flugzeug fliegt nach Hause. |
| 20 | Die Luftballons wollen noch nicht schlafen | `die-luftballons-wollen-noch-nicht-schlafen` | `geschichten/20_die-luftballons-wollen-noch-nicht-schlafen.html` | `02-bilder/motive-ausgemalt/gb02.png` | Die Party ist vorbei, aber die drei Luftballons wollen noch weiter tanzen. Bis sie merken, wie gemütlich es auch ganz ruhig sein kann. |
| 21 | Ritter Rasmus und die Angst vor dem Dunkeln | `ritter-rasmus-und-die-angst-vor-dem-dunkeln` | `geschichten/21_ritter-rasmus-und-die-angst-vor-dem-dunkeln.html` | `02-bilder/motive-ausgemalt/mf07.png` | Rasmus ist der kleinste Ritter der Burg – und nachts knarrt und knackt es überall. Mit Schild, Holzschwert und Laterne macht er sich auf, das Geheimnis der Geräusche zu lüften. |
| 22 | Nixe Nele schwimmt in den Hafen | `nixe-nele-schwimmt-in-den-hafen` | `geschichten/22_nixe-nele-schwimmt-in-den-hafen.html` | `02-bilder/motive-ausgemalt/mf08.png` | Die kleine Meerjungfrau Nele will wissen, wohin die großen Schiffe fahren. Also schwimmt sie von der Nordsee die Elbe hinauf – bis mitten in den Hamburger Hafen. |
| 23 | Robo lernt träumen | `robo-lernt-traeumen` | `geschichten/23_robo-lernt-traeumen.html` | `02-bilder/motive-ausgemalt/wr06.png` | Robo ist ein kleiner Roboter, der alles kann – nur nicht schlafen. Denn er hat keinen Aus-Knopf zum Träumen. Oder vielleicht doch? |
| 24 | Das Einhorn, das seinen Regenbogen verlor | `das-einhorn-das-seinen-regenbogen-verlor` | `geschichten/24_das-einhorn-das-seinen-regenbogen-verlor.html` | `02-bilder/motive-ausgemalt/mf01.png` | Einhorn Fiona kann Regenbögen an den Himmel zaubern – bis ihr eines Morgens die Farben fehlen. Zum Glück helfen ihr ihre Freunde, sie wiederzufinden. |

## Schritt 6: Startseite

`05_teaser-startseite.html` als Code-Block auf der Startseite einfügen, z. B. unter „Bücher aus dem Kreativhafen“. Die Überschrift wechselt mit der Saison.

## Schritt 7: Testen

- `/kreativhafen`: Reiter oben, darunter die Regale Bücher und „Gratis im Hafen“
- `/ausmalbilder`:
  - Pakete mit Bild
  - „PDF“ lädt die Datei
  - „Drucken“ öffnet die Druckansicht
  - „Ausmalen“ holt das Motiv ins Mal-Werkzeug
- `/gute-nacht-geschichten`: Suche und Filter funktionieren, „Für heute Abend“ zeigt eine Geschichte
- eine Geschichte öffnen und prüfen:
  - Nachtmodus
  - A−/A+
  - „Vorlesen lassen“
  - Ausmalbild drucken
- alles auch am Handy

---

## Wichtig: Datenschutz und Texte

1. **Datenschutzerklärung:** Die Seiten laden Bilder und Daten von **GitHub** (`raw.githubusercontent.com`, GitHub Inc., USA). Dabei wird die IP-Adresse der Besucher an GitHub übertragen. Deine Twitch-Seite macht das schon heute mit `helden.json`. Prüfe, ob GitHub in deiner Datenschutzerklärung steht, und ergänze sonst einen Absatz. Dazu ein Satz zum Mal-Werkzeug und zum Nachtmodus: *„Das Mal-Werkzeug und die Leseeinstellungen speichern Daten ausschließlich lokal in deinem Browser (localStorage); es wird nichts an uns übertragen.“*
2. **Die Geschichten und Motive habe ich als KI geschrieben bzw. gezeichnet.** Lies jede Geschichte vor dem Veröffentlichen einmal selbst und passe sie an deine Art zu erzählen an. Dann sind es wirklich deine Geschichten. Rein KI-generierte Texte und Bilder sind nach deutschem Recht wahrscheinlich nicht urheberrechtlich geschützt. Durch deine Überarbeitung wird deine Position stärker.
3. **„Vorlesen lassen“** nutzt die eingebaute Computerstimme des Geräts. Die Qualität hängt vom Gerät ab. Eigene Aufnahmen („Papa liest vor“) lassen sich später einfach ergänzen: In `quelle/geschichten/*.py` bei der Geschichte `audio='https://…/datei.mp3'` eintragen und neu erzeugen. Dann erscheint ein Audio-Player über dem Text.

## Neu erzeugen nach Änderungen

```bash
cd ausmalbilder/quelle
python3 export.py             # Motive/Bilder für GitHub (Ordner kreativhafen/)
python3 gratis_pdf.py         # PDFs + ZIP der Ausmalbilder
python3 kreativhafen_web.py   # alle Code-Blöcke + Vorschau
python3 kh_doku.py            # diese Anleitung
```

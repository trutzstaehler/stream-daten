# Die 24 Gute-Nacht-Geschichten im Blog anlegen

Jede Geschichte bekommt eine **eigene Seite** unter `trutzstaehler.de/geschichten/…`, genau wie bei Zitronenbande und Zwergenstark. So findet Google jede Geschichte einzeln. Die Übersicht `/gute-nacht-geschichten` verlinkt automatisch auf diese Adressen.

**Was du brauchst** (alles in der ZIP „Kreativhafen_Komplett“):
- `01_Code-Bloecke_fuer-Squarespace/geschichten_je-ein-Blog-Beitrag/`: eine HTML-Datei pro Geschichte
- `03_Bilder/Vorschaubilder-Geschichten_fuer-Blog-Beitraege/`: ein JPG pro Geschichte

**Zeit:** Einmal einrichten etwa 10 Minuten, danach etwa 3 Minuten pro Geschichte. Du musst nicht alle auf einmal machen. Die Übersicht verlinkt zwar sofort alle 24 Geschichten, also am besten an einem Abend alle anlegen oder die Übersicht erst danach veröffentlichen.

> Die Menünamen in Squarespace können je nach Version leicht abweichen (z. B. „Optionen“ statt „Inhalt“). Gemeint ist immer das Einstellungsfenster des Beitrags.

---

## Teil A: Den Blog einmalig anlegen

1. Links im Menü **Seiten** öffnen.
2. Ganz unten bei **„Nicht verlinkt“** auf **+** klicken → **Blog** wählen. Ein beliebiges Layout nehmen, das Aussehen spielt keine Rolle. Die Geschichten bringen ihr eigenes Design mit.
   *„Nicht verlinkt“ ist wichtig: So erscheint der Blog nicht in deiner Hauptnavigation. Besucher kommen über den Kreativhafen und die Übersicht `/gute-nacht-geschichten`.*
3. Den Blog **„Geschichten“** nennen.
4. Beim Blog auf das **Zahnrad** (Seiteneinstellungen) → **URL-Slug** auf **`geschichten`** setzen → Speichern.
   *Genau dieser Slug ist nötig, weil alle Links auf `/geschichten/…` zeigen.*
5. Die **Beispiel-Beiträge**, die Squarespace mitliefert, löschen.
6. Optional: In den Blog-Einstellungen **Kommentare** einschalten (wie „Was sagst du zur Geschichte?“ bei Zitronenbande). Wenn du das nicht willst, einfach aus lassen.

7. **Wichtig, einmalig: CSS eintragen.** Öffne **Website → Design → Benutzerdefiniertes CSS** und füge den Inhalt der Datei `06_custom-css_blog-geschichten.css` ein (ans Ende, falls dort schon etwas steht) → Speichern.
   Das blendet bei allen Geschichten den Squarespace-Beitragstitel, Datum/Autor und die Vor/Zurück-Leiste aus und gibt der Reiter-Leiste die volle Breite. Ohne diesen Schritt steht der Titel doppelt da und die Reiter-Leiste ist ein kleines, seitlich rollendes Fenster. (Die neuen Geschichten-Blöcke enthalten das CSS zusätzlich selbst; der Eintrag im Design sorgt dafür, dass es auch bei bereits eingefügten älteren Blöcken greift.)

---

## Teil B: Eine Geschichte anlegen (für jede der 24 wiederholen)

1. Im Blog „Geschichten“ auf **+** (Beitrag hinzufügen) klicken.
2. **Titel** eintragen (aus dem Steckbrief unten).
3. Im Textfeld darunter den Platzhaltertext löschen, dann **Block hinzufügen → Code** wählen.
4. Die passende Datei aus `geschichten_je-ein-Blog-Beitrag/` öffnen (Rechtsklick → Öffnen mit → Texteditor/TextEdit), **alles markieren (Strg/Cmd + A), kopieren** und in den Code-Block einfügen.
   - Im Code-Block muss **HTML** eingestellt sein, und **„Quellcode anzeigen“** muss **aus** sein.
   - Im Editor sieht man nur einen Platzhalter „Script deaktiviert“ o. Ä.; das ist normal. Die Geschichte erscheint erst in der Vorschau bzw. auf der echten Seite.
5. **Einstellungen** des Beitrags öffnen (Zahnrad bzw. „…“ → Einstellungen):
   - **URL** (bzw. „Beitrags-URL“): den Slug aus dem Steckbrief eintragen. Im Feld steht dann `/geschichten/moewe-mats-will-nicht-schlafen` o. Ä.
   - **Auszug:** Text aus dem Steckbrief
   - **Beitragsbild/Miniaturbild:** das JPG aus `03_Bilder/Vorschaubilder…` hochladen (gleicher Name wie der Slug)
   - **Kategorie** und **Tags** wie im Steckbrief (optional, hilft beim Ordnen)
   - **Autor:** Trutz Stähler
   - Reiter **SEO:** SEO-Titel und SEO-Beschreibung aus dem Steckbrief
6. Speichern → **Veröffentlichen**.
7. Kurz testen: `trutzstaehler.de/geschichten/<slug>` aufrufen. Die Geschichte muss mit Bild, Reiter-Leiste und „Vorlesen“-Leiste erscheinen.

**Schneller arbeiten:** Wenn die erste Geschichte fertig ist, kannst du sie in der Beitragsliste über „…“ → **Duplizieren** kopieren. Dann nur noch Titel, URL, Code-Block-Inhalt, Auszug, Bild und SEO-Texte austauschen. Wichtig: beim Code-Block **wirklich alles** ersetzen.

---

## Teil C: Zum Schluss prüfen

- [ ] `/gute-nacht-geschichten` öffnen → auf mehrere Geschichten klicken: Jede Karte führt zur richtigen Seite (keine „Seite nicht gefunden“).
- [ ] In einer Geschichte unten „Weitere Gute-Nacht-Geschichten“ und „Geschichten auf einen Blick“ anklicken.
- [ ] Am Handy: Nachtmodus, A−/A+ und „Vorlesen“ ausprobieren.
- [ ] Google: Die Seiten tauchen nach einigen Tagen auf. In der Google Search Console kannst du `/gute-nacht-geschichten` zur Indexierung einreichen; Squarespace nimmt die Blog-Beiträge automatisch in die Sitemap auf.

**Typische Fehler:**
- *Karte führt ins Leere:* Der URL-Slug des Beitrags weicht vom Steckbrief ab (Tippfehler, Umlaut statt `ae`/`oe`/`ue`, Datum im Slug). Slug in den Beitragseinstellungen korrigieren.
- *Geschichte erscheint als Code-Text:* Im Code-Block ist „Quellcode anzeigen“ eingeschaltet oder Markdown statt HTML gewählt.
- *Bild fehlt in der Karte/Geschichte:* Die Bilder kommen von GitHub; das ist erledigt (Branch ist in `main`). Seite einmal neu laden.

---

## Übersicht

| # | Titel | URL-Slug | Datei | Alter · Dauer |
|---|---|---|---|---|
| 01 | Möwe Mats will nicht schlafen | `moewe-mats-will-nicht-schlafen` | `01_moewe-mats-will-nicht-schlafen.html` | ab 3 · 4 Min. |
| 02 | Leuchtturm Lotte und der Nebel | `leuchtturm-lotte-und-der-nebel` | `02_leuchtturm-lotte-und-der-nebel.html` | ab 3 · 4 Min. |
| 03 | Die Fähre Frieda fährt nach Hause | `die-faehre-frieda-faehrt-nach-hause` | `03_die-faehre-frieda-faehrt-nach-hause.html` | ab 3 · 4 Min. |
| 04 | Ein Schlaflied für Kran Karl | `ein-schlaflied-fuer-kran-karl` | `04_ein-schlaflied-fuer-kran-karl.html` | ab 3 · 4 Min. |
| 05 | Das kleine Gespenst Huhu | `das-kleine-gespenst-huhu` | `05_das-kleine-gespenst-huhu.html` | ab 3 · 5 Min. |
| 06 | Die Laterne, die sich vor dem Wind fürchtete | `die-laterne-die-sich-vor-dem-wind-fuerchtete` | `06_die-laterne-die-sich-vor-dem-wind-fuerchtete.html` | ab 3 · 4 Min. |
| 07 | Wichtel Wilbur und das Warten | `wichtel-wilbur-und-das-warten` | `07_wichtel-wilbur-und-das-warten.html` | ab 4 · 5 Min. |
| 08 | Der Schneemann, der die Sterne sehen wollte | `der-schneemann-der-die-sterne-sehen-wollte` | `08_der-schneemann-der-die-sterne-sehen-wollte.html` | ab 3 · 4 Min. |
| 09 | Funki, der kleine Drache | `funki-der-kleine-drache` | `09_funki-der-kleine-drache.html` | ab 3 · 5 Min. |
| 10 | Ella fliegt zum Mond | `ella-fliegt-zum-mond` | `10_ella-fliegt-zum-mond.html` | ab 3 · 5 Min. |
| 11 | Bagger Bruno macht Feierabend | `bagger-bruno-macht-feierabend` | `11_bagger-bruno-macht-feierabend.html` | ab 3 · 4 Min. |
| 12 | Teddy hält Wache | `teddy-haelt-wache` | `12_teddy-haelt-wache.html` | ab 3 · 4 Min. |
| 13 | Mats und das Schietwetter | `mats-und-das-schietwetter` | `13_mats-und-das-schietwetter.html` | ab 3 · 4 Min. |
| 14 | Mats sucht ihre Lieblingsfeder | `mats-sucht-ihre-lieblingsfeder` | `14_mats-sucht-ihre-lieblingsfeder.html` | ab 3 · 4 Min. |
| 15 | Mats hat Geburtstag | `mats-hat-geburtstag` | `15_mats-hat-geburtstag.html` | ab 3 · 4 Min. |
| 16 | Mats und die Sternschnuppe | `mats-und-die-sternschnuppe` | `16_mats-und-die-sternschnuppe.html` | ab 3 · 4 Min. |
| 17 | Das kleine Auto fährt nach Hause | `das-kleine-auto-faehrt-nach-hause` | `17_das-kleine-auto-faehrt-nach-hause.html` | ab 2 · 2 Min. |
| 18 | Gute Nacht, Obstkorb | `gute-nacht-obstkorb` | `18_gute-nacht-obstkorb.html` | ab 2 · 2 Min. |
| 19 | Das Flugzeug landet am Abend | `das-flugzeug-landet-am-abend` | `19_das-flugzeug-landet-am-abend.html` | ab 2 · 2 Min. |
| 20 | Die Luftballons wollen noch nicht schlafen | `die-luftballons-wollen-noch-nicht-schlafen` | `20_die-luftballons-wollen-noch-nicht-schlafen.html` | ab 2 · 2 Min. |
| 21 | Ritter Rasmus und die Angst vor dem Dunkeln | `ritter-rasmus-und-die-angst-vor-dem-dunkeln` | `21_ritter-rasmus-und-die-angst-vor-dem-dunkeln.html` | ab 5 · 7 Min. |
| 22 | Nixe Nele schwimmt in den Hafen | `nixe-nele-schwimmt-in-den-hafen` | `22_nixe-nele-schwimmt-in-den-hafen.html` | ab 5 · 7 Min. |
| 23 | Robo lernt träumen | `robo-lernt-traeumen` | `23_robo-lernt-traeumen.html` | ab 5 · 7 Min. |
| 24 | Das Einhorn, das seinen Regenbogen verlor | `das-einhorn-das-seinen-regenbogen-verlor` | `24_das-einhorn-das-seinen-regenbogen-verlor.html` | ab 5 · 7 Min. |

---

## Die Steckbriefe zum Kopieren

### 01 · Möwe Mats will nicht schlafen

- [ ] erledigt
- **Titel:** `Möwe Mats will nicht schlafen`
- **URL des Beitrags:** `moewe-mats-will-nicht-schlafen` → später erreichbar unter `trutzstaehler.de/geschichten/moewe-mats-will-nicht-schlafen`
- **Code-Block:** Inhalt der Datei `geschichten/01_moewe-mats-will-nicht-schlafen.html`
- **Beitragsbild:** `moewe-mats-will-nicht-schlafen.jpg`
- **Auszug:** Im Hafen ist abends noch so viel los – da kann Möwe Mats doch unmöglich schlafen gehen! Oder leuchtet der Hafen vielleicht auch ohne sie weiter?
- **SEO-Titel:** `Möwe Mats will nicht schlafen – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Im Hafen ist abends noch so viel los – da kann Möwe Mats doch unmöglich schlafen gehen! Oder leuchtet der Hafen vielleicht auch ohne sie weiter?
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Tiere`, `Einschlafen`

### 02 · Leuchtturm Lotte und der Nebel

- [ ] erledigt
- **Titel:** `Leuchtturm Lotte und der Nebel`
- **URL des Beitrags:** `leuchtturm-lotte-und-der-nebel` → später erreichbar unter `trutzstaehler.de/geschichten/leuchtturm-lotte-und-der-nebel`
- **Code-Block:** Inhalt der Datei `geschichten/02_leuchtturm-lotte-und-der-nebel.html`
- **Beitragsbild:** `leuchtturm-lotte-und-der-nebel.jpg`
- **Auszug:** Leuchtturm Lotte findet ihr Licht viel zu klein. Doch in einer nebligen Nacht braucht ein kleines Boot genau dieses Licht, um nach Hause zu finden.
- **SEO-Titel:** `Leuchtturm Lotte und der Nebel – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Leuchtturm Lotte findet ihr Licht viel zu klein. Doch in einer nebligen Nacht braucht ein kleines Boot genau dieses Licht, um nach Hause zu finden.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Mut`, `Gefühle`

### 03 · Die Fähre Frieda fährt nach Hause

- [ ] erledigt
- **Titel:** `Die Fähre Frieda fährt nach Hause`
- **URL des Beitrags:** `die-faehre-frieda-faehrt-nach-hause` → später erreichbar unter `trutzstaehler.de/geschichten/die-faehre-frieda-faehrt-nach-hause`
- **Code-Block:** Inhalt der Datei `geschichten/03_die-faehre-frieda-faehrt-nach-hause.html`
- **Beitragsbild:** `die-faehre-frieda-faehrt-nach-hause.jpg`
- **Auszug:** Es ist die letzte Fahrt des Tages: Hafenfähre Frieda bringt alle nach Hause – müde Menschen, einen schnarchenden Hund und ein Kind mit einer roten Mütze.
- **SEO-Titel:** `Die Fähre Frieda fährt nach Hause – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Es ist die letzte Fahrt des Tages: Hafenfähre Frieda bringt alle nach Hause – müde Menschen, einen schnarchenden Hund und ein Kind mit einer roten Mütze.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Familie`, `Einschlafen`

### 04 · Ein Schlaflied für Kran Karl

- [ ] erledigt
- **Titel:** `Ein Schlaflied für Kran Karl`
- **URL des Beitrags:** `ein-schlaflied-fuer-kran-karl` → später erreichbar unter `trutzstaehler.de/geschichten/ein-schlaflied-fuer-kran-karl`
- **Code-Block:** Inhalt der Datei `geschichten/04_ein-schlaflied-fuer-kran-karl.html`
- **Beitragsbild:** `ein-schlaflied-fuer-kran-karl.jpg`
- **Auszug:** Kran Karl ist der größte Kran im Hafen – und heute Abend ist er so müde wie noch nie. Zum Glück hat ein Kind am Ufer eine Idee.
- **SEO-Titel:** `Ein Schlaflied für Kran Karl – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Kran Karl ist der größte Kran im Hafen – und heute Abend ist er so müde wie noch nie. Zum Glück hat ein Kind am Ufer eine Idee.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Freundschaft`, `Einschlafen`

### 05 · Das kleine Gespenst Huhu

- [ ] erledigt
- **Titel:** `Das kleine Gespenst Huhu`
- **URL des Beitrags:** `das-kleine-gespenst-huhu` → später erreichbar unter `trutzstaehler.de/geschichten/das-kleine-gespenst-huhu`
- **Code-Block:** Inhalt der Datei `geschichten/05_das-kleine-gespenst-huhu.html`
- **Beitragsbild:** `das-kleine-gespenst-huhu.jpg`
- **Auszug:** Huhu ist ein Gespenst – und fürchtet sich vor allem. Sogar vor sich selbst im Spiegel. Doch in der Halloween-Nacht klopft jemand an seine Tür.
- **SEO-Titel:** `Das kleine Gespenst Huhu – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Huhu ist ein Gespenst – und fürchtet sich vor allem. Sogar vor sich selbst im Spiegel. Doch in der Halloween-Nacht klopft jemand an seine Tür.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Jahreszeiten`, `Gefühle`, `Freundschaft`

### 06 · Die Laterne, die sich vor dem Wind fürchtete

- [ ] erledigt
- **Titel:** `Die Laterne, die sich vor dem Wind fürchtete`
- **URL des Beitrags:** `die-laterne-die-sich-vor-dem-wind-fuerchtete` → später erreichbar unter `trutzstaehler.de/geschichten/die-laterne-die-sich-vor-dem-wind-fuerchtete`
- **Code-Block:** Inhalt der Datei `geschichten/06_die-laterne-die-sich-vor-dem-wind-fuerchtete.html`
- **Beitragsbild:** `die-laterne-die-sich-vor-dem-wind-fuerchtete.jpg`
- **Auszug:** Lina die Laterne soll beim Laternenumzug leuchten. Doch draußen weht der Novemberwind – und Lina hat Angst, dass er ihr Licht auspustet.
- **SEO-Titel:** `Die Laterne, die sich vor dem Wind fürchtete – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Lina die Laterne soll beim Laternenumzug leuchten. Doch draußen weht der Novemberwind – und Lina hat Angst, dass er ihr Licht auspustet.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Jahreszeiten`, `Mut`, `Gefühle`

### 07 · Wichtel Wilbur und das Warten

- [ ] erledigt
- **Titel:** `Wichtel Wilbur und das Warten`
- **URL des Beitrags:** `wichtel-wilbur-und-das-warten` → später erreichbar unter `trutzstaehler.de/geschichten/wichtel-wilbur-und-das-warten`
- **Code-Block:** Inhalt der Datei `geschichten/07_wichtel-wilbur-und-das-warten.html`
- **Beitragsbild:** `wichtel-wilbur-und-das-warten.jpg`
- **Auszug:** Jede Nacht bewacht der kleine Wichtel Wilbur ein Türchen im Adventskalender. Doch das Warten fällt ihm so schwer – bis er entdeckt, wie schön es sein kann.
- **SEO-Titel:** `Wichtel Wilbur und das Warten – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Jede Nacht bewacht der kleine Wichtel Wilbur ein Türchen im Adventskalender. Doch das Warten fällt ihm so schwer – bis er entdeckt, wie schön es sein kann.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Jahreszeiten`, `Gefühle`, `Familie`

### 08 · Der Schneemann, der die Sterne sehen wollte

- [ ] erledigt
- **Titel:** `Der Schneemann, der die Sterne sehen wollte`
- **URL des Beitrags:** `der-schneemann-der-die-sterne-sehen-wollte` → später erreichbar unter `trutzstaehler.de/geschichten/der-schneemann-der-die-sterne-sehen-wollte`
- **Code-Block:** Inhalt der Datei `geschichten/08_der-schneemann-der-die-sterne-sehen-wollte.html`
- **Beitragsbild:** `der-schneemann-der-die-sterne-sehen-wollte.jpg`
- **Auszug:** Schneemann Kalle steht im Garten und schaut jede Nacht zu den Sternen hinauf. Wie gern würde er sie einmal von Nahem sehen! Zum Glück hat er gute Freunde.
- **SEO-Titel:** `Der Schneemann, der die Sterne sehen wollte – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Schneemann Kalle steht im Garten und schaut jede Nacht zu den Sternen hinauf. Wie gern würde er sie einmal von Nahem sehen! Zum Glück hat er gute Freunde.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Jahreszeiten`, `Freundschaft`, `Einschlafen`

### 09 · Funki, der kleine Drache

- [ ] erledigt
- **Titel:** `Funki, der kleine Drache`
- **URL des Beitrags:** `funki-der-kleine-drache` → später erreichbar unter `trutzstaehler.de/geschichten/funki-der-kleine-drache`
- **Code-Block:** Inhalt der Datei `geschichten/09_funki-der-kleine-drache.html`
- **Beitragsbild:** `funki-der-kleine-drache.jpg`
- **Auszug:** Alle Drachen im Tal können Feuer spucken – nur Funki nicht. Aus seinem Maul kommt bloß warme Luft. Doch in einer eisigen Nacht wird genau das zu etwas ganz Besonderem.
- **SEO-Titel:** `Funki, der kleine Drache – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Alle Drachen im Tal können Feuer spucken – nur Funki nicht. Aus seinem Maul kommt bloß warme Luft. Doch in einer eisigen Nacht wird genau das zu etwas ganz Besonderem.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Fantasie`, `Gefühle`, `Freundschaft`

### 10 · Ella fliegt zum Mond

- [ ] erledigt
- **Titel:** `Ella fliegt zum Mond`
- **URL des Beitrags:** `ella-fliegt-zum-mond` → später erreichbar unter `trutzstaehler.de/geschichten/ella-fliegt-zum-mond`
- **Code-Block:** Inhalt der Datei `geschichten/10_ella-fliegt-zum-mond.html`
- **Beitragsbild:** `ella-fliegt-zum-mond.jpg`
- **Auszug:** Ella kann nicht einschlafen – also baut sie aus ihrem Bett eine Rakete. Gemeinsam mit Kuschelhase Momo fliegt sie bis zum Mond, um ihm persönlich gute Nacht zu sagen.
- **SEO-Titel:** `Ella fliegt zum Mond – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Ella kann nicht einschlafen – also baut sie aus ihrem Bett eine Rakete. Gemeinsam mit Kuschelhase Momo fliegt sie bis zum Mond, um ihm persönlich gute Nacht zu sagen.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Weltraum`, `Einschlafen`, `Fantasie`

### 11 · Bagger Bruno macht Feierabend

- [ ] erledigt
- **Titel:** `Bagger Bruno macht Feierabend`
- **URL des Beitrags:** `bagger-bruno-macht-feierabend` → später erreichbar unter `trutzstaehler.de/geschichten/bagger-bruno-macht-feierabend`
- **Code-Block:** Inhalt der Datei `geschichten/11_bagger-bruno-macht-feierabend.html`
- **Beitragsbild:** `bagger-bruno-macht-feierabend.jpg`
- **Auszug:** Bagger Bruno liebt seine Baustelle so sehr, dass er abends einfach nicht aufhören will zu baggern. Bis ein alter Kran ihm verrät, was Bagger in der Nacht Schönes erleben.
- **SEO-Titel:** `Bagger Bruno macht Feierabend – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Bagger Bruno liebt seine Baustelle so sehr, dass er abends einfach nicht aufhören will zu baggern. Bis ein alter Kran ihm verrät, was Bagger in der Nacht Schönes erleben.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Fahrzeuge`, `Einschlafen`

### 12 · Teddy hält Wache

- [ ] erledigt
- **Titel:** `Teddy hält Wache`
- **URL des Beitrags:** `teddy-haelt-wache` → später erreichbar unter `trutzstaehler.de/geschichten/teddy-haelt-wache`
- **Code-Block:** Inhalt der Datei `geschichten/12_teddy-haelt-wache.html`
- **Beitragsbild:** `teddy-haelt-wache.jpg`
- **Auszug:** Jede Nacht, wenn Noah schläft, öffnet sein Teddy Brummel ganz leise die Augen. Denn er hat eine wichtige Aufgabe: Er hält Wache. Und dabei entdeckt er, wie friedlich die Nacht sein kann.
- **SEO-Titel:** `Teddy hält Wache – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Jede Nacht, wenn Noah schläft, öffnet sein Teddy Brummel ganz leise die Augen. Denn er hat eine wichtige Aufgabe: Er hält Wache. Und dabei entdeckt er, wie friedlich die Nacht sein kann.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Familie`, `Einschlafen`, `Mut`

### 13 · Mats und das Schietwetter

- [ ] erledigt
- **Titel:** `Mats und das Schietwetter`
- **URL des Beitrags:** `mats-und-das-schietwetter` → später erreichbar unter `trutzstaehler.de/geschichten/mats-und-das-schietwetter`
- **Code-Block:** Inhalt der Datei `geschichten/13_mats-und-das-schietwetter.html`
- **Beitragsbild:** `mats-und-das-schietwetter.jpg`
- **Auszug:** Regen, Wind und graue Wolken über dem Hafen – Möwe Mats findet das Wetter doof. Bis sie merkt, wie gemütlich Regen klingen kann.
- **SEO-Titel:** `Mats und das Schietwetter – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Regen, Wind und graue Wolken über dem Hafen – Möwe Mats findet das Wetter doof. Bis sie merkt, wie gemütlich Regen klingen kann.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Gefühle`, `Jahreszeiten` · `Möwe Mats`

### 14 · Mats sucht ihre Lieblingsfeder

- [ ] erledigt
- **Titel:** `Mats sucht ihre Lieblingsfeder`
- **URL des Beitrags:** `mats-sucht-ihre-lieblingsfeder` → später erreichbar unter `trutzstaehler.de/geschichten/mats-sucht-ihre-lieblingsfeder`
- **Code-Block:** Inhalt der Datei `geschichten/14_mats-sucht-ihre-lieblingsfeder.html`
- **Beitragsbild:** `mats-sucht-ihre-lieblingsfeder.jpg`
- **Auszug:** Mats hat eine ganz besondere Feder mit einem silbernen Glanz – und plötzlich ist sie weg! Der ganze Hafen hilft beim Suchen.
- **SEO-Titel:** `Mats sucht ihre Lieblingsfeder – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Mats hat eine ganz besondere Feder mit einem silbernen Glanz – und plötzlich ist sie weg! Der ganze Hafen hilft beim Suchen.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Freundschaft`, `Tiere` · `Möwe Mats`

### 15 · Mats hat Geburtstag

- [ ] erledigt
- **Titel:** `Mats hat Geburtstag`
- **URL des Beitrags:** `mats-hat-geburtstag` → später erreichbar unter `trutzstaehler.de/geschichten/mats-hat-geburtstag`
- **Code-Block:** Inhalt der Datei `geschichten/15_mats-hat-geburtstag.html`
- **Beitragsbild:** `mats-hat-geburtstag.jpg`
- **Auszug:** Heute ist Mats’ Geburtstag! Am Hamburger Hafen wird gefeiert – mit Fischbrötchen-Torte, Hupkonzert und einem Lichtgeschenk von Lotte.
- **SEO-Titel:** `Mats hat Geburtstag – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Heute ist Mats’ Geburtstag! Am Hamburger Hafen wird gefeiert – mit Fischbrötchen-Torte, Hupkonzert und einem Lichtgeschenk von Lotte.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Familie`, `Freundschaft` · `Möwe Mats`

### 16 · Mats und die Sternschnuppe

- [ ] erledigt
- **Titel:** `Mats und die Sternschnuppe`
- **URL des Beitrags:** `mats-und-die-sternschnuppe` → später erreichbar unter `trutzstaehler.de/geschichten/mats-und-die-sternschnuppe`
- **Code-Block:** Inhalt der Datei `geschichten/16_mats-und-die-sternschnuppe.html`
- **Beitragsbild:** `mats-und-die-sternschnuppe.jpg`
- **Auszug:** In einer klaren Nacht saust eine Sternschnuppe über den Hafen. Mats darf sich etwas wünschen – aber was nur?
- **SEO-Titel:** `Mats und die Sternschnuppe – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** In einer klaren Nacht saust eine Sternschnuppe über den Hafen. Mats darf sich etwas wünschen – aber was nur?
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Einschlafen`, `Familie` · `Möwe Mats`

### 17 · Das kleine Auto fährt nach Hause

- [ ] erledigt
- **Titel:** `Das kleine Auto fährt nach Hause`
- **URL des Beitrags:** `das-kleine-auto-faehrt-nach-hause` → später erreichbar unter `trutzstaehler.de/geschichten/das-kleine-auto-faehrt-nach-hause`
- **Code-Block:** Inhalt der Datei `geschichten/17_das-kleine-auto-faehrt-nach-hause.html`
- **Beitragsbild:** `das-kleine-auto-faehrt-nach-hause.jpg`
- **Auszug:** Den ganzen Tag ist das kleine Auto gefahren. Jetzt wird es dunkel – Zeit, nach Hause zu fahren und allen gute Nacht zu sagen.
- **SEO-Titel:** `Das kleine Auto fährt nach Hause – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Den ganzen Tag ist das kleine Auto gefahren. Jetzt wird es dunkel – Zeit, nach Hause zu fahren und allen gute Nacht zu sagen.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Fahrzeuge`, `Einschlafen`

### 18 · Gute Nacht, Obstkorb

- [ ] erledigt
- **Titel:** `Gute Nacht, Obstkorb`
- **URL des Beitrags:** `gute-nacht-obstkorb` → später erreichbar unter `trutzstaehler.de/geschichten/gute-nacht-obstkorb`
- **Code-Block:** Inhalt der Datei `geschichten/18_gute-nacht-obstkorb.html`
- **Beitragsbild:** `gute-nacht-obstkorb.jpg`
- **Auszug:** In der Küche steht ein Obstkorb. Apfel, Banane und die zwei Kirschen sind schon ganz müde – und sagen sich gute Nacht.
- **SEO-Titel:** `Gute Nacht, Obstkorb – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** In der Küche steht ein Obstkorb. Apfel, Banane und die zwei Kirschen sind schon ganz müde – und sagen sich gute Nacht.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Einschlafen`, `Fantasie`

### 19 · Das Flugzeug landet am Abend

- [ ] erledigt
- **Titel:** `Das Flugzeug landet am Abend`
- **URL des Beitrags:** `das-flugzeug-landet-am-abend` → später erreichbar unter `trutzstaehler.de/geschichten/das-flugzeug-landet-am-abend`
- **Code-Block:** Inhalt der Datei `geschichten/19_das-flugzeug-landet-am-abend.html`
- **Beitragsbild:** `das-flugzeug-landet-am-abend.jpg`
- **Auszug:** Hoch über den Wolken fliegt ein kleines Flugzeug. Jetzt geht die Sonne unter – und das Flugzeug fliegt nach Hause.
- **SEO-Titel:** `Das Flugzeug landet am Abend – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Hoch über den Wolken fliegt ein kleines Flugzeug. Jetzt geht die Sonne unter – und das Flugzeug fliegt nach Hause.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Fahrzeuge`, `Einschlafen`

### 20 · Die Luftballons wollen noch nicht schlafen

- [ ] erledigt
- **Titel:** `Die Luftballons wollen noch nicht schlafen`
- **URL des Beitrags:** `die-luftballons-wollen-noch-nicht-schlafen` → später erreichbar unter `trutzstaehler.de/geschichten/die-luftballons-wollen-noch-nicht-schlafen`
- **Code-Block:** Inhalt der Datei `geschichten/20_die-luftballons-wollen-noch-nicht-schlafen.html`
- **Beitragsbild:** `die-luftballons-wollen-noch-nicht-schlafen.jpg`
- **Auszug:** Die Party ist vorbei, aber die drei Luftballons wollen noch weiter tanzen. Bis sie merken, wie gemütlich es auch ganz ruhig sein kann.
- **SEO-Titel:** `Die Luftballons wollen noch nicht schlafen – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Die Party ist vorbei, aber die drei Luftballons wollen noch weiter tanzen. Bis sie merken, wie gemütlich es auch ganz ruhig sein kann.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Gefühle`, `Einschlafen`

### 21 · Ritter Rasmus und die Angst vor dem Dunkeln

- [ ] erledigt
- **Titel:** `Ritter Rasmus und die Angst vor dem Dunkeln`
- **URL des Beitrags:** `ritter-rasmus-und-die-angst-vor-dem-dunkeln` → später erreichbar unter `trutzstaehler.de/geschichten/ritter-rasmus-und-die-angst-vor-dem-dunkeln`
- **Code-Block:** Inhalt der Datei `geschichten/21_ritter-rasmus-und-die-angst-vor-dem-dunkeln.html`
- **Beitragsbild:** `ritter-rasmus-und-die-angst-vor-dem-dunkeln.jpg`
- **Auszug:** Rasmus ist der kleinste Ritter der Burg – und nachts knarrt und knackt es überall. Mit Schild, Holzschwert und Laterne macht er sich auf, das Geheimnis der Geräusche zu lüften.
- **SEO-Titel:** `Ritter Rasmus und die Angst vor dem Dunkeln – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Rasmus ist der kleinste Ritter der Burg – und nachts knarrt und knackt es überall. Mit Schild, Holzschwert und Laterne macht er sich auf, das Geheimnis der Geräusche zu lüften.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Mut`, `Fantasie`, `Gefühle`

### 22 · Nixe Nele schwimmt in den Hafen

- [ ] erledigt
- **Titel:** `Nixe Nele schwimmt in den Hafen`
- **URL des Beitrags:** `nixe-nele-schwimmt-in-den-hafen` → später erreichbar unter `trutzstaehler.de/geschichten/nixe-nele-schwimmt-in-den-hafen`
- **Code-Block:** Inhalt der Datei `geschichten/22_nixe-nele-schwimmt-in-den-hafen.html`
- **Beitragsbild:** `nixe-nele-schwimmt-in-den-hafen.jpg`
- **Auszug:** Die kleine Meerjungfrau Nele will wissen, wohin die großen Schiffe fahren. Also schwimmt sie von der Nordsee die Elbe hinauf – bis mitten in den Hamburger Hafen.
- **SEO-Titel:** `Nixe Nele schwimmt in den Hafen – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Die kleine Meerjungfrau Nele will wissen, wohin die großen Schiffe fahren. Also schwimmt sie von der Nordsee die Elbe hinauf – bis mitten in den Hamburger Hafen.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Hafen`, `Freundschaft`, `Fantasie`

### 23 · Robo lernt träumen

- [ ] erledigt
- **Titel:** `Robo lernt träumen`
- **URL des Beitrags:** `robo-lernt-traeumen` → später erreichbar unter `trutzstaehler.de/geschichten/robo-lernt-traeumen`
- **Code-Block:** Inhalt der Datei `geschichten/23_robo-lernt-traeumen.html`
- **Beitragsbild:** `robo-lernt-traeumen.jpg`
- **Auszug:** Robo ist ein kleiner Roboter, der alles kann – nur nicht schlafen. Denn er hat keinen Aus-Knopf zum Träumen. Oder vielleicht doch?
- **SEO-Titel:** `Robo lernt träumen – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Robo ist ein kleiner Roboter, der alles kann – nur nicht schlafen. Denn er hat keinen Aus-Knopf zum Träumen. Oder vielleicht doch?
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Weltraum`, `Einschlafen`, `Gefühle`

### 24 · Das Einhorn, das seinen Regenbogen verlor

- [ ] erledigt
- **Titel:** `Das Einhorn, das seinen Regenbogen verlor`
- **URL des Beitrags:** `das-einhorn-das-seinen-regenbogen-verlor` → später erreichbar unter `trutzstaehler.de/geschichten/das-einhorn-das-seinen-regenbogen-verlor`
- **Code-Block:** Inhalt der Datei `geschichten/24_das-einhorn-das-seinen-regenbogen-verlor.html`
- **Beitragsbild:** `das-einhorn-das-seinen-regenbogen-verlor.jpg`
- **Auszug:** Einhorn Fiona kann Regenbögen an den Himmel zaubern – bis ihr eines Morgens die Farben fehlen. Zum Glück helfen ihr ihre Freunde, sie wiederzufinden.
- **SEO-Titel:** `Das Einhorn, das seinen Regenbogen verlor – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** Einhorn Fiona kann Regenbögen an den Himmel zaubern – bis ihr eines Morgens die Farben fehlen. Zum Glück helfen ihr ihre Freunde, sie wiederzufinden.
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** `Fantasie`, `Freundschaft`, `Gefühle`


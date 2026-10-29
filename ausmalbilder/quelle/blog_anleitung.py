"""Anleitung: die Gute-Nacht-Geschichten als Beiträge im Squarespace-Blog „Geschichten“ anlegen.

python3 blog_anleitung.py -> ../08-kreativhafen-gratis/ANLEITUNG_BLOG-GESCHICHTEN.md
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import katalog as KAT
from geschichten import ALLE

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '08-kreativhafen-gratis', 'ANLEITUNG_BLOG-GESCHICHTEN.md')
N = len(ALLE)


def datei(i, g):
    return f'{i:02d}_{g["slug"]}.html'


def steckbrief(i, g):
    return f'''### {i:02d} · {g['titel']}

- [ ] erledigt
- **Titel:** `{g['titel']}`
- **URL des Beitrags:** `{g['slug']}` → später erreichbar unter `{KAT.DOMAIN}/geschichten/{g['slug']}`
- **Code-Block:** Inhalt der Datei `geschichten/{datei(i, g)}`
- **Beitragsbild:** `{g['slug']}.jpg`
- **Auszug:** {g['teaser']}
- **SEO-Titel:** `{g['titel']} – Gute-Nacht-Geschichte zum Vorlesen | Kreativhafen`
- **SEO-Beschreibung:** {g['teaser']}
- **Kategorie:** `Gute-Nacht-Geschichten` · **Tags:** {', '.join(f'`{t}`' for t in g['themen'])}{(' · `' + g['reihe'] + '`') if g.get('reihe') else ''}
'''


def main():
    tabelle = '\n'.join(f"| {i:02d} | {g['titel']} | `{g['slug']}` | `{datei(i, g)}` | ab {g['alter']} · {g['lesezeit']} Min. |"
                        for i, g in enumerate(ALLE, 1))
    briefe = '\n'.join(steckbrief(i, g) for i, g in enumerate(ALLE, 1))
    doc = f'''# Die {N} Gute-Nacht-Geschichten im Blog anlegen

Jede Geschichte bekommt eine **eigene Seite** unter `{KAT.DOMAIN}/geschichten/…`, genau wie bei Zitronenbande und Zwergenstark. So findet Google jede Geschichte einzeln. Die Übersicht `/gute-nacht-geschichten` verlinkt automatisch auf diese Adressen.

**Was du brauchst** (alles in der ZIP „Kreativhafen_Komplett“):
- `01_Code-Bloecke_fuer-Squarespace/geschichten_je-ein-Blog-Beitrag/`: eine HTML-Datei pro Geschichte
- `03_Bilder/Vorschaubilder-Geschichten_fuer-Blog-Beitraege/`: ein JPG pro Geschichte

**Zeit:** Einmal einrichten etwa 10 Minuten, danach etwa 3 Minuten pro Geschichte. Du musst nicht alle auf einmal machen. Die Übersicht verlinkt zwar sofort alle {N} Geschichten, also am besten an einem Abend alle anlegen oder die Übersicht erst danach veröffentlichen.

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

## Teil B: Eine Geschichte anlegen (für jede der {N} wiederholen)

1. Im Blog „Geschichten“ auf **+** (Beitrag hinzufügen) klicken.
2. **Titel** eintragen (aus dem Steckbrief unten).
3. Im Textfeld darunter den Platzhaltertext löschen, dann **Block hinzufügen → Code** wählen.
4. Die passende Datei aus `geschichten_je-ein-Blog-Beitrag/` öffnen (Rechtsklick → Öffnen mit → Texteditor/TextEdit), **alles markieren (Strg/Cmd + A), kopieren** und in den Code-Block einfügen.
   - Im Code-Block muss **HTML** eingestellt sein, und **„Quellcode anzeigen“** muss **aus** sein.
   - Im Editor sieht man nur einen Platzhalter „Script deaktiviert“ o. Ä.; das ist normal. Die Geschichte erscheint erst in der Vorschau bzw. auf der echten Seite.
5. **Einstellungen** des Beitrags öffnen (Zahnrad bzw. „…“ → Einstellungen):
   - **URL** (bzw. „Beitrags-URL“): den Slug aus dem Steckbrief eintragen. Im Feld steht dann `/geschichten/{ALLE[0]['slug']}` o. Ä.
   - **Auszug:** Text aus dem Steckbrief
   - **Beitragsbild/Miniaturbild:** das JPG aus `03_Bilder/Vorschaubilder…` hochladen (gleicher Name wie der Slug)
   - **Kategorie** und **Tags** wie im Steckbrief (optional, hilft beim Ordnen)
   - **Autor:** Trutz Stähler
   - Reiter **SEO:** SEO-Titel und SEO-Beschreibung aus dem Steckbrief
6. Speichern → **Veröffentlichen**.
7. Kurz testen: `{KAT.DOMAIN}/geschichten/<slug>` aufrufen. Die Geschichte muss mit Bild, Reiter-Leiste und „Vorlesen“-Leiste erscheinen.

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
{tabelle}

---

## Die Steckbriefe zum Kopieren

{briefe}
'''
    open(OUT, 'w', encoding='utf-8').write(doc)
    print('ok', os.path.relpath(OUT))


if __name__ == '__main__':
    main()

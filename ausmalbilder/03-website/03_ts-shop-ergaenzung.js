/* =====================================================================
   AUSMALBILDER – Ergänzungen für window.TS_SHOP (Einstellungen → Erweitert → Code-Injection)
   1) In  kategorien: [ … ]  diese Zeile ergänzen (Komma an der vorherigen Zeile nicht vergessen):
====================================================================== */
    { id: 'ausmalbilder', nr: '03', titel: 'Ausmalbilder', text: 'Halloween, Laterne, Adventskalender und Winter – Ausmalbilder zum Ausdrucken, sofort als PDF.', link: '/shop/ausmalbilder', farbe: 'rgb(110, 231, 183)' }

/* =====================================================================
   2) In  produkte: [ … ]  diese Zeilen ergänzen (z. B. ganz am Ende, vor der schließenden Klammer ] ):
      Die Produktbilder holt sich die Kachel automatisch vom Squarespace-Produkt.
====================================================================== */
    { kat: 'ausmalbilder', id: 'am-halloween', icon: '✎', titel: "Kleine Gruselfreunde", text: "Halloween-Ausmalbilder. Kürbis, Gespenst & Co. – 10 freundliche Halloween-Motive, die kein bisschen gruselig sind.", preis: '3,90 €', link: '/store/p/ausmalbilder-halloween' },
    { kat: 'ausmalbilder', id: 'am-laterne', icon: '✎', titel: "Laterne, Laterne", text: "Ausmalbilder zu St. Martin. Sonne, Mond und Sterne – 8 Motive plus Bastelvorlage für die eigene Laterne.", preis: '3,90 €', link: '/store/p/ausmalbilder-laterne' },
    { kat: 'ausmalbilder', id: 'am-advent', icon: '✎', titel: "24 Türchen", text: "Adventskalender zum Ausmalen. Jeden Tag ein Bild: 24 Weihnachtsmotive vom Adventskranz bis zum Tannenbaum.", preis: '5,90 €', link: '/store/p/ausmalbilder-adventskalender' },
    { kat: 'ausmalbilder', id: 'am-winter', icon: '✎', titel: "Winterzeit", text: "Ausmalbilder für Winter & Silvester. Schneemann, Eisbär und Glücksschwein – 10 Motive für kalte Tage und Silvester.", preis: '3,90 €', link: '/store/p/ausmalbilder-winter' },
    { kat: 'ausmalbilder', id: 'am-anhaenger', icon: '✎', titel: "Für dich!", text: "Geschenkanhänger & Karten zum Ausmalen. 16 Anhänger und 4 Karten – Kinder malen, die Geschenke werden persönlich.", preis: '2,90 €', link: '/store/p/ausmalbilder-geschenkanhaenger' },
    { kat: 'ausmalbilder', id: 'am-bundle', icon: '✎', titel: "Saisonpaket", text: "Alle Ausmalbilder für Herbst & Winter. Alle fünf Pakete in einem: 52 Motive, Bastelvorlage, Anhänger & Karten – du sparst 7,60 €.", preis: '12,90 €', link: '/store/p/ausmalbilder-saisonpaket', highlight: true },
    { kat: 'ausmalbilder', id: 'am-kita', icon: '✎', titel: "Kita-Lizenz", text: "Alle Ausmalbilder für Kita, Schule & Hort. Das komplette Saisonpaket mit Lizenz für eine Einrichtung – so oft kopieren, wie ihr Kinder habt.", preis: '29,00 €', link: '/store/p/ausmalbilder-kita-lizenz' },

/* =====================================================================
   3) Brotkrumen auf den Produktseiten („Shop › …“ soll „Ausmalbilder“ zeigen):
      Im Skript „Produktseiten (Squarespace-Store) im Design“ diese Zeile suchen:
        : /eigenes-thema/i.test(pth) ? ['/shop/stream-widgets/eigener-stil', 'Dein eigener Stil']
      und DIREKT DAVOR diese Zeile einfügen:
====================================================================== */
      : /\/store\/p\/ausmalbilder-/i.test(pth) ? ['/shop/ausmalbilder', 'Ausmalbilder']

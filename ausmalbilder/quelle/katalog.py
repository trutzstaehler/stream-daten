"""Zentrale Produktdaten: Pakete, Preise, Texte, Termine.

Aus dieser Datei werden PDFs, Produktbilder, Shop-Texte und Webseiten erzeugt.
Preise im Stil des Shops (x,90 €), Kleinunternehmer nach § 19 UStG.
"""

DOMAIN = 'trutzstaehler.de'
MAIL = 'moin@trutzstaehler.de'
INSTA = '@trutzstaehler'

# Reihenfolge = Reihenfolge im Shop
PAKETE = [
    dict(
        id='halloween', nr='01', slug='ausmalbilder-halloween',
        name='Kleine Gruselfreunde', sub='Halloween-Ausmalbilder',
        titel_lettering=['KLEINE', 'GRUSELFREUNDE'],
        preis='3,90 €', preis_cent=390,
        farbe='#f6a33b', saison='Halloween', termin='Sa, 31. Oktober',
        motive=[f'hw{i:02d}' for i in range(1, 11)],
        cover=['hw02', 'hw01', 'hw04'],
        extras=['Deckblatt zum Ausmalen', 'Mal-Urkunde zum Schluss'],
        kurz='Kürbis, Gespenst & Co. – 10 freundliche Halloween-Motive, die kein bisschen gruselig sind.',
        intro='Kürbis, Gespenst, Fledermaus und ein Monster, das eigentlich nur kuscheln will: zehn Halloween-Freunde zum Ausmalen – mit dicken Linien, großen Flächen und dem Namen zum Mitlesen. Kein bisschen gruselig, versprochen.',
        widget='hw01',
    ),
    dict(
        id='laterne', nr='02', slug='ausmalbilder-laterne',
        name='Laterne, Laterne', sub='Ausmalbilder zu St. Martin',
        titel_lettering=['LATERNE,', 'LATERNE'],
        preis='3,90 €', preis_cent=390,
        farbe='#f7d046', saison='St. Martin', termin='Mi, 11. November',
        motive=[f'lt{i:02d}' for i in range(1, 9)],
        cover=['lt03', 'lt01', 'lt04'],
        extras=['Laternen-Bastelvorlage (zum Ausmalen, Ausschneiden, Kleben)', 'Liedblatt „Laterne, Laterne“',
                'Deckblatt zum Ausmalen', 'Mal-Urkunde zum Schluss'],
        kurz='Sonne, Mond und Sterne – 8 Motive plus Bastelvorlage für die eigene Laterne.',
        intro='Laterne, Laterne, Sonne, Mond und Sterne: acht Motive für die Laternenzeit – dazu eine Bastelvorlage, aus der eure ganz eigene Laterne wird, und das Liedblatt zum Mitsingen.',
        widget='lt01',
    ),
    dict(
        id='advent', nr='03', slug='ausmalbilder-adventskalender',
        name='24 Türchen', sub='Adventskalender zum Ausmalen',
        titel_lettering=['24', 'TÜRCHEN'],
        preis='5,90 €', preis_cent=590,
        farbe='#e8505b', saison='Advent', termin='ab Di, 1. Dezember',
        motive=[f'ad{i:02d}' for i in range(1, 25)],
        cover=['ad11', 'ad24', 'ad06'],
        extras=['Türchen-Plan zum Abhaken', 'Nummer auf jeder Seite (1–24)', 'Deckblatt zum Ausmalen',
                'Mal-Urkunde an Heiligabend'],
        kurz='Jeden Tag ein Bild: 24 Weihnachtsmotive vom Adventskranz bis zum Tannenbaum.',
        intro='Jeden Tag ein Türchen – und hinter jedem wartet ein Bild: vom Adventskranz am 1. Dezember bis zum geschmückten Tannenbaum an Heiligabend. Mit Türchen-Plan zum Abhaken und Nikolaus pünktlich am 6.',
        widget='ad11',
    ),
    dict(
        id='winter', nr='04', slug='ausmalbilder-winter',
        name='Winterzeit', sub='Ausmalbilder für Winter & Silvester',
        titel_lettering=['WINTER', 'ZEIT'],
        preis='3,90 €', preis_cent=390,
        farbe='#5ec8e5', saison='Winter & Silvester', termin='Dezember bis Februar',
        motive=[f'wi{i:02d}' for i in range(1, 11)],
        cover=['wi05', 'wi01', 'wi08'],
        extras=['Glücksbringer für Silvester', 'Deckblatt zum Ausmalen', 'Mal-Urkunde zum Schluss'],
        kurz='Schneemann, Eisbär und Glücksschwein – 10 Motive für kalte Tage und Silvester.',
        intro='Schneemann, Eisbär, Iglu und ein Glücksschwein für Silvester: zehn Motive für die Zeit nach Weihnachten, wenn draußen Schietwetter ist und drinnen die Stifte glühen.',
        widget='wi01',
    ),
    dict(
        id='anhaenger', nr='05', slug='ausmalbilder-geschenkanhaenger',
        name='Für dich!', sub='Geschenkanhänger & Karten zum Ausmalen',
        titel_lettering=['FÜR', 'DICH!'],
        preis='2,90 €', preis_cent=290,
        farbe='#f29bc4', saison='Weihnachten', termin='bis Do, 24. Dezember',
        motive=[],
        cover=['ad10', 'ad09', 'wi02'],
        extras=['16 Geschenkanhänger mit „Für“ und „Von“', '4 Karten: 2× Weihnachten, Neujahr, Danke'],
        kurz='16 Anhänger und 4 Karten – Kinder malen, die Geschenke werden persönlich.',
        intro='Die schönsten Geschenkanhänger malen die Kinder selbst: 16 Anhänger mit „Für“ und „Von“, dazu vier Karten für Weihnachten, Neujahr und ein großes Danke.',
        widget=None,
    ),
]

BUNDLE = dict(
    id='bundle', nr='06', slug='ausmalbilder-saisonpaket',
    name='Saisonpaket', sub='Alle Ausmalbilder für Herbst & Winter',
    titel_lettering=['SAISON', 'PAKET'],
    preis='12,90 €', preis_cent=1290, farbe='#6ee7b7',
    kurz='Alle fünf Pakete in einem: 52 Motive, Bastelvorlage, Anhänger & Karten – du sparst 7,60 €.',
    intro='Von Halloween bis Silvester alles in einem Download: alle fünf Pakete mit 52 Motiven, der Laternen-Bastelvorlage, 16 Geschenkanhängern und 4 Karten.',
)

KITA = dict(
    id='kita', nr='07', slug='ausmalbilder-kita-lizenz',
    name='Kita-Lizenz', sub='Alle Ausmalbilder für Kita, Schule & Hort',
    titel_lettering=['KITA', 'LIZENZ'],
    preis='29,00 €', preis_cent=2900, farbe='#4ade80',
    kurz='Das komplette Saisonpaket mit Lizenz für eine Einrichtung – so oft kopieren, wie ihr Kinder habt.',
    intro='Alle Ausmalbilder der Saison für eure ganze Einrichtung: das komplette Saisonpaket plus Lizenzurkunde – kopieren für alle Gruppen, so oft ihr wollt, ohne Ablaufdatum.',
)

GRATIS = dict(
    id='probier', name='Probierpaket', sub='3 Ausmalbilder gratis',
    motive=['hw01', 'lt01', 'ad24'],
)


def einzelsumme():
    return sum(p['preis_cent'] for p in PAKETE)


def euro(cent):
    return f'{cent // 100},{cent % 100:02d} €'


# Termine 2026/27 – für Saison-Leiste und Launch-Plan
TERMINE = [
    ('2026-10-31', 'Halloween', 'halloween'),
    ('2026-11-11', 'St. Martin', 'laterne'),
    ('2026-11-27', 'Black Friday', None),
    ('2026-11-29', '1. Advent', 'advent'),
    ('2026-12-01', 'Erstes Türchen', 'advent'),
    ('2026-12-06', 'Nikolaus', 'advent'),
    ('2026-12-24', 'Heiligabend', 'anhaenger'),
    ('2026-12-31', 'Silvester', 'winter'),
]

ALLE_IDS = [p['id'] for p in PAKETE]


def paket(pid):
    for p in PAKETE + [BUNDLE, KITA]:
        if p['id'] == pid:
            return p
    raise KeyError(pid)

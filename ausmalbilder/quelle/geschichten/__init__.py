"""Gute-Nacht-Geschichten. Jedes Modul definiert GESCHICHTEN = [dict(...), ...]."""
import importlib, pkgutil, os

ALLE = []
for _m in sorted(pkgutil.iter_modules([os.path.dirname(__file__)])):
    ALLE += importlib.import_module(f'{__name__}.{_m.name}').GESCHICHTEN

# Abwechslung: Nicht jede Geschichte endet mit derselben Formel, nicht jede hat Fragen.
# form = Art der Geschichte (Filter auf der Website). gn = Gute-Nacht-Zeile behalten? fr = Fragen behalten?
_ART = {
    'moewe-mats-will-nicht-schlafen': ('Tiergeschichte', True, True),
    'leuchtturm-lotte-und-der-nebel': ('Abenteuer', False, True),
    'die-faehre-frieda-faehrt-nach-hause': ('Hafengeschichte', False, False),
    'ein-schlaflied-fuer-kran-karl': ('Hafengeschichte', False, False),
    'das-kleine-gespenst-huhu': ('Fantasiegeschichte', False, True),
    'die-laterne-die-sich-vor-dem-wind-fuerchtete': ('Jahreszeitengeschichte', True, False),
    'wichtel-wilbur-und-das-warten': ('Jahreszeitengeschichte', True, True),
    'der-schneemann-der-die-sterne-sehen-wollte': ('Märchen', True, False),
    'funki-der-kleine-drache': ('Fabel', False, True),
    'ella-fliegt-zum-mond': ('Fantasiereise', False, False),
    'bagger-bruno-macht-feierabend': ('Alltagsgeschichte', False, False),
    'teddy-haelt-wache': ('Alltagsgeschichte', False, True),
    'mats-und-das-schietwetter': ('Tiergeschichte', False, False),
    'mats-sucht-ihre-lieblingsfeder': ('Tiergeschichte', False, True),
    'mats-hat-geburtstag': ('Tiergeschichte', False, False),
    'mats-und-die-sternschnuppe': ('Tiergeschichte', True, False),
    'das-kleine-auto-faehrt-nach-hause': ('Mitmachgeschichte', True, False),
    'gute-nacht-obstkorb': ('Mitmachgeschichte', False, True),
    'das-flugzeug-landet-am-abend': ('Mitmachgeschichte', False, False),
    'die-luftballons-wollen-noch-nicht-schlafen': ('Mitmachgeschichte', True, True),
    'ritter-rasmus-und-die-angst-vor-dem-dunkeln': ('Abenteuer', False, True),
    'nixe-nele-schwimmt-in-den-hafen': ('Abenteuer', False, False),
    'robo-lernt-traeumen': ('Fantasiegeschichte', False, True),
    'das-einhorn-das-seinen-regenbogen-verlor': ('Märchen', False, True),
}
for _g in ALLE:
    _f, _gn, _fr = _ART.get(_g['slug'], ('Gute-Nacht-Geschichte', True, True))
    _g.setdefault('form', _f)
    if not _gn:
        _g['gute_nacht'] = ''
    if not _fr:
        _g['fragen'] = []

"""Gute-Nacht-Geschichten. Jedes Modul definiert GESCHICHTEN = [dict(...), ...]."""
import importlib, pkgutil, os

ALLE = []
for _m in sorted(pkgutil.iter_modules([os.path.dirname(__file__)])):
    ALLE += importlib.import_module(f'{__name__}.{_m.name}').GESCHICHTEN

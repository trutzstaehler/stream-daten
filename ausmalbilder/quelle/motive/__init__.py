import importlib, pkgutil, os
for _m in sorted(pkgutil.iter_modules([os.path.dirname(__file__)])):
    importlib.import_module(f'{__name__}.{_m.name}')

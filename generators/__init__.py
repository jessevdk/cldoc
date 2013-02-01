import inspect, os, glob, importlib

current = inspect.getfile(inspect.currentframe())
d = os.path.dirname(current)

__all__ = []

for py in glob.glob(os.path.join(d, '*.py')):
    base = os.path.basename(py)

    if base.startswith('_'):
        continue

    modname = base[:-3]
    mod = importlib.import_module('.' + modname, 'generators')

    for a in dir(mod):
        aa = getattr(mod, a)

        if isinstance(aa, type) and aa.__module__ == mod.__name__:
            globals()[a] = aa

# vi:ts=4:et

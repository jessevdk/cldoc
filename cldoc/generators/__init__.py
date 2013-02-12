# This file is part of cldoc.  cldoc is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import inspect, os, glob, importlib

current = inspect.getfile(inspect.currentframe())
d = os.path.dirname(current)

__all__ = []

for py in glob.glob(os.path.join(d, '*.py')):
    base = os.path.basename(py)

    if base.startswith('_'):
        continue

    modname = base[:-3]
    mod = importlib.import_module('.' + modname, 'cldoc.generators')

    for a in dir(mod):
        aa = getattr(mod, a)

        if isinstance(aa, type) and aa.__module__ == mod.__name__:
            globals()[a] = aa

# vi:ts=4:et

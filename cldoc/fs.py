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
from __future__ import absolute_import

import os, tempfile, shutil, random

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class System:
    @staticmethod
    def open(*args):
        return open(*args)

    @staticmethod
    def makedirs(*args):
        return os.makedirs(*args)

    @staticmethod
    def mkdtemp():
        return tempfile.mkdtemp()

    @staticmethod
    def clear():
        pass

    @staticmethod
    def copytree(*args):
        shutil.copytree(*args)

    @staticmethod
    def rmtree(*args):
        shutil.rmtree(*args)

class Virtual:
    class NeverCloseIO(StringIO):
        def close(self):
            self.seek(0)

        def __exit__(self, type, value, traceback):
            self.close()

        def __enter__(self):
            return self

        @property
        def value(self):
            data = self.getvalue()
            self.seek(0)

            return data

    files = {}

    @staticmethod
    def open(*args):
        fname = args[0]

        if not os.path.isabs(fname):
            fname = os.path.join(os.getcwd(), fname)

        if len(args) != 1 and 'w' in args[1]:
            ret = Virtual.NeverCloseIO()

            Virtual.files[fname] = ret
            return ret
        elif fname in Virtual.files:
            return Virtual.NeverCloseIO(Virtual.files[fname].getvalue())
        else:
            ret = Virtual.NeverCloseIO(open(*args).read().decode('utf-8'))
            Virtual.files[fname] = ret

            return ret

    @staticmethod
    def makedirs(*args):
        pass

    @staticmethod
    def mkdtemp():
        def randname(n):
            alpha = "abcdefhijklmnopqrstuvwxyz"
            ret = ""

            for i in range(n):
                ret += alpha[random.randrange(0, len(alpha))]

            return ret

        while True:
            n = os.path.join("/", "tmp", randname(8))

            if not n in Virtual.files:
                return n

    @staticmethod
    def clear():
        Virtual.files = {}

    @staticmethod
    def copytree(*args):
        pass

    @staticmethod
    def rmtree(*args):
        pass

fs = System

# vi:ts=4:et

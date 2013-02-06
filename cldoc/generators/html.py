from __future__ import absolute_import

import inspect, os, shutil

from .generator import Generator

class Html(Generator):
    def generate(self, output):
        current = inspect.getfile(inspect.currentframe())
        d = os.path.dirname(current)

        datadir = os.path.abspath(os.path.join(d, '../data'))
        index = os.path.join(datadir, 'index.html')

        try:
            os.makedirs(datadir)
        except:
            pass

        outfile = os.path.join(output, 'index.html')
        shutil.copyfile(index, outfile)

        print('Generated `{0}\''.format(outfile))

# vi:ts=4:et

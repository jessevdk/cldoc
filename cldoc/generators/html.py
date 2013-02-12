from __future__ import absolute_import

import inspect, os, shutil, json

from .generator import Generator
from .search import Search

class Html(Generator):
    def generate(self, output):
        # Write out json document for search
        self.write_search(output)

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

    def write_search(self, output):
        search = Search(self.tree)

        records = [None] * len(search.records)

        for r in range(len(search.records)):
            rec = search.records[r]

            records[r] = (
                rec.s,
                rec.node.refid,
            )

        outfile = os.path.join(output, 'search.json')
        f = file(outfile, 'w')
        f.write(json.dumps({'records': records, 'suffixes': search.db}))
        f.close()


# vi:ts=4:et

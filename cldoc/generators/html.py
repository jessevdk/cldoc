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

import inspect, os, shutil, json

from .generator import Generator
from .search import Search

class Html(Generator):
    def generate(self, output, isstatic, customjs=[], customcss=[]):
        # Write out json document for search
        self.write_search(output)

        d = os.path.dirname(__file__)

        datadir = os.path.abspath(os.path.join(d, '..', 'data'))
        index = os.path.join(datadir, 'index.html')

        try:
            os.makedirs(datadir)
        except:
            pass

        outfile = os.path.join(output, 'index.html')

        jstags = ['<script type="text/javascript" src="{0}"></script>'.format(x) for x in customjs]
        csstags = ['<link rel="stylesheet" href="{0}" type="text/css" charset="utf-8"/>'.format(x) for x in customcss]

        with open(index) as f:
            content = f.read()

            templ = '<custom-js></custom-js>'
            content = content.replace(templ, " ".join(jstags))

            templ = '<custom-css></custom-css>'
            content = content.replace(templ, " ".join(csstags))

            with open(outfile, 'w') as o:
                o.write(content)

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

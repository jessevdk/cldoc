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

import bisect
from cldoc.clang import cindex
from cldoc.struct import Struct

class Search:
    Record = Struct.define('Record', node=None, s='', id=0)

    def __init__(self, tree):
        self.records = []
        self.suffixes = []
        self.db = []

        for node in tree.root.descendants():
            if not node._refid is None and node.access != cindex.CXXAccessSpecifier.PRIVATE:
                self.make_index(node)

    def make_index(self, node):
        name = node.qid.lower()

        r = Search.Record(node=node, s=name, id=len(self.records))
        self.records.append(r)

        for i in range(len(name) - 3):
            suffix = name[i:]

            # Determine where to insert the suffix
            idx = bisect.bisect_left(self.suffixes, suffix)

            if idx != len(self.suffixes) and self.suffixes[idx] == suffix:
                self.db[idx].append((r.id, i))
            else:
                self.suffixes.insert(idx, suffix)
                self.db.insert(idx, [(r.id, i)])

# vi:ts=4:et

from __future__ import absolute_import

import bisect

from cldoc.struct import Struct

class Search:
    Record = Struct.define('Record', node=None, s='', id=0)

    def __init__(self, tree):
        self.records = []
        self.suffixes = []
        self.db = []

        for node in tree.root.descendants():
            if not node._refid is None:
                self.make_index(node)

    def make_index(self, node):
        name = node.qid

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

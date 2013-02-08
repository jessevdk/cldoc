from node import Node
from cldoc.clang import cindex

class Union(Node):
    kind = cindex.CursorKind.UNION_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.process_children = True
        self.sortid = Node.SortId.FIELD

    @property
    def is_anonymous(self):
        return not self.cursor.spelling

    def compare_same(self, other):
        return cmp(self.sort_index, other.sort_index)

# vi:ts=4:et

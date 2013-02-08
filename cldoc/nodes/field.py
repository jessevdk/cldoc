from node import Node
from ctype import Type
from cldoc.clang import cindex

class Field(Node):
    kind = cindex.CursorKind.FIELD_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)
        self.type = Type(cursor.type)

    def compare_same(self, other):
        return cmp(self.sort_index, other.sort_index)

# vi:ts=4:et

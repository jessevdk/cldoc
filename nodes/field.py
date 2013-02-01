from node import Node
from ctype import Type
from clang import cindex

class Field(Node):
    kind = cindex.CursorKind.FIELD_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.type = Type(cursor.type)

# vi:ts=4:et

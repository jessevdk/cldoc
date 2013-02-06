from node import Node
from cldoc.clang import cindex
from ctype import Type

class Typedef(Node):
    kind = cindex.CursorKind.TYPEDEF_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.process_children = True
        self.type = Type(self.cursor.type.get_canonical())

    def visit(self, cursor, citer):
        if cursor.kind == cindex.CursorKind.TYPE_REF:
            self.type = Type(cursor.type)

        return []



# vi:ts=4:et

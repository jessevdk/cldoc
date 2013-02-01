from node import Node
from clang import cindex

class Union(Node):
    kind = cindex.CursorKind.UNION_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)
        self.visit_children = True

# vi:ts=4:et

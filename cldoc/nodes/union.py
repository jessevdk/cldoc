from node import Node
from cldoc.clang import cindex

class Union(Node):
    kind = cindex.CursorKind.UNION_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)
        self.visit_children = True

    @property
    def is_anonymous(self):
        return not self.cursor.spelling

# vi:ts=4:et

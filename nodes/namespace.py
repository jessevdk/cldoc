from node import Node
from clang import cindex
from root import Root

class Namespace(Node):
    kind = cindex.CursorKind.NAMESPACE

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.process_children = True

# vi:ts=4:et

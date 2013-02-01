from node import Node
from clang import cindex

class Enum(Node):
    kind = cindex.CursorKind.ENUM_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.typedef = None
        self.process_children = True

    @property
    def comment(self):
        ret = Node.comment.fget(self)

        if not ret and self.typedef:
            ret = self.typedef.comment

        return ret

    @property
    def name(self):
        if not self.typedef is None:
            # The name is really the one of the typedef
            return self.typedef.name
        else:
            return Node.name.fget(self)

# vi:ts=4:et

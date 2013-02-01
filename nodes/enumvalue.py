from node import Node
from clang import cindex

class EnumValue(Node):
    kind = cindex.CursorKind.ENUM_CONSTANT_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

    def compare_sort(self, other):
        if not isinstance(other, EnumValue):
            return Node.compare_sort(self, other)

        loc1 = self.cursor.location
        loc2 = other.cursor.location

        if loc1.line != loc2.line:
            return cmp(loc1.line, loc2.line)
        else:
            return cmp(loc1.column, loc2.column)

    @property
    def value(self):
        return self.cursor.enum_value

# vi:ts=4:et

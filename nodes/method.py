from function import Function
from clang import cindex

class Method(Function):
    kind = cindex.CursorKind.CXX_METHOD

    def __init__(self, cursor, comment):
        Function.__init__(self, cursor, comment)

        self.static = cursor.is_static_method()
        self.virtual = cursor.is_virtual_method()

# vi:ts=4:et

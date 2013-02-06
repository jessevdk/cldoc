from function import Function
from cldoc.clang import cindex

class Method(Function):
    kind = cindex.CursorKind.CXX_METHOD

    def __init__(self, cursor, comment):
        Function.__init__(self, cursor, comment)

        self.static = cursor.is_static_method()
        self.virtual = cursor.is_virtual_method()

        self.abstract = True
        self.update_abstract(cursor)

    def update_abstract(self, cursor):
        if cursor.is_definition() or cursor.get_definition():
            self.abstract = False

    def add_ref(self, cursor):
        super(Method, self).add_ref(cursor)
        self.update_abstract(cursor)

# vi:ts=4:et

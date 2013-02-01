from method import Method
from clang import cindex

class Destructor(Method):
    kind = cindex.CursorKind.DESTRUCTOR

    def __init__(self, cursor, comment):
        Method.__init__(self, cursor, comment)

# vi:ts=4:et

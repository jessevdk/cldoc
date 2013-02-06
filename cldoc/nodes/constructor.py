from method import Method
from cldoc.clang import cindex

class Constructor(Method):
    kind = cindex.CursorKind.CONSTRUCTOR

    def __init__(self, cursor, comment):
        Method.__init__(self, cursor, comment)

# vi:ts=4:et

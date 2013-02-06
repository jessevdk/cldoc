from method import Method
from cldoc.clang import cindex

class FunctionTemplate(Method):
    kind = cindex.CursorKind.FUNCTION_TEMPLATE

    def __init__(self, cursor, comment):
        Method.__init__(self, cursor, comment)

# vi:ts=4:et

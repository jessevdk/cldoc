from method import Method
from cldoc.clang import cindex

class ConversionFunction(Method):
    kind = cindex.CursorKind.CONVERSION_FUNCTION

    def __init__(self, cursor, comment):
        Method.__init__(self, cursor, comment)

# vi:ts=4:et

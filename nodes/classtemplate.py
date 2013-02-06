from node import Node
from clang import cindex
import importlib

cls = importlib.import_module('.class', 'nodes')

class ClassTemplate(cls.Class):
    kind = cindex.CursorKind.CLASS_TEMPLATE

    def __init__(self, cursor, comment):
        cls.Class.__init__(self, cursor, comment)

        # Check manually if this is actually a struct, so that we set the
        # current access level correctly. I'm not sure there is another
        # way to do this right now
        l = list(cursor.get_tokens())

        for i in range(len(l)):
            if l[i].kind == cindex.TokenKind.PUNCTUATION and l[i].spelling == '>':
                if i < len(l) - 2:
                    if l[i + 1].kind == cindex.TokenKind.KEYWORD and \
                       l[i + 1].spelling == 'struct':
                        self.current_access = cindex.CXXAccessSpecifier.PUBLIC
                break

class TemplateTypeParameter(Node):
    kind = cindex.CursorKind.TEMPLATE_TYPE_PARAMETER

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

# vi:ts=4:et

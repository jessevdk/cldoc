from node import Node
from cldoc.clang import cindex
from ctype import Type

class TemplateType(Type):
    kind = cindex.CursorKind.TEMPLATE_REF

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.definition = cursor.get_definition()
        self.process_children = True

# vi:ts=4:et

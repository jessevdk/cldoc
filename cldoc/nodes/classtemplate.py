from node import Node
from cldoc.clang import cindex
import importlib
from cldoc.comment import Comment
from cldoc.comment import Parser
import re

cls = importlib.import_module('.class', 'cldoc.nodes')

class TemplateTypeParameter(Node):
    kind = cindex.CursorKind.TEMPLATE_TYPE_PARAMETER

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

    def compare_same(self, other):
        return cmp(self.sort_index, other.sort_index)

class ClassTemplate(cls.Class):
    kind = cindex.CursorKind.CLASS_TEMPLATE

    def __init__(self, cursor, comment):
        cls.Class.__init__(self, cursor, comment)

        self.template_types = {}
        self.template_type_comments = {}

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

    def append(self, child):
        Node.append(self, child)

        if isinstance(child, TemplateTypeParameter):
            self.template_types[child.name] = child

            if child.name in self.template_type_comments:
                child.merge_comment(self.template_type_comments[child.name])

    def parse_comment(self):
        m = Parser.parse(self._comment.text)

        if len(m.brief) > 0:
            self._comment.brief = m.brief
            self._comment.doc = m.body

            for p in m.preparam:
                cm = Comment(p.description, self._comment.location)
                self.template_type_comments[p.name] = cm

                if p.name in self.template_types:
                    self.template_types[p.name].merge_comment(cm)

# vi:ts=4:et

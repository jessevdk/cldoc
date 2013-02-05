from node import Node
from clang import cindex
from ctype import Type
from comment import Comment

import re

class Argument:
    def __init__(self, func, cursor):
        self.cursor = cursor
        self.parent = func

        self._type = Type(self.cursor.type)

    @property
    def name(self):
        return self.cursor.spelling

    @property
    def type(self):
        return self._type

    @property
    def qid(self):
        return self.parent.qid + '::' + self.name

class Function(Node):
    kind = cindex.CursorKind.FUNCTION_DECL

    recomment = re.compile('^' + Comment.rebrief + '\s*' + Comment.reparams + '\s*' + Comment.redoc + '\s*' + Comment.rereturn, re.S)
    reparam = re.compile(Comment.reparam)

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self._return_type = Type(self.cursor.type.get_result())

        self._arguments = []

        for child in cursor.get_children():
            if child.kind != cindex.CursorKind.PARM_DECL:
                continue

            self._arguments.append(Argument(self, child))

    def parse_comment(self):
        m = Function.recomment.match(self.comment.text)
        self.comment.params = {}

        if m:
            self.comment.brief = m.group('brief').strip()
            self.comment.doc = m.group('doc').strip()

            self.comment.returns = m.group('return')

            for p in Function.reparam.finditer(m.group('params')):
                self.comment.params[p.group('paramname')] = p.group('paramdoc').strip()

    @property
    def return_type(self):
        return self._return_type

    @property
    def arguments(self):
        return list(self._arguments)

# vi:ts=4:et

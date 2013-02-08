from node import Node
from cldoc.clang import cindex
from ctype import Type
from cldoc.comment import Comment
from cldoc.comment import Parser

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

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self._return_type = Type(self.cursor.type.get_result())

        self._arguments = []

        for child in cursor.get_children():
            if child.kind != cindex.CursorKind.PARM_DECL:
                continue

            self._arguments.append(Argument(self, child))

    @property
    def resolve_nodes(self):
        for arg in self._arguments:
            yield arg

    @property
    def argument_names(self):
        for k in self._arguments:
            yield k.name

    def parse_comment(self):
        m = Parser.parse(self._comment.text)
        self._comment.params = {}

        if len(m.brief) > 0:
            self._comment.brief = m.brief
            self._comment.doc = m.body

            for pre in m.preparam:
                self._comment.params[pre.name] = pre.description

            for post in m.postparam:
                if post.name == 'return':
                    self._comment.returns = post.description

    @property
    def return_type(self):
        return self._return_type

    @property
    def arguments(self):
        return list(self._arguments)

# vi:ts=4:et

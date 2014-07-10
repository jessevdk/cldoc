# This file is part of cldoc.  cldoc is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
from .node import Node
from .namespace import Namespace
from .ctype import Type

from cldoc.clang import cindex
from cldoc.comment import Comment
from cldoc.comment import Parser

import re

class Argument:
    def __init__(self, func, cursor):
        self.cursor = cursor
        self.parent = func
        self._type = None

        for child in cursor.get_children():
            if child.kind == cindex.CursorKind.TYPE_REF:
                self._type = Type(self.cursor.type, cursor=child)
                break

        if self._type is None:
            self._type = Type(self.cursor.type)

        self._refid = None

    @property
    def refid(self):
        return self.parent.refid + '::' + self.name

    @property
    def name(self):
        return self.cursor.spelling

    @property
    def type(self):
        return self._type

    @property
    def qid(self):
        return self.parent.qid + '::' + self.name

    @property
    def force_page(self):
        return False

    def semantic_path_until(self, other):
        if other == self.parent:
            ret = []
        else:
            ret = self.parent.semantic_path_until(other)

        ret.append(self)
        return ret

    def qlbl_from(self, other):
        if other == self.parent:
            return self.name

        return self.parent.qlbl_from(other) + '::' + self.name

    def qlbl_to(self, other):
        return other.qlbl_from(self)

    @property
    def semantic_parent(self):
        return self.parent

    @property
    def is_unlabeled(self):
        return False

class Function(Node):
    kind = cindex.CursorKind.FUNCTION_DECL

    def __init__(self, cursor, comment):
        super(Function, self).__init__(cursor, comment)

        self._return_type = Type(self.cursor.type.get_result())
        self._arguments = []

        for child in cursor.get_children():
            if child.kind != cindex.CursorKind.PARM_DECL:
                continue

            self._arguments.append(Argument(self, child))

    @property
    def semantic_parent(self):
        from namespace import Namespace

        parent = self.parent

        while not parent is None and not isinstance(parent, Namespace):
            parent = parent.parent

        return parent

    @property
    def resolve_nodes(self):
        for arg in self._arguments:
            yield arg

    @property
    def argument_names(self):
        for k in self._arguments:
            yield k.name

    def parse_comment(self):
        super(Function, self).parse_comment()
        self._comment.params = {}

        for pre in self._parsed_comment.preparam:
            self._comment.params[pre.name] = pre.description

        for post in self._parsed_comment.postparam:
            if post.name == 'return':
                self._comment.returns = post.description

    @property
    def return_type(self):
        return self._return_type

    @property
    def arguments(self):
        return list(self._arguments)

# vi:ts=4:et

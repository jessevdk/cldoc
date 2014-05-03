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
from node import Node
from method import Method
from function import Function
from ctype import Type

from cldoc.clang import cindex

class TemplateType(object):
    def __init__(self, node, cursor):
        self._node = node
        self._cursor = cursor
        self._default_type = None
        self._default_value = None

        if not self.is_non_type:
            for child in self._cursor.get_children():
                if child.kind == cindex.CursorKind.TYPE_REF:
                    self._default_type = Type(child.type)
                    break
        else:
            for child in self._cursor.get_children():
                if child.kind == cindex.CursorKind.TYPE_REF:
                    continue

                self._default_value = ''.join([t.spelling for t in child.get_tokens()][:-1])
                break

    @property
    def name(self):
        return self._cursor.spelling

    @property
    def default_type(self):
        return self._default_type

    @property
    def default_value(self):
        return self._default_value

    @property
    def is_non_type(self):
        return self._cursor.kind == cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER

    @property
    def non_type(self):
        return Type(self._cursor.type)

class FunctionTemplated(object):
    def __init__(self, cursor, comment):
        super(FunctionTemplated, self).__init__(cursor, comment)

        self._template_types = []

        for child in cursor.get_children():
            if child.kind != cindex.CursorKind.TEMPLATE_TYPE_PARAMETER and \
               child.kind != cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
                continue

            self._template_types.append(TemplateType(self, child))

    @property
    def template_types(self):
        return self._template_types

class FunctionTemplate(FunctionTemplated, Function):
    kind = None

    def __init__(self, cursor, comment):
        super(FunctionTemplate, self).__init__(cursor, comment)

class MethodTemplate(FunctionTemplated, Method):
    kind = None

    def __init__(self, cursor, comment):
        super(MethodTemplate, self).__init__(cursor, comment)

class FunctionPlexer(Node):
    kind = cindex.CursorKind.FUNCTION_TEMPLATE

    def __new__(cls, cursor, comment):
        if not cursor is None and (cursor.semantic_parent.kind == cindex.CursorKind.CLASS_DECL or \
                                   cursor.semantic_parent.kind == cindex.CursorKind.CLASS_TEMPLATE or \
                                   cursor.semantic_parent.kind == cindex.CursorKind.STRUCT_DECL):
            return MethodTemplate(cursor, comment)
        else:
            return FunctionTemplate(cursor, comment)

# vi:ts=4:et

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
from cldoc.clang import cindex

class FunctionTemplate(Function):
    kind = None

class MethodTemplate(Method):
    kind = None

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

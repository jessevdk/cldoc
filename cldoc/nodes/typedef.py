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
from cldoc.clang import cindex
from ctype import Type

class Typedef(Node):
    kind = cindex.CursorKind.TYPEDEF_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.process_children = True
        self.type = Type(self.cursor.type.get_canonical())

    def visit(self, cursor, citer):
        if cursor.kind == cindex.CursorKind.TYPE_REF:
            self.type = Type(cursor.type)

        return []



# vi:ts=4:et

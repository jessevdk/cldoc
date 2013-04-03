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

class EnumValue(Node):
    kind = cindex.CursorKind.ENUM_CONSTANT_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

    def compare_sort(self, other):
        if not isinstance(other, EnumValue) or not hasattr(self.cursor, 'location'):
            return Node.compare_sort(self, other)

        loc1 = self.cursor.location
        loc2 = other.cursor.location

        if loc1.line != loc2.line:
            return cmp(loc1.line, loc2.line)
        else:
            return cmp(loc1.column, loc2.column)

    @property
    def value(self):
        return self.cursor.enum_value

# vi:ts=4:et

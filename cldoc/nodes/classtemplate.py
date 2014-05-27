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
from .cclass import Class
from .cstruct import Struct
from .templated import Templated

from cldoc.clang import cindex

class StructTemplate(Struct, Templated):
    kind = None

    def __init__(self, cursor, comment):
        super(StructTemplate, self).__init__(cursor, comment)

class ClassTemplate(Class, Templated):
    kind = None

    def __init__(self, cursor, comment):
        super(ClassTemplate, self).__init__(cursor, comment)

class ClassTemplatePlexer(Node):
    kind = cindex.CursorKind.CLASS_TEMPLATE

    def __new__(cls, cursor, comment):
        # Check manually if this is actually a struct, so that we instantiate
        # the right thing. I'm not sure there is another way to do this right now
        l = list(cursor.get_tokens())

        for i in range(len(l)):
            if l[i].kind == cindex.TokenKind.PUNCTUATION and l[i].spelling == '>':
                if i < len(l) - 2:
                    if l[i + 1].kind == cindex.TokenKind.KEYWORD and \
                       l[i + 1].spelling == 'struct':
                        return StructTemplate(cursor, comment)
                break

        return ClassTemplate(cursor, comment)

# vi:ts=4:et

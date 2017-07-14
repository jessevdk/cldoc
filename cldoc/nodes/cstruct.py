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
from .cclass import Class

from cldoc.clang import cindex

class Struct(Class):
    kind = cindex.CursorKind.STRUCT_DECL

    def __init__(self, cursor, comment):
        Class.__init__(self, cursor, comment)

        self.typedef = None
        self.current_access = cindex.AccessSpecifier.PUBLIC

    @property
    def is_anonymous(self):
        return self.anonymous_id > 0 and self.typedef is None

    @property
    def comment(self):
        ret = Class.comment.fget(self)

        if not ret and self.typedef:
            ret = self.typedef.comment

        return ret

    @property
    def name(self):
        if not self.typedef is None:
            # The name is really the one of the typedef
            return self.typedef.name
        else:
            return Class.name.fget(self)

    @property
    def force_page(self):
        return not self.is_anonymous

# vi:ts=4:et

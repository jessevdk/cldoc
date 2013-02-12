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
from cldoc.struct import Struct

class Example(list):
    Item = Struct.define('Item', text='', classes=None)

    def append(self, text, classes=None):
        if isinstance(classes, basestring):
            classes = [classes]

        list.append(self, Example.Item(text=text, classes=classes))

# vi:ts=4:et

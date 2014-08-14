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

class Category(Node):
    def __init__(self, name):
        Node.__init__(self, None, None)

        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_unlabeled(self):
        return True

    def sorted_children(self):
        schildren = list(Node.sorted_children(self))

        # Keep categories in order though
        c = [x for x in self.children if isinstance(x, Category)]
        c.reverse()

        if len(c) == 0:
            return schildren

        for i in range(0, len(schildren)):
            if isinstance(schildren[i], Category):
                schildren[i] = c.pop()

        return schildren

# vi:ts=4:et

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
from .templatetypeparameter import TemplateTypeParameter, TemplateNonTypeParameter
from cldoc.comment import Comment
from cldoc.comment import Parser
import re

class Templated(Node):
    def __init__(self, cursor, comment):
        super(Templated, self).__init__(cursor, comment)

        self._template_types = {}
        self._template_type_comments = {}

        self.process_children = True

    def sorted_children(self):
        return list(self.children)

    def append(self, child):
        if isinstance(child, TemplateTypeParameter) or \
           isinstance(child, TemplateNonTypeParameter):
            self._template_types[child.name] = child

            if child.name in self._template_type_comments:
                child.merge_comment(self._template_type_comments[child.name])

        super(Templated, self).append(child)

    def parse_comment(self):
        m = Parser.parse(self._comment.text)

        if len(m.brief) > 0:
            self._comment.brief = m.brief
            self._comment.doc = m.body

            for p in m.preparam:
                cm = Comment(p.description, self._comment.location)
                self._template_type_comments[p.name] = cm

                if p.name in self._template_types:
                    self._template_types[p.name].merge_comment(cm)

# vi:ts=4:et
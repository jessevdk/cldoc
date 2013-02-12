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
class Generator(object):
    def __init__(self, tree=None, opts=None):
        self.tree = tree
        self.options = opts

    def generate(self, outdir):
        self.outdir = outdir

        for node in self.tree.root.sorted_children():
            self.generate_node(node)

    def generate_node(self, node, passfunc=None):
        for child in node.sorted_children():
            if passfunc is None or passfunc(child):
                self.generate_node(child)

# vi:ts=4:et

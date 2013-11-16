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
# -*- coding: utf-8 -*-

from clang import cindex
import tempfile

from defdict import Defdict

import comment
import nodes
import includepaths
import documentmerger

from cldoc import example

import os, sys, sets, re, glob, platform

if platform.system() == 'Darwin':
    libclang = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib'

    if os.path.exists(libclang):
        cindex.Config.set_library_path(os.path.dirname(libclang))

class Tree(documentmerger.DocumentMerger):
    def __init__(self, files, flags):
        self.processed = {}
        self.files = [os.path.realpath(f) for f in files]
        self.flags = includepaths.flags(flags)

        # Sort files on sources, then headers
        self.files.sort(lambda a, b: cmp(self.is_header(a), self.is_header(b)))

        self.processing = {}
        self.kindmap = {}

        # Things to skip
        self.kindmap[cindex.CursorKind.USING_DIRECTIVE] = None

        # Create a map from CursorKind to classes representing those cursor
        # kinds.
        for cls in nodes.Node.subclasses():
            if hasattr(cls, 'kind'):
                self.kindmap[cls.kind] = cls

        self.root = nodes.Root()

        self.all_nodes = []
        self.cursor_to_node = Defdict()
        self.usr_to_node = Defdict()
        self.qid_to_node = Defdict()

        # Map from category name to the nodes.Category for that category
        self.category_to_node = Defdict()

        # Map from filename to comment.CommentsDatabase
        self.commentsdbs = Defdict()

        self.qid_to_node[None] = self.root
        self.usr_to_node[None] = self.root

    def is_header(self, filename):
        return filename.endswith('.hh') or filename.endswith('.hpp') or filename.endswith('.h')

    def find_node_comment(self, node):
        for location in node.comment_locations:
            db = self.commentsdbs[location.file.name]

            if db:
                cm = db.lookup(location)

                if cm:
                    return cm

        return None

    def process(self):
        """
        process processes all the files with clang and extracts all relevant
        nodes from the generated AST
        """

        index = cindex.Index.create()
        self.headers = {}

        for f in self.files:
            if f in self.processed:
                continue

            print "Processing `%s'" % (os.path.basename(f),)

            tu = index.parse(f, self.flags)

            if len(tu.diagnostics) != 0:
                fatal = False

                for d in tu.diagnostics:
                    sys.stderr.write(d.format)
                    sys.stderr.write("\n")

                    if d.severity == cindex.Diagnostic.Fatal or \
                       d.severity == cindex.Diagnostic.Error:
                        fatal = True

                if fatal:
                    sys.stderr.write("\nCould not generate documentation due to parser errors\n")
                    sys.exit(1)

            if not tu:
                sys.stderr.write("Could not parse file %s...\n" % (f,))
                sys.exit(1)

            # Extract comments from files and included files that we are
            # supposed to inspect
            extractfiles = [f]

            for inc in tu.get_includes():
                filename = str(inc.include)
                self.headers[filename] = True

                if filename in self.processed or (not filename in self.files) or filename in extractfiles:
                    continue

                extractfiles.append(filename)

            for e in extractfiles:
                db = comment.CommentsDatabase(e, tu)

                self.add_categories(db.category_names)
                self.commentsdbs[e] = db

            self.visit(tu.cursor.get_children())

            for f in self.processing:
                self.processed[f] = True

            self.processing = {}

        # Construct hierarchy of nodes.
        for node in self.all_nodes:
            q = node.qid

            if node.parent is None:
                par = self.find_parent(node)

                # Lookup categories for things in the root
                if (par is None or par == self.root) and (not node.cursor is None):
                    location = node.cursor.extent.start
                    db = self.commentsdbs[location.file.name]

                    if db:
                        par = self.category_to_node[db.lookup_category(location)]

                if par is None:
                    par = self.root

                par.append(node)

            # Resolve comment
            cm = self.find_node_comment(node)

            if cm:
                node.merge_comment(cm)

        # Keep track of classes to resolve bases and subclasses
        classes = {}

        # Map final qid to node
        for node in self.all_nodes:
            q = node.qid
            self.qid_to_node[q] = node

            if isinstance(node, nodes.Class):
                classes[q] = node

        # Resolve bases and subclasses
        for qid in classes:
            classes[qid].resolve_bases(classes)

        self.markup_code(index)

    def markup_code(self, index):
        for node in self.all_nodes:
            if not node.comment:
                continue

            if not node.comment.doc:
                continue

            comps = node.comment.doc.components

            for i in range(len(comps)):
                component = comps[i]

                if not isinstance(component, comment.Comment.Example):
                    continue

                text = str(component)

                tmpfile = tempfile.NamedTemporaryFile(delete=False)
                tmpfile.write(text)
                filename = tmpfile.name
                tmpfile.close()

                tu = index.parse(filename, self.flags, options=1)
                tokens = tu.get_tokens(extent=tu.get_extent(filename, (0, os.stat(filename).st_size)))
                os.unlink(filename)

                hl = []
                incstart = None

                for token in tokens:
                    start = token.extent.start.offset
                    end = token.extent.end.offset

                    if token.kind == cindex.TokenKind.KEYWORD:
                        hl.append((start, end, 'keyword'))
                        continue
                    elif token.kind == cindex.TokenKind.COMMENT:
                        hl.append((start, end, 'comment'))

                    cursor = token.cursor

                    if cursor.kind == cindex.CursorKind.PREPROCESSING_DIRECTIVE:
                        hl.append((start, end, 'preprocessor'))
                    elif cursor.kind == cindex.CursorKind.INCLUSION_DIRECTIVE and incstart is None:
                        incstart = cursor
                    elif (not incstart is None) and \
                         token.kind == cindex.TokenKind.PUNCTUATION and \
                         token.spelling == '>':
                        hl.append((incstart.extent.start.offset, end, 'preprocessor'))
                        incstart = None

                ex = example.Example()
                lastpos = 0

                for ih in range(len(hl)):
                    h = hl[ih]

                    ex.append(text[lastpos:h[0]])
                    ex.append(text[h[0]:h[1]], h[2])

                    lastpos = h[1]

                ex.append(text[lastpos:])
                comps[i] = ex

    def match_ref(self, child, name):
        if isinstance(name, basestring):
            return name == child.name
        else:
            return name.match(child.name)

    def find_ref(self, node, name, goup):
        if node is None:
            return []

        ret = []

        for child in node.resolve_nodes:
            if self.match_ref(child, name):
                ret.append(child)

        if goup and len(ret) == 0:
            return self.find_ref(node.parent, name, True)
        else:
            return ret

    def cross_ref(self, node = None):
        if node is None:
            node = self.root

        if node.comment:
            node.comment.resolve_refs(self.find_ref, node)

        for child in node.children:
            self.cross_ref(child)

    def decl_on_c_struct(self, node, tp):
        n = self.cursor_to_node[tp.decl]

        if isinstance(n, nodes.Struct) or \
           isinstance(n, nodes.Typedef) or \
           isinstance(n, nodes.Enum):
            return n

        return None

    def node_on_c_struct(self, node):
        if isinstance(node, nodes.Method) or \
           not isinstance(node, nodes.Function):
            return None

        decl = self.decl_on_c_struct(node, node.return_type)

        if not decl:
            args = node.arguments

            if len(args) > 0:
                decl = self.decl_on_c_struct(node, args[0].type)

        return decl

    def find_parent(self, node):
        cursor = node.cursor

        # If node is a C function, then see if we should group it to a struct
        parent = self.node_on_c_struct(node)

        if parent:
            return parent

        while cursor:
            cursor = cursor.semantic_parent
            parent = self.cursor_to_node[cursor]

            if parent:
                return parent

        return self.root

    def register_node(self, node, parent=None):
        self.all_nodes.append(node)

        self.usr_to_node[node.cursor.get_usr()] = node
        self.cursor_to_node[node.cursor] = node

        # Typedefs in clang are not parents of typedefs, but we like it better
        # that way, explicitly set the parent directly here
        if parent and isinstance(parent, nodes.Typedef):
            parent.append(node)

        if parent and hasattr(parent, 'current_access'):
            node.access = parent.current_access

    def register_anon_typedef(self, node, parent):
        node.typedef = parent
        node.add_comment_location(parent.cursor.extent.start)

        self.all_nodes.remove(parent)

        # Map references to the typedef directly to the node
        self.usr_to_node[parent.cursor.get_usr()] = node
        self.cursor_to_node[parent.cursor] = node

    def cursor_is_exposed(self, cursor):
        # Only cursors which are in headers are exposed.
        filename = str(cursor.location.file)
        return filename in self.headers or self.is_header(filename)

    def visit(self, citer, parent=None):
        """
        visit iterates over the provided cursor iterator and creates nodes
        from the AST cursors.
        """
        if not citer:
            return

        while True:
            try:
                item = citer.next()
            except StopIteration:
                return

            # Check the source of item
            if not item.location.file:
                self.visit(item.get_children())
                continue

            # Ignore files we already processed
            if str(item.location.file) in self.processed:
                continue

            # Ignore files other than the ones we are scanning for
            if not str(item.location.file) in self.files:
                continue

            # Ignore unexposed things
            if item.kind == cindex.CursorKind.UNEXPOSED_DECL:
                self.visit(item.get_children(), parent)
                continue

            self.processing[str(item.location.file)] = True

            if item.kind in self.kindmap:
                cls = self.kindmap[item.kind]

                if not cls:
                    # Skip
                    continue

                # see if we already have a node for this thing
                node = self.usr_to_node[item.get_usr()]

                if not node:
                    # Only register new nodes if they are exposed.
                    if self.cursor_is_exposed(item):
                        node = cls(item, None)
                        self.register_node(node, parent)

                elif isinstance(parent, nodes.Typedef) and isinstance(node, nodes.Struct):
                    # Typedefs are handled a bit specially because what happens
                    # is that clang first exposes an unnamed struct/enum, and
                    # then exposes the typedef, with as a child again the
                    # cursor to the already defined struct/enum. This is a
                    # bit reversed as to how we normally process things.
                    self.register_anon_typedef(node, parent)
                else:
                    self.cursor_to_node[item] = node
                    node.add_ref(item)

                if node and node.process_children:
                    self.visit(item.get_children(), node)
            else:
                par = self.cursor_to_node[item.semantic_parent]

                if not par:
                    par = parent

                if par:
                    ret = par.visit(item, citer)

                    if not ret is None:
                        for node in ret:
                            self.register_node(node, par)

                ignoretop = [cindex.CursorKind.TYPE_REF]

                if (not par or ret is None) and not item.kind in ignoretop:
                    sys.stderr.write("Unhandled cursor: %s\n" % (item.kind))

# vi:ts=4:et

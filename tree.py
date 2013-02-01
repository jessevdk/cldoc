# -*- coding: utf-8 -*-

from clang import cindex

from defdict import Defdict

import comment
import nodes
import includepaths

import os, sys, sets, re, glob

class Tree:
    def __init__(self, files, flags):
        self.processed = {}
        self.files = [os.path.realpath(f) for f in files]
        self.flags = flags

        self.processing = {}
        self.kindmap = {}

        # Create a map from CursorKind to classes representing those cursor
        # kinds.
        for cls in nodes.Node.subclasses():
            if hasattr(cls, 'kind'):
                self.kindmap[cls.kind] = cls

        self.root = nodes.Root()

        self.cursor_to_node = Defdict()
        self.usr_to_node = Defdict()
        self.qid_to_node = Defdict()
        self.comments = Defdict()

        self.qid_to_node[None] = self.root
        self.usr_to_node[None] = self.root

    def merge(self, *files):
        for f in files:
            if os.path.isdir(f):
                self.merge(*glob.glob(os.path.join(f, '*.md')))
            else:
                self._merge_file(f)

    def _split_categories(self, filename):
        lines = open(filename).readlines()

        ret = {}

        category = None
        doc = []
        first = False

        for line in lines:
            prefix = '#<cldoc:'

            line = line.rstrip('\n')

            if first:
                first = False

                if line == '':
                    continue

            if line.startswith(prefix) and line.endswith('>'):
                if len(doc) > 0 and not category:
                    sys.stderr.write('Failed to merge file `{0}\': no #<cldoc:id> specified\n'.format(filename))
                    sys.exit(1)

                if category:
                    ret[category] = "\n".join(doc)

                doc = []
                category = line[len(prefix):-1]
                first = True
            else:
                doc.append(line)

        if category:
            ret[category] = "\n".join(doc)
        elif len(doc) > 0:
            sys.stderr.write('Failed to merge file `{0}\': no #<cldoc:id> specified\n'.format(filename))
            sys.exit(1)

        return ret

    def _normalized_qid(self, qid):
        if qid == 'index':
            return None

        if qid.startswith('::'):
            return qid[2:]

        return qid

    def _merge_file(self, filename):
        categories = self._split_categories(filename)

        for category in categories:
            parts = category.split('/')

            qid = self._normalized_qid(parts[0])
            key = 'doc'

            if len(parts) > 1:
                key = parts[1]

            if not self.qid_to_node[qid]:
                sys.stderr.write('Could not find node for id `{0}\'\n'.format(parts[0]))
                sys.exit(1)

            node = self.qid_to_node[qid]

            if key == 'doc':
                node.merge_comment(comment.Comment(categories[category]), override=True)
            else:
                sys.stderr.write('Unknown type `{0}\' for id `{1}\'\n'.format(key, parts[0]))
                sys.exit(1)

    def add_categories(self, categories, categoriesmap):
        secmap = {}

        for category in categories:
            parts = category.split('::')

            root = self.root

            for part in parts:
                found = False

                for child in root.children:
                    if isinstance(child, nodes.Category) and child.name == part:
                        root = child
                        found = True
                        break

                if not found:
                    s = nodes.Category(part)
                    root.append(s)

                    root = s

            secmap[category] = root

        for cursor in categoriesmap:
            categoriesmap[cursor] = secmap[categoriesmap[cursor]]

    def process(self):
        """
        process processes all the files with clang and extracts all relevant
        nodes from the generated AST
        """

        index = cindex.Index.create()
        categoriesmap = {}

        for f in self.files:
            if f in self.processed:
                continue

            print "Processing `%s'" % (os.path.basename(f),)
            tu = index.parse(f, self.flags + includepaths.flags)

            if len(tu.diagnostics) != 0:
                    for d in tu.diagnostics:
                        sys.stderr.write(d.format)
                        sys.stderr.write("\n")

                    sys.exit(1)

            if not tu:
                sys.stderr.write("Could not parse file %s...\n" % (f,))
                sys.exit(1)

            # Extract comments from files and included files that we are
            # supposed to inspect
            extractfiles = [f]

            for inc in tu.get_includes():
                filename = str(inc.source)

                if filename in self.processed or (not filename in self.files) or filename in extractfiles:
                    continue

                extractfiles.append(filename)

            for e in extractfiles:
                comments, categories, secmap = comment.extract(e, tu)
                self.add_categories(categories, secmap)

                categoriesmap.update(secmap)
                self.comments.update(comments)

            self.visit(tu.cursor.get_children())

            for f in self.processing:
                self.processed[f] = True

            self.processing = {}

        # Construct hierarchy of nodes.
        nds = sets.Set(self.cursor_to_node.values())

        for node in nds:
            q = node.qid

            if node.parent is None:
                par = self.find_parent(node)

                if (par is None or par == self.root) and node.cursor in categoriesmap:
                    par = categoriesmap[node.cursor]

                if not par is None:
                    par.append(node)

        for node in self.root.descendants():
            self.qid_to_node[node.qid] = node

        # Resolve cross-references in documentation
        self.cross_ref(self.root)

    def find_ref(self, node, name):
        if node is None:
            return None

        for child in node.children:
            if child.name == name:
                return child

        return self.find_ref(node.parent, name)

    def cross_ref(self, node):
        if node.comment:
            def resolver(name):
                return self.find_ref(node, name)

            node.comment.resolve_refs(resolver)

        for child in node.children:
            self.cross_ref(child)

    def decl_on_c_struct(self, node, tp):
        n = self.cursor_to_node[tp.decl]

        if isinstance(n, nodes.Struct) or isinstance(n, nodes.Typedef):
            return n

        return None

    def node_on_c_struct(self, node):
        if not isinstance(node, nodes.Function):
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
        self.usr_to_node[node.cursor.get_usr()] = node
        self.cursor_to_node[node.cursor] = node

        # Typedefs in clang are not parents of typerefs, but we like it better
        # that way, explicitly set the parent directly here
        if parent and isinstance(parent, nodes.Typedef):
            parent.append(node)

        if parent and hasattr(parent, 'current_access'):
            node.access = parent.current_access

    def register_anon_typedef(self, node, parent):
        node.typedef = parent

        # Map references to the typedef directly to the node
        self.usr_to_node[parent.cursor.get_usr()] = node
        self.cursor_to_node[parent.cursor] = node

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

                # see if we already have a node for this thing
                node = self.usr_to_node[item.get_usr()]

                if not node:
                    node = cls(item, self.comments[item])
                    self.register_node(node, parent)
                elif isinstance(parent, nodes.Typedef):
                    # Typedefs are handled a bit specially because what happens
                    # is that clang first exposes an unnamed struct/enum, and
                    # then exposes the typedef, with as a child again the
                    # cursor to the already defined struct/enum. This is a
                    # bit reversed as to how we normally process things.
                    self.register_anon_typedef(node, parent)
                else:
                    node.merge_comment(self.comments[item])
                    self.cursor_to_node[item] = node

                if node.process_children:
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

                if not par or ret is None:
                    sys.stderr.write("Unhandled cursor: %s\n" % (item.kind))

# vi:ts=4:et

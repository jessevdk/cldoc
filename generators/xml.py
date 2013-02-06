from __future__ import absolute_import
from clang import cindex

from .generator import Generator
import nodes

from xml.etree import ElementTree
import sys, os

class Xml(Generator):
    def __init__(self, tree):
        Generator.__init__(self, tree)

    def generate(self, outdir):
        if not outdir:
            outdir = 'xml'

        try:
            os.makedirs(outdir)
        except OSError:
            pass

        self.index = ElementTree.Element('index')

        self.indexmap = {
            self.tree.root: self.index
        }

        cm = self.tree.root.comment

        if cm:
            if cm.brief:
                self.index.append(self.doc_to_xml(self.tree.root, cm.brief, 'brief'))

            if cm.doc:
                self.index.append(self.doc_to_xml(self.tree.root, cm.doc))

        Generator.generate(self, outdir)

        self.write_xml(self.index, 'index.xml')

    def indent(self, elem, level=0):
        i = "\n" + "  " * level

        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "

            for e in elem:
                self.indent(e, level + 1)

                if not e.tail or not e.tail.strip():
                    e.tail = i + "  "
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def write_xml(self, elem, fname):
        tree = ElementTree.ElementTree(elem)

        self.indent(tree.getroot())

        f = open(os.path.join(self.outdir, fname), 'w')
        tree.write(f, encoding='utf-8', xml_declaration=True)
        f.close()

    def is_page(self, node):
        if isinstance(node, nodes.Class):
            for child in node.children:
                if not (isinstance(child, nodes.Field) or \
                        isinstance(child, nodes.Variable) or \
                        isinstance(child, nodes.TemplateTypeParameter)):
                    return True

            return False

        pagecls = [nodes.Namespace, nodes.Category, nodes.Root]

        for cls in pagecls:
            if isinstance(node, cls):
                return True

        if isinstance(node, nodes.Typedef) and len(node.children) > 0:
            return True

        return False

    def is_top(self, node):
        if self.is_page(node):
            return True

        if node.parent == self.tree.root:
            return True

        return False

    def add_ref_node_id(self, node, elem):
        parent = node

        meid = node.qid

        if not node.parent or (isinstance(node.parent, nodes.Root) and not self.is_page(node)):
            elem.set('ref', 'index#' + meid)
            return

        # Find topmost parent
        while not self.is_page(node):
            node = node.parent

        if not node is None:
            elem.set('ref', node.qid + '#' + meid)

    def add_ref_id(self, cursor, elem):
        if not cursor:
            return

        if cursor in self.tree.cursor_to_node:
            node = self.tree.cursor_to_node[cursor]
        elif cursor.get_usr() in self.tree.usr_to_node:
            node = self.tree.usr_to_node[cursor.get_usr()]
        else:
            return

        self.add_ref_node_id(node, elem)

    def type_to_xml(self, tp, parent=None):
        elem = ElementTree.Element('type')

        if tp.is_array:
            elem.set('size', str(tp.array_size))
            elem.append(self.type_to_xml(tp.element_type, parent))
        else:
            elem.set('name', tp.typename_for(parent))

        if len(tp.qualifier) > 0:
            elem.set('qualifier', " ".join(tp.qualifier))

        if tp.builtin:
            elem.set('builtin', 'yes')

        self.add_ref_id(tp.decl, elem)
        return elem

    def enumvalue_to_xml(self, node, elem):
        elem.set('value', str(node.value))

    def function_to_xml(self, node, elem):
        if not (isinstance(node, nodes.Constructor) or
                isinstance(node, nodes.Destructor)):
            ret = ElementTree.Element('return')

            if node.comment and hasattr(node.comment, 'returns') and node.comment.returns:
                ret.append(self.doc_to_xml(node, node.comment.returns))

            tp = self.type_to_xml(node.return_type, node.parent)

            ret.append(tp)
            elem.append(ret)

        for arg in node.arguments:
            ret = ElementTree.Element('argument')
            ret.set('name', arg.name)
            ret.set('id', arg.qid)

            if node.comment and arg.name in node.comment.params:
                ret.append(self.doc_to_xml(node, node.comment.params[arg.name]))

            ret.append(self.type_to_xml(arg.type, node.parent))
            elem.append(ret)

    def typedef_to_xml(self, node, elem):
        elem.append(self.type_to_xml(node.type, node))

    def typedef_to_xml_ref(self, node, elem):
        elem.append(self.type_to_xml(node.type, node))

    def variable_to_xml(self, node, elem):
        elem.append(self.type_to_xml(node.type, node.parent))

    def set_access_attribute(self, node, elem):
        if node.access == cindex.CXXAccessSpecifier.PROTECTED:
            elem.set('access', 'protected')
        elif node.access == cindex.CXXAccessSpecifier.PRIVATE:
            elem.set('access', 'private')
        elif node.access == cindex.CXXAccessSpecifier.PUBLIC:
            elem.set('access', 'public')

    def class_to_xml(self, node, elem):
        for base in node.bases:
            child = ElementTree.Element('base')

            self.set_access_attribute(base, child)

            child.append(self.type_to_xml(base.type, node))
            elem.append(child)

    def field_to_xml(self, node, elem):
        elem.append(self.type_to_xml(node.type, node.parent))

    def doc_to_xml(self, parent, doc, tagname='doc'):
        doce = ElementTree.Element(tagname)

        s = ''
        last = None

        for component in doc.components:
            if isinstance(component, basestring):
                s += component
            else:
                if last is None:
                    doce.text = s
                else:
                    last.tail = s

                s = ''

                last = ElementTree.Element('ref')
                last.text = parent.qid_from(component.qid)

                self.add_ref_node_id(component, last)

                doce.append(last)

        if last is None:
            doce.text = s
        else:
            last.tail = s

        return doce

    def call_type_specific(self, node, elem, fn):
        cls = node.__class__

        while cls != nodes.Node:
            nm = cls.__name__.lower() + '_' + fn

            if hasattr(self, nm):
                getattr(self, nm)(node, elem)
                break

            cls = cls.__base__

    def node_to_xml(self, node):
        elem = ElementTree.Element(node.classname)
        props = node.props

        for prop in props:
            if props[prop]:
                elem.set(prop, props[prop])

        if node.comment and node.comment.brief:
            elem.append(self.doc_to_xml(node, node.comment.brief, 'brief'))

        if node.comment and node.comment.doc:
            elem.append(self.doc_to_xml(node, node.comment.doc))

        self.call_type_specific(node, elem, 'to_xml')

        for child in node.sorted_children():
            if child.access == cindex.CXXAccessSpecifier.PRIVATE:
                continue

            if self.is_page(child):
                chelem = self.node_to_xml_ref(child)
            else:
                chelem = self.node_to_xml(child)

            elem.append(chelem)

        return elem

    def generate_page(self, node):
        elem = self.node_to_xml(node)
        self.write_xml(elem, node.qid + '.xml')

    def node_to_xml_ref(self, node):
        elem = ElementTree.Element(node.classname)
        props = node.props

        # Add reference item to index
        self.add_ref_node_id(node, elem)

        if 'name' in props:
            elem.set('name', props['name'])

        if node.comment and node.comment.brief:
            elem.append(self.doc_to_xml(node, node.comment.brief, 'brief'))

        self.call_type_specific(node, elem, 'to_xml_ref')

        return elem

    def generate_node(self, node):
        # Ignore private stuff
        if node.access == cindex.CXXAccessSpecifier.PRIVATE:
            return

        if self.is_page(node):
            elem = self.node_to_xml_ref(node)

            self.indexmap[node.parent].append(elem)
            self.indexmap[node] = elem

            self.generate_page(node)
        elif self.is_top(node):
            self.index.append(self.node_to_xml(node))

        if isinstance(node, nodes.Namespace) or isinstance(node, nodes.Category):
            # Go deep for namespaces and categories
            Generator.generate_node(self, node)
        elif isinstance(node, nodes.Class):
            # Go deep, but only for inner classes
            Generator.generate_node(self, node, lambda x: isinstance(x, nodes.Class))

# vi:ts=4:et

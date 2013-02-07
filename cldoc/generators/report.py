from __future__ import absolute_import

import inspect, os, shutil

from cldoc.struct import Struct
from cldoc.clang import cindex

from cldoc import nodes

from xml.etree import ElementTree

class Report:
    Coverage = Struct.define('Coverage', name='', documented=[], undocumented=[])

    def __init__(self, tree):
        self.tree = tree

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

    def arguments(self, root):
        elem = ElementTree.Element('arguments')
        root.append(elem)

        for node in self.tree.all_nodes:
            if not isinstance(node, nodes.Function):
                continue

            if node.access == cindex.CXXAccessSpecifier.PRIVATE:
                continue

            if not node.comment:
                continue

            # Check documented arguments
            notdocumented = []
            misspelled = []

            cm = node.comment
            argnames = {}

            for name in node.argument_names:
                argnames[name] = False

            for k in cm.params:
                if k in argnames:
                    argnames[k] = True
                else:
                    misspelled.append(k)

            for k in argnames:
                if not argnames[k]:
                    notdocumented.append(k)

            if node.return_type.typename != 'void' and not hasattr(cm, 'returns'):
                missingret = True
            else:
                missingret = False

            if len(notdocumented) > 0 or len(misspelled) > 0 or missingret:
                e = ElementTree.Element('function')
                e.set('id', node.qid)
                e.set('name', node.name)

                loc = node.cursor.extent.start
                e.set('file', os.path.relpath(str(loc.file)))
                e.set('line', str(loc.line))
                e.set('column', str(loc.column))

                if missingret:
                    ee = ElementTree.Element('undocumented-return')
                    e.append(ee)

                for ndoc in notdocumented:
                    ee = ElementTree.Element('undocumented')
                    ee.set('name', ndoc)
                    e.append(ee)

                for mis in misspelled:
                    ee = ElementTree.Element('misspelled')
                    ee.set('name', mis)
                    e.append(ee)

                elem.append(e)

    def coverage(self, root):
        pertype = {}

        for node in self.tree.all_nodes:
            cname = node.__class__.__name__

            if node.access == cindex.CXXAccessSpecifier.PRIVATE:
                continue

            if not cname in pertype:
                pertype[cname] = Report.Coverage(name=cname.lower())

            if node.comment:
                pertype[cname].documented.append(node)
            else:
                pertype[cname].undocumented.append(node)

        cov = ElementTree.Element('coverage')
        root.append(cov)

        for item in pertype.values():
            elem = ElementTree.Element('type')
            elem.set('name', item.name)
            elem.set('documented', str(len(item.documented)))
            elem.set('undocumented', str(len(item.undocumented)))

            item.undocumented.sort(key=lambda x: x.qid)

            for undoc in item.undocumented:
                e = ElementTree.Element('undocumented')
                e.set('id', undoc.qid)
                e.set('name', undoc.name)

                loc = undoc.cursor.extent.start
                e.set('file', os.path.relpath(str(loc.file)))
                e.set('line', str(loc.line))
                e.set('column', str(loc.column))

                elem.append(e)

            cov.append(elem)

    def generate(self, filename):
        root = ElementTree.Element('report')
        root.set('id', filename)
        root.set('title', 'Documention generator')

        self.coverage(root)
        self.arguments(root)



        root.append(doc)

        return root

# vi:ts=4:et

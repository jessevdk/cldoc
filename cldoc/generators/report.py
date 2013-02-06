from __future__ import absolute_import

import inspect, os, shutil

from .generator import Generator
from cldoc.struct import Struct
from cldoc.clang import cindex

from xml.etree import ElementTree

class Report(Generator):
    Coverage = Struct.define('Coverage', name='', documented=[], undocumented=[])

    def __init__(self, t):
        Generator.__init__(self, t)

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
                e.set('file', str(loc.file))
                e.set('line', str(loc.line))
                e.set('column', str(loc.column))

                elem.append(e)

            cov.append(elem)

    def generate(self, output):
        root = ElementTree.Element('report')
        self.coverage(root)

        tree = ElementTree.ElementTree(root)
        self.indent(tree.getroot())

        outfile = os.path.join(output, 'report.xml')

        f = open(outfile, 'w')
        tree.write(f, encoding='utf-8', xml_declaration=True)
        f.close()

        print('Generated `{0}\''.format(outfile))

# vi:ts=4:et

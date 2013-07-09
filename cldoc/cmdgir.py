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
from __future__ import absolute_import

import sys, argparse, re, os

try:
    from xml.etree import cElementTree as ElementTree
except:
    from xml.etree import ElementTree

from cldoc.clang import cindex

from . import defdict

from . import nodes
from . import generators
from . import comment
from . import documentmerger

def nsgtk(s):
    return '{{{0}}}{1}'.format('http://www.gtk.org/introspection/core/1.0', s)

def nsc(s):
    return '{{{0}}}{1}'.format('http://www.gtk.org/introspection/c/1.0', s)

def nsglib(s):
    return '{{{0}}}{1}'.format('http://www.gtk.org/introspection/glib/1.0', s)

def stripns(tag):
    try:
        pos = tag.index('}')
        return tag[pos+1:]
    except:
        return tag

class Interface(nodes.Class):
    @property
    def classname(self):
        return '{http://jessevdk.github.com/cldoc/gobject/1.0}interface'

class Class(nodes.Class):
    def __init__(self, cursor, comment):
        nodes.Class.__init__(self, cursor, comment)

        # Extract bases
        for b in cursor.bases:
            self.bases.append(nodes.Class.Base(b))

        for i in cursor.implements:
            self.implements.append(nodes.Class.Base(i))

    @property
    def classname(self):
        return '{http://jessevdk.github.com/cldoc/gobject/1.0}class'

class Property(nodes.Node):
    def __init__(self, cursor, comment):
        nodes.Node.__init__(self, cursor, comment)

        self.type = nodes.Type(cursor.type)

    @property
    def classname(self):
        return '{http://jessevdk.github.com/cldoc/gobject/1.0}property'

    @property
    def props(self):
        ret = nodes.Node.props.fget(self)

        mode = []

        if not ('writable' in self.cursor.node.attrib and self.cursor.node.attrib['writable'] == '1'):
            mode.append('readonly')

        if 'construct-only' in self.cursor.node.attrib and self.cursor.node.attrib['construct-only'] == '1':
            mode.append('construct-only')

        if 'construct' in self.cursor.node.attrib and self.cursor.node.attrib['construct'] == '1':
            mode.append('construct')

        if len(mode) > 0:
            ret['mode'] = ",".join(mode)

        return ret

class Boxed(nodes.Struct):
    def __init__(self, cursor, comment):
        nodes.Struct.__init__(self, cursor, comment)

    @property
    def classname(self):
        return '{http://jessevdk.github.com/cldoc/gobject/1.0}boxed'

    @property
    def force_page(self):
        return True

class GirComment(comment.Comment):
    hashref = re.compile('#([a-z_][a-z0-9_]*)', re.I)
    emph = re.compile('<emphasis>(.*?)</emphasis>', re.I)
    title = re.compile('<title>(.*?)</title>', re.I)
    refsect2 = re.compile('(<refsect2 [^>]*>|</refsect2>)\n?', re.I)
    varref = re.compile('@([a-z][a-z0-9_]*)', re.I)
    constref = re.compile('%([a-z_][a-z0-9_]*)', re.I)

    def __init__(self, cursor):
        doc = cursor.node.find(nsgtk('doc'))

        if not doc is None:
            text = doc.text
        else:
            text = ''

        text = self.subst_format(text)

        brieftext = text
        doctext = ''

        try:
            firstdot = text.index('.')

            try:
                firstnl = text.index("\n")
            except:
                firstnl = firstdot

            if firstnl < firstdot:
                firstdot = firstnl - 1

            nextnonsp = firstdot + 1

            while nextnonsp < len(text) and text[nextnonsp] != '\n' and not text[nextnonsp].isspace():
                nextnonsp += 1

            if nextnonsp != len(text):
                # Replicate brief and non brief...
                # Insert newline just after .
                brieftext = text[:firstdot]
                doctext = text
        except:
            pass

        if cursor.typename in ['method', 'function', 'virtual-method', 'constructor']:
            # Assemble function argument comments and return value comment
            preat = []
            postat = []

            for param in cursor.children:
                paramdoc = param.node.find(nsgtk('doc'))

                if not paramdoc is None:
                    paramdoc = self.subst_format(paramdoc.text)
                else:
                    paramdoc = '*documentation missing...*'

                preat.append('@{0} {1}'.format(param.spelling, paramdoc.replace('\n', ' ')))

            return_node = cursor.node.find(nsgtk('return-value'))

            if not return_node is None and cursor.type.get_result().spelling != 'void':
                doc = return_node.find(nsgtk('doc'))

                if not doc is None:
                    postat.append('@return {0}'.format(self.subst_format(doc.text).replace('\n', ' ')))
                else:
                    postat.append('@return *documentation missing...*')

            if len(cursor.children) > 0:
                preat.append('')

                if len(doctext) > 0:
                    preat.append('')

            if brieftext == '':
                brieftext = '*Documentation missing...*'

            text = brieftext.replace('\n', ' ').rstrip() + "\n" + "\n".join(preat) + doctext

            if len(postat) != 0:
                text += '\n\n' + '\n'.join(postat)
        else:
            if doctext != '':
                text = brieftext + "\n\n" + doctext
            else:
                text = brieftext.replace("\n", ' ')

        comment.Comment.__init__(self, text, None)

    def subst_format(self, text):
        text = GirComment.hashref.sub(lambda x: '<{0}>'.format(x.group(1)), text)
        text = GirComment.varref.sub(lambda x: '<{0}>'.format(x.group(1)), text)
        text = GirComment.constref.sub(lambda x: '`{0}`'.format(x.group(1)), text)
        text = GirComment.emph.sub(lambda x: '*{0}*'.format(x.group(1)), text)
        text = GirComment.title.sub(lambda x: '## {0}'.format(x.group(1)), text)
        text = GirComment.refsect2.sub(lambda x: '', text)

        return text

class GirType:
    builtins = [
        'utf8',
        'gchar',
        'gint',
        'gint8',
        'gint16',
        'gint32',
        'gint64',
        'guint',
        'guint8',
        'guint16',
        'guint32',
        'guint64',
        'gfloat',
        'gdouble',
        'gpointer',
        'gsize',
        'gboolean',
        'none'
    ];

    def __init__(self, node):
        self.node = node
        self.kind = cindex.TypeKind.UNEXPOSED
        self.const_qualified = False

        self.is_out = False
        self.transfer_ownership = 'none'
        self.allow_none = False

        aname = nsc('type')

        if aname in self.node.attrib:
            self.spelling = self.node.attrib[aname]
        else:
            self.spelling = ''

        self._extract_const()
        self._extract_kind()
        self.declaration = None

        retval = self.node.find(nsgtk('return-value'))

        if not retval is None:
            self.return_type = GirCursor(retval).type

            if 'transfer-ownership' in retval.attrib:
                self.return_type.transfer_ownership = retval.attrib['transfer-ownership']

            if 'allow-none' in retval.attrib:
                self.return_type.allow_none = retval.attrib['allow-none'] == '1'
        else:
            self.return_type = None

    def is_builtin(self):
        return self.spelling in GirType.builtins

    def _extract_const(self):
        prefix = 'const '

        if self.spelling.startswith(prefix):
            self.const_qualified = True
            self.spelling = self.spelling[len(prefix):]

    def _extract_kind(self):
        if self.spelling == '':
            return

        if self.spelling.endswith('*'):
            self.kind = cindex.TypeKind.POINTER
            return

        for k in nodes.Type.namemap:
            if nodes.Type.namemap[k] == self.spelling:
                self.kind = k
                break

    def get_pointee(self):
        return GirTypePointer(self)

    def get_result(self):
        return self.return_type

    def get_canonical(self):
        return self

    def get_declaration(self):
        return self.declaration

    def is_const_qualified(self):
        return self.const_qualified

    def resolve_refs(self, resolver):
        if not self.return_type is None:
            self.return_type.resolve_refs(resolver)

        if not self.declaration is None:
            return

        if 'name' in self.node.attrib:
            name = self.node.attrib['name']
            self.declaration = resolver(name)

            if self.spelling == '' and not self.declaration is None:
                self.spelling = self.declaration.spelling

                if self.declaration.typename in ['record', 'class', 'interface']:
                    self.spelling += ' *'
                    self.kind = cindex.TypeKind.POINTER

            elif self.spelling == '' and name in GirType.builtins:
                if name == 'utf8':
                    self.spelling = 'gchar *'
                elif name == 'none':
                    self.spelling = 'void'
                else:
                    self.spelling = name

class GirTypePointer(GirType):
    def __init__(self, tp):
        self.node = tp.node
        self.pointer_type = tp
        self.spelling = tp.spelling[:-1]
        self.kind = cindex.TypeKind.UNEXPOSED
        self.const_qualified = False

        self._extract_const()
        self._extract_kind()

    def get_declaration(self):
        return self.pointer_type.get_declaration()

class GirCursor:
    kindmap = {
        'parameter': cindex.CursorKind.PARM_DECL
    }

    global_gerror_param = None

    def __init__(self, node):
        self.node = node
        self.typename = stripns(self.node.tag)
        self.children = []
        self.parent = None
        self.bases = None
        self.implements = None

        self.type = self._extract_type()
        self.kind = self._extract_kind()

        self._virtual_param = None

        if self._is_object_type():
            self._create_virtual_param()

        if self.typename == 'member':
            self.enum_value = node.attrib['value']

        self._extract_children()

    def _extract_kind(self):
        if self.typename in GirCursor.kindmap:
            return GirCursor.kindmap[self.typename]
        else:
            return cindex.CursorKind.UNEXPOSED_DECL

    def _extract_type(self):
        if self.typename == 'type':
            return GirType(self.node)

        t = self.node.find(nsgtk('type'))

        if not t is None:
            retval = GirType(t)

            if 'direction' in self.node.attrib:
                retval.is_out = self.node.attrib['direction'] == 'out'

            if 'transfer-ownership' in self.node.attrib and not retval.is_out:
                retval.transfer_ownership = self.node.attrib['transfer-ownership']

            if 'allow-none' in self.node.attrib:
                retval.allow_none = self.node.attrib['allow-none'] == '1'

            return retval

        va = self.node.find(nsgtk('varargs'))

        if not va is None:
            return GirType(va)

        ar = self.node.find(nsgtk('array'))

        if not ar is None:
            return GirType(ar)

        ret = GirType(self.node)
        ret.declaration = self

        return ret

    def _is_object_type(self):
        return self.typename in ['class', 'interface'] or \
               (self.typename == 'record' and nsglib('get-type') in self.node.attrib)

    def _create_virtual_param(self):
        # Make virtual first parameter representing pointer to object
        param = ElementTree.Element(nsgtk('parameter'))

        param.attrib['name'] = 'self'
        param.attrib['transfer-ownership'] = 'none'

        ntp = nsc('type')

        tp = ElementTree.Element(nsgtk('type'))
        tp.attrib['name'] = self.node.attrib['name']
        tp.attrib[ntp] = self.node.attrib[ntp] + '*'

        doc = ElementTree.Element(nsgtk('doc'))
        doc.text = 'a <{0}>.'.format(self.node.attrib[ntp])

        param.append(doc)
        param.append(tp)

        self._virtual_param = param

    def _setup_first_param(self, method):
        method.children.insert(0, GirCursor(self._virtual_param))

    def _make_gerror_param(self):
        if not GirCursor.global_gerror_param is None:
            return GirCursor.global_gerror_param

        param = ElementTree.Element(nsgtk('parameter'))

        param.attrib['name'] = 'error'
        param.attrib['transfer-ownership'] = 'none'
        param.attrib['allow-none'] = '1'

        tp = ElementTree.Element(nsgtk('type'))

        tp.attrib['name'] = 'Error'
        tp.attrib[nsc('type')] = 'GError **'

        doc = ElementTree.Element(nsgtk('doc'))
        doc.text = 'a #GError.'

        param.append(doc)
        param.append(tp)

        GirCursor.global_gerror_param = param
        return param

    def _extract_children(self):
        children = []

        if self.typename in ['function', 'method', 'virtual-method', 'constructor']:
            children = list(self.node.iterfind(nsgtk('parameters') + '/' + nsgtk('parameter')))

            if 'throws' in self.node.attrib and self.node.attrib['throws'] == '1':
                children.append(self._make_gerror_param())

        elif self.typename in ['enumeration', 'bitfield']:
            children = self.node.iterfind(nsgtk('member'))
        elif self.typename in ['record', 'class', 'interface']:
            self.bases = []
            self.implements = []

            def childgen():
                childtypes = ['function', 'method', 'constructor', 'virtual-method', 'property', 'field']

                for child in self.node:
                    if stripns(child.tag) in childtypes:
                        yield child

            children = childgen()

        for child in children:
            cursor = GirCursor(child)

            if not self._virtual_param is None and \
               cursor.typename == 'method' or cursor.typename == 'virtual-method':
                self._setup_first_param(cursor)

            cursor.parent = self
            self.children.append(cursor)

    @property
    def displayname(self):
        return self.name

    @property
    def semantic_parent(self):
        return self.parent

    @property
    def spelling(self):
        if self.typename in ['function', 'method', 'member', 'constructor']:
            n = nsc('identifier')
        elif self.typename in ['parameter', 'field', 'property']:
            n = 'name'
        else:
            n = nsc('type')

        if n in self.node.attrib:
            return self.node.attrib[n]
        else:
            return ''

    def is_static_method(self):
        return False

    def is_virtual_method(self):
        return self.typename == 'virtual-method'

    def is_definition(self):
        return True

    @property
    def name(self):
        return self.spelling

    @property
    def refname(self):
        if nsglib('type-name') in self.node.attrib and 'name' in self.node.attrib:
            return self.node.attrib['name']
        else:
            return None

    def get_children(self):
        return self.children

    def _add_base(self, b):
        if not b is None:
            self.bases.append(b)

    def _add_implements(self, i):
        if not i is None:
            self.implements.append(i)

    def get_usr(self):
        return self.spelling

    def resolve_refs(self, resolver):
        # Resolve things like types and stuff
        if not self.type is None:
            self.type.resolve_refs(resolver)

        for child in self.children:
            child.resolve_refs(resolver)

        # What about, like, baseclasses...
        if self.typename in ['class', 'interface']:
            if 'parent' in self.node.attrib:
                self._add_base(resolver(self.node.attrib['parent']))

            for implements in self.node.iterfind(nsgtk('implements')):
                self._add_implements(resolver(implements.attrib['name']))

class GirTree(documentmerger.DocumentMerger):
    def __init__(self, category=None):
        self.mapping = {
            'function': self.parse_function,
            'class': self.parse_class,
            'record': self.parse_record,
            'interface': self.parse_interface,
            'enumeration': self.parse_enumeration,
            'callback': self.parse_callback,
            'bitfield': self.parse_enumeration,
            'virtual-method': self.parse_virtual_method,
            'method': self.parse_method,
            'constructor': self.parse_constructor,
            'property': self.parse_property,
            'signal': self.parse_signal,
            'field': self.parse_field,
            'doc': None,
            'implements': None,
            'prerequisite': None,
        }

        self.category_to_node = defdict.Defdict()

        self.root = nodes.Root()
        self.namespaces = {}
        self.processed = {}
        self.map_id_to_cusor = {}
        self.cursor_to_node = {}
        self.exported_namespaces = []
        self.usr_to_node = defdict.Defdict()
        self.qid_to_node = defdict.Defdict()
        self.all_nodes = []

        self.usr_to_node[None] = self.root
        self.qid_to_node[None] = self.root

        if not category is None:
            self.category = self.add_categories([category])
        else:
            self.category = None

        if not self.category is None:
            self.root_node = self.category
        else:
            self.root_node = self.root

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

    def cross_ref(self, node=None):
        if node is None:
            node = self.root

        if node.comment:
            node.comment.resolve_refs(self.find_ref, node)

        for child in node.children:
            self.cross_ref(child)

    def parse_function(self, cursor):
        return nodes.Function(cursor, GirComment(cursor))

    def parse_struct_children(self, ret):
        for child in ret.cursor.children:
            c = self.parse_cursor(child)

            if not c is None:
                ret.append(c)

    def parse_class(self, cursor):
        ret = Class(cursor, GirComment(cursor))

        ret.typedef = nodes.Typedef(cursor, None)
        self.parse_struct_children(ret)

        return ret

    def parse_signal(self, node):
        # TODO
        return None

    def parse_field(self, cursor):
        if 'private' in cursor.node.attrib and cursor.node.attrib['private'] == '1':
            return None

        return nodes.Field(cursor, GirComment(cursor))

    def parse_constructor(self, cursor):
        return nodes.Function(cursor, GirComment(cursor))

    def parse_virtual_method(self, node):
        # TODO
        return None

    def parse_method(self, cursor):
        return nodes.Function(cursor, GirComment(cursor))

    def parse_property(self, cursor):
        return Property(cursor, GirComment(cursor))

    def parse_boxed(self, cursor):
        ret = Boxed(cursor, GirComment(cursor))
        ret.typedef = nodes.Typedef(cursor, None)

        self.parse_struct_children(ret)
        return ret

    def parse_record(self, cursor):
        if nsglib('is-gtype-struct-for') in cursor.node.attrib:
            return None

        if 'disguised' in cursor.node.attrib and cursor.node.attrib['disguised'] == '1':
            return None

        if nsglib('get-type') in cursor.node.attrib:
            return self.parse_boxed(cursor)

        ret = nodes.Struct(cursor, GirComment(cursor))
        ret.typedef = nodes.Typedef(cursor, None)

        self.parse_struct_children(ret)

        return ret

    def parse_interface(self, cursor):
        ret = Interface(cursor, GirComment(cursor))
        self.parse_struct_children(ret)

        return ret

    def parse_enumeration(self, cursor):
        ret = nodes.Enum(cursor, GirComment(cursor))

        # All enums are typedefs
        ret.typedef = nodes.Typedef(cursor, None)

        for member in cursor.children:
            ret.append(nodes.EnumValue(member, GirComment(member)))

        return ret

    def parse_callback(self, cursor):
        pass

    def parse_cursor(self, cursor):
        fn = self.mapping[cursor.typename]

        if not fn is None:
            ret = fn(cursor)

            if not ret is None:
                self.cursor_to_node[cursor] = ret
                self.all_nodes.append(ret)

                return ret
        else:
            return None

    def lookup_gir(self, ns, version):
        dirs = os.getenv('XDG_DATA_DIRS')

        if dirs is None:
            dirs = ['/usr/local/share', '/usr/share']
        else:
            dirs = dirs.split(os.pathsep)

        for d in dirs:
            fname = os.path.join(d, 'gir-1.0', "{0}-{1}.gir".format(ns, version))

            if os.path.exists(fname):
                return fname

        return None

    def gir_split(self, filename):
        name, _ = os.path.splitext(os.path.basename(filename))
        return name.split('-', 2)

    def add_gir(self, filename, included=False):
        ns, version = self.gir_split(filename)

        if (ns, version) in self.processed:
            return

        tree = ElementTree.parse(filename)
        repository = tree.getroot()

        self.processed[(ns, version)] = tree

        # First process includes
        for include in repository.iterfind(nsgtk('include')):
            incname = include.attrib['name']
            incversion = include.attrib['version']

            filename = self.lookup_gir(incname, incversion)

            if filename is None:
                sys.stderr.write('Could not find include `{0}-{1}\'\n'.format(incname, incversion))
                sys.exit(1)

            self.add_gir(filename, True)

        # Then process cursors
        ns = repository.find(nsgtk('namespace'))
        nsname = ns.attrib['name']

        cursors = []

        for child in ns:
            cursor = GirCursor(child)
            refname = cursor.refname

            if not refname is None:
                self.map_id_to_cusor[nsname + '.' + refname] = cursor

            cursors.append(cursor)

        self.namespaces[nsname] = cursors

        if not included:
            self.exported_namespaces.append(nsname)

    def resolve_ref(self, ns):
        def resolver(item):
            item = item.rstrip('*')

            if item in GirType.builtins:
                return None

            if not '.' in item:
                item = ns + '.' + item

            if item in self.map_id_to_cusor:
                return self.map_id_to_cusor[item]
            else:
                return None

        return resolver

    def parse(self):
        # Resolve cursor references
        for ns in self.namespaces:
            for cursor in self.namespaces[ns]:
                cursor.resolve_refs(self.resolve_ref(ns))

        classes = {}

        for ns in self.exported_namespaces:
            for cursor in self.namespaces[ns]:
                node = self.parse_cursor(cursor)

                if not node is None:
                    self.root_node.append(node)

                    if isinstance(node, Class) or isinstance(node, Interface):
                        classes[node.qid] = node

        for qid in classes:
            classes[qid].resolve_bases(classes)

        for node in self.all_nodes:
            self.qid_to_node[node.qid] = node

def run(args):
    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s gir --output DIR [OPTIONS] GIRFILE')

    parser.add_argument('--quiet', default=False, action='store_const', const=True,
                        help='be quiet about it')

    parser.add_argument('--report', default=False,
                          action='store_const', const=True, help='report documentation coverage and errors')

    parser.add_argument('--output', default=None, metavar='DIR',
                          help='specify the output directory')

    parser.add_argument('--type', default='html', metavar='TYPE',
                          help='specify the type of output (html or xml, default html)')

    parser.add_argument('--merge', default=[], metavar='FILES', action='append',
                          help='specify additional description files to merge into the documentation')

    parser.add_argument('--merge-filter', default=None, metavar='FILTER',
                          help='specify program to pass merged description files through')

    parser.add_argument('--static', default=False, action='store_const', const=True,
                          help='generate a static website (only for when --output is html)')

    parser.add_argument('--category', default=None, metavar='CATEGORY',
                          help='category in which to place all symbols')

    parser.add_argument('--custom-js', default=[], metavar='FILES', action='append',
                          help='specify additional javascript files to be merged into the html (only for when --output is html)')

    parser.add_argument('--custom-css', default=[], metavar='FILES', action='append',
                          help='specify additional css files to be merged into the html (only for when --output is html)')

    parser.add_argument('files', nargs='+', help='gir files to parse')

    opts = parser.parse_args(args)

    t = GirTree(opts.category)

    # Generate artificial tree
    for f in opts.files:
        t.add_gir(f)

    t.parse()

    if opts.merge:
        t.merge(opts.merge_filter, opts.merge)

    t.cross_ref()

    from .cmdgenerate import run_generate

    run_generate(t, opts)

# vi:ts=4:et

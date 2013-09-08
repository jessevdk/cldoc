# -*- coding: utf-8 -*-
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

from clang import cindex
import os, sys

def inspect_print_row(a, b, link=None):
    from xml.sax.saxutils import escape

    b = escape(str(b))

    if link:
        b = "<a href='#" + escape(link) + "'>" + b + "</a>"

    print "<tr><td>%s</td><td>%s</td></tr>" % (escape(str(a)), b)

def inspect_print_subtype(name, tp, subtype, indent=1):
    if not subtype or tp == subtype or subtype.kind == cindex.TypeKind.INVALID:
        return

    inspect_print_row('  ' * indent + '→ .' + name + '.kind', subtype.kind)
    inspect_print_row('  ' * indent + '→ .' + name + '.spelling', subtype.kind.spelling)
    inspect_print_row('  ' * indent + '→ .' + name + '.is_const_qualified', subtype.is_const_qualified())

    if subtype.kind == cindex.TypeKind.CONSTANTARRAY:
        etype = subtype.get_array_element_type()
        num = subtype.get_array_size()

        inspect_print_subtype('array_type', subtype, etype, indent + 1)
        inspect_print_row('  ' * (indent + 1) + '→ .size', str(num))

    decl = subtype.get_declaration()

    if decl:
        inspect_print_row('  ' * indent + '→ .' + name + '.declaration', decl.displayname, decl.get_usr())

    inspect_print_subtype('get_canonical', subtype, subtype.get_canonical(), indent + 1)
    inspect_print_subtype('get_pointee', subtype, subtype.get_pointee(), indent + 1)
    inspect_print_subtype('get_result', subtype, subtype.get_result(), indent + 1)

def inspect_cursor(tree, cursor, indent):
    from xml.sax.saxutils import escape

    if not cursor.location.file:
        return

    if not str(cursor.location.file) in tree.files:
        return

    print "<table id='" + escape(cursor.get_usr()) + "' class='cursor' style='margin-left: " + str(indent * 20) + "px;'>"

    inspect_print_row('kind', cursor.kind)
    inspect_print_row('  → .is_declaration', cursor.kind.is_declaration())
    inspect_print_row('  → .is_reference', cursor.kind.is_reference())
    inspect_print_row('  → .is_expression', cursor.kind.is_expression())
    inspect_print_row('  → .is_statement', cursor.kind.is_statement())
    inspect_print_row('  → .is_attribute', cursor.kind.is_attribute())
    inspect_print_row('  → .is_invalid', cursor.kind.is_invalid())
    inspect_print_row('  → .is_preprocessing', cursor.kind.is_preprocessing())

    inspect_print_subtype('type', None, cursor.type, 0)

    inspect_print_row('usr', cursor.get_usr())
    inspect_print_row('spelling', cursor.spelling)
    inspect_print_row('displayname', cursor.displayname)
    inspect_print_row('location', "%s (%d:%d - %d:%d)" % (os.path.basename(str(cursor.location.file)), cursor.extent.start.line, cursor.extent.start.column, cursor.extent.end.line, cursor.extent.end.column))
    inspect_print_row('is_definition', cursor.is_definition())
    inspect_print_row('is_virtual_method', cursor.is_virtual_method())
    inspect_print_row('is_static_method', cursor.is_static_method())

    spec = cursor.access_specifier

    if not spec is None:
        inspect_print_row('access_specifier', spec)

    defi = cursor.get_definition()

    if defi and defi != cursor:
        inspect_print_row('definition', defi.displayname, link=defi.get_usr())

    if cursor.kind == cindex.CursorKind.CXX_METHOD:
        for t in cursor.type.argument_types():
            inspect_print_subtype('argument', None, t)

    print "</table>"

def inspect_cursors(tree, cursors, indent=0):
    for cursor in cursors:
        inspect_cursor(tree, cursor, indent)

        if (not cursor.location.file) or str(cursor.location.file) in tree.files:
            inspect_cursors(tree, cursor.get_children(), indent + 1)

def inspect_tokens(tree, filename, tu):
    it = tu.get_tokens(extent=tu.get_extent(filename, (0, os.stat(filename).st_size)))

    print "<table class='tokens'>"

    for token in it:
        print "<tr>"
        print "<td>%s</td>" % (token.kind,)
        print "<td>" + token.spelling + "</td>"
        print "<td>%s</td>" % (token.cursor.kind,)
        print "<td>%d:%d</td>" % (token.extent.start.line, token.extent.start.column,)
        print "</tr>"

    print "</table>"

def inspect(tree):
    index = cindex.Index.create()

    print """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type='text/css'>
div.filename {
padding: 3px;
background-color: #eee;
}

table.cursor {
border-collapse: collapse;
margin-bottom: 10px;
}

a {
color: #3791db;
}

table.cursor tr td:first-child {
font-weight: bold;
padding-right: 10px;
color: #666;
vertical-align: top;
}
</style>
</head>
<body>"""

    for f in tree.files:
        tu = index.parse(f, tree.flags)

        if not tu:
            sys.stderr.write("Could not parse file %s...\n" % (f,))
            sys.exit(1)

        print "<div class='file'><div class='filename'>" + f + "</div>"

        inspect_tokens(tree, f, tu)

        # Recursively inspect cursors
        inspect_cursors(tree, tu.cursor.get_children())

        print "</div>"

    print "</body>\n</html>"

# vi:ts=4:et

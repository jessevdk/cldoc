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

from ..clang import cindex

class Type(Node):
    kindmap = {
        cindex.TypeKind.POINTER: '*',
        cindex.TypeKind.LVALUEREFERENCE: '&',
    }

    namemap = {
        cindex.TypeKind.VOID: 'void',
        cindex.TypeKind.BOOL: 'bool',
        cindex.TypeKind.CHAR_U: 'char',
        cindex.TypeKind.UCHAR: 'unsigned char',
        cindex.TypeKind.CHAR16: 'char16_t',
        cindex.TypeKind.CHAR32: 'char32_t',
        cindex.TypeKind.USHORT: 'unsigned short',
        cindex.TypeKind.UINT: 'unsigned int',
        cindex.TypeKind.ULONG: 'unsigned long',
        cindex.TypeKind.ULONGLONG: 'unsigned long long',
        cindex.TypeKind.UINT128: 'uint128_t',
        cindex.TypeKind.CHAR_S: 'char',
        cindex.TypeKind.SCHAR: 'signed char',
        cindex.TypeKind.WCHAR: 'wchar_t',
        cindex.TypeKind.SHORT: 'unsigned short',
        cindex.TypeKind.INT: 'int',
        cindex.TypeKind.LONG: 'long',
        cindex.TypeKind.LONGLONG: 'long long',
        cindex.TypeKind.INT128: 'int128_t',
        cindex.TypeKind.FLOAT: 'float',
        cindex.TypeKind.DOUBLE: 'double',
        cindex.TypeKind.LONGDOUBLE: 'long double',
        cindex.TypeKind.NULLPTR: 'float',
    }

    def __init__(self, tp, cursor=None):
        Node.__init__(self, None, None)

        self.tp = tp

        self._qualifier = []
        self._declared = None
        self._builtin = False
        self._cursor = cursor
        self._kind = tp.kind
        self._is_template = False

        self.extract(tp)

    @property
    def is_function(self):
        return self._kind == cindex.TypeKind.FUNCTIONPROTO

    @property
    def function_arguments(self):
        return self._arguments

    @property
    def function_result(self):
        return self._result

    @property
    def is_template(self):
        return self._is_template

    @property
    def template_arguments(self):
        return self._template_arguments

    @property
    def is_constant_array(self):
        return self._kind == cindex.TypeKind.CONSTANTARRAY

    @property
    def is_out(self):
        if hasattr(self.tp, 'is_out'):
            return self.tp.is_out
        else:
            return False

    @property
    def transfer_ownership(self):
        if hasattr(self.tp, 'transfer_ownership'):
            return self.tp.transfer_ownership
        else:
            return 'none'

    @property
    def allow_none(self):
        if hasattr(self.tp, 'allow_none'):
            return self.tp.allow_none
        else:
            return False

    @property
    def element_type(self):
        return self._element_type

    @property
    def constant_array_size(self):
        return self._array_size

    def _declaration_full_name(self, decl):
        cursor_template = decl.specialized_cursor_template

        if cursor_template is None or not self._is_template:
            return decl.displayname
        else:
            return cursor_template.spelling


    def _full_typename(self, decl):
        parent = decl.semantic_parent

        if decl.kind == cindex.CursorKind.NAMESPACE and decl.displayname == '__1' and parent and parent.displayname == 'std':
            # Skip over special inline namespace. Ideally we can skip over inline namespaces
            # in general, but I can't find a way to determine whether a namespace is inline
            return self._full_typename(parent)

        meid = self._declaration_full_name(decl)

        if not parent or parent.kind == cindex.CursorKind.TRANSLATION_UNIT:
            return meid

        if not meid:
            return self._full_typename(parent)

        parval = self._full_typename(parent)

        if parval:
            return parval + '::' + meid
        else:
            return meid

    def _extract_constant_array_type(self, tp):
        if tp.kind != cindex.TypeKind.CONSTANTARRAY:
            return

        self._element_type = Type(tp.get_array_element_type())
        self._array_size = tp.get_array_size()

    def _extract_template_argument_types(self, tp):
        # Ignore typedefs, we don't want to get any template arguments
        if tp.get_declaration().kind == cindex.CursorKind.TYPEDEF_DECL:
            return

        num_template_arguments = tp.get_num_template_arguments()

        if num_template_arguments <= 0:
            return

        self._is_template = True
        self._template_arguments = []

        for i in range(0, num_template_arguments):
            template_argument_type = tp.get_template_argument_type(i)
            self._template_arguments.append(Type(template_argument_type))

    def _extract_subtypes(self, tp):
        self._extract_constant_array_type(tp)
        self._extract_template_argument_types(tp)

    def extract(self, tp):

        if tp.is_const_qualified():
            self._qualifier.append('const')

        if hasattr(tp, 'is_builtin'):
            self._builtin = tp.is_builtin()

        if tp.kind in Type.kindmap:
            self.extract(tp.get_pointee())
            self._qualifier.append(Type.kindmap[tp.kind])
            return

        self._decl = tp.get_declaration()
        self._extract_subtypes(tp)

        if self._decl and self._decl.displayname:
            self._typename = self._full_typename(self._decl)
        elif tp.kind in Type.namemap:
            self._typename = Type.namemap[tp.kind]
            self._builtin = True
        elif tp.kind != cindex.TypeKind.CONSTANTARRAY and hasattr(tp, 'spelling'):
            canon = tp.get_canonical()

            if canon.kind == cindex.TypeKind.FUNCTIONPROTO:
                self._kind = canon.kind
                self._result = Type(canon.get_result())
                self._arguments = [Type(arg) for arg in canon.argument_types()]

            self._typename = tp.spelling
        elif (not self._cursor is None):
            self._typename = self._cursor.displayname
        else:
            self._typename = ''

    @property
    def builtin(self):
        return self._builtin

    @property
    def typename(self):
        if self.is_constant_array:
            return self._element_type.typename
        else:
            return self._typename

    def typename_for(self, node):
        if self.is_constant_array:
            return self._element_type.typename_for(node)

        if node is None or not '::' in self._typename:
            return self._typename

        return node.qid_from(self._typename)

    @property
    def decl(self):
        return self._decl

    @property
    def qualifier(self):
        return self._qualifier

    @property
    def qualifier_string(self):
        ret = ''

        for x in self._qualifier:
            if x != '*' or (len(ret) != 0 and ret[-1] != '*'):
                ret += ' '

            ret += x

        return ret

# vi:ts=4:et

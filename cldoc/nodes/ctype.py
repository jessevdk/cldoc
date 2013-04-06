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
from cldoc.clang import cindex
from node import Node

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

    def __init__(self, tp):
        Node.__init__(self, None, None)

        self.tp = tp

        self._qualifier = []
        self._declared = None
        self._builtin = False

        self.extract(tp)

    @property
    def is_constant_array(self):
        return self.tp.kind == cindex.TypeKind.CONSTANTARRAY

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

    def _full_typename(self, decl):
        parent = decl.semantic_parent
        meid = decl.displayname

        if not parent or parent.kind == cindex.CursorKind.TRANSLATION_UNIT:
            return meid

        if not meid:
            return self._full_typename(parent)

        parval = self._full_typename(parent)

        if parval:
            return parval + '::' + meid
        else:
            return meid

    def extract(self, tp):
        if tp.is_const_qualified():
            self._qualifier.append('const')

        if hasattr(tp, 'is_builtin'):
            self._builtin = tp.is_builtin()

        if tp.kind in Type.kindmap:
            self.extract(tp.get_pointee())
            self._qualifier.append(Type.kindmap[tp.kind])

            return
        elif tp.kind == cindex.TypeKind.CONSTANTARRAY:
            self._element_type = Type(tp.get_array_element_type())
            self._array_size = tp.get_array_size()

        self._decl = tp.get_declaration()

        if self._decl and self._decl.displayname:
            self._typename = self._full_typename(self._decl)
        elif tp.kind in Type.namemap:
            self._typename = Type.namemap[tp.kind]
            self._builtin = True
        elif tp.kind != cindex.TypeKind.CONSTANTARRAY and hasattr(tp, 'spelling'):
            self._typename = tp.spelling
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

        if not node or not '::' in self._typename:
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

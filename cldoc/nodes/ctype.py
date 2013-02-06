from cldoc.clang import cindex
from node import Node

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

class Type(Node):
    def __init__(self, tp):
        Node.__init__(self, None, None)

        self.tp = tp

        self._qualifier = []
        self._declared = None
        self._builtin = False

        self.extract(tp)

    @property
    def is_array(self):
        return self.tp.kind == cindex.TypeKind.CONSTANTARRAY

    @property
    def element_type(self):
        return self._element_type

    @property
    def array_size(self):
        return self._array_size

    def _full_typename(self, decl):
        parent = decl.semantic_parent
        meid = decl.displayname

        if not parent:
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

        if tp.kind in kindmap:
            self.extract(tp.get_pointee())
            self._qualifier.append(kindmap[tp.kind])

            return
        elif tp.kind == cindex.TypeKind.CONSTANTARRAY:
            self._element_type = Type(tp.get_array_element_type())
            self._array_size = tp.get_array_size()

        self._decl = tp.get_declaration()

        if self._decl and self._decl.displayname:
            self._typename = self._full_typename(self._decl)
        elif tp.kind in namemap:
            self._typename = namemap[tp.kind]
            self._builtin = True
        else:
            self._typename = ''

    @property
    def builtin(self):
        return self._builtin

    @property
    def typename(self):
        if self.is_array:
            return self._element_type.typename
        else:
            return self._typename

    def typename_for(self, node):
        if self.is_array:
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

# vi:ts=4:et

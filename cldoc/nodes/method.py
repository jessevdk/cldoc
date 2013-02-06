from function import Function
from cldoc.clang import cindex
from cldoc.comment import Comment

class Method(Function):
    kind = cindex.CursorKind.CXX_METHOD

    def __init__(self, cursor, comment):
        Function.__init__(self, cursor, comment)

        self.static = cursor.is_static_method()
        self.virtual = cursor.is_virtual_method()

        self.abstract = True
        self._override = None

        self.update_abstract(cursor)

    @property
    def override(self):
        if not self._override is None:
            return self._override

        # Lookup in bases, recursively
        bases = list(self.parent.bases)
        mname = self.name

        self._override = []

        while len(bases) > 0:
            b = bases[0]
            bases = bases[1:]

            if not b.node:
                continue

            b = b.node

            if mname in b.name_to_method:
                self._override.append(b.name_to_method[mname])
            else:
                # Look in the bases of bases also
                bases = bases + b.bases

        return self._override

    @property
    def comment(self):
        cm = Function.comment.fget(self)

        if not cm:
            return cm

        if cm.text.strip() == '@inherit':
            for ov in self.override:
                ovcm = ov.comment

                if ovcm:
                    self.merge_comment(Comment(ovcm.text, ovcm.location), True)
                    return self._comment

        return cm

    def update_abstract(self, cursor):
        if cursor.is_definition() or cursor.get_definition():
            self.abstract = False

    def add_ref(self, cursor):
        super(Method, self).add_ref(cursor)
        self.update_abstract(cursor)

# vi:ts=4:et

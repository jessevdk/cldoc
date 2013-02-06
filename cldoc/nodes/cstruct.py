import importlib
from cldoc.clang import cindex

cls = importlib.import_module('.class', 'cldoc.nodes')

class Struct(cls.Class):
    kind = cindex.CursorKind.STRUCT_DECL

    def __init__(self, cursor, comment):
        cls.Class.__init__(self, cursor, comment)

        self.typedef = None
        self.current_access = cindex.CXXAccessSpecifier.PUBLIC

    @property
    def comment(self):
        ret = cls.Class.comment.fget(self)

        if not ret and self.typedef:
            ret = self.typedef.comment

        return ret

    @property
    def name(self):
        if not self.typedef is None:
            # The name is really the one of the typedef
            return self.typedef.name
        else:
            return cls.Class.name.fget(self)

# vi:ts=4:et

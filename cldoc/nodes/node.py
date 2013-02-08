from cldoc.clang import cindex
from cldoc.comment import Comment
from cldoc.comment import Parser
import re

class Node(object):
    class SortId:
        CATEGORY = 0
        NAMESPACE = 1
        CLASS = 2
        ENUM = 3
        ENUMVALUE = 4
        FIELD = 5
        TYPEDEF = 6
        CONSTRUCTOR = 7
        DESTRUCTOR = 8
        METHOD = 9
        FUNCTION = 10

    def __init__(self, cursor, comment):
        self.cursor = cursor
        self._comment = comment
        self.children = []
        self.parent = None
        self.access = cindex.CXXAccessSpecifier.PUBLIC
        self._comment_locations = []
        self._refs = []

        self.sortid = 0
        cls = self.__class__

        while cls.__name__ != 'object':
            nm = cls.__name__.upper()

            if hasattr(Node.SortId, nm):
                self.sortid = getattr(Node.SortId, nm)
                break
            else:
                cls = cls.__base__

        self.process_children = False

        if self._comment:
            self.parse_comment()

    def qid_from_to(self, nq, mq):
        # Find the minimal required typename from the perspective of <node>
        # to reach our type
        lnq = nq.split('::')
        lmq = mq.split('::')

        if nq == mq:
            return lmq[-1]

        for i in range(min(len(lnq), len(lmq))):
            if lnq[i] != lmq[i]:
                return "::".join(lmq[i:])

        return "::".join(lmq[len(lnq):])

    def qid_from(self, qid):
        return self.qid_from_to(self.qid, qid)

    def qid_to(self, qid):
        return self.qid_from_to(qid, self.qid)

    def add_ref(self, cursor):
        self._refs.append(cursor)
        self.add_comment_location(cursor.extent.start)

    def add_comment_location(self, location):
        self._comment_locations.append(location)

    @property
    def comment_locations(self):
        if self.cursor:
            yield self.cursor.extent.start

        for loc in self._comment_locations:
            yield loc

    def parse_comment(self):
        # Just extract brief and doc
        m = Parser.parse(self._comment.text)

        if len(m.brief) > 0:
            self._comment.brief = m.brief
            self._comment.doc = m.body

    def compare_sort(self, other):
        ret = cmp(self.access, other.access)

        if ret == 0:
            ret = cmp(self.sortid, other.sortid)

        if ret == 0 and self.name and other.name:
            ret = cmp(self.name.lower(), other.name.lower())

        return ret

    @property
    def resolve_nodes(self):
        from enum import Enum

        for child in self.children:
            yield child

            if isinstance(child, Enum):
                for ev in child.children:
                    yield ev

    @property
    def name(self):
        if self.cursor is None:
            return ''
        else:
            return self.cursor.spelling

    def descendants(self):
        for child in self.children:
            yield child

            for d in child.descendants():
                yield d

    def sorted_children(self):
        ret = list(self.children)
        ret.sort(lambda x, y: x.compare_sort(y))

        return ret

    @property
    def qid(self):
        from root import Root

        meid = self.name

        if self.parent and not isinstance(self.parent, Root):
            q = self.parent.qid
            return q + '::' + meid
        else:
            return meid

    @property
    def comment(self):
        return self._comment

    @property
    def props(self):
        ret = {
            'id': self.qid,
            'name': self.name,
        }

        if self.access == cindex.CXXAccessSpecifier.PROTECTED:
            ret['access'] = 'protected'
        elif self.access == cindex.CXXAccessSpecifier.PRIVATE:
            ret['access'] = 'private'

        return ret

    @property
    def classname(self):
        return self.__class__.__name__.lower()

    def append(self, child):
        self.children.append(child)
        child.parent = self

    def visit(self, cursor, citer):
        return None

    def merge_comment(self, comment, override=False):
        if not comment:
            return

        if not override and self._comment:
            return

        self._comment = comment
        self.parse_comment()

    @staticmethod
    def _subclasses(cls):
        for c in cls.__subclasses__():
            yield c

            for cc in Node._subclasses(c):
                yield cc

    @staticmethod
    def subclasses():
        return Node._subclasses(Node)

# vi:ts=4:et

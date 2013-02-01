from clang import cindex
from defdict import Defdict

import os, re, sys

class Comment(object):
    redocref = re.compile('<(operator>>|[^>]+)>')

    class String(object):
        def __init__(self, s):
            self.components = [s]

        def __str__(self):
           return "".join(self.components)

        def __nonzero__(self):
            l = len(self.components)

            return l > 0 and (l > 1 or len(self.components[0]) > 0)

    rebrief = '(?P<brief>[^.]*(\.|$))'
    redoc = '(?P<doc>.*?)'
    reparam = '(?:@(?P<paramname>[^\s]+)\s+(?P<paramdoc>[^\n]*))\n'
    reparams = '(?P<params>(?:' + reparam + ')*)'
    rereturn = '(@return\s(?P<return>[^.]*.))?'

    def __init__(self, text):
        self.__dict__['docstrings'] = []
        self.__dict__['text'] = text

        self.doc = text
        self.brief = ''

    def __setattr__(self, name, val):
        if not name in self.docstrings:
            self.docstrings.append(name)

        if isinstance(val, dict):
            for key in val:
                if not isinstance(val[key], Comment.String):
                    val[key] = Comment.String(str(val[key]))
        elif not isinstance(val, Comment.String):
            val = Comment.String(str(val))

        self.__dict__[name] = val

    def resolve_refs_for_doc(self, doc, resolver):
        components = re.split(Comment.redocref, str(doc))

        for i in range(1, len(components), 2):
            resolved = resolver(components[i])

            if not resolved is None:
                components[i] = resolved

        doc.components = components

    def resolve_refs(self, resolver):
        for name in self.docstrings:
            doc = getattr(self, name)

            if not doc:
                continue

            if isinstance(doc, dict):
                for key in doc:
                    if not isinstance(doc[key], Comment.String):
                        doc[key] = Comment.String(str(doc[key]))
                    self.resolve_refs_for_doc(doc[key], resolver)
            else:
                self.resolve_refs_for_doc(doc, resolver)

cldoc_instrre = re.compile('^cldoc:([a-zA-Z_-]+)(\(([^\)]*)\))?')

def parse_cldoc_instruction(s):
    m = cldoc_instrre.match(s)

    if not m:
        return None

    func = m.group(1)
    args = m.group(3)

    if args:
        args = [x.strip() for x in args.split(",")]
    else:
        args = []

    return [func, args]

def extract(filename, tu):
    """
    extract extracts comments from a translation unit for a given file by
    iterating over all the tokens in the TU, locating the COMMENT tokens and
    finding out to which cursors the comments semantically belong.
    """
    it = tu.get_tokens(extent=tu.get_extent(filename, (0, os.stat(filename).st_size)))

    itptr = 0
    tokens = list(it)

    prev = None
    ret = Defdict()

    categoriestack = []
    categories = []
    categoriesmap = {}

    while itptr < len(tokens):
        token = tokens[itptr]
        itptr += 1

        comments = []
        firsttok = None

        if len(categoriestack) > 0:
            categoriesmap[token.cursor] = categoriestack[-1]

        # Concatenate individual comments
        while (not token is None) and token.kind == cindex.TokenKind.COMMENT:
            if firsttok is None:
                firsttok = token

            comments.append(clean(token))

            if itptr < len(tokens):
                token = tokens[itptr]

                if len(categoriestack) > 0:
                    categoriesmap[token.cursor] = categoriestack[-1]
            else:
                token = None

            itptr += 1

        instr = parse_cldoc_instruction(" ".join(comments).strip())

        if instr:
            if instr[0] == 'begin-category' and len(instr[1]) == 1:
                category = instr[1][0]
                categoriestack.append(category)

                if not category in categories:
                    categories.append(category)

            elif instr[0] == 'end-category':
                if len(categoriestack) == 0:
                    sys.stderr.write('Failed to end cldoc category: no category to end\n')
                    sys.exit(1)

                if len(instr[1]) == 1 and categoriestack[-1] != instr[1][0]:
                    sys.stderr.write('Failed to end cldoc category: current category is `{0}\', not `{1}\'\n'.format(categoriestack[-1], instr[1][0]))
                    sys.exit(1)

                categoriestack.pop()

            continue

        if not firsttok is None:
            # Check if first comment token was on the same line as the
            # previous token
            if prev and prev.extent.end.line == firsttok.extent.start.line:
                ret[prev.cursor] = Comment("\n".join(comments))
            elif token:
                token = skip_nontoks(token, tokens, itptr)

                if token:
                    ret[token.cursor] = Comment("\n".join(comments))

        if token and token.cursor.kind != cindex.CursorKind.INVALID_FILE:
            prev = token

    return ret, categories, categoriesmap

def skip_nontoks(token, tokens, itptr):
    if not token:
        return None

    start = token.extent.start

    skips = [cindex.CursorKind.INVALID_FILE,
             cindex.CursorKind.NAMESPACE_REF,
             cindex.CursorKind.TYPE_REF]

    while True:
        if (not token.cursor.kind in skips) and token.cursor.extent.start == start:
            return token

        if itptr >= len(tokens):
            return None

        token = tokens[itptr]
        itptr += 1

def clean(token):
    prelen = token.extent.start.column - 1
    comment = token.spelling.strip()

    if comment.startswith('//'):
        return comment[2:].strip()
    elif comment.startswith('/*') and comment.endswith('*/'):
        lines = comment[2:-2].splitlines()
        retl = []

        for line in lines:
            if prelen == 0 or line[0:prelen].isspace():
                line = line[prelen:].rstrip()

                if line.startswith(' *') or line.startswith('  '):
                    line = line[3:]

                    if len(line) > 0 and line[0] == ' ':
                        line = line[1:]

            retl.append(line)

        return "\n".join(retl)
    else:
        return comment

# vi:ts=4:et

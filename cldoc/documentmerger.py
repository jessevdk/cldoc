import os, subprocess

import comment
import nodes
import sys, re

from . import fs

class DocumentMerger:
    reinclude = re.compile('#<cldoc:include[(]([^)]*)[)]>')

    def merge(self, mfilter, files):
        for f in files:
            if os.path.basename(f).startswith('.'):
                continue

            if os.path.isdir(f):
                self.merge(mfilter, [os.path.join(f, x) for x in os.listdir(f)])
            elif f.endswith('.md'):
                self._merge_file(mfilter, f)

    def _split_categories(self, filename, contents):
        lines = contents.splitlines()

        ret = {}

        category = None
        doc = []
        first = False
        ordered = []

        for line in lines:
            prefix = '#<cldoc:'

            line = line.rstrip('\n')

            if first:
                first = False

                if line == '':
                    continue

            if line.startswith(prefix) and line.endswith('>'):
                if len(doc) > 0 and not category:
                    sys.stderr.write('Failed to merge file `{0}\': no #<cldoc:id> specified\n'.format(filename))
                    sys.exit(1)

                if category:
                    if not category in ret:
                        ordered.append(category)

                    ret[category] = "\n".join(doc)

                doc = []
                category = line[len(prefix):-1]
                first = True
            else:
                doc.append(line)

        if category:
            if not category in ret:
                ordered.append(category)

            ret[category] = "\n".join(doc)
        elif len(doc) > 0:
            sys.stderr.write('Failed to merge file `{0}\': no #<cldoc:id> specified\n'.format(filename))
            sys.exit(1)

        return [[c, ret[c]] for c in ordered]

    def _normalized_qid(self, qid):
        if qid == 'index':
            return None

        if qid.startswith('::'):
            return qid[2:]

        return qid

    def _do_include(self, mfilter, filename, relpath):
        if not os.path.isabs(relpath):
            relpath = os.path.join(os.path.dirname(filename), relpath)

        return self._read_merge_file(mfilter, relpath)

    def _process_includes(self, mfilter, filename, contents):
        def repl(m):
            return self._do_include(mfilter, filename, m.group(1))

        return DocumentMerger.reinclude.sub(repl, contents)

    def _read_merge_file(self, mfilter, filename):
        if not mfilter is None:
            contents = unicode(subprocess.check_output([mfilter, filename]), 'utf-8')
        else:
            contents = unicode(fs.fs.open(filename).read(), 'utf-8')

        return self._process_includes(mfilter, filename, contents)

    def _merge_file(self, mfilter, filename):
        contents = self._read_merge_file(mfilter, filename)
        categories = self._split_categories(filename, contents)

        for (category, docstr) in categories:
            parts = category.split('/')

            qid = self._normalized_qid(parts[0])
            key = 'doc'

            if len(parts) > 1:
                key = parts[1]

            if not self.qid_to_node[qid]:
                self.add_categories([qid])
                node = self.category_to_node[qid]
            else:
                node = self.qid_to_node[qid]

            if key == 'doc':
                node.merge_comment(comment.Comment(docstr, None), override=True)
            else:
                sys.stderr.write('Unknown type `{0}\' for id `{1}\'\n'.format(key, parts[0]))
                sys.exit(1)

    def add_categories(self, categories):
        root = None

        for category in categories:
            parts = category.split('::')

            root = self.root
            fullname = ''

            for i in range(len(parts)):
                part = parts[i]
                found = False

                if i != 0:
                    fullname += '::'

                fullname += part

                for child in root.children:
                    if isinstance(child, nodes.Category) and child.name == part:
                        root = child
                        found = True
                        break

                if not found:
                    s = nodes.Category(part)

                    root.append(s)
                    root = s

                    self.category_to_node[fullname] = s
                    self.qid_to_node[s.qid] = s
                    self.all_nodes.append(s)

        return root

# vi:ts=4:et

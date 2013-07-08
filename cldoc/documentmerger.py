import os, subprocess

import comment
import nodes

class DocumentMerger:
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
                    ret[category] = "\n".join(doc)

                doc = []
                category = line[len(prefix):-1]
                first = True
            else:
                doc.append(line)

        if category:
            ret[category] = "\n".join(doc)
        elif len(doc) > 0:
            sys.stderr.write('Failed to merge file `{0}\': no #<cldoc:id> specified\n'.format(filename))
            sys.exit(1)

        return ret

    def _normalized_qid(self, qid):
        if qid == 'index':
            return None

        if qid.startswith('::'):
            return qid[2:]

        return qid

    def _read_merge_file(self, mfilter, filename):
        if not mfilter is None:
            contents = unicode(subprocess.check_output([mfilter, filename]), 'utf-8')
        else:
            contents = unicode(open(filename).read(), 'utf-8')

        return contents

    def _merge_file(self, mfilter, filename):
        contents = self._read_merge_file(mfilter, filename)
        categories = self._split_categories(filename, contents)

        for category in categories:
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
                node.merge_comment(comment.Comment(categories[category], None), override=True)
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

class Generator(object):
    def __init__(self, tree=None, opts=None):
        self.tree = tree
        self.options = opts

    def generate(self, outdir):
        self.outdir = outdir

        for node in self.tree.root.sorted_children():
            self.generate_node(node)

    def generate_node(self, node, passfunc=None):
        for child in node.sorted_children():
            if passfunc is None or passfunc(child):
                self.generate_node(child)

# vi:ts=4:et

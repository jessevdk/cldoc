from node import Node

class Root(Node):
    def __init__(self):
        Node.__init__(self, None, None)

    @property
    def is_anonymous(self):
        return True

# vi:ts=4:et

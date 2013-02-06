from node import Node

class Category(Node):
    def __init__(self, name):
        Node.__init__(self, None, None)

        self._name = name

    @property
    def name(self):
        return self._name

# vi:ts=4:et

from cldoc.struct import Struct

class Example(list):
    Item = Struct.define('Item', text='', classes=None)

    def append(self, text, classes=None):
        if isinstance(classes, basestring):
            classes = [classes]

        list.append(self, Example.Item(text=text, classes=classes))

# vi:ts=4:et

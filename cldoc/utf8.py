try:
    unicode # Just to see if it exists
    basecls = unicode

    def makeutf8(s):
        if not isinstance(s, unicode):
            if hasattr(s, '__unicode__'):
                return unicode(s)

            return str(s).decode('utf-8')

        return s
except:
    basecls = str

    def makeutf8(s):
        if not isinstance(s, str):
            if hasattr(s, '__str__'):
                return str(s)
            elif hasattr(s, '__bytes__'):
                return s.__bytes__().decode('utf-8')

        return s

string = basecls

class utf8(string):
    def __init__(self, s):
        super(utf8, self).__init__(makeutf8(s))

    def __str__(self):
        if not isinstance(self, str):
            return self.encode('utf-8')
        else:
            return self

    def __bytes__(self):
        return self.encode('utf-8')

    def __unicode__(self):
        return self

    def __add__(self, other):
        return utf8(super(utf8, self).__add__(makeutf8(other)))

# vi:ts=4:et

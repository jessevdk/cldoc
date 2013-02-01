class Defdict(dict):
    def __missing__(self, key):
        return None

# vi:ts=4:et

import copy

class Struct(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @staticmethod
    def define(_name, **kwargs):
        defaults = kwargs

        class subclass(Struct):
            def __init__(self, **kwargs):
                defs = copy.deepcopy(defaults)

                for key in kwargs:
                    if not key in defs:
                        raise AttributeError("'{0}' has no attribute '{1}'".format(_name, key))
                    else:
                        defs[key] = kwargs[key]

                super(subclass, self).__init__(**defs)

        subclass.__name__ = _name
        return subclass

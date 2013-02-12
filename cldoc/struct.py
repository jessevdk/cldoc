# This file is part of cldoc.  cldoc is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
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

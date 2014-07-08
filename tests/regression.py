#!/usr/bin/env python

import sys, os

lcldoc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, lcldoc)

import unittest
from cldoc import cmdgenerate

from cldoc import fs
import glob, os

from lxml import objectify
from lxml import etree

fs.fs = fs.Virtual

class Regression(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

def create_test(name, files, ofiles):
    def t(self):
        cmdgenerate.run(['--', '--quiet', '--type', 'xml', '--output', 'xml'] + files)

        for f in ofiles:
            b = os.path.basename(f)
            xmlname = b[len(name)+1:]

            gf = fs.fs.open(os.path.join('xml', 'xml', xmlname))

            got = objectify.parse(gf)
            got = etree.tostring(got, pretty_print=True)

            exp = objectify.parse(open(f))
            exp = etree.tostring(exp, pretty_print=True)

            self.maxDiff = None
            self.assertMultiLineEqual(got, exp)

        fs.fs.clear()

    return t

def generate_tests():
    dname = os.path.join(os.path.dirname(__file__))
    hfiles = glob.glob(os.path.join(dname, 'input', '*.hh')) + glob.glob(os.path.join(dname, 'input', '*.h'))

    for hfile in hfiles:
        (hname, hext) = os.path.splitext(os.path.basename(hfile))

        files = [hfile]

        ccfile = os.path.join(os.path.dirname(hfile), hname + '.cc')
        cfile = os.path.join(os.path.dirname(hfile), hname + '.c')

        if os.path.exists(ccfile):
            files.append(ccfile)

        if os.path.exists(cfile):
            files.append(cfile)

        ofiles = glob.glob(os.path.join(dname, 'output', hname + '-*'))

        t = create_test(hname, files, ofiles)
        t.__name__ = 'test_' + hname

        setattr(Regression, 'test_' + hname, t)

generate_tests()

if __name__ == '__main__':
    unittest.main()

# vi:ts=4:et

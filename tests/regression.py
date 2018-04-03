#!/usr/bin/env python

import sys, os

lcldoc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, lcldoc)

import unittest
from cldoc import cmdgenerate

from cldoc import fs
import glob, os

from xml import etree

class Regression(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

def create_test(name, files, ofiles):
    def t(self):
        fs.fs = fs.Virtual

        cmdgenerate.run(['--', '--quiet', '--type', 'xml', '--output', 'xml'] + files)

        for f in ofiles:
            b = os.path.basename(f)
            xmlname = b[len(name)+1:]

            gf = fs.fs.open(os.path.join('xml', 'xml', xmlname))

            got = gf.read()
            exp = open(f).read()

            self.maxDiff = None
            self.assertMultiLineEqual(got, exp)

        fs.fs.clear()

    t.__name__ = 'test_' + name
    return t

def create_test_static(name, files, ofiles):
    def t(self):
        fs.fs = fs.System

        tmpdir = fs.fs.mkdtemp()
        gendir = os.path.join(tmpdir, 'static')

        cmdgenerate.run(['--', '--quiet', '--type', 'html', '--static', '--output', gendir] + files)

        for f in ofiles:
            b = os.path.basename(f)
            htmlname = b[len(name)+1:len(b)-7]

            gf = fs.fs.open(os.path.join(gendir, htmlname))

            got = gf.read()
            exp = open(f).read()

            self.maxDiff = None
            self.assertMultiLineEqual(got, exp)

        fs.fs.rmtree(gendir)

    t.__name__ = 'test_static_' + name
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

        ofiles = glob.glob(os.path.join(dname, 'output', hname + '-*.xml'))

        t = create_test(hname, files, ofiles)
        setattr(Regression, t.__name__, t)

        # ofiles = glob.glob(os.path.join(dname, 'output', hname + '-*.html.static'))

        # t = create_test_static(hname, files, ofiles)
        # setattr(Regression, t.__name__, t)

os.environ['CLDOC_DEV'] = '1'

generate_tests()

if __name__ == '__main__':
    unittest.main()

# vi:ts=4:et

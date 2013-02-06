from __future__ import absolute_import

import sys, os

from . import tree
from . import generators

import argparse

def run():
    parser = argparse.ArgumentParser(description='clang based documentation generator.')

    parser.add_argument('--inspect', default=False,
                        action='store_const', const=True, help='inspect the AST')

    parser.add_argument('--serve', default=False,
                        action='store_const', const=True, help='serve generated xml')

    parser.add_argument('--output', default=None, metavar='DIR',
                        help='specify the output directory')

    parser.add_argument('--merge', default=None, metavar='FILES',
                        help='specify additional description files to merge into the documentation')

    parser.add_argument('files', nargs='+', help='files to parse')

    opts, flags = parser.parse_known_args()
    files = opts.files

    t = tree.Tree(files, flags)

    if opts.inspect:
        import inspecttree

        inspecttree.inspect(t)
    elif opts.serve:
        import subprocess, SimpleHTTPServer, SocketServer

        if opts.output:
            filepath = os.path.join(opts.output, '..')
        else:
            sys.stderr.write("Please specify the output xml directory to serve\n")
            sys.exit(1)

        curwd = os.getcwd()
        os.chdir(filepath)

        url = 'http://localhost:6060/'

        if sys.platform.startswith('darwin'):
            subprocess.Popen(('open', url))
        elif os.name == 'posix':
            subprocess.Popen(('xdg-open', url))

        try:
            handler = SimpleHTTPServer.SimpleHTTPRequestHandler

            httpd = SocketServer.TCPServer(("", 6060), handler)
            httpd.allow_reuse_address = True

            httpd.serve_forever()
        finally:
            os.chdir(curwd)

    else:
        t.process()

        if opts.merge:
            t.merge(opts.merge)

        generator = generators.Xml(t)
        generator.generate(opts.output)

if __name__ == '__main__':
    run()

# vi:ts=4:et

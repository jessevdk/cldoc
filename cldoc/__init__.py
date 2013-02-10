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
from __future__ import absolute_import

import sys, os, argparse, shlex

def generate(opts, cxxflags):
    from . import tree
    from . import generators

    if not opts.output:
        sys.stderr.write("Please specify the output directory\n")
        sys.exit(1)

    haslang = False

    for x in cxxflags:
        if x.startswith('-x'):
            haslang = True

    if not haslang:
        cxxflags.append('-x')
        cxxflags.append(opts.language)

    t = tree.Tree(opts.files, cxxflags)

    t.process()

    if opts.merge:
        t.merge(opts.merge)

    if opts.type == 'html' or opts.type == 'xml':
        generator = generators.Xml(t, opts)

        xmlout = os.path.join(opts.output, 'xml')
        generator.generate(xmlout)

        isstatic = opts.static

        if opts.type == 'html':
            generators.Html(t).generate(opts.output, isstatic)

            if isstatic:
                shutil.rmtree(xmlout)

def serve(opts):
    import subprocess, SimpleHTTPServer, SocketServer, threading, time

    if not opts.output:
        sys.stderr.write("Please specify the output directory to serve\n")
        sys.exit(1)

    class Server(SocketServer.TCPServer):
        allow_reuse_address = True

    class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            while path.startswith('/'):
                path = path[1:]

            path = os.path.join(opts.output, path)
            return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)

        def log_message(self, format, *args):
            pass

    class SocketThread(threading.Thread):
        def __init__(self, host):
            threading.Thread.__init__(self)

            if not ':' in host:
                self.host = host
                self.port = 6060
            else:
                self.host, port = host.split(':')
                self.port = int(port)

            self.httpd = Server((self.host, self.port), Handler)

        def shutdown(self):
            self.httpd.shutdown()
            self.httpd.server_close()

        def run(self):
            self.httpd.serve_forever()

    t = SocketThread(opts.serve)
    t.start()

    dn = open(os.devnull)

    if t.host == '':
        url = 'http://localhost:{0}/'.format(t.port)
    else:
        url = 'http://{0}:{1}/'.format(t.host, t.port)

    if sys.platform.startswith('darwin'):
        subprocess.call(('open', url), stdout=dn, stderr=dn)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', url), stdout=dn, stderr=dn)

    while True:
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            t.shutdown()
            t.join()
            break

def inspect(opts, cxxflags):
    from . import tree
    from . import inspecttree

    t = tree.Tree(opts.files, cxxflags)
    inspecttree.inspect(t)

def run():
    try:
        sep = sys.argv.index('--')
    except ValueError:
        if not '--help' in sys.argv:
            sys.stderr.write('Please use: cldoc [CXXFLAGS] -- [OPTIONS] [FILES]\n')
            sys.exit(1)
        else:
            sep = 0

    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s [CXXFLAGS] -- [OPTIONS] [FILES]')

    parser.add_argument('--inspect', default=False,
                        action='store_const', const=True, help='inspect the AST')

    parser.add_argument('--report', default=False,
                        action='store_const', const=True, help='report documentation coverage and errors')

    parser.add_argument('--serve', default=None, nargs='?', const=':6060', metavar='HOST:PORT',
                        help='serve generated documentation (default on :6060)')

    parser.add_argument('--output', default=None, metavar='DIR',
                        help='specify the output directory')

    parser.add_argument('--language', default='c++', metavar='LANGUAGE',
                        help='specify the default parse language (c++, c or objc)')

    parser.add_argument('--type', default='html', metavar='TYPE',
                        help='specify the type of output (html or xml, default html)')

    parser.add_argument('--merge', default=None, metavar='FILES',
                        help='specify additional description files to merge into the documentation')

    parser.add_argument('--basedir', default=None, metavar='DIR',
                        help='the project base directory')

    parser.add_argument('--static', default=False,
                        help='generate a static website (only for when --output is html)')

    parser.add_argument('files', nargs='*', help='files to parse')

    args = sys.argv[sep + 1:]

    cxxflags = sys.argv[1:sep]
    opts = parser.parse_args(args)

    if opts.inspect:
        inspect(opts, cxxflags)
    elif opts.serve:
        serve(opts)
    else:
        generate(opts, cxxflags)

if __name__ == '__main__':
    run()

# vi:ts=4:et

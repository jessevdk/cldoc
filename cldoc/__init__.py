from __future__ import absolute_import

import sys, os, argparse, shlex

def generate(opts):
    from . import tree
    from . import generators

    flags = shlex.split(os.getenv('CXXFLAGS'))
    t = tree.Tree(opts.files, flags)

    t.process()

    if opts.merge:
        t.merge(opts.merge)

    if opts.type == 'html' or opts.type == 'xml':
        generator = generators.Xml(t, opts)
        generator.generate(os.path.join(opts.output, 'xml'))

        if opts.type == 'html':
            generators.Html().generate(opts.output)

def serve(opts):
    import subprocess, SimpleHTTPServer, SocketServer, threading, time

    if not opts.output:
        sys.stderr.write("Please specify the output directory to serve\n")
        sys.exit(1)

    url = 'http://localhost:6060/'

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
        def __init__(self):
            threading.Thread.__init__(self)

            self.httpd = Server(("", 6060), Handler)

        def shutdown(self):
            self.httpd.shutdown()
            self.httpd.server_close()

        def run(self):
            self.httpd.serve_forever()

    t = SocketThread()
    t.start()

    dn = open(os.devnull)

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

def inspect(opts):
    from . import tree
    from . import inspecttree

    flags = shlex.split(os.getenv('CXXFLAGS'))

    t = tree.Tree(opts.files, flags)
    inspecttree.inspect(t)

def run():
    parser = argparse.ArgumentParser(description='clang based documentation generator.')

    parser.add_argument('--inspect', default=False,
                        action='store_const', const=True, help='inspect the AST')

    parser.add_argument('--report', default=False,
                        action='store_const', const=True, help='report documentation coverage and errors')

    parser.add_argument('--serve', default=False,
                        action='store_const', const=True, help='serve generated documentation')

    parser.add_argument('--output', default=None, metavar='DIR',
                        help='specify the output directory')

    parser.add_argument('--type', default='html', metavar='TYPE',
                        help='specify the type of output (html or xml)')

    parser.add_argument('--merge', default=None, metavar='FILES',
                        help='specify additional description files to merge into the documentation')

    parser.add_argument('--basedir', default=None, metavar='DIR',
                        help='the project base directory')

    parser.add_argument('files', nargs='+', help='files to parse')

    opts = parser.parse_args()

    if opts.inspect:
        inspect(opts)
    elif opts.serve:
        serve(opts)
    else:
        generate(opts)

if __name__ == '__main__':
    run()

# vi:ts=4:et

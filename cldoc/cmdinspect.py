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

import subprocess, threading, time, sys, argparse, os
import SimpleHTTPServer, SocketServer

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

def run(args):
    try:
        sep = args.index('--')
    except ValueError:
        if not '--help' in args:
            sys.stderr.write('Please use: cldoc inspect [CXXFLAGS] -- [OPTIONS] [FILES]\n')
            sys.exit(1)
        else:
            sep = 0

    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s inspect [CXXFLAGS] -- [OPTIONS] DIRECTORY')

    parser.add_argument('files', nargs='*', help='files to parse')

    restargs = args[sep + 1:]
    cxxflags = args[1:sep]

    opts = parser.parse_args(restargs)

    from . import tree
    from . import inspecttree

    t = tree.Tree(opts.files, cxxflags)
    inspecttree.inspect(t)

# vi:ts=4:et

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

def handler_bind(directory):
    class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            while path.startswith('/'):
                path = path[1:]

            path = os.path.join(directory, path)
            return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)

        def log_message(self, format, *args):
            pass

    return Handler

class SocketThread(threading.Thread):
    def __init__(self, directory, host):
        threading.Thread.__init__(self)

        if not ':' in host:
            self.host = host
            self.port = 6060
        else:
            self.host, port = host.split(':')
            self.port = int(port)

        self.httpd = Server((self.host, self.port), handler_bind(directory))

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def run(self):
        self.httpd.serve_forever()

def run(args):
    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s serve [OPTIONS] [DIRECTORY]')

    parser.add_argument('--address', default=':6060', metavar='HOST:PORT',
                        help='address (host:port) on which to serve documentation')

    parser.add_argument('directory', nargs='?', help='directory to serve', default='.')

    opts = parser.parse_args(args)

    t = SocketThread(opts.directory, opts.address)
    t.start()

    dn = open(os.devnull, 'w')

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

# vi:ts=4:et

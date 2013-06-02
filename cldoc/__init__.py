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

import sys

def run_inspect(args):
    from . import cmdinspect
    cmdinspect.run(args)

def run_serve(args):
    from . import cmdserve
    cmdserve.run(args)

def run_generate(args):
    from . import cmdgenerate
    cmdgenerate.run(args)

def run_gir(args):
    from . import cmdgir
    cmdgir.run(args)

def print_available_commands():
    sys.stderr.write('Available commands:\n')

    commands = ['inspect', 'serve', 'generate', 'gir']

    for c in commands:
        sys.stderr.write('  ' + c + '\n')

    sys.stderr.write('\n')

def run():
    if len(sys.argv) <= 1:
        sys.stderr.write('Please use: cldoc [command] [OPTIONS] [FILES...]\n\n')
        print_available_commands()
        sys.exit(1)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == 'inspect':
        run_inspect(rest)
    elif cmd == 'serve':
        run_serve(rest)
    elif cmd == 'generate':
        run_generate(rest)
    elif cmd == 'gir':
        run_gir(rest)
    elif cmd == '--help' or cmd == '-h':
        sys.stderr.write('Please use: cldoc [command] --help\n\n')
        print_available_commands()
        sys.exit(1)
    else:
        sys.stderr.write('Unknown command `{0}\'\n'.format(cmd))
        sys.exit(1)

if __name__ == '__main__':
    run()

# vi:ts=4:et

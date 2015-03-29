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
import os, subprocess, sys

def flags(f):
    devnull = open(os.devnull)

    try:
        p = subprocess.Popen(['clang++', '-E', '-xc++'] + f + ['-v', '-'],
                             stdin=devnull,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except OSError as e:
        sys.stderr.write("\nFatal: Failed to run clang++ to obtain system include headers, please install clang++ to use cldoc\n")

        message = str(e)

        if message:
            sys.stderr.write("  Error message: " + message + "\n")

        sys.stderr.write("\n")
        sys.exit(1)

    devnull.close()

    lines = p.communicate()[1].splitlines()
    init = False
    paths = []

    for line in lines:
        if line.startswith('#include <...>'):
            init = True
        elif line.startswith('End of search list.'):
            init = False
        elif init:
            p = line.strip()

            suffix = ' (framework directory)'

            if p.endswith(suffix):
                p = p[:-len(suffix)]

            paths.append(p)

    return ['-I{0}'.format(x) for x in paths] + f

# vi:ts=4:et

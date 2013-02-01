import os, subprocess

devnull = open(os.devnull)
p = subprocess.Popen(['clang++', '-E', '-xc++', '-v', '-'],
                     stdin=devnull,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
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
        paths.append(line.strip())

flags = ['-I{0}'.format(x) for x in paths]

__all__ = ['flags']

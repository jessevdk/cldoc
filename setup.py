#!/usr/bin/env python

from distutils.core import setup
from distutils.command.build import build

import subprocess, os

coffee_files = [
    'cldoc.coffee',
    'page.coffee',
    'sidebar.coffee',
    'node.coffee',
    'type.coffee',
    'doc.coffee',
    'category.coffee',
    'enum.coffee',
    'struct.coffee',
    'class.coffee',
    'namespace.coffee',
    'typedef.coffee',
    'variable.coffee',
    'function.coffee',
    'field.coffee',
    'method.coffee',
    'constructor.coffee',
    'destructor.coffee',
    'base.coffee',
    'subclass.coffee',
    'coverage.coffee',
    'arguments.coffee',
    'report.coffee',
    'references.coffee'
]

class cldoc_build(build):
    user_options = build.user_options + [
        ('coffee=', None, 'path to coffeescript compiler'),
        ('sass=', None, 'path to sass compiler'),
        ('inliner=', None, 'path to inliner')
    ]

    def initialize_options(self):
        build.initialize_options(self)

        self.coffee = 'coffee'
        self.sass = 'sass'
        self.inliner = 'inliner'

    def run_coffee(self):
        print('running {0}'.format(self.coffee))

        try:
            os.makedirs('html/javascript')
        except:
            pass

        args = [self.coffee, '--bare', '--join', 'html/javascript/cldoc.js', '--compile']
        files = ['html/coffee/' + x for x in coffee_files]

        subprocess.call(args + files)

    def run_sass(self):
        print('running {0}'.format(self.sass))

        try:
            os.makedirs('html/styles')
        except:
            pass

        args = [self.sass, '--scss', '--line-numbers', '--no-cache', '--style', 'compressed']
        files = ['html/sass/cldoc.scss', 'html/styles/cldoc.css']

        subprocess.call(args + files)

    def run_inliner(self):
        print('running {0}'.format(self.inliner))

        args = [self.inliner, 'html/index.html']

        try:
            os.makedirs('cldoc/data')
        except:
            pass

        fout = file('cldoc/data/index.html', 'w')

        proc = subprocess.Popen(args, stdout=fout)
        proc.wait()

    def run(self):
        self.run_coffee()
        self.run_sass()
        self.run_inliner()

        build.run(self)

cmdclass = {
    'build': cldoc_build
}

setup(name='cldoc',
      version='1.0',
      description='clang based documentation generator for C/C++',
      author='Jesse van den Kieboom',
      author_email='jessevdk@gmail.com',
      url='http://github.com/jessevdk/cldoc',
      packages=['cldoc'],
      scripts=['scripts/cldoc'],
      package_data={'cldoc': ['data/*']},
      cmdclass=cmdclass)

# vi:ts=4:et

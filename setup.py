#!/usr/bin/env python

from setuptools import setup, Command

import subprocess, os, shutil, glob

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
    'implements.coffee',
    'subclass.coffee',
    'implementedby.coffee',
    'coverage.coffee',
    'arguments.coffee',
    'report.coffee',
    'references.coffee',
    'union.coffee',
    'gobjectclass.coffee',
    'gobjectinterface.coffee',
    'gobjectboxed.coffee',
    'gobjectproperty.coffee',
]

class cldoc_generate(Command):
    description = "generate css, js and html files"

    user_options = [
        ('coffee=', None, 'path to coffeescript compiler'),
        ('sass=', None, 'path to sass compiler'),
        ('inliner=', None, 'path to inliner')
    ]

    def initialize_options(self):
        self.coffee = 'coffee'
        self.sass = 'sass'
        self.inliner = 'inliner'

    def finalize_options(self):
        pass

    def run_coffee(self):
        print('running {0}'.format(self.coffee))

        for d in ('html/javascript', 'cldoc/data/javascript'):
            try:
                os.makedirs(d)
            except:
                pass

        args = [self.coffee, '--bare', '--join', 'html/javascript/cldoc.js', '--compile']
        files = ['html/coffee/' + x for x in coffee_files]

        subprocess.call(args + files)

        for js in glob.glob('html/javascript/*.js'):
            shutil.copyfile(js, 'cldoc/data/javascript/' + os.path.basename(js))

    def run_sass(self):
        print('running {0}'.format(self.sass))

        for d in ('html/styles', 'cldoc/data/styles'):
            try:
                os.makedirs(d)
            except:
                pass

        args = [self.sass, '--scss', '--line-numbers', '--no-cache', '--style', 'compressed']
        files = ['html/sass/cldoc.scss', 'html/styles/cldoc.css']

        subprocess.call(args + files)

        for css in glob.glob('html/styles/*.css'):
            shutil.copyfile(css, 'cldoc/data/styles/' + os.path.basename(css))

    def run_inliner(self):
        if self.inliner == '':
            shutil.copyfile('html/index.html', 'cldoc/data/index.html')
            return

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

cmdclass = {
    'generate': cldoc_generate
}

datafiles = []
dataprefix = 'cldoc'

for dirpath, dirnames, filenames in os.walk(os.path.join(dataprefix, 'data')):
    datafiles += [os.path.join(dirpath[len(dataprefix)+1:], f) for f in filenames]

setup(name='cldoc',
      version='1.5',
      description='clang based documentation generator for C/C++',
      author='Jesse van den Kieboom',
      author_email='jessevdk@gmail.com',
      url='http://jessevdk.github.com/cldoc',
      license='GPLv2',
      keywords=['clang', 'c++', 'documentation'],
      packages=['cldoc', 'cldoc.clang', 'cldoc.nodes', 'cldoc.generators'],
      entry_points = {
          'console_scripts': [
              'cldoc = cldoc:run'
          ]
      },
      package_data={'cldoc': datafiles},
      cmdclass=cmdclass,
      install_requires=['pyparsing ==1.5.7'])

# vi:ts=4:et

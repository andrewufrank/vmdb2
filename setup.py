#!/usr/bin/python
# Copyright (C) 2017  Lars Wirzenius <liw@liw.fi>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from distutils.core import setup, Extension
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
import os
import glob

import cliapp

import vmdb


class Build(build):

    def run(self):
        build.run(self)
        self.build_manpage('vmdb2', '')
        self.format_yarns()

    def build_manpage(self, program, lang):
        print 'building manpage for %s (lang=%s)' % (program, lang)
        self.generate_troff(program, lang)
        self.format_man_as_txt(program)

    def generate_troff(self, program, lang):
        with open('%s.1%s' % (program, lang), 'w') as f:
            cliapp.runcmd(
                ['python', program,
                 '--generate-manpage=%s.1%s.in' % (program, lang),
                 '--output=%s.1' % program],
                stdout=f)

    def format_man_as_txt(self, program):
        env = dict(os.environ)
        env['MANWIDTH'] = '80'
        with open('%s.1.txt' % program, 'w') as f:
            cliapp.runcmd(
                ['man', '-l', '%s.1' % program],
                ['col', '-b'],
                stdout=f,
                env=env)

    def format_yarns(self):
        print 'building yarns'
        runcmd(['make', '-C', 'yarns'])


setup(
    name='FIXME',
    version=vmdb.__version__,
    description='create disk image with Debian installed',
    author='Lars Wirzenius',
    author_email='liw@liw.fi',
    url='http://liw.fi/vmdebootstrap/',
    scripts=['vmdb2'],
    packages=['vmdb'],
    data_files=[('share/man/man1', glob.glob('*.1'))],
    cmdclass={
        'build': Build,
    },
)

#! /usr/bin/env python3
"""Setup file for distutils

__author__ = "http://www.gemalto.com"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

Copyright 2007-2018 Ludovic Rousseau ludovic.rousseau@free.fr

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from distutils.util import get_platform
import sys

from setuptools import setup, Extension
from setuptools.command.build_py import build_py


if sys.version_info[0:2] < (2, 6):
    raise RuntimeError("pyscard requires Python 2.6+ to build.")

platform_include_dirs = []
platform_sources = []
platform_libraries = []
platform_extra_compile_args = []    # ['-ggdb', '-O0']
platform_extra_link_args = []   # ['-ggdb']

if get_platform() in ('win32', 'win-amd64'):
    platform__cc_defines = [('WIN32', '100')]
    platform_swig_opts = ['-DWIN32']
    platform_sources = ['smartcard/scard/scard.rc']
    platform_libraries = ['winscard']

elif 'cygwin-' in get_platform():
    platform__cc_defines = [('WIN32', '100')]
    platform_swig_opts = ['-DWIN32']
    platform_libraries = ['winscard']

elif 'macosx-' in get_platform():
    if 'macosx-10.6' in get_platform():
        macosx_define = '__LEOPARD__'  # Snow Leopard, Python 2.6
    else:
        macosx_define = '__LION__'  # Lion (and above), Python 2.7
    platform__cc_defines = [('PCSCLITE', '1'),
                            ('__APPLE__', '1'),
                            (macosx_define, '1')]
    platform_swig_opts = ['-DPCSCLITE', '-D__APPLE__', '-D' + macosx_define]

# Other (GNU/Linux, etc.)
#
else:
    platform__cc_defines = [('PCSCLITE', '1')]
    platform_swig_opts = ['-DPCSCLITE']
    platform_include_dirs = ['/usr/include/PCSC', '/usr/local/include/PCSC']


VERSION_INFO = (2, 0, 2, 0)
VERSION_STR = '%i.%i.%i' % VERSION_INFO[:3]
VERSION_ALT = '%i,%01i,%01i,%04i' % VERSION_INFO


class BuildPyBuildExtFirst(build_py):
    """Workaround substitude `build_py` command for SWIG"""
    def run(self):
        # Run build_ext first so that SWIG generated files are included
        self.run_command('build_ext')
        return build_py.run(self)


kw = {'name': "pyscard",
      'version': VERSION_STR,
      'description': "Smartcard module for Python.",
      'author': "Ludovic Rousseau",
      'author_email': "ludovic.rousseau@free.fr",
      'url': "https://github.com/LudovicRousseau/pyscard",
      'long_description': 'Smartcard package for Python',
      'platforms': ['linux', 'win32'],
      'packages': ["smartcard",
                   "smartcard.pcsc",
                   "smartcard.pyro",
                   "smartcard.reader",
                   "smartcard.scard",
                   "smartcard.sw",
                   "smartcard.util",
                   "smartcard.wx",
                   ],
      'package_dir': {"": "."},
      'package_data': {
                         "smartcard.wx": ["resources/*.ico"],
                       },

      'cmdclass': {'build_py': BuildPyBuildExtFirst},
      # the _scard.pyd extension to build
      'ext_modules': [Extension("smartcard.scard._scard",
                      define_macros=[
                                    ('VER_PRODUCTVERSION', VERSION_ALT),
                                    ('VER_PRODUCTVERSION_STR', VERSION_STR)] \
                      + platform__cc_defines,
                      include_dirs=['smartcard/scard/'] \
                      + platform_include_dirs,
                      sources=["smartcard/scard/helpers.c",
                               "smartcard/scard/winscarddll.c",
                               "smartcard/scard/scard.i"] \
                                       + platform_sources,
                      libraries=platform_libraries,
                      extra_compile_args=platform_extra_compile_args,
                      extra_link_args=platform_extra_link_args,
                      swig_opts=['-outdir',
                                 'smartcard/scard'] \
                      + platform_swig_opts)],
      'extras_require': {
            'Gui': ['wxPython'],
            'Pyro': ['Pyro'],
            },

      'test_suite': 'test',

      'classifiers': [
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU Lesser General Public License v2 '
          'or later (LGPLv2+)',
          'Intended Audience :: Developers',
          'Operating System :: Unix',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Security',
          ]
      }

# FIXME Sourceforge downloads are unauthenticated, migrate to PyPI
kw['download_url'] = ('http://sourceforge.net/projects/%(name)s/files'
                      '/%(name)s/%(name)s%%20%(version)s'
                      '/%(name)s-%(version)s.tar.gz/download' % kw)

setup(**kw)

#! /usr/bin/env python
"""Setup file for distutils

__author__ = "http://www.gemalto.com"

Copyright 2001-2010 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

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

from distutils import core, dir_util, file_util
from distutils.core import Extension
from distutils.util import get_platform
from distutils.command.build_ext import build_ext
import glob
import os
import sys

if sys.version[0:1] == '1':
    raise RuntimeError("pyscard requires Python 2.x to build.")

if 'win32' == get_platform():
    platform__cc_defines = [('WIN32', '100')]
    platform_swig_opts = ['-DWIN32']
    platform_sources = ['smartcard/scard/scard.rc']
    platform_libraries = ['winscard']
    platform_include_dirs = []
    platform_extra_compile_args = []
    platform_extra_link_args = []

#
# Mac OS X Tiger has python 2.3 preinstalled
# get_platform() returns a string similar to 'darwin-8.11.1-i386' with
# python 2.3
# if python 2.5 is installed, get_platform() returns a string similar to
# 'macosx-10.3-fat'
elif 'darwin' in get_platform() or 'macosx-10.3' in get_platform() or 'macosx-10.4' in get_platform():
    platform__cc_defines = [('PCSCLITE', '1'), ('__APPLE__', '1'), ('__TIGER__', '1')]
    platform_swig_opts = ['-DPCSCLITE', '-D__APPLE__', '-D__TIGER__']
    platform_sources = []
    platform_libraries = []
    platform_include_dirs = []
    platform_extra_compile_args = ['-v', '-framework', 'PCSC', '-arch', 'i386', '-arch', 'ppc', '-ggdb', '-O0']
    platform_extra_link_args = ['-arch', 'i386', '-arch', 'ppc', '-ggdb']

#
# Mac OS X Snow Leopard, python 2.6
# PowerPC is no more supported, x86_64 is new
#
elif 'macosx-10.6' in get_platform():
    platform__cc_defines = [('PCSCLITE', '1'), ('__APPLE__', '1'), ('__LEOPARD__', '1')]
    platform_swig_opts = ['-DPCSCLITE', '-D__APPLE__', '-D__LEOPARD__']
    platform_sources = []
    platform_libraries = []
    platform_include_dirs = []
    platform_extra_compile_args = ['-v', '-arch', 'i386', '-arch', 'x86_64', '-ggdb']
    platform_extra_link_args = ['-arch', 'i386', '-arch', 'x86_64', '-ggdb']

#
# Mac OS X Leopard has python 2.5 preinstalled
# get_platform() returns a string similar to 'macosx-10.5-i386'
#
elif 'macosx-10.' in get_platform():
    platform__cc_defines = [('PCSCLITE', '1'), ('__APPLE__', '1'), ('__LEOPARD__', '1')]
    platform_swig_opts = ['-DPCSCLITE', '-D__APPLE__', '-D__LEOPARD__']
    platform_sources = []
    platform_libraries = []
    platform_include_dirs = []
    platform_extra_compile_args = ['-v', '-framework', 'PCSC', '-arch', 'i386', '-arch', 'ppc', '-ggdb', '-O0']
    platform_extra_link_args = ['-arch', 'i386', '-arch', 'ppc', '-ggdb']
else:
    platform__cc_defines = [('PCSCLITE', '1')]
    platform_swig_opts = ['-DPCSCLITE']
    platform_sources = []
    platform_libraries = ["python%d.%d" % sys.version_info[:2]]
    platform_include_dirs = ['/usr/include/PCSC']
    platform_extra_compile_args = []    #['-ggdb', '-O0']
    platform_extra_link_args = []   #['-ggdb']


class _pyscardBuildExt(build_ext):
    '''Specialization of build_ext to enable swig_opts for python 2.3 distutils'''
if sys.version_info < (2, 4):

    # This copy of swig_sources is from Python 2.3.
    # This is to add support of swig_opts for Python 2.3 distutils
    # (in particular for MacOS X darwin that comes with Python 2.3)

    def swig_sources(self, sources):

        """Walk the list of source files in 'sources', looking for SWIG
        interface (.i) files.  Run SWIG on all that are found, and
        return a modified 'sources' list with SWIG source files replaced
        by the generated C (or C++) files.
        """

        new_sources = []
        swig_sources = []
        swig_targets = {}

        # XXX this drops generated C/C++ files into the source tree, which
        # is fine for developers who want to distribute the generated
        # source -- but there should be an option to put SWIG output in
        # the temp dir.

        if self.swig_cpp:
            target_ext = '.cpp'
        else:
            target_ext = '.c'

        for source in sources:
            (base, ext) = os.path.splitext(source)
            if ext == ".i":             # SWIG interface file
                new_sources.append(base + target_ext)
                swig_sources.append(source)
                swig_targets[source] = new_sources[-1]
            else:
                new_sources.append(source)

        if not swig_sources:
            return new_sources

        swig = self.find_swig()
        swig_cmd = [swig, "-python"]
        if self.swig_cpp:
            swig_cmd.append("-c++")

        swig_cmd += platform_swig_opts

        for source in swig_sources:
            target = swig_targets[source]
            self.announce("swigging %s to %s" % (source, target))
            self.spawn(swig_cmd + ["-o", target, source])

        return new_sources

    build_ext.swig_sources = swig_sources

kw = {'name': "pyscard",
      'version': "1.6.12",
      'description': "Smartcard module for Python.",
      'author': "Jean-Daniel Aussel",
      'author_email': "aussel.jean-daniel@gemalto.com",
      'url': "http://www.gemalto.com",
      'long_description': 'Smartcard package for Python',
      'license': 'GNU LESSER GENERAL PUBLIC LICENSE',
      'platforms': ['linux', 'win32'],
      'packages': ["smartcard",
                   "smartcard/pcsc",
                   "smartcard/reader",
                   "smartcard/scard",
                   "smartcard/sw",
                   "smartcard/util",
                   "smartcard/wx",
                   ],
      'package_dir': {"": "."},
      'package_data': {
                         "smartcard": [
                                        "ACKS",
                                        "ChangeLog",
                                        "LICENSE",
                                        "README",
                                        "TODO",
                                        ],
                         "smartcard/wx": ["resources/*.ico"],
                       },

      # the _scard.pyd extension to build
      'ext_modules': [Extension("smartcard.scard._scard",
                             define_macros=platform__cc_defines,
                             include_dirs=['smartcard/scard/'] + platform_include_dirs,
                             sources=["smartcard/scard/helpers.c",
                                      "smartcard/scard/winscarddll.c",
                                      "smartcard/scard/scard.i"] + platform_sources,
                             libraries=platform_libraries,
                             extra_compile_args=platform_extra_compile_args,
                             extra_link_args=platform_extra_link_args,
                             swig_opts=['-outdir', 'smartcard/scard'] + platform_swig_opts)],
      'cmdclass': {'build_ext': _pyscardBuildExt},
     }

# If we're running >Python 2.3, add extra information
if hasattr(core, 'setup_keywords'):
    if 'classifiers' in core.setup_keywords:
        kw['classifiers'] = [
          'Development Status :: 1.6.12 - Release',
          'License :: GNU LESSER GENERAL PUBLIC LICENSE',
          'Intended Audience :: Developers',
          'Operating System :: Unix',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Security :: Smartcards',
          ]
    if 'download_url' in core.setup_keywords:
        kw['download_url'] = ('http://sourceforge.net/projects/pyscard/'
                              '%s-%s.zip' % (kw['name'], kw['version']))


pyscard_dist = core.setup(**kw)


# Python 2.3 distutils does not support package_data
# copy manually package_data
if sys.version_info < (2, 4):
    from distutils.util import convert_path
    from glob import glob
    if "install" in sys.argv:
        targetdir = pyscard_dist.command_obj['install'].install_purelib
        package_data = kw['package_data']
        files = []
        for directory in package_data:
            for pattern in package_data[directory]:
                filelist = glob(os.path.join(directory, convert_path(pattern)))
                files.extend([fn for fn in filelist if fn not in files])
        for file in files:
            newdir = os.path.dirname(file)
            dir_util.mkpath(os.path.join(targetdir, newdir))
            file_util.copy_file(file, os.path.join(targetdir, file))

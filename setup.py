#! /usr/bin/env python3
"""Setup file for setuptools

__author__ = "https://www.gemalto.com/"

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

import platform
import shlex
import subprocess
from shutil import which
from sysconfig import get_platform

from setuptools import Extension, setup
from setuptools.command.build_py import build_py

platform_include_dirs = []
platform_sources = []
platform_libraries = []
platform_extra_compile_args = []  # ['-ggdb', '-O0']
platform_extra_link_args = []  # ['-ggdb']

if platform.system() == "Windows":
    platform__cc_defines = [("WIN32", "100")]
    platform_swig_opts = ["-DWIN32"]
    if "mingw" not in get_platform():
        platform_sources = ["src/smartcard/scard/scard.rc"]
    platform_libraries = ["winscard"]

elif platform.system() == "Darwin":
    platform__cc_defines = [("PCSCLITE", "1"), ("__APPLE__", "1")]
    platform_swig_opts = ["-DPCSCLITE", "-D__APPLE__"]

# Other (GNU/Linux, etc.)
#
else:
    platform__cc_defines = [("PCSCLITE", "1")]
    platform_swig_opts = ["-DPCSCLITE"]
    try:
        pkg_config_cflags = subprocess.check_output(
            ["pkg-config", "--cflags", "libpcsclite"]
        )
        platform_extra_compile_args += shlex.split(pkg_config_cflags.decode())
    except:
        platform_include_dirs = ["/usr/include/PCSC", "/usr/local/include/PCSC"]

VERSION_INFO = (2, 2, 2, 0)
VERSION_STR = "%i.%i.%i" % VERSION_INFO[:3]
VERSION_ALT = "%i,%01i,%01i,%04i" % VERSION_INFO


class BuildPyBuildExtFirst(build_py):
    """Workaround substitute `build_py` command for SWIG"""

    def run(self):
        if which("swig") is None:
            print("Install swig and try again")
            print("")
            exit(1)
        # Run build_ext first so that SWIG generated files are included
        self.run_command("build_ext")
        return build_py.run(self)


kw = {
    "name": "pyscard",
    "version": VERSION_STR,
    "description": "Smartcard module for Python.",
    "author": "Ludovic Rousseau",
    "author_email": "ludovic.rousseau@free.fr",
    "url": "https://github.com/LudovicRousseau/pyscard",
    "long_description": "Smartcard package for Python",
    "platforms": ["linux", "win32"],
    "python_requires": ">=3.9",
    "packages": [
        "smartcard",
        "smartcard.pcsc",
        "smartcard.reader",
        "smartcard.scard",
        "smartcard.sw",
        "smartcard.util",
        "smartcard.wx",
    ],
    "package_dir": {"": "src"},
    "package_data": {
        "smartcard.wx": ["resources/*.ico"],
    },
    "cmdclass": {"build_py": BuildPyBuildExtFirst},
    # the _scard.pyd extension to build
    "ext_modules": [
        Extension(
            "smartcard.scard._scard",
            define_macros=[
                ("VER_PRODUCTVERSION", VERSION_ALT),
                ("VER_PRODUCTVERSION_STR", VERSION_STR),
            ]
            + platform__cc_defines,
            include_dirs=["src/smartcard/scard/"] + platform_include_dirs,
            sources=[
                "src/smartcard/scard/helpers.c",
                "src/smartcard/scard/winscarddll.c",
                "src/smartcard/scard/scard.i",
            ]
            + platform_sources,
            libraries=platform_libraries,
            extra_compile_args=platform_extra_compile_args,
            extra_link_args=platform_extra_link_args,
            swig_opts=["-outdir", "src/smartcard/scard"] + platform_swig_opts,
        )
    ],
    "install_requires": [
        "typing_extensions; python_version=='3.9'",
    ],
    "extras_require": {
        "Gui": ["wxPython"],
    },
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Security",
    ],
}

# FIXME Sourceforge downloads are unauthenticated, migrate to PyPI
kw["download_url"] = (
    "https://sourceforge.net/projects/%(name)s/files"
    "/%(name)s/%(name)s%%20%(version)s"
    "/%(name)s-%(version)s.tar.gz/download" % kw
)

setup(**kw)

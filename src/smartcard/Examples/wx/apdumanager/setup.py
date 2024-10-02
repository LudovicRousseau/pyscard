#! /usr/bin/env python3
"""
Setup script to build a standalone apdumanager.exe executable on windows
using py2exe. Run: python.exe setup.py py2exe, to build executable file.

__author__ = "https://www.gemalto.com/"

Copyright 2001-2012 gemalto
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

from distutils.core import setup

import py2exe

from smartcard.wx import ICO_READER, ICO_SMARTCARD

Mydata_files = [("images", ["images/mysmartcard.ico", ICO_SMARTCARD, ICO_READER])]


setup(
    windows=["apdumanager.py"],
    data_files=Mydata_files,
    options={"py2exe": {"dll_excludes": ["MSVCP90.dll"]}},
)

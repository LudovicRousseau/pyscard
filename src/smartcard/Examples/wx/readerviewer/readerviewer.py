#! /usr/bin/env python3
"""Simple smart card reader monitoring application.

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

import os.path
import sys

from smartcard.wx.SimpleSCardApp import *


def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    From WhereAmI page on py2exe wiki."""

    return hasattr(sys, "frozen")


def module_path():
    """This will get us the program's directory,
    even if we are frozen using py2exe. From WhereAmI page on py2exe wiki."""

    if we_are_frozen():
        return os.path.dirname(sys.executable)

    return os.path.dirname(__file__)


def main(argv):
    app = SimpleSCardApp(
        appname="A simple reader monitoring tool",
        apppanel=None,
        appstyle=TR_READER,
        appicon=os.path.join(module_path(), "images", "readerviewer.ico"),
        size=(800, 600),
    )
    app.MainLoop()


if __name__ == "__main__":
    import sys

    main(sys.argv)

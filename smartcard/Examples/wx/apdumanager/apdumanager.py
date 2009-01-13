#! /usr/bin/env python
"""
Simple application to send APDUs to a card.

__author__ = "http://www.gemalto.com"

Copyright 2001-2008 gemalto
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
from smartcard.wx.SimpleSCardApp import *

from SampleAPDUManagerPanel import SampleAPDUManagerPanel

def main( argv ):
    app = SimpleSCardApp(
        appname = 'A tool to send apdu to a card',
        apppanel = SampleAPDUManagerPanel,
        appstyle =  TR_SMARTCARD | TR_READER | PANEL_APDUTRACER,
        appicon = os.path.join( os.path.dirname( __file__ ), 'images', 'mysmartcard.ico' ),
        size = (800,600) )
    app.MainLoop()

if __name__ == "__main__":
    import sys
    main( sys.argv )




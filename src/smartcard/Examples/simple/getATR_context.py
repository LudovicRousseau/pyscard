#! /usr/bin/env python3
"""
Sample script that displays the ATR of inserted cards.

__author__ = "https://www.gemalto.com/"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
Copyright 2010 Ludovic Rousseau
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

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
import sys

from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString

# Use a connection context
# the connection object is automatically destroyed at the end of with block

for reader in readers():
    with reader.createConnection() as connection:
        try:
            connection.connect()
            print(reader, toHexString(connection.getATR()))
        except NoCardException:
            print(reader, "no card inserted")

# sleep(5)

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

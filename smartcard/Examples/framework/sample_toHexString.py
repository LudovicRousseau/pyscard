#! /usr/bin/env python3
"""
Sample script to illustrate toHexString() utility method

__author__ = "http://www.gemalto.com"

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

from smartcard.util import *


print(40 * '-')
bytes = [59, 101, 0, 0, 156, 17, 1, 1, 3]
print('bytes = [59, 101, 0, 0, 156, 17, 1, 1, 3]')
print('toHexString(bytes) =', toHexString(bytes))
print('toHexString(bytes, COMMA) =', toHexString(bytes, COMMA))
print('toHexString(bytes, PACK) =', toHexString(bytes, PACK))
print('toHexString(bytes, HEX) =', toHexString(bytes, HEX))
print('toHexString(bytes, HEX | COMMA) =', toHexString(bytes, HEX | COMMA))
print('toHexString(bytes, HEX | UPPERCASE) =',
      toHexString(bytes, HEX | UPPERCASE))
print('toHexString(bytes, HEX | UPPERCASE | COMMA) =',
      toHexString(bytes, HEX | UPPERCASE | COMMA))


print(40 * '-')
bytes = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
print('bytes = [ 0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03 ]')
print('toHexString(bytes, COMMA) =', toHexString(bytes, COMMA))
print('toHexString(bytes) =', toHexString(bytes))
print('toHexString(bytes, PACK) =', toHexString(bytes, PACK))
print('toHexString(bytes, HEX) =', toHexString(bytes, HEX))
print('toHexString(bytes, HEX | COMMA) =', toHexString(bytes, HEX | COMMA))
print('toHexString(bytes, HEX | UPPERCASE) =',
      toHexString(bytes, HEX | UPPERCASE))
print('toHexString(bytes, HEX | UPPERCASE | COMMA) =',
      toHexString(bytes, HEX | UPPERCASE | COMMA))


import sys
if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)

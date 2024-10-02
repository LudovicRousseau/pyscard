#! /usr/bin/env python3
"""
Sample script for the smartcard.ATR utility class.

__author__ = "https://www.gemalto.com/"

Copyright 2001-2009 gemalto
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
from smartcard.ATR import ATR
from smartcard.util import toHexString

atr = ATR(
    [
        0x3B,
        0x9E,
        0x95,
        0x80,
        0x1F,
        0xC3,
        0x80,
        0x31,
        0xA0,
        0x73,
        0xBE,
        0x21,
        0x13,
        0x67,
        0x29,
        0x02,
        0x01,
        0x01,
        0x81,
        0xCD,
        0xB9,
    ]
)

print(atr)
print("historical bytes: ", toHexString(atr.getHistoricalBytes()))
print("checksum: ", "0x%X" % atr.getChecksum())
print("checksum OK: ", atr.checksumOK)
print("T0  supported: ", atr.isT0Supported())
print("T1  supported: ", atr.isT1Supported())
print("T15 supported: ", atr.isT15Supported())

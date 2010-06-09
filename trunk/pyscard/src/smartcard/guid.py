"""smartcard.guid

Utility functions to handle GUIDs as strings or list of bytes

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
from struct import unpack

# guid is ulong+ushort+ushort+uchar[8]; we need a map because bytes
# are swappted for the first three
map = {0: 3, 1: 2, 2: 1, 3: 0, 4: 5, 5: 4, 6: 7, 7: 6, 8: 8, 9: 9,
    10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15}


def  strToGUID(s):
    """Converts a GUID string into a list of bytes."""
    l = []
    for i in unpack('x' + '2s' * 4 + 'x' + '2s2sx' * 3 + '2s' * 6 + 'x', s):
        l += [int(i, 16)]
    zr = []
    for i in xrange(len(l)):
        zr.append(l[map[i]])
    return zr


def GUIDToStr(g):
    """Converts a GUID sequence of bytes into a string."""
    zr = []
    for i in xrange(len(g)):
        zr.append(g[map[i]])
    return "{%2X%2X%2X%2X-%2X%2X-%2X%2X-%2X%2X-%2X%2X%2X%2X%2X%2X}" % tuple(zr)

if __name__ == "__main__":
    """Small sample illustrating the use of guid.py."""
    import smartcard.guid
    dummycardguid1 = strToGUID('{AD4F1667-EA75-4124-84D4-641B3B197C65}')
    print dummycardguid1
    print GUIDToStr(dummycardguid1)

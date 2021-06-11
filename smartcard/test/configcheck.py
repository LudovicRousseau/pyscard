#! /usr/bin/env python3
"""Generates test suite smartcard configuration from
connected readers and cards.

The generated configuration is store in local_config.py.

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


from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.util import toHexString


def getATR(reader):
    cc = reader.createConnection()
    cc.connect()
    atr = cc.getATR()
    cc.disconnect()
    return atr


def checklocalconfig():
    try:
        f = open('local_config.py', 'r')
    except IOError:
        print('local_config.py not found; generating local_config.py...')
    else:
        print('regenerating local_config.py...')
        f.close()

    # generate local configuration
    f = open('local_config.py', 'w+')

    f.write('from smartcard.util import toHexString\n')
    f.write('expectedReaders = ')
    f.write(str(readers()) + '\n')
    expectedATRs = []
    for reader in readers():
        try:
            expectedATRs.append(getATR(reader))
        except NoCardException:
            expectedATRs.append([])
    f.write('expectedATRs = ')
    #for atr in expectedATRs: print `toHexString(atr)`
    f.write(repr(expectedATRs) + '\n')

    f.write('expectedATRinReader = {}\n')
    f.write('for i in range(len(expectedReaders)):\n')
    f.write('    expectedATRinReader[expectedReaders[i]] = expectedATRs[i]\n')

    f.write('expectedReaderForATR = {}\n')
    f.write('for i in range(len(expectedReaders)):\n')
    f.write('    expectedReaderForATR[toHexString(expectedATRs[i])] = ' + \
                    'expectedReaders[i]\n')

    f.write('expectedReaderGroups = [\'SCard$DefaultReaders\']\n')

    f.close()


if __name__ == '__main__':
    import sys
    checklocalconfig()
    sys.exit()

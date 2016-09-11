"""ATR class managing some of the Answer To Reset content.

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

from __future__ import print_function
from smartcard.Exceptions import SmartcardException
from smartcard.util import toHexString


class ATR(object):
    """ATR class."""

    clockrateconversion = [372, 372, 558, 744, 1116, 1488, 1860, 'RFU',
                           'RFU', 512, 768, 1024, 1536, 2048, 'RFU', 'RFU',
                           'RFU']
    bitratefactor = ['RFU', 1, 2, 4, 8, 16, 32, 'RFU', 12, 20, 'RFU',
                     'RFU', 'RFU', 'RFU', 'RFU', 'RFU']
    currenttable = [25, 50, 100, 'RFU']

    def __init__(self, bytes):
        """Construct a new atr from bytes."""
        self.bytes = bytes
        self.__initInstance__()

    def __checksyncbyte__(self):
        """Check validity of TS."""
        if not 0x3b == self.bytes[0] and not 0x03f == self.bytes[0]:
            raise SmartcardException("invalid TS 0x%-0.2x" % self.bytes[0])

    def __initInstance__(self):
        """
        Parse ATR and initialize members:
          - TS: initial character
          - T0: format character
          - TA[n], TB[n], TC[n], TD[n], for n=0,1,...: protocol parameters

        @note: protocol parameters indices start at 0, e.g.
        TA[0], TA[1] correspond to the ISO standard TA1, TA2
        parameters

          - historicalBytes: the ATR T1, T2, ..., TK historical bytes
          - TCK: checksum byte (only for protocols different from T=0)
          - FI: clock rate conversion factor
          - DI: voltage adjustment factor
          - PI1: programming voltage factor
          - II: maximum programming current factor
          - N: extra guard time
        """
        self.__checksyncbyte__()

        # initial character
        self.TS = self.bytes[0]

        # format character
        self.T0 = self.bytes[1]

        # count of historical bytes
        self.K = self.T0 & 0x0f

        # initialize optional characters lists
        self.TA = []
        self.TB = []
        self.TC = []
        self.TD = []
        self.Y = []
        self.hasTA = []
        self.hasTB = []
        self.hasTC = []
        self.hasTD = []

        TD = self.T0
        hasTD = 1
        n = 0
        offset = 1
        self.interfaceBytesCount = 0
        while hasTD:
            self.Y += [TD >> 4 & 0x0f]

            self.hasTD += [(self.Y[n] & 0x08) != 0]
            self.hasTC += [(self.Y[n] & 0x04) != 0]
            self.hasTB += [(self.Y[n] & 0x02) != 0]
            self.hasTA += [(self.Y[n] & 0x01) != 0]

            self.TA += [None]
            self.TB += [None]
            self.TC += [None]
            self.TD += [None]

            if self.hasTA[n]:
                self.TA[n] = self.bytes[offset + self.hasTA[n]]
            if self.hasTB[n]:
                self.TB[n] = self.bytes[offset + self.hasTA[n] + self.hasTB[n]]
            if self.hasTC[n]:
                self.TC[n] = self.bytes[offset +
                                        self.hasTA[n] +
                                        self.hasTB[n] +
                                        self.hasTC[n]]
            if self.hasTD[n]:
                self.TD[n] = self.bytes[offset +
                                        self.hasTA[n] +
                                        self.hasTB[n] +
                                        self.hasTC[n] +
                                        self.hasTD[n]]

            self.interfaceBytesCount += self.hasTA[n] +\
                self.hasTB[n] +\
                self.hasTC[n] +\
                self.hasTD[n]
            TD = self.TD[n]
            hasTD = self.hasTD[n]
            offset = offset + self.hasTA[n] + self.hasTB[n] +\
                self.hasTC[n] + self.hasTD[n]
            n = n + 1

        # historical bytes
        self.historicalBytes = self.bytes[offset + 1:offset + 1 + self.K]

        # checksum
        self.hasChecksum = (len(self.bytes) == offset + 1 + self.K + 1)
        if self.hasChecksum:
            self.TCK = self.bytes[-1]
            checksum = 0
            for b in self.bytes[1:]:
                checksum = checksum ^ b
            self.checksumOK = (checksum == 0)
        else:
            self.TCK = None

        # clock-rate conversion factor
        if self.hasTA[0]:
            self.FI = self.TA[0] >> 4 & 0x0f
        else:
            self.FI = None

        # bit-rate adjustment factor
        if self.hasTA[0]:
            self.DI = self.TA[0] & 0x0f
        else:
            self.DI = None

        # maximum programming current factor
        if self.hasTB[0]:
            self.II = self.TB[0] >> 5 & 0x03
        else:
            self.II = None

        # programming voltage factor
        if self.hasTB[0]:
            self.PI1 = self.TB[0] & 0x1f
        else:
            self.PI1 = None

        # extra guard time
        self.N = self.TC[0]

    def getChecksum(self):
        """Return the checksum of the ATR. Checksum is mandatory only
        for T=1."""
        return self.TCK

    def getHistoricalBytes(self):
        """Return historical bytes."""
        return self.historicalBytes

    def getHistoricalBytesCount(self):
        """Return count of historical bytes."""
        return len(self.historicalBytes)

    def getInterfaceBytesCount(self):
        """Return count of interface bytes."""
        return self.interfaceBytesCount

    def getTA1(self):
        """Return TA1 byte."""
        return self.TA[0]

    def getTB1(self):
        """Return TB1 byte."""
        return self.TB[0]

    def getTC1(self):
        """Return TC1 byte."""
        return self.TC[0]

    def getTD1(self):
        """Return TD1 byte."""
        return self.TD[0]

    def getBitRateFactor(self):
        """Return bit rate factor."""
        if self.DI is not None:
            return ATR.bitratefactor[self.DI]
        else:
            return 1

    def getClockRateConversion(self):
        """Return clock rate conversion."""
        if self.FI is not None:
            return ATR.clockrateconversion[self.FI]
        else:
            return 372

    def getProgrammingCurrent(self):
        """Return maximum programming current."""
        if self.II is not None:
            return ATR.currenttable[self.II]
        else:
            return 50

    def getProgrammingVoltage(self):
        """Return programming voltage."""
        if self.PI1 is not None:
            return 5 * (1 + self.PI1)
        else:
            return 5

    def getGuardTime(self):
        """Return extra guard time."""
        return self.N

    def getSupportedProtocols(self):
        """Returns a dictionnary of supported protocols."""
        protocols = {}
        for td in self.TD:
            if td is not None:
                strprotocol = "T=%d" % (td & 0x0F)
                protocols[strprotocol] = True
        if not self.hasTD[0]:
            protocols['T=0'] = True
        return protocols

    def isT0Supported(self):
        """Return True if T=0 is supported."""
        protocols = self.getSupportedProtocols()
        return 'T=0' in protocols

    def isT1Supported(self):
        """Return True if T=1 is supported."""
        protocols = self.getSupportedProtocols()
        return 'T=1' in protocols

    def isT15Supported(self):
        """Return True if T=15 is supported."""
        protocols = self.getSupportedProtocols()
        return 'T=15' in protocols

    def dump(self):
        """Dump the details of an ATR."""

        for i in range(0, len(self.TA)):
            if self.TA[i] is not None:
                print("TA%d: %x" % (i + 1, self.TA[i]))
            if self.TB[i] is not None:
                print("TB%d: %x" % (i + 1, self.TB[i]))
            if self.TC[i] is not None:
                print("TC%d: %x" % (i + 1, self.TC[i]))
            if self.TD[i] is not None:
                print("TD%d: %x" % (i + 1, self.TD[i]))

        print('supported protocols ' + ','.join(self.getSupportedProtocols()))
        print('T=0 supported: ' + str(self.isT0Supported()))
        print('T=1 supported: ' + str(self.isT1Supported()))

        if self.getChecksum():
            print('checksum: %d' % self.getChecksum())

        print('\tclock rate conversion factor: ' +
              str(self.getClockRateConversion()))
        print('\tbit rate adjustment factor: ' + str(self.getBitRateFactor()))

        print('\tmaximum programming current: ' +
              str(self.getProgrammingCurrent()))
        print('\tprogramming voltage: ' + str(self.getProgrammingVoltage()))

        print('\tguard time: ' + str(self.getGuardTime()))

        print('nb of interface bytes: %d' % self.getInterfaceBytesCount())
        print('nb of historical bytes: %d' % self.getHistoricalBytesCount())

    def __str__(self):
        """Returns a string representation of the ATR as a strem of bytes."""
        return toHexString(self.bytes)


if __name__ == '__main__':
    """Small sample illustrating the use of ATR."""

    atrs = [[0x3F, 0x65, 0x25, 0x00, 0x2C, 0x09, 0x69, 0x90, 0x00],
            [0x3F, 0x65, 0x25, 0x08, 0x93, 0x04, 0x6C, 0x90, 0x00],
            [0x3B, 0x16, 0x94, 0x7C, 0x03, 0x01, 0x00, 0x00, 0x0D],
            [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03],
            [0x3B, 0xE3, 0x00, 0xFF, 0x81, 0x31, 0x52, 0x45, 0xA1,
             0xA2, 0xA3, 0x1B],
            [0x3B, 0xE5, 0x00, 0x00, 0x81, 0x21, 0x45, 0x9C, 0x10,
             0x01, 0x00, 0x80, 0x0D]]

    for atr in atrs:
        a = ATR(atr)
        print(80 * '-')
        print(a)
        a.dump()
        print(toHexString(a.getHistoricalBytes()))

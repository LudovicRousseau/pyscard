"""ATR class managing some of the Answer To Reset content.

__author__ = "http://www.gemalto.com"

Copyright 2001-2007 gemalto
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

class ATR:

    clockrateconversion=[ 372, 372, 558, 744, 1116, 1488, 1860, 'RFU', 'RFU', 512, 768, 1024, 1536, 2048, 'RFU' ]
    bitratefactor=['RFU', 1, 2, 4, 8, 16, 32, 'RFU', 12, 20, 'RFU', 'RFU', 'RFU', 'RFU', 'RFU', 'RFU' ]
    currenttable=[ 25, 50, 'RFU', 'RFU' ]


    """ATR class."""
    def __init__( self, bytes ):
        """Construct a new atr from bytes."""
        self.bytes = bytes

    def __checksyncbyte__( self ):
        """Check validity of TS."""
        if not 0x3b==self.bytes[0] and not 0x03f==self.bytes[0]:
            raise 'invalid TS',"0x%-0.2x"%self.bytes[0]

    def getChecksum( self ):
        """Return the checksum of the ATR. Checksum is mandatory only for T=1."""
        self.__checksyncbyte__()
        # check for the presence of an historical byte
        # TS+T0+interface bytes+historical bytes [+checksum] =ATR
        atrlenwithouthcheckum = 2 + self.getHistoricalBytesCount() + self.getInterfaceBytesCount()
        if atrlenwithouthcheckum < len( self.bytes ):
            return reduce( lambda a, b: a^b, self.bytes[2:], self.bytes[1] )
        else:
            return None

    def getHistoricalBytes( self ):
        """Return historical bytes."""
        self.__checksyncbyte__()

        # count of historical bytes
        nbhistoricalbytes = self.bytes[1] & 0x0f

        # offset of historical bytes
        starthistoricalbytes = 2 + self.getInterfaceBytesCount()

        return self.bytes[starthistoricalbytes:starthistoricalbytes+nbhistoricalbytes]

    def getHistoricalBytesCount( self ):
        """Return count of historical bytes."""
        self.__checksyncbyte__()
        return self.bytes[1] & 0x0f


    def getInterfaceBytesCount( self ):
        """Return count of interface bytes."""
        self.__checksyncbyte__()
        countinterfacechars = 0

        # TA1, TB1, TC1, TD1
        # not not to account for 1 or 0
        hasTA = not not self.bytes[1] & 0x10
        hasTB = not not self.bytes[1] & 0x20
        hasTC = not not self.bytes[1] & 0x40
        hasTD = not not self.bytes[1] & 0x80
        countinterfacechars += hasTA + hasTB + hasTC + hasTD

        # TA2, TB2, TC2, TD2
        if hasTD:
            hasTA = not not self.bytes[countinterfacechars+1] & 0x10
            hasTB = not not self.bytes[countinterfacechars+1] & 0x20
            hasTC = not not self.bytes[countinterfacechars+1] & 0x40
            hasTD = not not self.bytes[countinterfacechars+1] & 0x80
            countinterfacechars += hasTA + hasTB + hasTC + hasTD

            # TAi, TBi, TCi, TDi
            for i in (1,2,3):
                if not hasTA and not hasTB and not hasTC and not hasTD:
                    break;
                if hasTD:
                    hasTA = not not self.bytes[countinterfacechars+1] & 0x10
                    hasTB = not not self.bytes[countinterfacechars+1] & 0x20
                    hasTC = not not self.bytes[countinterfacechars+1] & 0x40
                    hasTD = not not self.bytes[countinterfacechars+1] & 0x80
                    countinterfacechars += hasTA + hasTB + hasTC + hasTD
        return countinterfacechars


    def getTA1( self ):
        """Return TA1 byte."""
        self.__checksyncbyte__()
        if self.bytes[1] & 0x10:
            return self.bytes[2]
        else:
            return None

    def getTB1( self ):
        """Return TB1 byte."""
        self.__checksyncbyte__()
        if self.bytes[1] & 0x20:
            return self.bytes[3]
        else:
            return None

    def getTC1( self ):
        """Return TC1 byte."""
        self.__checksyncbyte__()
        if self.bytes[1] & 0x40:
            return self.bytes[4]
        else:
            return None

    def getTD1( self ):
        """Return TD1 byte."""
        self.__checksyncbyte__()
        if self.bytes[1] & 0x80:
            return self.bytes[5]
        else:
            return None

    def getBitRateFactor( self ):
        if self.bytes[1] & 0x10:
            return ATR.bitratefactor[ self.getTA1() & 0x0f]
        else:
            return 1

    def getClockRateConversion( self ):
        if self.bytes[1] & 0x10:
            return ATR.clockrateconversion[ (self.getTA1()>>4) & 0x0f ]
        else:
            return 372

    def getProgrammingCurrent( self ):
        if self.bytes[1] & 0x20:
            return ATR.currenttable[ (self.getTB1() >> 5) & 3]
        else:
            return 50

    def getProgrammingVoltage( self ):
        if self.bytes[1] & 0x20:
            return 5*((self.getTB1() & 0x1f)+1)
        else:
            return 5

    def getGuardTime( self ):
        if self.bytes[1] & 0x40:
            return self.getTC1()
        else:
            return 0

    def dump( self ):
        print 'checksum:', self.getChecksum()

        if self.getTA1():
            print 'TA: present'
            print '\tclock rate conversion factor:', self.getClockRateConversion()
            print '\tbit rate adjustment factor:', self.getBitRateFactor()

        if self.getTB1():
            print 'TB: present'
            print '\tmaximum programming current:', self.getProgrammingCurrent()
            print '\tprogramming voltage:', self.getProgrammingVoltage()

        if self.getTC1():
            print 'TC: present'
            print '\tguard time:', self.getGuardTime()

        print 'nb of interface bytes:', self.getInterfaceBytesCount()
        print 'nb of historical bytes:', self.getHistoricalBytesCount()



    def __str__( self ):
        return reduce( lambda a, b: a+"%-0.2X " % ((b+256)%256), self.bytes, '' )


if __name__ == '__main__':
    """Small sample illustrating the use of ATR."""

    atrs = [ [ 0x3F, 0x65, 0x25, 0x00, 0x2C, 0x09, 0x69, 0x90, 0x00 ],
             [ 0x3F, 0x65, 0x25, 0x08, 0x93, 0x04, 0x6C, 0x90, 0x00 ],
             [ 0x3B, 0x16, 0x94, 0x7C, 0x03, 0x01, 0x00, 0x00, 0x0D ],
             [ 0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03 ],
           ]

    for atr in atrs:
        a=ATR( atr )
        print 80*'-'
        print a
        a.dump()
        print reduce( lambda a, b: a+"%-0.2X " % ((b+256)%256), a.getHistoricalBytes(), '' )
















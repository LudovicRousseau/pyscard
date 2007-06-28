"""PCSCCardConnection class manages connections thru a PCSC reader.

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

from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.Observer import Observable

from smartcard.scard import *


class PCSCCardConnection( CardConnection ):
    """PCSCCard connection class. Handles connection with a card thru a PCSC reader."""

    def __init__( self, reader ):
        """Construct a new PCSC card connection.

        reader: the reader in which the smartcard to connect to is located.
        """
        CardConnection.__init__( self, reader )
        self.hcard = None
        hresult, self.hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
        if hresult!=0:
            raise CardConnectionException( 'Failed to establish context : ' + SCardGetErrorMessage(hresult) )

    def __del__( self ):
        """Destructor. Clean PCSC connection resources."""
        # race condition: module CardConnection
        # can disappear before __del__ is called
        self.disconnect()
        hresult = SCardReleaseContext( self.hcontext )
        if hresult!=0:
            raise CardConnectionException( 'Failed to release context: ' + SCardGetErrorMessage(hresult) )
        CardConnection.__del__( self )

    def connect( self, protocol=CardConnection.DEFAULT_protocol ):
        """Connect to the card. If protocol is not specified, connect with the default connection protocol
        set with CardConnection.setProtocol()."""
        CardConnection.connect( self, protocol )
        if CardConnection.DEFAULT_protocol==protocol:
            pcscprotocol = self.getProtocol()
        else:
            pcscprotocol = 0
            if CardConnection.T0_protocol & protocol:
                pcscprotocol |= SCARD_PROTOCOL_T0
            if CardConnection.T1_protocol & protocol:
                pcscprotocol |= SCARD_PROTOCOL_T1
            if 0==pcscprotocol:
                pcscprotocol = SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1

        hresult, self.hcard, dwActiveProtocol = SCardConnect(
            self.hcontext, str(self.reader), SCARD_SHARE_SHARED, pcscprotocol )
        if hresult!=0:
            self.hcard=None
            raise NoCardException( 'Unable to connect: ' + SCardGetErrorMessage(hresult) )

    def disconnect( self ):
        """Disconnect from the card."""

        # when __del__() is invoked in response to a module being deleted,
        # e.g., when execution of the program is done, other globals referenced
        # by the __del__() method may already have been deleted.
        # this causes CardConnection.disconnect to except with a TypeError
        try:
            CardConnection.disconnect( self )
        except TypeError:
            pass
        if None!=self.hcard:
            hresult = SCardDisconnect( self.hcard, SCARD_UNPOWER_CARD )
            if hresult!=0:
                raise CardConnectionException( 'Failed to disconnect: ' + SCardGetErrorMessage(hresult) )
            self.hcard = None

    def getATR( self ):
        """Return card ATR"""
        CardConnection.getATR( self )
        if None==self.hcard:
            raise CardConnectionException( 'Card not connected' )
        hresult, reader, state, protocol, atr = SCardStatus( self.hcard )
        if hresult!=0:
            raise CardConnectionException( 'Failed to get status: ' + SCardGetErrorMessage(hresult) )
        return atr

    def doTransmit( self, bytes, protocol=SCARD_PCI_T0 ):
        """Transmit an apdu to the card and return response apdu.

        bytes:      command apdu to transmit (list of bytes)

        protocol:   SCARD_PCI_T0 for T=0
                    SCARD_PCI_T1 for T=1
                    default if SCARD_PCI_T0 if protocol is not specified

        return:     a tuple (response, sw1, sw2) where
                    sw1 is status word 1, e.g. 0x90
                    sw2 is status word 2, e.g. 0x1A
                    response are the response bytes excluding status words
        """
        CardConnection.doTransmit( self, bytes, protocol )
        if CardConnection.T0_protocol==protocol:
            protocol=SCARD_PCI_T0
        if None==self.hcard:
            raise CardConnectionException( 'Card not connected' )
        hresult, response = SCardTransmit( self.hcard, protocol, bytes )
        if hresult!=0:
            raise CardConnectionException( 'Failed to transmit: ' + SCardGetErrorMessage(hresult) )

        sw1=(response[-2]+256)%256
        sw2=(response[-1]+256)%256

        data = map(lambda x: (x+256)%256, response[:-2])
        return data, sw1, sw2

if __name__ == '__main__':
    """Small sample illustrating the use of CardConnection."""
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]
    from smartcard.pcsc.PCSCReader import readers
    cc = readers()[0].createConnection()
    cc.connect()
    print "%r %x %x" % cc.transmit( SELECT + DF_TELECOM )











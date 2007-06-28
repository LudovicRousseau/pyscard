"""The CardConnection abstract class manages connections with a card and apdu transmission.

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

from smartcard.CardConnectionEvent import CardConnectionEvent
from smartcard.Exceptions import SmartcardException
from smartcard.Observer import Observer
from smartcard.Observer import Observable

class CardConnection(Observable):
    """Card connection abstract class.

    Known subclasses: smartcard.pcsc.PCSCCardConnection
    """
    DEFAULT_protocol=0x00
    T0_protocol=0x01
    T1_protocol=0x02

    def __init__( self, reader ):
        """Construct a new card connection.

        readerName: name of the reader in which the smartcard to connect to is located.
        """
        Observable.__init__(self)
        self.reader = reader
        self.errorcheckingchain=None
        self.defaultprotocol = CardConnection.T0_protocol

    def __del__( self ):
        """Connect to card."""
        pass

    def addSWExceptionToFilter( self, exClass ):
        """Add a status word exception class to be filtered.

        exClass: the class to filter, e.g. smartcard.sw.SWException.WarningProcessingException

        Filtered exceptions will not be raised when encountered in the
        error checking chain."""
        if None!=self.errorcheckingchain:
            self.errorcheckingchain[0].addFilterException( exClass )

    def addObserver(self, observer):
        """Add a CardConnection observer."""
        Observable.addObserver( self, observer )

    def deleteObserver(self, observer):
        """Remove a CardConnection observer."""
        Observable.deleteObserver( self, observer )

    def connect( self, protocol=DEFAULT_protocol ):
        """Connect to card.
        protocol: a bit mask of the protocols to use."""
        Observable.setChanged( self )
        Observable.notifyObservers( self, CardConnectionEvent('connect') )

    def disconnect( self ):
        """Disconnect from card."""
        Observable.setChanged( self )
        Observable.notifyObservers( self, CardConnectionEvent('disconnect') )

    def getATR( self ):
        """Return card ATR"""
        pass

    def getProtocol( self ):
        """Return bit mask for the protocol of connection, or None if no protocol set.
        The return value is a bit mask of of CardConnection.T0_protocol for T0 and CardConnection.T1_protocol for T1"""
        return self.defaultprotocol

    def getReader( self ):
        """Return card connection reader"""
        return self.reader

    def setErrorCheckingChain( self, errorcheckingchain ):
        """Add an error checking chain.
        errorcheckingchain: a smartcard.sw.ErrorCheckingChain object
        The error checking strategies in errorchecking chain will be tested
        with each received response APDU, and a smartcard.sw.SWException.SWException
        will be raised upon error."""
        self.errorcheckingchain=errorcheckingchain

    def setProtocol( self, protocol ):
        """Set protocol for card connection.
        protocol: a bit mask of CardConnection.T0_protocol for T0 and CardConnection.T1_protocol for T1
        e.g. setProtocol( CardConnection.T0_protocol) or setProtocol( CardConnection.T1_protocol | CardConnection.T0_protocol )
        """
        self.defaultprotocol = protocol

    def transmit( self, bytes, protocol=T0_protocol ):
        """Transmit an apdu. Internally calls doTransmit() class method and notify observers
        upon command/response APDU events.
        Subclasses must override the doTransmit() class method.

        bytes:      list of bytes to transmit
        protocol:   T0_protocol for T=0 protocol (default); T1_protocol for T=1 protocol
        """
        Observable.setChanged( self )
        Observable.notifyObservers( self, CardConnectionEvent('command', [bytes, protocol] ) )
        data, sw1, sw2 = self.doTransmit( bytes, protocol )
        Observable.setChanged( self )
        Observable.notifyObservers( self, CardConnectionEvent( 'response', [data, sw1, sw2 ] ) )
        if None!=self.errorcheckingchain:
            self.errorcheckingchain[0]( data, sw1, sw2 )
        return data, sw1, sw2

    def doTransmit( self, bytes, protocol ):
        """Performs the command APDU transmission.

        Subclasses must override this method for implementing apdu transmission."""
        pass













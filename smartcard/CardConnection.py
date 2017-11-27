"""The CardConnection abstract class manages connections with a card and
apdu transmission.

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

from smartcard.CardConnectionEvent import CardConnectionEvent
from smartcard.Observer import Observable


class CardConnection(Observable):
    """Card connection abstract class.

    Known subclasses: smartcard.pcsc.PCSCCardConnection
    """
    T0_protocol = 0x00000001
    T1_protocol = 0x00000002
    RAW_protocol = 0x00010000
    T15_protocol = 0x00000008

    def __init__(self, reader):
        """Construct a new card connection.

        @param reader: name of the reader in which the smartcard to connect
        to is located.
        """
        Observable.__init__(self)
        self.reader = reader
        self.errorcheckingchain = None
        self.defaultprotocol = CardConnection.T0_protocol |\
            CardConnection.T1_protocol

    def __del__(self):
        """Connect to card."""
        pass

    def addSWExceptionToFilter(self, exClass):
        """Add a status word exception class to be filtered.

        @param exClass: the class to filter, e.g.
        L{smartcard.sw.SWException.WarningProcessingException}

        Filtered exceptions will not be raised when encountered in the
        error checking chain."""
        if self.errorcheckingchain is not None:
            self.errorcheckingchain[0].addFilterException(exClass)

    def addObserver(self, observer):
        """Add a CardConnection observer."""
        Observable.addObserver(self, observer)

    def deleteObserver(self, observer):
        """Remove a CardConnection observer."""
        Observable.deleteObserver(self, observer)

    def connect(self, protocol=None, mode=None, disposition=None):
        """Connect to card.
        @param protocol: a bit mask of the protocols to use, from
        L{CardConnection.T0_protocol}, L{CardConnection.T1_protocol},
        L{CardConnection.RAW_protocol}, L{CardConnection.T15_protocol}

        @param mode: SCARD_SHARE_SHARED (default), SCARD_SHARE_EXCLUSIVE or
        SCARD_SHARE_DIRECT

        @param disposition: SCARD_LEAVE_CARD (default), SCARD_RESET_CARD,
        SCARD_UNPOWER_CARD or SCARD_EJECT_CARD
        """
        Observable.setChanged(self)
        Observable.notifyObservers(self, CardConnectionEvent('connect'))

    def disconnect(self):
        """Disconnect from card."""
        Observable.setChanged(self)
        Observable.notifyObservers(self, CardConnectionEvent('disconnect'))

    def getATR(self):
        """Return card ATR"""
        pass

    def getProtocol(self):
        """Return bit mask for the protocol of connection, or None if no
        protocol set.  The return value is a bit mask of
        CardConnection.T0_protocol, CardConnection.T1_protocol,
        CardConnection.RAW_protocol, CardConnection.T15_protocol
        """
        return self.defaultprotocol

    def getReader(self):
        """Return card connection reader"""
        return self.reader

    def setErrorCheckingChain(self, errorcheckingchain):
        """Add an error checking chain.
        @param errorcheckingchain: a smartcard.sw.ErrorCheckingChain object The
        error checking strategies in errorchecking chain will be tested
        with each received response APDU, and a
        smartcard.sw.SWException.SWException will be raised upon
        error."""
        self.errorcheckingchain = errorcheckingchain

    def setProtocol(self, protocol):
        """Set protocol for card connection.
        @param protocol: a bit mask of CardConnection.T0_protocol,
        CardConnection.T1_protocol, CardConnection.RAW_protocol,
        CardConnection.T15_protocol e.g.
        setProtocol(CardConnection.T1_protocol |
        CardConnection.T0_protocol) """
        self.defaultprotocol = protocol

    def transmit(self, bytes, protocol=None):
        """Transmit an apdu. Internally calls doTransmit() class method
        and notify observers upon command/response APDU events.
        Subclasses must override the doTransmit() class method.

        @param bytes:      list of bytes to transmit

        @param protocol:   the transmission protocol, from
                    CardConnection.T0_protocol,
                    CardConnection.T1_protocol, or
                    CardConnection.RAW_protocol
        """
        Observable.setChanged(self)
        Observable.notifyObservers(self,
                                   CardConnectionEvent(
                                       'command',
                                       [bytes, protocol]))
        data, sw1, sw2 = self.doTransmit(bytes, protocol)
        Observable.setChanged(self)
        Observable.notifyObservers(self,
                                   CardConnectionEvent(
                                       'response',
                                       [data, sw1, sw2]))
        if self.errorcheckingchain is not None:
            self.errorcheckingchain[0](data, sw1, sw2)
        return data, sw1, sw2

    def doTransmit(self, bytes, protocol):
        """Performs the command APDU transmission.

        Subclasses must override this method for implementing apdu
        transmission."""
        pass

    def control(self, controlCode, bytes=[]):
        """Send a control command and buffer.  Internally calls doControl()
        class method and notify observers upon command/response events.
        Subclasses must override the doControl() class method.

        @param controlCode: command code

        @param bytes:       list of bytes to transmit
        """
        Observable.setChanged(self)
        Observable.notifyObservers(self,
                                   CardConnectionEvent(
                                       'command',
                                       [controlCode, bytes]))
        data = self.doControl(controlCode, bytes)
        Observable.setChanged(self)
        Observable.notifyObservers(self,
                                   CardConnectionEvent(
                                       'response',
                                       data))
        if self.errorcheckingchain is not None:
            self.errorcheckingchain[0](data)
        return data

    def doControl(self, controlCode, bytes):
        """Performs the command control.

        Subclasses must override this method for implementing control."""
        pass

    def getAttrib(self, attribId):
        """return the requested attribute

        @param attribId: attribute id like SCARD_ATTR_VENDOR_NAME
        """
        Observable.setChanged(self)
        Observable.notifyObservers(self,
                                   CardConnectionEvent(
                                       'attrib',
                                       [attribId]))
        data = self.doGetAttrib(attribId)
        if self.errorcheckingchain is not None:
            self.errorcheckingchain[0](data)
        return data

    def doGetAttrib(self, attribId):
        """Performs the command get attrib.

        Subclasses must override this method for implementing get attrib."""
        pass

    def __enter__(self):
        """Enter the runtime context.
        """
        return self

    def __exit__(self, type, value, traceback):
        """Exit the runtime context trying to disconnect.
        """
        self.disconnect()

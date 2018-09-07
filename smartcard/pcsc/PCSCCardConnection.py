"""PCSCCardConnection class manages connections thru a PCSC reader.

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
from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import (CardConnectionException,
    NoCardException, SmartcardException)

from smartcard.scard import *


def translateprotocolmask(protocol):
    """Translate CardConnection protocol mask into PCSC protocol mask."""
    pcscprotocol = 0
    if None != protocol:
        if CardConnection.T0_protocol & protocol:
            pcscprotocol |= SCARD_PROTOCOL_T0
        if CardConnection.T1_protocol & protocol:
            pcscprotocol |= SCARD_PROTOCOL_T1
        if CardConnection.RAW_protocol & protocol:
            pcscprotocol |= SCARD_PROTOCOL_RAW
        if CardConnection.T15_protocol & protocol:
            pcscprotocol |= SCARD_PROTOCOL_T15
    return pcscprotocol


def translateprotocolheader(protocol):
    """Translate protocol into PCSC protocol header."""
    pcscprotocol = 0
    if None != protocol:
        if CardConnection.T0_protocol == protocol:
            pcscprotocol = SCARD_PCI_T0
        if CardConnection.T1_protocol == protocol:
            pcscprotocol = SCARD_PCI_T1
        if CardConnection.RAW_protocol == protocol:
            pcscprotocol = SCARD_PCI_RAW
    return pcscprotocol

dictProtocolHeader = {SCARD_PCI_T0: 'T0', SCARD_PCI_T1: 'T1',
    SCARD_PCI_RAW: 'RAW'}
dictProtocol = {SCARD_PROTOCOL_T0: 'T0', SCARD_PROTOCOL_T1: 'T1',
    SCARD_PROTOCOL_RAW: 'RAW', SCARD_PROTOCOL_T15: 'T15',
    SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1: 'T0 or T1'}


class PCSCCardConnection(CardConnection):
    """PCSCCard connection class. Handles connection with a card thru a
    PCSC reader."""

    def __init__(self, reader):
        """Construct a new PCSC card connection.

        reader: the reader in which the smartcard to connect to is located.
        """
        CardConnection.__init__(self, reader)
        self.hcard = None
        hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != 0:
            raise CardConnectionException(
                'Failed to establish context : ' + \
                SCardGetErrorMessage(hresult))

    def __del__(self):
        """Destructor. Clean PCSC connection resources."""
        # race condition: module CardConnection
        # can disappear before __del__ is called
        self.disconnect()
        hresult = SCardReleaseContext(self.hcontext)
        if hresult != 0:
            raise CardConnectionException(
                'Failed to release context: ' + \
                SCardGetErrorMessage(hresult))
        CardConnection.__del__(self)

    def connect(self, protocol=None, mode=None, disposition=None):
        """Connect to the card.

        If protocol is not specified, connect with the default
        connection protocol.

        If mode is not specified, connect with SCARD_SHARE_SHARED."""
        CardConnection.connect(self, protocol)
        pcscprotocol = translateprotocolmask(protocol)
        if 0 == pcscprotocol:
            pcscprotocol = self.getProtocol()

        if mode == None:
            mode = SCARD_SHARE_SHARED

        # store the way to dispose the card
        if disposition == None:
            disposition = SCARD_UNPOWER_CARD
        self.disposition = disposition

        hresult, self.hcard, dwActiveProtocol = SCardConnect(
            self.hcontext, str(self.reader), mode, pcscprotocol)
        if hresult != 0:
            self.hcard = None
            if hresult in (SCARD_W_REMOVED_CARD, SCARD_E_NO_SMARTCARD):
                raise NoCardException('Unable to connect', hresult=hresult)
            else:
                raise CardConnectionException(
                    'Unable to connect with protocol: ' + \
                    dictProtocol[pcscprotocol] + '. ' + \
                    SCardGetErrorMessage(hresult))

        protocol = 0
        if dwActiveProtocol == SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1:
            # special case for T0 | T1
            # this happen when mode=SCARD_SHARE_DIRECT and no protocol is
            # then negociated with the card
            protocol = CardConnection.T0_protocol | CardConnection.T1_protocol
        else:
            for p in dictProtocol:
                if p == dwActiveProtocol:
                    protocol = eval("CardConnection.%s_protocol" % dictProtocol[p])
        PCSCCardConnection.setProtocol(self, protocol)

    def disconnect(self):
        """Disconnect from the card."""

        # when __del__() is invoked in response to a module being deleted,
        # e.g., when execution of the program is done, other globals referenced
        # by the __del__() method may already have been deleted.
        # this causes CardConnection.disconnect to except with a TypeError
        try:
            CardConnection.disconnect(self)
        except TypeError:
            pass
        if None != self.hcard:
            hresult = SCardDisconnect(self.hcard, self.disposition)
            if hresult != 0:
                raise CardConnectionException(
                    'Failed to disconnect: ' + \
                    SCardGetErrorMessage(hresult))
            self.hcard = None

    def getATR(self):
        """Return card ATR"""
        CardConnection.getATR(self)
        if None == self.hcard:
            raise CardConnectionException('Card not connected')
        hresult, reader, state, protocol, atr = SCardStatus(self.hcard)
        if hresult != 0:
            raise CardConnectionException(
                'Failed to get status: ' + \
                SCardGetErrorMessage(hresult))
        return atr

    def doTransmit(self, bytes, protocol=None):
        """Transmit an apdu to the card and return response apdu.

        @param bytes:    command apdu to transmit (list of bytes)

        @param protocol: the transmission protocol, from
            CardConnection.T0_protocol, CardConnection.T1_protocol, or
            CardConnection.RAW_protocol

        @return:     a tuple (response, sw1, sw2) where
                    sw1 is status word 1, e.g. 0x90
                    sw2 is status word 2, e.g. 0x1A
                    response are the response bytes excluding status words
        """
        if None == protocol:
            protocol = self.getProtocol()
        CardConnection.doTransmit(self, bytes, protocol)
        pcscprotocolheader = translateprotocolheader(protocol)
        if 0 == pcscprotocolheader:
            raise CardConnectionException(
                'Invalid protocol in transmit: must be ' + \
                'CardConnection.T0_protocol, ' + \
                'CardConnection.T1_protocol, or ' + \
                'CardConnection.RAW_protocol')
        if None == self.hcard:
            raise CardConnectionException('Card not connected')
        hresult, response = SCardTransmit(
            self.hcard, pcscprotocolheader, bytes)
        if hresult != 0:
            raise CardConnectionException(
                'Failed to transmit with protocol ' + \
                dictProtocolHeader[pcscprotocolheader] + '. ' + \
                SCardGetErrorMessage(hresult))

        sw1 = (response[-2] + 256) % 256
        sw2 = (response[-1] + 256) % 256

        data = [(x + 256) % 256 for x in response[:-2]]
        return list(data), sw1, sw2

    def doControl(self, controlCode, bytes=[]):
        """Transmit a control command to the reader and return response.

        controlCode: control command

        bytes:       command data to transmit (list of bytes)

        return:      response are the response bytes (if any)
        """
        CardConnection.doControl(self, controlCode, bytes)
        hresult, response = SCardControl(self.hcard, controlCode, bytes)
        if hresult != 0:
            raise SmartcardException(
                'Failed to control ' + SCardGetErrorMessage(hresult))

        data = [(x + 256) % 256 for x in response]
        return list(data)

    def doGetAttrib(self, attribId):
        """get an attribute

        attribId: Identifier for the attribute to get

        return:   response are the attribute byte array
        """
        CardConnection.doGetAttrib(self, attribId)
        hresult, response = SCardGetAttrib(self.hcard, attribId)
        if hresult != 0:
            raise SmartcardException(
                'Failed to getAttrib ' + SCardGetErrorMessage(hresult))
        return response


if __name__ == '__main__':
    """Small sample illustrating the use of CardConnection."""
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]
    from smartcard.pcsc.PCSCReader import PCSCReader
    from smartcard.pcsc.PCSCPart10 import CM_IOCTL_GET_FEATURE_REQUEST
    cc = PCSCReader.readers()[0].createConnection()
    cc.connect()
    print("%r %x %x" % cc.transmit(SELECT + DF_TELECOM))

    print(cc.control(CM_IOCTL_GET_FEATURE_REQUEST, []))


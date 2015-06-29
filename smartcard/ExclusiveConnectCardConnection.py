"""CardConnectionDecorator that provides exclusive use of a card.

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
from smartcard.CardConnection import CardConnection
from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.Exceptions import CardConnectionException
from smartcard.scard import SCardConnect, SCardDisconnect
from smartcard.scard import SCARD_LEAVE_CARD, SCARD_SHARE_EXCLUSIVE
from smartcard.scard import SCardGetErrorMessage
from smartcard.pcsc import PCSCCardConnection
import smartcard.pcsc


class ExclusiveConnectCardConnection(CardConnectionDecorator):
    '''This decorator uses exclusive access to the card during
    connection to prevent other processes to connect to this card.'''

    def __init__(self, cardconnection):
        CardConnectionDecorator.__init__(self, cardconnection)

    def connect(self, protocol=None, mode=None, disposition=None):
        '''Disconnect and reconnect in exclusive mode PCSCCardconnections.'''
        CardConnectionDecorator.connect(self, protocol, mode, disposition)
        component = self.component
        while True:
            if isinstance(
                component,
                smartcard.pcsc.PCSCCardConnection.PCSCCardConnection):
                pcscprotocol = PCSCCardConnection.translateprotocolmask(
                    protocol)
                if 0 == pcscprotocol:
                    pcscprotocol = component.getProtocol()

                if None != component.hcard:
                    hresult = SCardDisconnect(component.hcard,
                                              SCARD_LEAVE_CARD)
                    if hresult != 0:
                        raise CardConnectionException('Failed to disconnect: '
                            + SCardGetErrorMessage(hresult))
                hresult, component.hcard, dwActiveProtocol = SCardConnect(
                    component.hcontext, str(component.reader),
                    SCARD_SHARE_EXCLUSIVE, pcscprotocol)
                if hresult != 0:
                    raise CardConnectionException(
                        'Failed to connect with SCARD_SHARE_EXCLUSIVE' +\
                        SCardGetErrorMessage(hresult))
                # print 'reconnected exclusive'
                break
            if hasattr(component, 'component'):
                component = component.component
            else:
                break

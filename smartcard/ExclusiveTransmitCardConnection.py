"""Sample CardConnectionDecorator that provides exclusive transmit()

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
from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.Exceptions import CardConnectionException
from smartcard.scard import SCardBeginTransaction, SCardEndTransaction
from smartcard.scard import SCARD_LEAVE_CARD
from smartcard.scard import SCardGetErrorMessage
import smartcard.pcsc


class ExclusiveTransmitCardConnection(CardConnectionDecorator):
    '''This decorator uses SCardBeginTransaction/SCardEndTransaction to
    preserve other processes of threads to access the card during
    transmit().'''

    def __init__(self, cardconnection):
        CardConnectionDecorator.__init__(self, cardconnection)

    def lock(self):
        '''Lock card with SCardBeginTransaction.'''

        component = self.component
        while True:
            if isinstance(
                    component,
                    smartcard.pcsc.PCSCCardConnection.PCSCCardConnection):
                hresult = SCardBeginTransaction(component.hcard)
                if 0 != hresult:
                    raise CardConnectionException(
                        'Failed to lock with SCardBeginTransaction: ' +
                        SCardGetErrorMessage(hresult))
                else:
                    # print('locked')
                    pass
                break
            if hasattr(component, 'component'):
                component = component.component
            else:
                break

    def unlock(self):
        '''Unlock card with SCardEndTransaction.'''
        component = self.component
        while True:
            if isinstance(
                    component,
                    smartcard.pcsc.PCSCCardConnection.PCSCCardConnection):
                hresult = SCardEndTransaction(component.hcard,
                                              SCARD_LEAVE_CARD)
                if 0 != hresult:
                    raise CardConnectionException(
                        'Failed to unlock with SCardEndTransaction: ' +
                        SCardGetErrorMessage(hresult))
                else:
                    # print('unlocked')
                    pass
                break
            if hasattr(component, 'component'):
                component = component.component
            else:
                break

    def transmit(self, bytes, protocol=None):
        '''Gain exclusive access to card during APDU transmission for if this
        decorator decorates a PCSCCardConnection.'''
        data, sw1, sw2 = CardConnectionDecorator.transmit(
            self, bytes, protocol)
        return data, sw1, sw2

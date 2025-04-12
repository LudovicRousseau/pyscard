#! /usr/bin/env python3
"""
Sample script that illustrates card connection decorators.

__author__ = "https://www.gemalto.com/"

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
from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.util import toHexString

# define two custom CardConnectionDecorator
# the decorators are very simple, just to illustrate
# shortly how several decorators can be added to the
# card connection


class SecureChannelConnection(CardConnectionDecorator):
    """This decorator is a mockup of secure channel connection.
    It merely pretends to cypher/uncypher upon apdu transmission."""

    def __init__(self, cardconnection):
        CardConnectionDecorator.__init__(self, cardconnection)

    def cypher(self, data):
        """Cypher mock-up; you would include the secure channel logics here."""
        print("cyphering", toHexString(data))
        return data

    def uncypher(self, data):
        """Uncypher mock-up;
        you would include the secure channel logics here."""
        print("uncyphering", toHexString(data))
        return data

    def transmit(self, command, protocol=None):
        """Cypher/uncypher APDUs before transmission"""
        cypheredbytes = self.cypher(command)
        data, sw1, sw2 = CardConnectionDecorator.transmit(self, cypheredbytes, protocol)
        if [] != data:
            data = self.uncypher(data)
        return data, sw1, sw2


class FakeATRConnection(CardConnectionDecorator):
    """This decorator changes the fist byte of the ATR. This is just an example
    to show that decorators can be nested."""

    def __init__(self, cardconnection):
        CardConnectionDecorator.__init__(self, cardconnection)

    def getATR(self):
        """Replace first BYTE of ATR by 3F"""
        atr = CardConnectionDecorator.getATR(self)
        return [0x3F] + atr[1:]


# define the apdus used in this script
GET_RESPONSE = [0xA0, 0xC0, 00, 00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


# request any card type
cardtype = AnyCardType()
cardrequest = CardRequest(timeout=1.5, cardType=cardtype)
with cardrequest.waitforcard() as cardservice:

    # attach the console tracer
    observer = ConsoleCardConnectionObserver()
    cardservice.connection.addObserver(observer)

    # attach our decorator
    cardservice.connection = FakeATRConnection(
        SecureChannelConnection(cardservice.connection)
    )

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    print("ATR", toHexString(cardservice.connection.getATR()))

    apdu = SELECT + DF_TELECOM
    response, sw1, sw2 = cardservice.connection.transmit(apdu)

    if sw1 == 0x9F:
        apdu = GET_RESPONSE + [sw2]
        response, sw1, sw2 = cardservice.connection.transmit(apdu)

    cardservice.connection.disconnect()
    cardservice.connection.release()

import sys

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

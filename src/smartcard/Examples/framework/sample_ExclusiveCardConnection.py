#! /usr/bin/env python3
"""
Sample script that illustrates exclusive card connection decorators.

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
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.ExclusiveConnectCardConnection import ExclusiveConnectCardConnection
from smartcard.ExclusiveTransmitCardConnection import ExclusiveTransmitCardConnection
from smartcard.util import toHexString

# define the apdus used in this script
GET_RESPONSE = [0xA0, 0xC0, 00, 00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]

# request any card type
cardtype = AnyCardType()
cardrequest = CardRequest(timeout=5, cardType=cardtype)
cardservice = cardrequest.waitforcard()

# attach the console tracer
observer = ConsoleCardConnectionObserver()
cardservice.connection.addObserver(observer)

# attach our decorator
cardservice.connection = ExclusiveTransmitCardConnection(
    ExclusiveConnectCardConnection(cardservice.connection)
)

# connect to the card and perform a few transmits
cardservice.connection.connect()

print("ATR", toHexString(cardservice.connection.getATR()))

try:
    # lock for initiating transaction
    cardservice.connection.lock()

    apdu = SELECT + DF_TELECOM
    response, sw1, sw2 = cardservice.connection.transmit(apdu)

    if sw1 == 0x9F:
        apdu = GET_RESPONSE + [sw2]
        response, sw1, sw2 = cardservice.connection.transmit(apdu)
finally:
    # unlock connection at the end of the transaction
    cardservice.connection.unlock()

    cardservice.connection.disconnect()
    cardservice.connection.release()

import sys

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

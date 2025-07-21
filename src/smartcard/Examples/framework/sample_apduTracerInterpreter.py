#! /usr/bin/env python3

# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

"""
Sample script that defines a custom card connection observer.

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

import sys

from smartcard.CardConnectionObserver import CardConnectionObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.util import toHexString


class TracerAndSELECTInterpreter(CardConnectionObserver):
    """This observer will interprer SELECT and GET RESPONSE bytes
    and replace them with a human readable string."""

    def update(self, observable, arg):

        if "connect" == arg.type:
            print("connecting to " + observable.getReader())

        elif "disconnect" == arg.type:
            print("disconnecting from " + observable.getReader())

        elif "release" == arg.type:
            print("release from " + observable.getReader())

        elif "command" == arg.type:
            str = toHexString(arg.args[0])
            str = str.replace("A0 A4 00 00 02", "SELECT")
            str = str.replace("A0 C0 00 00", "GET RESPONSE")
            print(">", str)

        elif "response" == arg.type:
            if [] == arg.args[0]:
                print("<  []", "%-2X %-2X" % tuple(arg.args[-2:]))
            else:
                print(
                    "<",
                    toHexString(arg.args[0]),
                    "%-2X %-2X" % tuple(arg.args[-2:]),
                )

        else:
            print("Unknown event:", arg.type)


# define the apdus used in this script
GET_RESPONSE = [0xA0, 0xC0, 00, 00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


# we request any type and wait for 10s for card insertion
cardtype = AnyCardType()
cardrequest = CardRequest(timeout=10, cardType=cardtype)
cardservice = cardrequest.waitforcard()

# create an instance of our observer and attach to the connection
observer = TracerAndSELECTInterpreter()
cardservice.connection.addObserver(observer)


# connect and send APDUs
# the observer will trace on the console
cardservice.connection.connect()

apdu = SELECT + DF_TELECOM
response, sw1, sw2 = cardservice.connection.transmit(apdu)
if sw1 == 0x9F:
    apdu = GET_RESPONSE + [sw2]
    response, sw1, sw2 = cardservice.connection.transmit(apdu)
else:
    print("no DF_TELECOM")

cardservice.connection.disconnect()
cardservice.connection.release()

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

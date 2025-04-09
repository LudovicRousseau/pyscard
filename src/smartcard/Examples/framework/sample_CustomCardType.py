#! /usr/bin/env python3
"""
Sample script that demonstrates how to create a custom CardType.

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
from smartcard.CardRequest import CardRequest
from smartcard.CardType import CardType
from smartcard.util import toHexString


class DCCardType(CardType):
    # define our custom CardType
    # this card type defines direct convention card
    # (first atr byte equal to 0x3b)

    def matches(self, atr, reader=None):
        return atr[0] == 0x3B


# request a direct convention card
cardtype = DCCardType()
cardrequest = CardRequest(timeout=1, cardType=cardtype)
with cardrequest.waitforcard() as cardservice:

    # connect and print atr and reader
    cardservice.connection.connect()
    print(toHexString(cardservice.connection.getATR()))
    print(cardservice.connection.getReader())


import sys

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

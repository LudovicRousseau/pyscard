#! /usr/bin/env python3
"""Sample script for APDU error checking.

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
from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
from smartcard.sw.ISO7816_9ErrorChecker import ISO7816_9ErrorChecker
from smartcard.sw.SWExceptions import SWException, WarningProcessingException

# define the apdus used in this script
GET_RESPONSE = [0xA0, 0xC0, 00, 00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


if __name__ == "__main__":

    print("Insert a card within 10 seconds")
    print("Cards without a DF_TELECOM will except")

    # request any card type
    cardtype = AnyCardType()
    cardrequest = CardRequest(timeout=10, cardType=cardtype)
    cardservice = cardrequest.waitforcard()

    # use ISO7816-4 and ISO7816-8 error checking strategy
    # first check iso7816_8 errors, then iso7816_4 errors
    errorchain = []
    errorchain = [ErrorCheckingChain(errorchain, ISO7816_9ErrorChecker())]
    errorchain = [ErrorCheckingChain(errorchain, ISO7816_8ErrorChecker())]
    errorchain = [ErrorCheckingChain(errorchain, ISO7816_4ErrorChecker())]
    cardservice.connection.setErrorCheckingChain(errorchain)

    # filter Warning Processing Exceptions (sw1 = 0x62 or 0x63)
    cardservice.connection.addSWExceptionToFilter(WarningProcessingException)

    # attach the console tracer
    observer = ConsoleCardConnectionObserver()
    cardservice.connection.addObserver(observer)

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    try:
        apdu = SELECT + DF_TELECOM
        response, sw1, sw2 = cardservice.connection.transmit(apdu)

        if sw1 == 0x9F:
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = cardservice.connection.transmit(apdu)

    except SWException as e:
        print(str(e))

    cardservice.connection.disconnect()
    cardservice.connection.release()

    import sys

    if "win32" == sys.platform:
        print("press Enter to continue")
        sys.stdin.read(1)

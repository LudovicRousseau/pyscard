#! /usr/bin/env python3
"""
Sample script that monitors smartcard insertion/removal and select
DF_TELECOM on inserted cards

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

from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

# define the apdus used in this script
GET_RESPONSE = [0xA0, 0xC0, 00, 00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


# a simple card observer that tries to select DF_TELECOM on an inserted card
class selectDFTELECOMObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def __init__(self):
        self.observer = ConsoleCardConnectionObserver()

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            apdu = SELECT + DF_TELECOM
            response, sw1, sw2 = card.connection.transmit(apdu)
            if sw1 == 0x9F:
                apdu = GET_RESPONSE + [sw2]
                response, sw1, sw2 = card.connection.transmit(apdu)
            card.connection.disconnect()
            card.connection.release()

        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))


if __name__ == "__main__":
    print("Insert or remove a SIM card in the system.")
    print("This program will exit in 60 seconds")
    print("")
    cardmonitor = CardMonitor()
    selectobserver = selectDFTELECOMObserver()
    cardmonitor.addObserver(selectobserver)

    sleep(60)

    # don't forget to remove observer, or the
    # monitor will poll forever...
    cardmonitor.deleteObserver(selectobserver)

    import sys

    if "win32" == sys.platform:
        print("press Enter to continue")
        sys.stdin.read(1)

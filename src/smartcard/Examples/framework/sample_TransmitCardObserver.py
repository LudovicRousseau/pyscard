#! /usr/bin/env python3
"""
Sample script that monitors card insertions,
connects to cards and transmit an apdu

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

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

# replace by your favourite apdu
SELECT_DF_TELECOM = [0xA0, 0xA4, 0x00, 0x00, 0x02, 0x7F, 0x10]


class transmitobserver(CardObserver):
    """A card observer that is notified when cards are inserted/removed
    from the system, connects to cards and SELECT DF_TELECOM"""

    def __init__(self):
        self.cards = []

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            if card not in self.cards:
                self.cards += [card]
                print("+Inserted: ", toHexString(card.atr))
                card.connection = card.createConnection()
                card.connection.connect()
                response, sw1, sw2 = card.connection.transmit(SELECT_DF_TELECOM)
                print(f"{sw1:02x} {sw2:02x}")
                card.connection.disconnect()
                card.connection.release()

        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))
            if card in self.cards:
                self.cards.remove(card)


if __name__ == "__main__":
    print("Insert or remove a smartcard in the system.")
    print("This program will exit in 100 seconds")
    print("")
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver(cardobserver)

    sleep(100)

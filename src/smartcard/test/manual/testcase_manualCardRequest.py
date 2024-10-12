#! /usr/bin/env python3
"""Manual unit tests for smartcard.CardRequest

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

import random
import time
import unittest

from smartcard.Card import Card
from smartcard.CardMonitoring import CardObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType, ATRCardType
from smartcard.Exceptions import (
    CardConnectionException,
    CardRequestTimeoutException,
    NoCardException,
)
from smartcard.System import readers
from smartcard.util import toHexString


def get_cards(readers):
    """return all the cards"""
    cards = []
    for reader in readers:
        try:
            c = reader.createConnection()
            c.connect()
            cards.append(Card(reader.name, c.getATR()))
            c.disconnect()
        except NoCardException:
            pass
    return cards


#
# setup test first: detect current readers and cards
#
print("insert two smartcard readers")
while True:
    readerz = readers()
    if 2 <= len(readerz):
        break
    time.sleep(0.3)
for reader in readerz:
    print("\t", reader)

print("insert two cards in the readers")
cardz = get_cards(readerz)
cardrequest = CardRequest(timeout=None)
while len(cardz) < 2:
    cardz = cardrequest.waitforcardevent()
for card in cardz:
    print("\t", toHexString(card.atr))


class testcase_manualCardRequest(unittest.TestCase, CardObserver):
    """Test case for CardRequest."""

    def removeAllCards(self):
        """Wait for no card present"""
        print("please remove all inserted smart cards")
        cardz = get_cards(readerz)
        cardrequest = CardRequest(timeout=None)
        while len(cardz) > 0:
            cardz = cardrequest.waitforcardevent()
        print("ok")

    def testcase_CardRequestNewCardAnyCardTypeInfiniteTimeOut(self):
        """Test smartcard.CardRequest for any new card without time-out."""

        self.removeAllCards()
        cardtype = AnyCardType()
        cardrequest = CardRequest(timeout=None, cardType=cardtype, newcardonly=True)
        print("re-insert any combination of cards six time")
        count = 0
        for _ in range(0, 6):
            cardservice = cardrequest.waitforcard()
            try:
                cardservice.connection.connect()
                print(
                    toHexString(cardservice.connection.getATR()),
                    "in",
                    cardservice.connection.getReader(),
                )
            except CardConnectionException:
                # card was removed too fast
                pass
            cardservice.connection.disconnect()
            count += 1
        self.assertEqual(6, count)

    def testcase_CardRequestNewCardATRCardTypeInfiniteTimeOut(self):
        """Test smartcard.CardRequest for new card with given ATR
        without time-out."""

        self.removeAllCards()
        count = 0
        for _ in range(0, 6):
            card = random.choice(cardz)
            cardtype = ATRCardType(card.atr)
            cardrequest = CardRequest(timeout=None, cardType=cardtype, newcardonly=True)
            print("re-insert card", toHexString(card.atr), "into", card.reader)
            cardservice = cardrequest.waitforcard()
            print("ok")
            try:
                cardservice.connection.connect()
                self.assertEqual(cardservice.connection.getATR(), card.atr)
            except CardConnectionException:
                # card was removed too fast
                pass
            cardservice.connection.disconnect()
            count += 1
        self.assertEqual(6, count)

    def testcase_CardRequestNewCardAnyCardTypeFiniteTimeOutNoInsertion(self):
        """Test smartcard.CardRequest for new card with time-out and no
        insertion before time-out."""

        self.removeAllCards()

        # make sure we have 6 time-outs
        cardtype = AnyCardType()
        cardrequest = CardRequest(timeout=1, cardType=cardtype, newcardonly=True)
        count = 0
        for _ in range(0, 6):
            before = time.time()
            try:
                cardrequest.waitforcard()
            except CardRequestTimeoutException:
                elapsed = int(10 * (time.time() - before))
                print(".", end=" ")
                self.assertTrue(elapsed >= 10 and elapsed <= 11.0)
                count += 1
        print("\n")
        self.assertEqual(6, count)

    def testcase_CardRequestNewCardAnyCardTypeFiniteTimeOutInsertion(self):
        """Test smartcard.CardRequest for new card with time-out and
        insertion before time-out."""

        self.removeAllCards()

        # make sure insertion is within 5s
        cardtype = AnyCardType()
        cardrequest = CardRequest(timeout=5, cardType=cardtype, newcardonly=True)
        count = 0
        for _ in range(0, 6):
            try:
                print("re-insert any card within the next 5 seconds")
                before = time.time()
                cardrequest.waitforcard()
                count += 1
                elapsed = int(10 * (time.time() - before))
                self.assertTrue(elapsed <= 55.0)
            except CardRequestTimeoutException:
                print("too slow... Test will show a failure")
        print("\n")
        self.assertEqual(6, count)

    def testcase_CardRequestNewCardInReaderNotPresentInfiniteTimeOut(self):
        """Test smartcard.CardRequest for any new card in a specific
        reader not present without time-out."""

        print("please remove a smart card reader")
        _readerz = readers()
        while True:
            readerz = readers()
            if len(_readerz) > len(readerz):
                break
            time.sleep(0.1)

        for reader in readerz:
            _readerz.remove(reader)

        cardtype = AnyCardType()
        cardrequest = CardRequest(
            timeout=None, readers=[_readerz[0]], cardType=cardtype, newcardonly=True
        )
        print("Re-insert reader", _readerz[0], "with a card inside")
        cardservice = cardrequest.waitforcard()
        cardservice.connection.connect()
        print(
            toHexString(cardservice.connection.getATR()),
            "in",
            cardservice.connection.getReader(),
        )
        cardservice.connection.disconnect()


if __name__ == "__main__":
    unittest.main(verbosity=1)

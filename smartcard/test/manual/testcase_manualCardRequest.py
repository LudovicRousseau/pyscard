#! /usr/bin/env python
"""Manual unit tests for smartcard.CardRequest

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
import random
import string
import time
import unittest

from smartcard.CardConnection import CardConnection
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType, ATRCardType
from smartcard.Exceptions import CardConnectionException
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import toHexString
from smartcard.System import readers

#
# setup test first: detect current readers and cards
#
print('insert two smartcard readers')
while True:
    readerz = readers()
    if 2 <= len(readerz):
        break
    time.sleep(.3)
for reader in readerz:
    print('\t', reader)

print('insert two cards in the readers')
cardrequest = CardRequest()
while True:
    cardz = cardrequest.waitforcardevent()
    if 2 <= len(cardz):
        break
    time.sleep(.3)
for card in cardz:
    print('\t', toHexString(card.atr))


class testcase_manualCardRequest(unittest.TestCase, CardObserver):
    """Test case for CardRequest."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def removeAllCards(self):
        print('please remove all inserted smart cards')
        cardrequest = CardRequest()
        while True:
            cards = cardrequest.waitforcardevent()
            if 0 == len(cards):
                break
            time.sleep(.3)
        print('ok')

    def testcase_CardRequestNewCardAnyCardTypeInfiniteTimeOut(self):
        """Test smartcard.CardRequest for any new card without time-out."""

        self.removeAllCards()
        cardtype = AnyCardType()
        cardrequest = CardRequest(
            timeout=None, cardType=cardtype, newcardonly=True)
        print('re-insert any combination of cards six time')
        count = 0
        for i in range(0, 6):
            cardservice = cardrequest.waitforcard()
            try:
                cardservice.connection.connect()
                print(toHexString(
                    cardservice.connection.getATR()), \
                    'in', cardservice.connection.getReader())
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
        for i in range(0, 6):
            card = random.choice(cardz)
            cardtype = ATRCardType(card.atr)
            cardrequest = CardRequest(
                timeout=None, cardType=cardtype, newcardonly=True)
            print('re-insert card', toHexString(card.atr), 'into', card.reader)
            cardservice = cardrequest.waitforcard()
            print('ok')
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
        cardrequest = CardRequest(
            timeout=1, cardType=cardtype, newcardonly=True)
        count = 0
        for i in range(0, 6):
            try:
                before = time.time()
                cardservice = cardrequest.waitforcard()
            except CardRequestTimeoutException as e:
                elapsed = int(10 * (time.time() - before))
                print('.', end=' ')
                self.assertTrue(elapsed >= 10 and elapsed <= 11.)
                count += 1
        print('\n')
        self.assertEqual(6, count)

    def testcase_CardRequestNewCardAnyCardTypeFiniteTimeOutInsertion(self):
        """Test smartcard.CardRequest for new card with time-out and
        insertion before time-out."""

        self.removeAllCards()

        # make sure insertion is within 5s
        cardtype = AnyCardType()
        cardrequest = CardRequest(
            timeout=5, cardType=cardtype, newcardonly=True)
        count = 0
        for i in range(0, 6):
            try:
                print('re-insert any card within the next 5 seconds')
                before = time.time()
                cardservice = cardrequest.waitforcard()
                count += 1
                elapsed = int(10 * (time.time() - before))
                self.assertTrue(elapsed <= 55.)
            except CardRequestTimeoutException as e:
                print('too slow... Test will show a failure')
        print('\n')
        self.assertEqual(6, count)

    def testcase_CardRequestNewCardInReaderNotPresentInfiniteTimeOut(self):
        """Test smartcard.CardRequest for any new card in a specific
        reader not present without time-out."""

        print('please remove a smart card reader')
        _readerz = readers()
        while True:
            readerz = readers()
            if len(_readerz) > len(readerz):
                break
            time.sleep(.1)

        for reader in readerz:
            _readerz.remove(reader)

        cardtype = AnyCardType()
        cardrequest = CardRequest(
            timeout=None,
            readers=[_readerz[0]],
            cardType=cardtype,
            newcardonly=True)
        print('Re-insert reader ', _readerz[0], 'with a card inside')
        cardservice = cardrequest.waitforcard()
        cardservice.connection.connect()
        print(toHexString(
            cardservice.connection.getATR()), \
            'in', cardservice.connection.getReader())
        cardservice.connection.disconnect()


def suite():
    suite1 = unittest.makeSuite(testcase_manualCardRequest)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()

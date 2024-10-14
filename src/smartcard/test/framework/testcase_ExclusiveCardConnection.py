#! /usr/bin/env python3
"""Unit tests for smartcard.ExclusiveTransmitCardConnection.

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

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
import threading
import time
import unittest

# from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.ExclusiveTransmitCardConnection import ExclusiveTransmitCardConnection

# define the apdus used in this script
GET_RESPONSE = [0xA0, 0xC0, 00, 00]
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


def signalEvent(evt):
    """A simple callback that signals an event."""
    evt.set()


class testthread(threading.Thread):
    """A test thread that repetitevely sends APDUs to a card within a
    transaction."""

    def __init__(self, threadindex):
        """Connect to a card with an ExclusiveTransmitCardConnection."""
        threading.Thread.__init__(self)

        self.threadindex = threadindex

        # request any card type
        cardtype = AnyCardType()
        cardrequest = CardRequest(timeout=5, cardType=cardtype)
        cardservice = cardrequest.waitforcard()

        # attach our decorator
        cardservice.connection = ExclusiveTransmitCardConnection(cardservice.connection)

        # uncomment to attach the console tracer
        # observer=ConsoleCardConnectionObserver()
        # cardservice.connection.addObserver(observer)

        # connect to the card
        cardservice.connection.connect()

        self.cardservice = cardservice

        # this event will signal the end of the thread
        self.evtStop = threading.Event()

        # this timer will set the event stop event in 30s
        timer = threading.Timer(10, signalEvent, [self.evtStop])
        timer.start()
        self.countTransmitted = 0

    def run(self):
        """Transmit APDUS with a random interval to the card."""
        connection = self.cardservice.connection
        while not self.evtStop.is_set():
            try:
                connection.lock()

                apdu = SELECT + DF_TELECOM
                _, sw1, sw2 = connection.transmit(apdu)

                if 0x90 == (sw1 & 0xF0):
                    apdu = GET_RESPONSE + [sw2]
                    _, sw1, sw2 = connection.transmit(apdu)
            finally:
                connection.unlock()
            self.countTransmitted = self.countTransmitted + 1
            time.sleep(float(random.uniform(1, 3)) * 0.01)


class testcase_cardmonitor(unittest.TestCase):
    """Test smartcard framework card monitoring classes"""

    def testcase_cardmonitorthread(self):
        """card monitor thread"""
        threads = []
        for i in range(0, 4):
            t = testthread(i)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # for t in threads:
        #     print(f"Thread {t.threadindex}: transmitted {t.countTransmitted} apdus.")


if __name__ == "__main__":
    unittest.main(verbosity=1)

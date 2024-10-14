#! /usr/bin/env python3
"""Unit tests for smartcard.CardMonitoring.

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


import sys
import threading
import time
import unittest

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

sys.path += [".."]

try:
    from local_config import expectedATRs
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


# a simple card observer that prints inserted/removed cards
class printobserver(CardObserver):
    """print observer"""

    def __init__(self, obsindex, testcase):
        self.obsindex = obsindex
        self.testcase = testcase

    def update(self, observable, handlers):
        (addedcards, removedcards) = handlers
        foundcards = {}
        self.testcase.assertEqual(removedcards, [])
        for card in addedcards:
            foundcards[toHexString(card.atr)] = 1
        for atr in expectedATRs:
            if atr and foundcards:
                self.testcase.assertTrue(toHexString(atr) in foundcards)


class testthread(threading.Thread):
    """thread"""

    def __init__(self, obsindex, testcase):
        threading.Thread.__init__(self)
        self.obsindex = obsindex
        self.testcase = testcase
        self.cardmonitor = CardMonitor()
        self.observer = None

    def run(self):
        # create and register observer
        self.observer = printobserver(self.obsindex, self.testcase)
        self.cardmonitor.addObserver(self.observer)
        time.sleep(1)
        self.cardmonitor.deleteObserver(self.observer)


class testcase_cardmonitor(unittest.TestCase):
    """Test smartcard framework card monitoring classes"""

    def testcase_cardmonitorthread(self):
        """card monitor thread"""
        threads = []
        for i in range(0, 4):
            t = testthread(i, self)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    unittest.main(verbosity=1)

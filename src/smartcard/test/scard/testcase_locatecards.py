#! /usr/bin/env python3
"""Unit tests for SCardLocateCards.

This test case can be executed individually, or with all other test cases
thru testsuite_scard.py.

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

import platform

# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
import unittest

from smartcard.scard import *

sys.path += [".."]

try:
    from local_config import expectedATRinReader, expectedReaders
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


class testcase_locatecards(unittest.TestCase):
    """Test scard API for ATR retrieval with SCardLocateCards"""

    def setUp(self):
        hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        self.assertEqual(hresult, 0)

    def tearDown(self):
        hresult = SCardReleaseContext(self.hcontext)
        self.assertEqual(hresult, 0)

    def test_locateCards(self):
        hresult, readers = SCardListReaders(self.hcontext, [])
        self.assertEqual(hresult, 0)

        foundReaders = {}
        for reader in readers:
            foundReaders[reader] = 1
        for reader in expectedReaders:
            self.assertTrue(reader in foundReaders)

        if "winscard" == resourceManager:
            hresult, cards = SCardListCards(self.hcontext, [], [])
            self.assertEqual(hresult, 0)

            readerstates = []
            for i in range(len(readers)):
                readerstates += [(readers[i], SCARD_STATE_UNAWARE)]

            hresult, newstates = SCardLocateCards(self.hcontext, cards, readerstates)
            self.assertEqual(hresult, 0)

            dictexpectedreaders = {}
            for reader in expectedReaders:
                dictexpectedreaders[reader] = 1
            for reader, eventstate, atr in newstates:
                if reader in dictexpectedreaders and [] != expectedATRinReader[reader]:
                    self.assertEqual(expectedATRinReader[reader], atr)
                    self.assertTrue(eventstate & SCARD_STATE_PRESENT)
                    self.assertTrue(eventstate & SCARD_STATE_CHANGED)

            # 10ms delay, so that time-out always occurs
            hresult, newstates = SCardGetStatusChange(self.hcontext, 10, newstates)
            self.assertEqual(hresult, SCARD_E_TIMEOUT)
            self.assertEqual(
                SCardGetErrorMessage(hresult),
                "The user-specified timeout value has expired. ",
            )

        elif "pcsclite" == resourceManager:
            readerstates = []
            for i in range(len(readers)):
                readerstates += [(readers[i], SCARD_STATE_UNAWARE)]

            hresult, newstates = SCardGetStatusChange(self.hcontext, 0, readerstates)
            self.assertEqual(hresult, 0)

            dictexpectedreaders = {}
            for reader in expectedReaders:
                dictexpectedreaders[reader] = 1
            for reader, eventstate, atr in newstates:
                if reader in dictexpectedreaders and [] != expectedATRinReader[reader]:
                    self.assertEqual(expectedATRinReader[reader], atr)
                    self.assertTrue(eventstate & SCARD_STATE_PRESENT)
                    self.assertTrue(eventstate & SCARD_STATE_CHANGED)


def suite():
    suite1 = unittest.defaultTestLoader.loadTestsFromTestCase(testcase_locatecards)
    return unittest.TestSuite(suite1)


if __name__ == "__main__":
    unittest.main()

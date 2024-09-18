#! /usr/bin/env python3
"""Unit tests for SCardConnect/SCardStatus/SCardDisconnect

This test case can be executed individually, or with all other test cases
thru testsuite_scard.py.

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


import unittest
from smartcard.scard import *

# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
sys.path += ['..']

try:
    from local_config import expectedATRs, expectedReaders
except ImportError:
    print('execute test suite first to generate the local_config.py file')
    sys.exit()


class testcase_getATR(unittest.TestCase):
    """Test scard API for ATR retrieval"""

    def setUp(self):
        hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        self.assertEqual(hresult, 0)
        hresult, self.readers = SCardListReaders(self.hcontext, [])
        self.assertEqual(hresult, 0)

    def tearDown(self):
        hresult = SCardReleaseContext(self.hcontext)
        self.assertEqual(hresult, 0)

    def _getATR(self, r):
        if r < len(expectedATRs) and [] != expectedATRs[r]:
            hresult, hcard, dwActiveProtocol = SCardConnect(
                self.hcontext,
                self.readers[r],
                SCARD_SHARE_SHARED,
                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
            self.assertEqual(hresult, 0)

            try:
                hresult, reader, state, protocol, atr = SCardStatus(hcard)
                self.assertEqual(hresult, 0)
                self.assertEqual(reader, expectedReaders[r])
                self.assertEqual(atr, expectedATRs[r])

            finally:
                hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                self.assertEqual(hresult, 0)

    def test_getATR0(self):
        testcase_getATR._getATR(self, 0)

    def test_getATR1(self):
        testcase_getATR._getATR(self, 1)

    def test_getATR2(self):
        testcase_getATR._getATR(self, 2)

    def test_getATR3(self):
        testcase_getATR._getATR(self, 3)


def suite():
    suite1 = unittest.makeSuite(testcase_getATR)
    return unittest.TestSuite(suite1)


if __name__ == '__main__':
    unittest.main()

#! /usr/bin/env python3
"""Unit tests for smartcard.CardRequest

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


# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
import unittest

sys.path += [".."]

try:
    from local_config import (
        expectedATRinReader,
        expectedATRs,
        expectedReaderForATR,
        expectedReaders,
    )
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


import smartcard.System
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType, ATRCardType
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.PassThruCardService import PassThruCardService
from smartcard.util import toHexString


class testcase_CardRequest(unittest.TestCase):
    """Test case for CardType."""

    def testcase_CardRequestATRCardType(self):
        """Test smartcard.AnyCardType."""

        for atr in expectedATRs:
            if atr:
                ct = ATRCardType(atr)
                cr = CardRequest(timeout=10, cardType=ct)
                cs = cr.waitforcard()
                cs.connection.connect()
                self.assertEqual(atr, cs.connection.getATR())
                self.assertEqual(
                    cs.connection.getReader(), expectedReaderForATR[toHexString(atr)]
                )
                cs.connection.disconnect()
                cs.connection.release()

    def testcase_CardRequestAnyCardTypeInSelectedReader(self):
        """Test smartcard.AnyCardType."""

        for reader in expectedReaders:
            atr = expectedATRinReader[reader]
            if atr:
                ct = AnyCardType()
                cr = CardRequest(timeout=10.6, readers=[reader], cardType=ct)
                cs = cr.waitforcard()
                cs.connection.connect()
                self.assertEqual(atr, cs.connection.getATR())
                self.assertEqual(
                    cs.connection.getReader(), expectedReaderForATR[toHexString(atr)]
                )
                cs.connection.disconnect()
                cs.connection.release()

    def testcase_CardRequestATRCardTypeTimeout(self):
        """Test smartcard.AnyCardType."""

        for reader in expectedReaders:
            atr = expectedATRinReader[reader][:-1]
            ct = ATRCardType(atr)
            cr = CardRequest(timeout=1, readers=[reader], cardType=ct)
            self.assertRaises(CardRequestTimeoutException, cr.waitforcard)

    def testcase_CardRequestATRCardTypeTimeoutAnyReader(self):
        """Test smartcard.AnyCardType."""

        readers = smartcard.System.readers()
        atr = expectedATRs[0][:-1]
        ct = ATRCardType(atr)
        cr = CardRequest(timeout=1.5, readers=readers, cardType=ct)
        self.assertRaises(CardRequestTimeoutException, cr.waitforcard)

    def testcase_CardRequestAnyCardTypeAnyReaderPassThru(self):
        """Test smartcard.AnyCardType."""

        for reader in expectedReaders:
            atr = expectedATRinReader[reader]
            if atr:
                ct = AnyCardType()
                cardservice = PassThruCardService
                cr = CardRequest(
                    timeout=10.6,
                    readers=[reader],
                    cardType=ct,
                    cardServiceClass=cardservice,
                )
                cs = cr.waitforcard()
                cs.connection.connect()
                self.assertEqual(cs.__class__, PassThruCardService)
                self.assertEqual(atr, cs.connection.getATR())
                self.assertEqual(
                    cs.connection.getReader(), expectedReaderForATR[toHexString(atr)]
                )
                cs.connection.disconnect()
                cs.connection.release()

    def testcase_CardRequestAnyCardTypeInSelectedReaderNewCard(self):
        """Test smartcard.AnyCardType."""

        for reader in expectedReaders:
            ct = AnyCardType()
            cr = CardRequest(newcardonly=True, timeout=1, readers=[reader], cardType=ct)
            self.assertRaises(CardRequestTimeoutException, cr.waitforcard)


if __name__ == "__main__":
    unittest.main(verbosity=1)

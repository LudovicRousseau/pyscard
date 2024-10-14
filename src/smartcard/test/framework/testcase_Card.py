#! /usr/bin/env python3
"""Unit tests for smartcard.Card

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
import unittest

from smartcard.Card import Card
from smartcard.Exceptions import NoCardException
from smartcard.System import readers

sys.path += [".."]

try:
    from local_config import expectedATRinReader, expectedReaders
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


class testcase_Card(unittest.TestCase):
    """Test case for smartcard.Card."""

    def testcase_CardDictionary(self):
        """Create a dictionary with Card keys"""
        mydict = {}
        for reader in readers():
            card = Card(reader, expectedATRinReader[reader.name])
            mydict[card] = reader

        for card in list(mydict.keys()):
            self.assertTrue(str(card.reader) in expectedReaders)

    def testcase_Card_FromReaders(self):
        """Create a Card from Readers and test that the response
        to SELECT DF_TELECOM has two bytes."""

        for reader in readers():
            card = Card(reader, expectedATRinReader[reader.name])
            cc = card.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect()
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "9f 20": 2, "6e 0": 3}
                self.assertEqual([], response)
                self.assertTrue(f"{sw1:x} {sw2:x}" in expectedSWs or "9f" == f"{sw1:x}")
            else:
                self.assertRaises(NoCardException, cc.connect)

    def testcase_Card_FromReaderStrings(self):
        """Create a Card from reader strings and test that the response
        to SELECT DF_TELECOM has two bytes."""

        for reader in readers():
            card = Card(str(reader), expectedATRinReader[reader.name])
            cc = card.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect()
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "9f 20": 2, "6e 0": 3}
                self.assertEqual([], response)
                self.assertTrue(f"{sw1:x} {sw2:x}" in expectedSWs or "9f" == f"{sw1:x}")
            else:
                self.assertRaises(NoCardException, cc.connect)

    def testcase_Card_Eq_NotEq(self):
        """Test == and != for Cards."""
        for reader in readers():
            card = Card(str(reader), expectedATRinReader[reader.name])
            cardcopy = Card(str(reader), expectedATRinReader[str(reader)])
            self.assertEqual(True, card == cardcopy)
            self.assertEqual(True, not card != cardcopy)

        for reader in readers():
            card = Card(str(reader), expectedATRinReader[reader.name])
            cardcopy = Card(str(reader), [0, 0])
            self.assertEqual(True, card != cardcopy)
            self.assertEqual(True, not card == cardcopy)


if __name__ == "__main__":
    unittest.main(verbosity=1)

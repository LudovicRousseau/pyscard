#! /usr/bin/env python3
"""Unit tests for smartcard.ATR

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

import unittest

# gemalto jython
from smartcard.ATR import ATR


class testcase_CAtr(unittest.TestCase):
    """Test APDU class and utilities"""

    def testcase_ATR1(self):
        """Usimera Classic 2."""
        a = ATR(
            [
                0x3B,
                0x9E,
                0x95,
                0x80,
                0x1F,
                0xC3,
                0x80,
                0x31,
                0xA0,
                0x73,
                0xBE,
                0x21,
                0x13,
                0x67,
                0x29,
                0x02,
                0x01,
                0x01,
                0x81,
                0xCD,
                0xB9,
            ]
        )
        historicalbytes = [
            0x80,
            0x31,
            0xA0,
            0x73,
            0xBE,
            0x21,
            0x13,
            0x67,
            0x29,
            0x02,
            0x01,
            0x01,
            0x81,
            0xCD,
        ]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), 0xB9)
        self.assertTrue(a.checksumOK)
        self.assertTrue(a.isT0Supported())
        self.assertTrue(not a.isT1Supported())
        self.assertTrue(a.isT15Supported())

    def testcase_ATR2(self):
        """Palmera Protect V2."""
        a = ATR([0x3B, 0x65, 0x00, 0x00, 0x9C, 0x02, 0x02, 0x01, 0x02])
        historicalbytes = [0x9C, 0x02, 0x02, 0x01, 0x02]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), None)
        self.assertTrue(a.isT0Supported())
        self.assertTrue(not a.isT1Supported())
        self.assertTrue(not a.isT15Supported())

    def testcase_ATR3(self):
        """Simera 3.13."""
        a = ATR([0x3B, 0x16, 0x18, 0x20, 0x02, 0x01, 0x00, 0x80, 0x0D])
        historicalbytes = [0x20, 0x02, 0x01, 0x00, 0x80, 0x0D]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), None)
        self.assertTrue(a.isT0Supported())
        self.assertTrue(not a.isT1Supported())
        self.assertTrue(not a.isT15Supported())

    def testcase_ATR4(self):
        """SIMRock'n Tree"""
        a = ATR(
            [0x3B, 0x77, 0x94, 0x00, 0x00, 0x82, 0x30, 0x00, 0x13, 0x6C, 0x9F, 0x22]
        )
        historicalbytes = [0x82, 0x30, 0x00, 0x13, 0x6C, 0x9F, 0x22]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), None)
        self.assertTrue(a.isT0Supported())
        self.assertTrue(not a.isT1Supported())
        self.assertTrue(not a.isT15Supported())

    def testcase_ATR5(self):
        """Demo Vitale online IGEA340"""
        a = ATR([0x3F, 0x65, 0x25, 0x00, 0x52, 0x09, 0x6A, 0x90, 0x00])
        historicalbytes = [0x52, 0x09, 0x6A, 0x90, 0x00]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), None)
        self.assertTrue(a.isT0Supported())
        self.assertTrue(not a.isT1Supported())
        self.assertTrue(not a.isT15Supported())

    def testcase_ATR6(self):
        """Simagine 2002"""
        a = ATR([0x3B, 0x16, 0x94, 0x20, 0x02, 0x01, 0x00, 0x00, 0x0D])
        historicalbytes = [0x20, 0x02, 0x01, 0x00, 0x00, 0x0D]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), None)

    def testcase_ATR7(self):
        """Protect V3 T=1"""
        a = ATR(
            [
                0x3B,
                0xE5,
                0x00,
                0x00,
                0x81,
                0x21,
                0x45,
                0x9C,
                0x10,
                0x01,
                0x00,
                0x80,
                0x0D,
            ]
        )
        historicalbytes = [0x9C, 0x10, 0x01, 0x00, 0x80]
        self.assertEqual(a.getHistoricalBytes(), historicalbytes)
        self.assertEqual(a.getChecksum(), 0x0D)
        self.assertTrue(not a.isT0Supported())
        self.assertTrue(a.isT1Supported())
        self.assertTrue(not a.isT15Supported())
        self.assertTrue(a.checksumOK)
        self.assertTrue(a.getTB1() == 0x00)
        self.assertTrue(a.getTC1() == 0x00)
        self.assertTrue(a.getTD1() == 0x81)
        self.assertTrue(a.TD[2 - 1] == 0x21)  # TD2
        self.assertTrue(a.TB[3 - 1] == 0x45)  # TB3


if __name__ == "__main__":
    unittest.main(verbosity=1)

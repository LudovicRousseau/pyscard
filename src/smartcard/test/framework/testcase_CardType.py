#! /usr/bin/env python3
"""Unit tests for smartcard.CardType

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
    from local_config import expectedATRinReader
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


from smartcard.CardType import AnyCardType, ATRCardType
from smartcard.System import readers


class testcase_CardType(unittest.TestCase):
    """Test case for CardType."""

    def testcase_AnyCardType(self):
        """Test smartcard.AnyCardType."""

        ct = AnyCardType()
        for reader in readers():
            if expectedATRinReader[reader.name]:
                connection = reader.createConnection()
                connection.connect()
                self.assertEqual(True, ct.matches(connection.getATR()))
                self.assertEqual(True, ct.matches(connection.getATR(), reader))
                connection.disconnect()
                connection.release()

    def testcase_ATRCardTypeWithoutMask(self):
        """Test smartcard.ATRCardType without mask."""

        for reader in readers():
            if expectedATRinReader[reader.name]:
                ct = ATRCardType(expectedATRinReader[reader.name])
                connection = reader.createConnection()
                connection.connect()
                self.assertEqual(True, ct.matches(connection.getATR()))
                self.assertEqual(True, ct.matches(connection.getATR(), reader))
                connection.disconnect()
                connection.release()

    def testcase_ATRCardTypeMisMatchWithoutMask(self):
        """Test smartcard.ATRCardType mismatch without mask."""

        for reader in readers():
            if expectedATRinReader[reader.name]:
                atr = list(expectedATRinReader[reader.name])
                # change the last byte of the expected atr
                atr[-1] = 0xFF
                ct = ATRCardType(atr)
                connection = reader.createConnection()
                connection.connect()
                self.assertEqual(False, ct.matches(connection.getATR()))
                self.assertEqual(False, ct.matches(connection.getATR(), reader))
                connection.disconnect()
                connection.release()

    def testcase_ATRCardTypeWithMask(self):
        """Test smartcard.ATRCardType with mask."""

        for reader in readers():
            if expectedATRinReader[reader.name]:
                mask = [0xFF for x in expectedATRinReader[reader.name]]
                # don't look to the last byte
                mask[-1] = 0x00
                ct = ATRCardType(expectedATRinReader[reader.name], mask)
                connection = reader.createConnection()
                connection.connect()
                atr = connection.getATR()
                connection.disconnect()
                connection.release()
                # change a bit in the last byte
                atr[-1] = atr[-1] ^ 0xFF
                self.assertEqual(True, ct.matches(atr))
                self.assertEqual(True, ct.matches(atr, reader))

    def testcase_ATRCardTypeWithMaskMismatch(self):
        """Test smartcard.ATRCardType with mask and mismatch."""

        for reader in readers():
            if expectedATRinReader[reader.name]:
                mask = [0xFF for x in expectedATRinReader[reader.name]]
                # don't look to the last byte
                mask[0] = mask[-1] = 0x00
                ct = ATRCardType(expectedATRinReader[reader.name], mask)
                connection = reader.createConnection()
                connection.connect()
                atr = connection.getATR()
                connection.disconnect()
                connection.release()
                # change a bit in the :-2 byte
                atr[-2] = atr[-2] ^ 0xFF
                self.assertEqual(False, ct.matches(atr))
                self.assertEqual(False, ct.matches(atr, reader))


if __name__ == "__main__":
    unittest.main(verbosity=1)

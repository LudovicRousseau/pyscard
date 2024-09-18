#! /usr/bin/env python3
"""Unit tests for smartcard.CardService

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

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
import string

# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
sys.path += ['..']

try:
    from local_config import expectedATRs, expectedReaders
    from local_config import expectedReaderGroups, expectedATRinReader
except ImportError:
    print('execute test suite first to generate the local_config.py file')
    sys.exit()


# gemalto jython
from smartcard.CardService import CardService
from smartcard.System import readers


class testcase_CardService(unittest.TestCase):
    """Test case for CardService."""

    def testcase_CardService(self):
        """Test the response to SELECT DF_TELECOM."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            if [] != expectedATRinReader[str(reader)]:
                cc = reader.createConnection()
                cs = CardService(cc)
                cs.connection.connect()
                response, sw1, sw2 = cs.connection.transmit(
                    SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEqual([], response)
                self.assertTrue(
                    "{:x} {:x}".format(sw1, sw2) in expectedSWs or "9f" == "%x" % sw1)


def suite():
    suite1 = unittest.makeSuite(testcase_CardService)
    return unittest.TestSuite(suite1)


if __name__ == '__main__':
    unittest.main()

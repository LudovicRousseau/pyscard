#! /usr/bin/env python
"""Unit tests for smartcard.CardConnection

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

__author__ = "http://www.gemalto.com"

Copyright 2001-2010 gemalto
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
    from local_config import expectedATRs, expectedReaders, expectedReaderGroups, expectedATRinReader
except:
    print 'execute test suite first to generate the local_config.py file'
    sys.exit()


from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.System import readers
from smartcard.CardConnection import CardConnection
from smartcard.scard import resourceManagerSubType


class testcase_CardConnection(unittest.TestCase):
    """Test case for CardConnection."""

    def testcase_CardConnection(self):
        """Test with default protocols the response to SELECT DF_TELECOM."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            cc = reader.createConnection()
            if [] != expectedATRinReader[str(reader)]:
                cc.connect()
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEquals([], response)
                self.assert_(expectedSWs.has_key("%x %x" % (sw1, sw2)) or "9f" == "%x" % sw1)
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()

    def testcase_CardConnectionT0(self):
        """Test with T0 the response to SELECT DF_TELECOM."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            cc = reader.createConnection()
            if [] != expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol)
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEquals([], response)
                self.assert_(expectedSWs.has_key("%x %x" % (sw1, sw2)) or "9f" == "%x" % sw1)
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()

    def testcase_CardConnectionT1inConnect(self):
        """Test that connecting with T1 on a T0 card fails."""

        for reader in readers():
            cc = reader.createConnection()
            # on Mac OS X Tiger, trying to connect with T=1 protocol does not except
            if not 'pcsclite-tiger' == resourceManagerSubType:
                if [] != expectedATRinReader[str(reader)]:
                    # should fail since the test card does not support T1
                    self.assertRaises(CardConnectionException, cc.connect, CardConnection.T1_protocol)
                else:
                    self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()

    def testcase_CardConnectionT1inTransmit(self):
        """Test that T1 in transmit for a T0 card fails."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            cc = reader.createConnection()
            if [] != expectedATRinReader[str(reader)]:
                cc.connect()
                self.assertRaises(CardConnectionException, cc.transmit, SELECT + DF_TELECOM, CardConnection.T1_protocol)
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()

    def testcase_CardConnectionT0T1(self):
        """Test test with T0 | T1  the response to SELECT DF_TELECOM."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            cc = reader.createConnection()
            if [] != expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEquals([], response)
                self.assert_(expectedSWs.has_key("%x %x" % (sw1, sw2)) or "9f" == "%x" % sw1)
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()

    def testcase_CardConnectionT0inTransmit(self):
        """Test with T0 in transmit the response to SELECT DF_TELECOM."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            cc = reader.createConnection()
            if [] != expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol)
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM, CardConnection.T0_protocol)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEquals([], response)
                self.assert_(expectedSWs.has_key("%x %x" % (sw1, sw2)) or "9f" == "%x" % sw1)
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()

    def testcase_CardConnectionT0T1inTransmitMustFail(self):
        """Test with bad parameter in transmit  the response to SELECT
        DF_TELECOM."""
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]

        for reader in readers():
            cc = reader.createConnection()
            if [] != expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)
                self.assertRaises(CardConnectionException, cc.transmit, SELECT + DF_TELECOM, CardConnection.T0_protocol | CardConnection.T1_protocol)
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()


def suite():
    suite1 = unittest.makeSuite(testcase_CardConnection)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()

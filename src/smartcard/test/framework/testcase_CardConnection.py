#! /usr/bin/env python3
"""Unit tests for smartcard.CardConnection

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

sys.path += [".."]

try:
    from local_config import expectedATRinReader
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.scard import (
    SCARD_LEAVE_CARD,
    SCARD_RESET_CARD,
    SCARD_SHARE_EXCLUSIVE,
    SCARD_UNPOWER_CARD,
)
from smartcard.System import readers

SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


class testcase_CardConnection(unittest.TestCase):
    """Test case for CardConnection."""

    def testcase_CardConnection(self):
        """Test with default protocols the response to SELECT DF_TELECOM."""
        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect()
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEqual([], response)
                self.assertTrue(f"{sw1:x} {sw2:x}" in expectedSWs or "9f" == f"{sw1:x}")
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardConnectionT0(self):
        """Test with T0 the response to SELECT DF_TELECOM."""

        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol)
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEqual([], response)
                self.assertTrue(f"{sw1:x} {sw2:x}" in expectedSWs or "9f" == f"{sw1:x}")
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardConnectionT1inConnect(self):
        """Test that connecting with T1 on a T0 card fails."""

        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                # should fail since the test card does not support T1
                self.assertRaises(
                    CardConnectionException, cc.connect, CardConnection.T1_protocol
                )
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardConnectionT1inTransmit(self):
        """Test that T1 in transmit for a T0 card fails."""

        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect()
                self.assertRaises(
                    CardConnectionException,
                    cc.transmit,
                    SELECT + DF_TELECOM,
                    CardConnection.T1_protocol,
                )
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardConnectionT0T1(self):
        """Test test with T0 | T1 the response to SELECT DF_TELECOM."""

        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)
                response, sw1, sw2 = cc.transmit(SELECT + DF_TELECOM)
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEqual([], response)
                self.assertTrue(f"{sw1:x} {sw2:x}" in expectedSWs or "9f" == f"{sw1:x}")
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardConnectionT0inTransmit(self):
        """Test with T0 in transmit the response to SELECT DF_TELECOM."""

        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol)
                response, sw1, sw2 = cc.transmit(
                    SELECT + DF_TELECOM, CardConnection.T0_protocol
                )
                expectedSWs = {"9f 1a": 1, "6e 0": 2, "9f 20": 3, "9f 22": 4}
                self.assertEqual([], response)
                self.assertTrue(f"{sw1:x} {sw2:x}" in expectedSWs or "9f" == f"{sw1:x}")
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardConnectionT0T1inTransmitMustFail(self):
        """Test with bad parameter in transmit the response to SELECT
        DF_TELECOM."""

        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)
                self.assertRaises(
                    CardConnectionException,
                    cc.transmit,
                    SELECT + DF_TELECOM,
                    CardConnection.T0_protocol | CardConnection.T1_protocol,
                )
            else:
                self.assertRaises(NoCardException, cc.connect)
        cc.disconnect()
        cc.release()

    def testcase_CardReconnectProtocol(self):
        """Test .reconnect()"""
        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)

                #  reconnect in T=1 when a T=0 card (GPK 8K) shall fail
                self.assertRaises(
                    CardConnectionException,
                    cc.reconnect,
                    protocol=CardConnection.T1_protocol,
                )
                cc.disconnect()
                cc.release()
            else:
                self.assertRaises(NoCardException, cc.connect)

    def testcase_CardReconnectMode(self):
        """Test .reconnect()"""
        for reader in readers():
            cc = reader.createConnection()
            cc2 = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)

                #  reconnect in exclusive mode should fail
                self.assertRaises(
                    CardConnectionException, cc2.reconnect, mode=SCARD_SHARE_EXCLUSIVE
                )
                cc.disconnect()
                cc.release()
            else:
                self.assertRaises(NoCardException, cc.connect)

    def testcase_CardReconnectDisposition(self):
        """Test .reconnect()"""
        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                cc.connect(CardConnection.T0_protocol | CardConnection.T1_protocol)
                cc.reconnect(disposition=SCARD_LEAVE_CARD)
                cc.reconnect(disposition=SCARD_RESET_CARD)
                cc.reconnect(disposition=SCARD_UNPOWER_CARD)
                cc.disconnect()
                cc.release()
            else:
                self.assertRaises(NoCardException, cc.connect)

    def testcase_CardReconnectNoConnect(self):
        """Test .reconnect()"""
        for reader in readers():
            cc = reader.createConnection()
            if expectedATRinReader[str(reader)]:
                #  reconnect without connect first shall fail
                self.assertRaises(CardConnectionException, cc.reconnect)
            else:
                self.assertRaises(NoCardException, cc.connect)


if __name__ == "__main__":
    unittest.main(verbosity=1)

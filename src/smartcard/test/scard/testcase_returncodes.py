#! /usr/bin/env python3
"""Unit tests for return codes

This test case can be executed individually, or with all other test cases
thru testsuite_scard.py.

__author__ = "https://www.gemalto.com/"

Copyright 2009 gemalto
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

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


class testcase_returncodes(unittest.TestCase):
    """Test scard API for return codes"""

    def test_getReturnCodes(self):
        errors = (
            SCARD_S_SUCCESS,
            SCARD_F_INTERNAL_ERROR,
            SCARD_E_CANCELLED,
            SCARD_E_INVALID_HANDLE,
            SCARD_E_INVALID_PARAMETER,
            SCARD_E_INVALID_TARGET,
            SCARD_E_NO_MEMORY,
            SCARD_F_WAITED_TOO_LONG,
            SCARD_E_INSUFFICIENT_BUFFER,
            SCARD_E_UNKNOWN_READER,
            SCARD_E_TIMEOUT,
            SCARD_E_SHARING_VIOLATION,
            SCARD_E_NO_SMARTCARD,
            SCARD_E_UNKNOWN_CARD,
            SCARD_E_CANT_DISPOSE,
            SCARD_E_PROTO_MISMATCH,
            SCARD_E_NOT_READY,
            SCARD_E_INVALID_VALUE,
            SCARD_E_SYSTEM_CANCELLED,
            SCARD_F_COMM_ERROR,
            SCARD_F_UNKNOWN_ERROR,
            SCARD_E_INVALID_ATR,
            SCARD_E_NOT_TRANSACTED,
            SCARD_E_READER_UNAVAILABLE,
            SCARD_E_PCI_TOO_SMALL,
            SCARD_E_READER_UNSUPPORTED,
            SCARD_E_DUPLICATE_READER,
            SCARD_E_CARD_UNSUPPORTED,
            SCARD_E_NO_SERVICE,
            SCARD_E_SERVICE_STOPPED,
            SCARD_E_UNEXPECTED,
            SCARD_E_ICC_INSTALLATION,
            SCARD_E_ICC_CREATEORDER,
            SCARD_E_UNSUPPORTED_FEATURE,
            SCARD_E_DIR_NOT_FOUND,
            SCARD_E_FILE_NOT_FOUND,
            SCARD_E_NO_DIR,
            SCARD_E_NO_FILE,
            SCARD_E_NO_ACCESS,
            SCARD_E_WRITE_TOO_MANY,
            SCARD_E_BAD_SEEK,
            SCARD_E_INVALID_CHV,
            SCARD_E_UNKNOWN_RES_MNG,
            SCARD_E_NO_SUCH_CERTIFICATE,
            SCARD_E_CERTIFICATE_UNAVAILABLE,
            SCARD_E_NO_READERS_AVAILABLE,
            SCARD_E_COMM_DATA_LOST,
            SCARD_E_NO_KEY_CONTAINER,
            SCARD_E_SERVER_TOO_BUSY,
            SCARD_W_UNSUPPORTED_CARD,
            SCARD_W_UNRESPONSIVE_CARD,
            SCARD_W_UNPOWERED_CARD,
            SCARD_W_RESET_CARD,
            SCARD_W_REMOVED_CARD,
            SCARD_W_SECURITY_VIOLATION,
            SCARD_W_WRONG_CHV,
            SCARD_W_CHV_BLOCKED,
            SCARD_W_EOF,
            SCARD_W_CANCELLED_BY_USER,
            SCARD_W_CARD_NOT_AUTHENTICATED,
        )
        # for e in errors:
        #    print(hex((e+0x100000000) & 0xFFFFFFFF), SCardGetErrorMessage(e))


def suite():
    suite1 = unittest.defaultTestLoader.loadTestsFromTestCase(testcase_returncodes)
    return unittest.TestSuite(suite1)


if __name__ == "__main__":
    unittest.main()

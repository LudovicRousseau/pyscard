#! /usr/bin/env python
"""Unit tests for SCardGetErrorMessage.

This test case can be executed individually, or with all other test cases
thru testsuite_scard.py.

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
from smartcard.scard import *
import sys


class testcase_geterrormessage(unittest.TestCase):
    """Test scard API for ATR retrieval with SCardLocateCards"""

    def setUp(self):
        hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        self.assertEquals(hresult, 0)

    def tearDown(self):
        hresult = SCardReleaseContext(self.hcontext)
        self.assertEquals(hresult, 0)

    def test_getErrorMessage(self):
        hresult, readers = SCardListReaders(self.hcontext, [])
        self.assertEquals(hresult, 0)

        hresult = SCardReleaseContext(123L)
        if 'win32' == sys.platform:
            self.assertEquals((SCARD_E_INVALID_HANDLE == hresult or ERROR_INVALID_HANDLE == hresult), True)
        else:
            self.assertEquals((SCARD_E_INVALID_HANDLE == hresult), True)
        self.assertEquals((SCardGetErrorMessage(hresult).rstrip() == 'Invalid handle.'.rstrip() or
             SCardGetErrorMessage(hresult).rstrip() == 'The handle is invalid.'.rstrip()), True)


def suite():
    suite1 = unittest.makeSuite(testcase_geterrormessage)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()

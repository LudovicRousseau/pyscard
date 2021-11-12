# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.Exceptions import *
from smartcard.scard import *
from distutils.util import get_platform


class TestUtil(unittest.TestCase):

    def test_Exceptions(self):
        exc = SmartcardException()
        self.assertEqual(exc.hresult, -1)


    def test_ListReadersException(self):
        exc = ListReadersException(0)
        self.assertEqual(exc.hresult, 0)
        text = str(exc)
        if not get_platform().startswith('win'):
            self.assertEqual(text, "Failed to list readers: Command successful. (0x00000000)")

        exc = ListReadersException(0x42)
        self.assertEqual(exc.hresult, 0x42)
        text = str(exc)
        if not get_platform().startswith('win'):
            expected = "Failed to list readers: Unknown error: 0x00000042 (0x00000042)"
            macos_bug_expected = expected.replace("Unknown", "Unkown")
            print(expected, macos_bug_expected)
            self.assertIn(text, [expected, macos_bug_expected])

        exc = ListReadersException(SCARD_S_SUCCESS)
        self.assertEqual(exc.hresult, 0)

        exc = ListReadersException(SCARD_E_NO_SERVICE)
        self.assertEqual(exc.hresult, SCARD_E_NO_SERVICE)
        text = str(exc)
        if not get_platform().startswith('win'):
            self.assertEqual(text, "Failed to list readers: Service not available. (0x8010001D)")

    def test_NoReadersException(self):
        exc = NoReadersException()
        self.assertEqual(exc.hresult, -1)
        text = str(exc)
        self.assertEqual(text, "No reader found")

    def test_InvalidReaderException(self):
        exc = InvalidReaderException("foobar")
        self.assertEqual(exc.hresult, -1)
        text = str(exc)
        self.assertEqual(text, "Invalid reader: foobar")

    def test_CardConnectionException(self):
        exc= CardConnectionException()
        self.assertEqual(exc.hresult, -1)
        text = str(exc)
        self.assertEqual(text, "")

    def test_hresult(self):
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult == SCARD_S_SUCCESS:
            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext, "INVALID READER NAME", SCARD_SHARE_SHARED, SCARD_PROTOCOL_ANY
            )
            self.assertEqual(hresult, SCARD_E_UNKNOWN_READER)
        else:
            self.assertEqual(hresult, SCARD_E_NO_SERVICE)

if __name__ == '__main__':
    unittest.main()

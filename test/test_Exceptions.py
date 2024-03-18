# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.Exceptions import *
from smartcard.pcsc.PCSCExceptions import *
from smartcard.scard import *
import platform


class TestUtil(unittest.TestCase):

    def test_Exceptions(self):
        exc = SmartcardException()
        self.assertEqual(exc.hresult, -1)


    def test_ListReadersException(self):
        exc = ListReadersException(0)
        self.assertEqual(exc.hresult, 0)
        text = str(exc)
        if platform.system() == 'Windows':
            expected = "Failed to list readers: The operation completed successfully.  (0x00000000)"
        else:
            expected = "Failed to list readers: Command successful. (0x00000000)"
        self.assertEqual(text, expected)

        exc = ListReadersException(0x42)
        self.assertEqual(exc.hresult, 0x42)
        text = str(exc)
        if platform.system() != 'Windows':
            expected = "Failed to list readers: Unknown error: 0x00000042 (0x00000042)"
            macos_bug_expected = expected.replace("Unknown", "Unkown")
            self.assertIn(text, [expected, macos_bug_expected])

        exc = ListReadersException(SCARD_S_SUCCESS)
        self.assertEqual(exc.hresult, 0)

        exc = ListReadersException(SCARD_E_NO_SERVICE)
        self.assertEqual(exc.hresult, SCARD_E_NO_SERVICE)
        text = str(exc)
        if platform.system() == 'Windows':
            expected = "Failed to list readers: The Smart Card Resource Manager is not running.  (0x8010001D)"
        else:
            expected = "Failed to list readers: Service not available. (0x8010001D)"

        self.assertEqual(text, expected)

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
        exc = CardConnectionException()
        self.assertEqual(exc.hresult, -1)
        text = str(exc)
        self.assertEqual(text, "")

        exc = CardConnectionException("foo", SCARD_W_REMOVED_CARD)
        self.assertEqual(exc.hresult, SCARD_W_REMOVED_CARD)
        text = str(exc)
        if platform.system() == 'Windows':
            expected = "foo: The smart card has been removed, so that further communication is not possible.  (0x80100069)"
        else:
            expected = "foo: Card was removed. (0x80100069)"

        self.assertEqual(text, expected)

    def test_hresult(self):
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult == SCARD_S_SUCCESS:
            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext, "INVALID READER NAME", SCARD_SHARE_SHARED, SCARD_PROTOCOL_ANY
            )
            self.assertEqual(hresult, SCARD_E_UNKNOWN_READER)
        else:
            self.assertEqual(hresult, SCARD_E_NO_SERVICE)

    # PCSC exceptions
    def test_EstablishContextException(self):
        exc= EstablishContextException(SCARD_E_NOT_TRANSACTED)
        self.assertEqual(exc.hresult, SCARD_E_NOT_TRANSACTED)
        text = str(exc)
        if platform.system() == 'Windows':
            expected = "An attempt was made to end a non-existent transaction. "
        else:
            expected = "Transaction failed."
        expected = "Failed to establish context: " + expected + " (0x80100016)"
        self.assertEqual(text, expected)

    def test_BaseSCardException(self):
        exc= BaseSCardException(message="foo", hresult=SCARD_E_NOT_TRANSACTED)
        self.assertEqual(exc.hresult, SCARD_E_NOT_TRANSACTED)
        text = str(exc)
        if platform.system() == 'Windows':
            expected = "An attempt was made to end a non-existent transaction. "
        else:
            expected = "Transaction failed."
        expected = "foo: " + expected + " (0x80100016)"
        self.assertEqual(text, expected)

    def test_wrongType(self):
        # SCardEstablishContext() argument should be int or long
        with self.assertRaises(TypeError):
            hresult, hcontext = SCardEstablishContext([0])

        with self.assertRaises(TypeError):
            hresult, hcontext = SCardEstablishContext("foo")

    def test_CardRequestTimeoutException(self):
        exc = CardRequestTimeoutException()
        self.assertEqual(str(exc), "Time-out during card request")
        exc = CardRequestTimeoutException(SCARD_E_NOT_TRANSACTED)
        if platform.system() == 'Windows':
            expected = "Time-out during card request: An attempt was made to end a non-existent transaction.  (0x80100016)"
        else:
            expected = "Time-out during card request: Transaction failed. (0x80100016)"
        self.assertEqual(str(exc), expected)
        exc = CardRequestTimeoutException(hresult=SCARD_E_NOT_TRANSACTED)
        self.assertEqual(str(exc), expected)

if __name__ == '__main__':
    unittest.main()

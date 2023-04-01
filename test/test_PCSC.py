import unittest
from smartcard.System import readers
from smartcard.scard import *


class TestPCSC(unittest.TestCase):

    def test_low_level(self):
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        self.assertIn(hresult, [SCARD_S_SUCCESS, SCARD_E_NO_SERVICE])

        if hresult == SCARD_E_NO_SERVICE:
            return

        hresult, readers = SCardListReaders(hcontext, [])
        self.assertIn(hresult, [SCARD_S_SUCCESS,
                                SCARD_E_NO_READERS_AVAILABLE])

        # the computer we are using may not have a reader connected
        # so we can't do much

        hresult = SCardReleaseContext(hcontext)
        self.assertEqual(hresult, SCARD_S_SUCCESS)

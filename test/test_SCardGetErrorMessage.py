# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.scard import SCardGetErrorMessage
from smartcard.scard import SCARD_S_SUCCESS, SCARD_F_INTERNAL_ERROR
from distutils.util import get_platform


class TestError(unittest.TestCase):

    def test_SCardGetErrorMessage(self):
        res = SCardGetErrorMessage(SCARD_S_SUCCESS)

        # do not test on Windows
        # the error messages are different and localized
        if get_platform() in ('win32', 'win-amd64'):
            return

        expected = "Command successful."
        self.assertEqual(res, expected)

        res = SCardGetErrorMessage(SCARD_F_INTERNAL_ERROR)
        expected = "Internal error."
        self.assertEqual(res, expected)

        res = SCardGetErrorMessage(1)
        expected = "Unknown error: 0x00000001"
        # macOS bug not yet fixed
        macos_bug_expected = "Unkown error: 0x00000001"
        self.assertIn(res, [expected, macos_bug_expected])


if __name__ == '__main__':
    unittest.main()

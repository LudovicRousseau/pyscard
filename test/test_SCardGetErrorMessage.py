#! /usr/bin/env python
# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.scard import *


class TestError(unittest.TestCase):

    def test_SCardGetErrorMessage(self):
        res = SCardGetErrorMessage(SCARD_S_SUCCESS)
        expected = "Command successful."
        self.assertEqual(res, expected)

        res = SCardGetErrorMessage(SCARD_F_INTERNAL_ERROR)
        expected = "Internal error."
        self.assertEqual(res, expected)

        res = SCardGetErrorMessage(1)
        expected = "Unkown error: 0x00000001"
        self.assertEqual(res, expected)


if __name__ == '__main__':
    unittest.main()

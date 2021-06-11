#! /usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""Unit tests for smartcard.utils

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

from smartcard.util import *


class testcase_utils(unittest.TestCase):
    """Test smartcard.utils."""

    def testcase_asciitostring(self):
        """tests ASCIIToString"""
        self.assertEqual(
            toASCIIString(
                [0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31]),
            "Number 101")

    def testcase_bytesto338(self):
        """tests toGSM3_38Bytes"""
        self.assertEqual(
            toGSM3_38Bytes("@ùPascal"),
            [0x00, 0x06, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C])

    def testcase_padd(self):
        """tests padd"""
        self.assertEqual(
            [0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3, 0xFF,
             0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
            padd([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3], 16))

        self.assertEqual([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3],
                           padd([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3], 9))

        self.assertEqual([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3],
                           padd([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3], 8))

        self.assertEqual([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3, 0xFF],
                           padd([0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3], 10))

    def testcase_toasciibytes(self):
        """tests toASCIIBytes"""
        self.assertEqual(
            [0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31],
            toASCIIBytes("Number 101"))

        self.assertEqual(
            toASCIIString(toASCIIBytes("Number 101")), "Number 101")

    def testcase_tobytestring(self):
        """tests toByteString"""
        self.assertEqual(
            [59, 101, 0, 0, 156, 17, 1, 1, 3],
            toBytes("3B 65 00 00 9C 11 01 01 03"))
        self.assertEqual(
            [59, 101, 0, 0, 156, 17, 1, 1, 3],
            toBytes("3B6500009C11010103"))
        self.assertEqual(
            [59, 101, 0, 0, 156, 17, 1, 1, 3],
            toBytes("3B65 0000 9C11 010103"))
        self.assertEqual(
            [59, 101, 0, 0, 156, 17, 1, 1, 3],
            toBytes("3B65 \t\t0000 \t9C11 \t0101\t03   \t\n"))

    def testcase_tohexstring(self):
        """tests toHexString"""
        self.assertEqual(
            "3B 65 00 00 9C 11 01 01 03",
            toHexString([59, 101, 0, 0, 156, 17, 1, 1, 3]))

        bytes = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
        self.assertEqual(
            "3B, 65, 00, 00, 9C, 11, 01, 01, 03",
            toHexString(bytes, COMMA))
        self.assertEqual("3B6500009C11010103", toHexString(bytes, PACK))
        self.assertEqual(
            "0x3B 0x65 0x00 0x00 0x9C 0x11 0x01 0x01 0x03",
            toHexString(bytes, HEX))
        self.assertEqual(
            "0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03",
            toHexString(bytes, HEX | COMMA))
        self.assertEqual(
            "0X3B 0X65 0X00 0X00 0X9C 0X11 0X01 0X01 0X03",
            toHexString(bytes, HEX | UPPERCASE))
        self.assertEqual(
            "0X3B, 0X65, 0X00, 0X00, 0X9C, 0X11, 0X01, 0X01, 0X03",
            toHexString(bytes, HEX | UPPERCASE | COMMA))

        bytes = [59, 101, 0, 0, 156, 17, 1, 1, 3]
        self.assertEqual(
            "3B, 65, 00, 00, 9C, 11, 01, 01, 03",
            toHexString(bytes, COMMA))
        self.assertEqual(
            "3B6500009C11010103", toHexString(bytes, PACK))
        self.assertEqual(
            "0x3B 0x65 0x00 0x00 0x9C 0x11 0x01 0x01 0x03",
            toHexString(bytes, HEX))
        self.assertEqual(
            "0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03",
            toHexString(bytes, HEX | COMMA))
        self.assertEqual(
            "0X3B 0X65 0X00 0X00 0X9C 0X11 0X01 0X01 0X03",
            toHexString(bytes, HEX | UPPERCASE))
        self.assertEqual(
            "0X3B, 0X65, 0X00, 0X00, 0X9C, 0X11, 0X01, 0X01, 0X03",
            toHexString(bytes, HEX | UPPERCASE | COMMA))

    def testcase_tohexstring_empty(self):
        """tests toHexString"""
        self.assertEqual("", toHexString())
        self.assertEqual("", toHexString([]))

    def testcase_tohexstring_nobytes(self):
        """tests toHexString"""
        self.assertRaises(TypeError, toHexString, 'bad input')
        self.assertRaises(TypeError, toHexString, ['bad', 'input'])


def suite():
    suite1 = unittest.makeSuite(testcase_utils)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()

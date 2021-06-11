# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.util import *


class TestUtil(unittest.TestCase):

    def test_toBytes(self):
        data_in = "3B 65 00 00 9C 11 01 01 03"
        data_out = [59, 101, 0, 0, 156, 17, 1, 1, 3]
        self.assertEqual(toBytes(data_in), data_out)

        data_in = "3B6500009C11010103"
        self.assertEqual(toBytes(data_in), data_out)

        data_in = "3B6500   009C1101  0103"
        self.assertEqual(toBytes(data_in), data_out)

        data_in = '''
                    3B 65 00
                    00 9C 11 01
                    01 03
                  '''
        self.assertEqual(toBytes(data_in), data_out)

        data_in = "zz"
        self.assertRaises(TypeError, toBytes, data_in)

    def test_padd(self):
        data_in = toBytes("3B 65 00 00 9C 11 01 01 03")
        data_out = [0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3,
                    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.assertEqual(padd(data_in, 16), data_out)

    def test_toASCIIBytes(self):
        data_in = "Number 101"
        data_out = [0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31]
        self.assertEqual(toASCIIBytes(data_in), data_out)

    def test_toASCIIString(self):
        data_in = [0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31]
        data_out = "Number 101"
        self.assertEqual(toASCIIString(data_in), data_out)

        data_in = [0x01, 0x20, 0x80, 0x7E, 0xF0]
        data_out = ". .~."
        self.assertEqual(toASCIIString(data_in), data_out)

    def test_toGSM3_38Bytes(self):
        data_in = "@Pascal"
        data_out = [0x00, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C]
        self.assertEqual(toGSM3_38Bytes(data_in), data_out)

        data_in = u"@ùPascal"
        data_out = [0x00, 0x06, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C]
        self.assertEqual(toGSM3_38Bytes(data_in), data_out)

        data_in = u"@ùPascal".encode('iso8859-1')
        data_out = [0x00, 0x06, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C]
        self.assertEqual(toGSM3_38Bytes(data_in), data_out)

        data_in = "1234"
        data_out = [0x31, 0x32, 0x33, 0x34]
        self.assertEqual(toGSM3_38Bytes(data_in), data_out)

    def test_toHexString(self):
        data_in = []
        data_out = ""
        self.assertEqual(toHexString(data_in), data_out)

        data_in = 42
        self.assertRaises(TypeError, toHexString, data_in)

        data_in = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
        data_out = "3B 65 00 00 9C 11 01 01 03"
        self.assertEqual(toHexString(data_in), data_out)

        data_out = "3B, 65, 00, 00, 9C, 11, 01, 01, 03"
        self.assertEqual(toHexString(data_in, COMMA), data_out)

        data_out = "0x3B 0x65 0x00 0x00 0x9C 0x11 0x01 0x01 0x03"
        self.assertEqual(toHexString(data_in, HEX), data_out)

        data_out = "0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03"
        self.assertEqual(toHexString(data_in, HEX | COMMA), data_out)

        data_out = "0X3B 0X65 0X00 0X00 0X9C 0X11 0X01 0X01 0X03"
        self.assertEqual(toHexString(data_in, HEX | UPPERCASE), data_out)

        data_out = "0X3B, 0X65, 0X00, 0X00, 0X9C, 0X11, 0X01, 0X01, 0X03"
        self.assertEqual(toHexString(data_in, HEX | UPPERCASE | COMMA),
                         data_out)

        data_out = "3B6500009C11010103"
        self.assertEqual(toHexString(data_in, PACK), data_out)

        data_out = "3B,65,00,00,9C,11,01,01,03"
        self.assertEqual(toHexString(data_in, COMMA | PACK), data_out)

        data_out = "0x3B0x650x000x000x9C0x110x010x010x03"
        self.assertEqual(toHexString(data_in, HEX | PACK), data_out)

        data_out = "0x3B,0x65,0x00,0x00,0x9C,0x11,0x01,0x01,0x03"
        self.assertEqual(toHexString(data_in, HEX | COMMA | PACK), data_out)

        data_out = "0X3B0X650X000X000X9C0X110X010X010X03"
        self.assertEqual(toHexString(data_in, HEX | UPPERCASE | PACK),
                         data_out)

        data_out = "0X3B,0X65,0X00,0X00,0X9C,0X11,0X01,0X01,0X03"
        self.assertEqual(toHexString(data_in, HEX | UPPERCASE | COMMA |
                                     PACK), data_out)

    def test_HexListToBinString(self):
        data_in = [1, 2, 3]
        data_out = "\x01\x02\x03"
        self.assertEqual(HexListToBinString(data_in), data_out)

    def test_BinStringToHexList(self):
        data_in = "\x01\x02\x03"
        data_out = [1, 2, 3]
        self.assertEqual(BinStringToHexList(data_in), data_out)

    def test_hl2bs(self):
        data_in = [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
        data_out = 'Number 101'
        self.assertEqual(hl2bs(data_in), data_out)

    def test_bs2hl(self):
        data_in = 'Number 101'
        data_out = [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
        self.assertEqual(bs2hl(data_in), data_out)


if __name__ == '__main__':
    unittest.main()

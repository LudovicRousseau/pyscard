# -*- coding: utf-8 -*-

import sys
import unittest
from smartcard.ATR import ATR
from smartcard.Exceptions import SmartcardException
from smartcard.util import toBytes

if sys.version_info >= (3, 0):
    from io import StringIO
else:
    from StringIO import StringIO


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_ATR1(self):
        atr = [0x3F, 0x65, 0x25, 0x00, 0x2C, 0x09, 0x69, 0x90, 0x00]
        data_out = """TB1: 25
TC1: 0
supported protocols T=0
T=0 supported: True
T=1 supported: False
	clock rate conversion factor: 372
	bit rate adjustment factor: 1
	maximum programming current: 50
	programming voltage: 30
	guard time: 0
nb of interface bytes: 2
nb of historical bytes: 5
"""
        a = ATR(atr)
        a.dump()
        output = sys.stdout.getvalue()
        self.assertEqual(output, data_out)

    def test_ATR2(self):
        atr = [0x3F, 0x65, 0x25, 0x08, 0x93, 0x04, 0x6C, 0x90, 0x00]
        data_out = """TB1: 25
TC1: 8
supported protocols T=0
T=0 supported: True
T=1 supported: False
	clock rate conversion factor: 372
	bit rate adjustment factor: 1
	maximum programming current: 50
	programming voltage: 30
	guard time: 8
nb of interface bytes: 2
nb of historical bytes: 5
"""
        a = ATR(atr)
        a.dump()
        output = sys.stdout.getvalue()
        self.assertEqual(output, data_out)

    def test_ATR3(self):
        atr = [0x3B, 0x16, 0x94, 0x7C, 0x03, 0x01, 0x00, 0x00, 0x0D]
        data_out = """TA1: 94
supported protocols T=0
T=0 supported: True
T=1 supported: False
	clock rate conversion factor: 512
	bit rate adjustment factor: 8
	maximum programming current: 50
	programming voltage: 5
	guard time: None
nb of interface bytes: 1
nb of historical bytes: 6
"""
        a = ATR(atr)
        a.dump()
        output = sys.stdout.getvalue()
        self.assertEqual(output, data_out)

    def test_ATR4(self):
        atr = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
        data_out = """TB1: 0
TC1: 0
supported protocols T=0
T=0 supported: True
T=1 supported: False
	clock rate conversion factor: 372
	bit rate adjustment factor: 1
	maximum programming current: 25
	programming voltage: 5
	guard time: 0
nb of interface bytes: 2
nb of historical bytes: 5
"""
        a = ATR(atr)
        a.dump()
        output = sys.stdout.getvalue()
        self.assertEqual(output, data_out)

    def test_ATR5(self):
        atr = [0x3B, 0xE3, 0x00, 0xFF, 0x81, 0x31, 0x52, 0x45, 0xA1,
               0xA2, 0xA3, 0x1B]
        data_out = """TB1: 0
TC1: ff
TD1: 81
TD2: 31
TA3: 52
TB3: 45
supported protocols T=1
T=0 supported: False
T=1 supported: True
checksum: 27
	clock rate conversion factor: 372
	bit rate adjustment factor: 1
	maximum programming current: 25
	programming voltage: 5
	guard time: 255
nb of interface bytes: 6
nb of historical bytes: 3
"""
        a = ATR(atr)
        a.dump()
        output = sys.stdout.getvalue()
        self.assertEqual(output, data_out)

    def test_ATR6(self):
        atr = [0x3B, 0xE5, 0x00, 0x00, 0x81, 0x21, 0x45, 0x9C, 0x10,
               0x01, 0x00, 0x80, 0x0D]
        data_out = """TB1: 0
TC1: 0
TD1: 81
TD2: 21
TB3: 45
supported protocols T=1
T=0 supported: False
T=1 supported: True
checksum: 13
	clock rate conversion factor: 372
	bit rate adjustment factor: 1
	maximum programming current: 25
	programming voltage: 5
	guard time: 0
nb of interface bytes: 5
nb of historical bytes: 5
"""
        a = ATR(atr)
        a.dump()
        output = sys.stdout.getvalue()
        self.assertEqual(output, data_out)

    def test_ATR_TS(self):
        atr = [0x42]
        self.assertRaises(SmartcardException, ATR, atr)

    def test_ATR_get(self):
        atr = "3B F2 95 12 34 01 36 06"
        a = ATR(toBytes(atr))
        self.assertEqual(a.getTA1(), 0x95)
        self.assertEqual(a.getTB1(), 0x12)
        self.assertEqual(a.getTC1(), 0x34)
        self.assertEqual(a.getTD1(), 0x01)
        self.assertEqual(a.getHistoricalBytes(), [0x36, 0x06])
        self.assertFalse(a.isT15Supported())
        self.assertEqual(str(a), atr)

if __name__ == '__main__':
    unittest.main(buffer=True)

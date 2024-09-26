import pytest

from smartcard.util import *


def test_to_bytes():
    data_in = "3B 65 00 00 9C 11 01 01 03"
    data_out = [59, 101, 0, 0, 156, 17, 1, 1, 3]
    assert toBytes(data_in) == data_out

    data_in = "3B6500009C11010103"
    assert toBytes(data_in) == data_out

    data_in = "3B6500   009C1101  0103"
    assert toBytes(data_in) == data_out

    data_in = """
                3B 65 00
                00 9C 11 01
                01 03
              """
    assert toBytes(data_in) == data_out

    data_in = "zz"
    with pytest.raises(TypeError):
        toBytes(data_in)


def test_padd():
    data_in = toBytes("3B 65 00 00 9C 11 01 01 03")
    old_data_in = list(data_in)
    data_out = [
        0x3B,
        0x65,
        0,
        0,
        0x9C,
        0x11,
        1,
        1,
        3,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
    ]
    assert padd(data_in, 16) == data_out
    assert data_in == old_data_in

    assert padd(data_in, 4) == data_in


def test_to_ascii_bytes():
    data_in = "Number 101"
    data_out = [0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31]
    assert toASCIIBytes(data_in) == data_out


def test_to_ascii_string():
    data_in = [0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31]
    data_out = "Number 101"
    assert toASCIIString(data_in) == data_out

    data_in = [0x01, 0x20, 0x80, 0x7E, 0xF0]
    data_out = ". .~."
    assert toASCIIString(data_in) == data_out


def test_to_gsm3_38_bytes():
    data_in = "@Pascal"
    data_out = [0x00, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C]
    assert toGSM3_38Bytes(data_in) == data_out

    data_in = "@ùPascal"
    data_out = [0x00, 0x06, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C]
    assert toGSM3_38Bytes(data_in) == data_out

    data_in = "@ùPascal".encode("iso8859-1")
    data_out = [0x00, 0x06, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C]
    assert toGSM3_38Bytes(data_in) == data_out

    data_in = "1234"
    data_out = [0x31, 0x32, 0x33, 0x34]
    assert toGSM3_38Bytes(data_in) == data_out


def test_to_hex_string():
    data_in = []
    data_out = ""
    assert toHexString(data_in) == data_out

    data_in = 42
    with pytest.raises(TypeError):
        toHexString(data_in)

    data_in = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
    data_out = "3B 65 00 00 9C 11 01 01 03"
    assert toHexString(data_in) == data_out

    data_out = "3B, 65, 00, 00, 9C, 11, 01, 01, 03"
    assert toHexString(data_in, COMMA) == data_out

    data_out = "0x3B 0x65 0x00 0x00 0x9C 0x11 0x01 0x01 0x03"
    assert toHexString(data_in, HEX) == data_out

    data_out = "0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03"
    assert toHexString(data_in, HEX | COMMA) == data_out

    data_out = "0X3B 0X65 0X00 0X00 0X9C 0X11 0X01 0X01 0X03"
    assert toHexString(data_in, HEX | UPPERCASE) == data_out

    data_out = "0X3B, 0X65, 0X00, 0X00, 0X9C, 0X11, 0X01, 0X01, 0X03"
    assert toHexString(data_in, HEX | UPPERCASE | COMMA) == data_out

    data_out = "3B6500009C11010103"
    assert toHexString(data_in, PACK) == data_out

    data_out = "3B,65,00,00,9C,11,01,01,03"
    assert toHexString(data_in, COMMA | PACK) == data_out

    data_out = "0x3B0x650x000x000x9C0x110x010x010x03"
    assert toHexString(data_in, HEX | PACK) == data_out

    data_out = "0x3B,0x65,0x00,0x00,0x9C,0x11,0x01,0x01,0x03"
    assert toHexString(data_in, HEX | COMMA | PACK) == data_out

    data_out = "0X3B0X650X000X000X9C0X110X010X010X03"
    assert toHexString(data_in, HEX | UPPERCASE | PACK) == data_out

    data_out = "0X3B,0X65,0X00,0X00,0X9C,0X11,0X01,0X01,0X03"
    assert toHexString(data_in, HEX | UPPERCASE | COMMA | PACK) == data_out

    with pytest.raises(TypeError):
        toHexString("foo")


def test_hex_list_to_bin_string():
    data_in = [1, 2, 3]
    data_out = "\x01\x02\x03"
    with pytest.warns(DeprecationWarning):
        assert HexListToBinString(data_in) == data_out


def test_bin_string_to_hex_list():
    data_in = "\x01\x02\x03"
    data_out = [1, 2, 3]
    with pytest.warns(DeprecationWarning):
        assert BinStringToHexList(data_in) == data_out


def test_hl2bs():
    data_in = [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
    data_out = "Number 101"
    with pytest.warns(DeprecationWarning):
        assert hl2bs(data_in) == data_out


def test_bs2hl():
    data_in = "Number 101"
    data_out = [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
    with pytest.warns(DeprecationWarning):
        assert bs2hl(data_in) == data_out

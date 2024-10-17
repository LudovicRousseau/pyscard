import pytest

from smartcard.ATR import ATR
from smartcard.Exceptions import SmartcardException
from smartcard.util import toBytes


def test_atr1(capsys):
    atr = [0x3F, 0x65, 0x25, 0x00, 0x2C, 0x09, 0x69, 0x90, 0x00]
    data_out = """TB1: 25
TC1: 0
supported protocols T=0
T=0 supported: True
T=1 supported: False
\tclock rate conversion factor: 372
\tbit rate adjustment factor: 1
\tmaximum programming current: 50
\tprogramming voltage: 30
\tguard time: 0
nb of interface bytes: 2
nb of historical bytes: 5
"""
    a = ATR(atr)
    a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr2(capsys):
    atr = [0x3F, 0x65, 0x25, 0x08, 0x93, 0x04, 0x6C, 0x90, 0x00]
    data_out = """TB1: 25
TC1: 8
supported protocols T=0
T=0 supported: True
T=1 supported: False
\tclock rate conversion factor: 372
\tbit rate adjustment factor: 1
\tmaximum programming current: 50
\tprogramming voltage: 30
\tguard time: 8
nb of interface bytes: 2
nb of historical bytes: 5
"""
    a = ATR(atr)
    a.dump()

    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr3(capsys):
    atr = [0x3B, 0x16, 0x94, 0x7C, 0x03, 0x01, 0x00, 0x00, 0x0D]
    data_out = """TA1: 94
supported protocols T=0
T=0 supported: True
T=1 supported: False
\tclock rate conversion factor: 512
\tbit rate adjustment factor: 8
\tmaximum programming current: 50
\tprogramming voltage: 5
\tguard time: None
nb of interface bytes: 1
nb of historical bytes: 6
"""
    a = ATR(atr)
    a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr4(capsys):
    atr = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
    data_out = """TB1: 0
TC1: 0
supported protocols T=0
T=0 supported: True
T=1 supported: False
\tclock rate conversion factor: 372
\tbit rate adjustment factor: 1
\tmaximum programming current: 25
\tprogramming voltage: 5
\tguard time: 0
nb of interface bytes: 2
nb of historical bytes: 5
"""
    a = ATR(atr)
    a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr5(capsys):
    atr = [0x3B, 0xE3, 0x00, 0xFF, 0x81, 0x31, 0x52, 0x45, 0xA1, 0xA2, 0xA3, 0x1B]
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
\tclock rate conversion factor: 372
\tbit rate adjustment factor: 1
\tmaximum programming current: 25
\tprogramming voltage: 5
\tguard time: 255
nb of interface bytes: 6
nb of historical bytes: 3
"""
    a = ATR(atr)
    a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr6(capsys):
    atr = [0x3B, 0xE5, 0x00, 0x00, 0x81, 0x21, 0x45, 0x9C, 0x10, 0x01, 0x00, 0x80, 0x0D]
    data_out = """TB1: 0
TC1: 0
TD1: 81
TD2: 21
TB3: 45
supported protocols T=1
T=0 supported: False
T=1 supported: True
checksum: 13
\tclock rate conversion factor: 372
\tbit rate adjustment factor: 1
\tmaximum programming current: 25
\tprogramming voltage: 5
\tguard time: 0
nb of interface bytes: 5
nb of historical bytes: 5
"""
    a = ATR(atr)
    a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr_ts():
    atr = [0x42]
    with pytest.raises(SmartcardException):
        ATR(atr)


def test_atr_get():
    atr = "3B F2 95 12 34 01 36 06"
    a = ATR(toBytes(atr))
    assert a.getTA1() == 0x95
    assert a.getTB1() == 0x12
    assert a.getTC1() == 0x34
    assert a.getTD1() == 0x01
    assert a.getHistoricalBytes(), [0x36 == 0x06]
    assert a.isT15Supported() is False
    assert str(a) == atr


@pytest.mark.parametrize(
    "field, expected_length",
    (
        ("clockrateconversion", 16),
        ("bitratefactor", 16),
    ),
)
def test_map_lengths(field, expected_length):
    """Verify ATR class fields have expected lengths.

    This doesn't validate values, but simply ensures the lengths match expectations.
    """

    assert len(getattr(ATR, field)) == expected_length

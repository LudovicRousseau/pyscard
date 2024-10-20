import re
import textwrap

import pytest

from smartcard.ATR import ATR
from smartcard.Exceptions import SmartcardException
from smartcard.util import toBytes


def test_atr1(capsys):
    atr = [0x3F, 0x65, 0x25, 0x00, 0x2C, 0x09, 0x69, 0x90, 0x00]
    data_out = textwrap.dedent(
        """\
        TB1: 25
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
    )
    a = ATR(atr)
    with pytest.warns(DeprecationWarning, match=re.escape("print(ATR.render())")):
        a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr2(capsys):
    atr = [0x3F, 0x65, 0x25, 0x08, 0x93, 0x04, 0x6C, 0x90, 0x00]
    data_out = textwrap.dedent(
        """\
        TB1: 25
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
    )
    a = ATR(atr)
    with pytest.warns(DeprecationWarning, match=re.escape("print(ATR.render())")):
        a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr3(capsys):
    atr = [0x3B, 0x16, 0x94, 0x7C, 0x03, 0x01, 0x00, 0x00, 0x0D]
    data_out = textwrap.dedent(
        """\
        TA1: 94
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
    )
    a = ATR(atr)
    with pytest.warns(DeprecationWarning, match=re.escape("print(ATR.render())")):
        a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr4(capsys):
    atr = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
    data_out = textwrap.dedent(
        """\
        TB1: 0
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
    )
    a = ATR(atr)
    with pytest.warns(DeprecationWarning, match=re.escape("print(ATR.render())")):
        a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr5(capsys):
    atr = [0x3B, 0xE3, 0x00, 0xFF, 0x81, 0x31, 0x52, 0x45, 0xA1, 0xA2, 0xA3, 0x1B]
    data_out = textwrap.dedent(
        """\
        TB1: 0
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
    )
    a = ATR(atr)
    with pytest.warns(DeprecationWarning, match=re.escape("print(ATR.render())")):
        a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


def test_atr6(capsys):
    atr = [0x3B, 0xE5, 0x00, 0x00, 0x81, 0x21, 0x45, 0x9C, 0x10, 0x01, 0x00, 0x80, 0x0D]
    data_out = textwrap.dedent(
        """\
        TB1: 0
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
    )
    a = ATR(atr)
    with pytest.warns(DeprecationWarning, match=re.escape("print(ATR.render())")):
        a.dump()
    stdout, _ = capsys.readouterr()
    assert stdout == data_out


@pytest.mark.parametrize(
    "ts",
    (
        pytest.param("0x42", id="numeric"),
        pytest.param("0xaa", id="lowercase"),
        pytest.param("0x00", id="zero padding"),
    ),
)
def test_invalid_ts(ts: str):
    atr = [int(ts[2:], 16), 0x00]
    with pytest.raises(SmartcardException, match=f"invalid TS {ts}"):
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


@pytest.mark.parametrize(
    "atr,",
    (
        pytest.param([], id="ATR is too short (0 bytes)"),
        pytest.param([0x3B], id="ATR is too short (1 byte, valid TS)"),
    ),
)
def test_invalid_atr_lengths(atr: list[int]):
    """Verify that short ATRs raise exceptions."""

    with pytest.raises(SmartcardException, match="at least 2 bytes"):
        ATR(atr)


@pytest.mark.parametrize("ts", (0x3B, 0x3F))
def test_2_bytes(ts):
    """Verify that a completely empty ATR parses well."""

    atr = ATR([ts, 0b0000_0000])
    #                |||| `-- no historical bytes
    #                |||`-- no TA
    #                ||`-- no TB
    #                |`-- no TC
    #                `-- no TD
    assert atr.getTA1() is None
    assert atr.getTB1() is None
    assert atr.II is None
    assert atr.PI1 is None
    assert atr.getTC1() is None
    assert atr.getTD1() is None
    assert atr.getChecksum() is None
    assert atr.getGuardTime() is None
    assert atr.getHistoricalBytesCount() == 0
    assert atr.getHistoricalBytes() == []
    assert atr.getInterfaceBytesCount() == 0

    # Default values
    assert atr.getBitRateFactor() == 1
    assert atr.getClockRateConversion() == 372
    assert atr.getProgrammingCurrent() == 50
    assert atr.getProgrammingVoltage() == 5

    # Protocols
    assert len(atr.getSupportedProtocols()) == 1
    assert "T=0" in atr.getSupportedProtocols()
    assert atr.isT0Supported() is True
    assert atr.isT1Supported() is False
    assert atr.isT15Supported() is False

    # Rendering
    expected_rendering = textwrap.dedent(
        """\
        supported protocols T=0
        T=0 supported: True
        T=1 supported: False
        \tclock rate conversion factor: 372
        \tbit rate adjustment factor: 1
        \tmaximum programming current: 50
        \tprogramming voltage: 5
        \tguard time: None
        nb of interface bytes: 0
        nb of historical bytes: 0
        """.rstrip()
    )
    assert atr.render() == expected_rendering

    # Warnings
    with pytest.warns(DeprecationWarning, match="ATR.TA"):
        assert atr.hasTA == [False]
    with pytest.warns(DeprecationWarning, match="ATR.TB"):
        assert atr.hasTB == [False]
    with pytest.warns(DeprecationWarning, match="ATR.TC"):
        assert atr.hasTC == [False]
    with pytest.warns(DeprecationWarning, match="ATR.TD"):
        assert atr.hasTD == [False]


def test_only_ta1():
    """Verify that TA1 can be conveyed standalone."""

    atr = ATR([0x3B, 0b0001_0000, 0xA7])
    #                     `-- only enable TA
    assert atr.TA == [0xA7]
    assert "TA1: a7\n" in atr.render()
    with pytest.warns(DeprecationWarning, match="ATR.TA"):
        assert atr.hasTA == [True]
    # TA1 affects these values
    assert atr.getClockRateConversion() == 768
    assert atr.getBitRateFactor() == 64
    # Sanity check
    assert atr.TB == atr.TC == atr.TD == [None]
    assert atr.N is None
    assert atr.getInterfaceBytesCount() == 1
    assert atr.getHistoricalBytesCount() == 0
    assert atr.hasChecksum is False
    assert atr.checksumOK is None
    assert atr.getChecksum() is None


def test_only_tb1():
    """Verify that TB1 can be conveyed standalone.

    TB1 and TB2 are deprecated in ISO 7816-3 2006, so no values are checked here.
    """

    atr = ATR([0x3B, 0b0010_0000, 0b0_10_11111])
    #                    `-- only enable TB
    assert atr.TB == [0b0_10_11111]
    assert "TB1: 5f\n" in atr.render()
    with pytest.warns(DeprecationWarning, match="ATR.TB"):
        assert atr.hasTB == [True]
    # TB1 affects these values
    assert atr.II == 0b10
    assert atr.PI1 == 0b11111
    assert atr.getProgrammingVoltage() != 5
    assert atr.getProgrammingCurrent() != 50
    # Sanity check
    assert atr.TA == atr.TC == atr.TD == [None]
    assert atr.N is None
    assert atr.getInterfaceBytesCount() == 1
    assert atr.getHistoricalBytesCount() == 0
    assert atr.hasChecksum is False
    assert atr.checksumOK is None
    assert atr.getChecksum() is None


def test_only_tc1():
    """Verify that TC1 can be conveyed standalone."""

    atr = ATR([0x3B, 0b0100_0000, 0xC1])
    #                   `-- only enable TC
    assert atr.TC == [0xC1]
    assert "TC1: c1\n" in atr.render()
    with pytest.warns(DeprecationWarning, match="ATR.TC"):
        assert atr.hasTC == [True]
    # TC1 affects these values
    assert atr.N == 0xC1
    # Sanity check
    assert atr.TA == atr.TB == atr.TD == [None]
    assert atr.getInterfaceBytesCount() == 1
    assert atr.getHistoricalBytesCount() == 0
    assert atr.hasChecksum is False
    assert atr.checksumOK is None
    assert atr.getChecksum() is None


def test_only_td1():
    """Verify that TD1 can be conveyed standalone."""

    atr = ATR([0x3B, 0b1000_0000, 0x00])
    #                  `-- only enable TD
    assert atr.TD == [0x00, None]
    assert atr.isT0Supported() is True
    assert atr.isT1Supported() is False
    assert atr.isT15Supported() is False
    assert "TD1: 0\n" in atr.render()
    with pytest.warns(DeprecationWarning, match="ATR.TD"):
        assert atr.hasTD == [True, False]
    # Sanity check
    assert atr.TA == atr.TB == atr.TC == [None, None]
    assert atr.N is None
    assert atr.getHistoricalBytesCount() == 0
    assert atr.hasChecksum is False
    assert atr.checksumOK is None
    assert atr.getChecksum() is None


def test_historical_bytes():
    """Verify that historical bytes can be conveyed standalone."""

    atr = ATR([0x3B, 0x0F, *list(range(15))])
    #                   `-- indicate 15 historical bytes
    assert atr.K == 15
    assert atr.getHistoricalBytesCount() == 15
    assert atr.getHistoricalBytes() == list(range(15))
    # Sanity check
    assert atr.TA == atr.TB == atr.TC == atr.TD == [None]
    assert atr.N is None
    assert atr.hasChecksum is False
    assert atr.checksumOK is None
    assert atr.getChecksum() is None


@pytest.mark.parametrize("ts", (0x3B, 0x3F))
@pytest.mark.parametrize("atr_bytes", ([0x00, 0x00], [0x1, 0xFE, 0xFF]))
def test_valid_checksums(ts, atr_bytes):
    """Verify behavior of valid checksums."""

    atr = ATR([ts] + atr_bytes)
    assert atr.hasChecksum is True
    assert atr.checksumOK is True
    assert atr.getChecksum() == atr_bytes[-1]
    assert f"checksum: {atr_bytes[-1]}\n" in atr.render()


@pytest.mark.parametrize("ts", (0x3B, 0x3F))
@pytest.mark.parametrize("atr_bytes", ([0x00, 0x01], [0x01, 0xFE, 0x0]))
def test_invalid_checksums(ts, atr_bytes):
    """Verify behavior of invalid checksums."""

    atr = ATR([ts] + atr_bytes)
    assert atr.hasChecksum is True
    assert atr.checksumOK is False
    assert atr.getChecksum() == atr_bytes[-1]
    assert f"checksum: {atr_bytes[-1]:x}\n" in atr.render()

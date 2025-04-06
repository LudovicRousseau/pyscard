import platform

import pytest

from smartcard.Exceptions import *
from smartcard.scard import *


def test_hresult_value():
    exc = SmartcardException()
    assert exc.hresult == -1


def test_list_readers_exception():
    exc = ListReadersException(-1)
    assert str(exc) == "Failed to list readers"

    exc = ListReadersException(0)
    assert exc.hresult == 0
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to list readers: "
            "The operation completed successfully.  (0x00000000)"
        )
    else:
        expected = "Failed to list readers: Command successful. (0x00000000)"
    assert text == expected

    exc = ListReadersException(0x42)
    assert exc.hresult == 0x42
    text = str(exc)
    if platform.system() != "Windows":
        expected = "Failed to list readers: Unknown error: 0x00000042 (0x00000042)"
        macos_bug_expected = expected.replace("Unknown", "Unkown")
        assert text in (expected, macos_bug_expected)

    exc = ListReadersException(SCARD_S_SUCCESS)
    assert exc.hresult == 0

    exc = ListReadersException(SCARD_E_NO_SERVICE)
    assert exc.hresult == SCARD_E_NO_SERVICE
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to list readers: "
            "The Smart Card Resource Manager is not running.  (0x8010001D)"
        )
    else:
        expected = "Failed to list readers: Service not available. (0x8010001D)"

    assert text == expected

    exc = ListReadersException(SCARD_E_NOT_TRANSACTED)
    if platform.system() == "Windows":
        expected = (
            "Failed to list readers: "
            "An attempt was made to end a non-existent transaction.  (0x80100016)"
        )
    else:
        expected = "Failed to list readers: Transaction failed. (0x80100016)"
    assert str(exc) == expected


def test_no_readers_exception():
    exc = NoReadersException()
    assert exc.hresult == -1
    text = str(exc)
    assert text == "No reader found"


def test_invalid_reader_exception():
    exc = InvalidReaderException("foobar")
    assert exc.hresult == -1
    text = str(exc)
    assert text == "Invalid reader: foobar"


def test_card_connection_exception():
    exc = CardConnectionException()
    assert exc.hresult == -1
    text = str(exc)
    assert text == ""

    exc = CardConnectionException(hresult=SCARD_W_REMOVED_CARD)
    assert exc.hresult == SCARD_W_REMOVED_CARD
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "The smart card has been removed, "
            "so that further communication is not possible.  (0x80100069)"
        )
    else:
        expected = "Card was removed. (0x80100069)"

    assert text == expected

    exc = CardConnectionException("", SCARD_W_REMOVED_CARD)
    assert exc.hresult == SCARD_W_REMOVED_CARD
    text = str(exc)
    assert text == expected

    # now add "foo" in the message
    expected = "foo: " + expected

    exc = CardConnectionException("foo", SCARD_W_REMOVED_CARD)
    assert exc.hresult == SCARD_W_REMOVED_CARD
    text = str(exc)
    assert text == expected

    exc = CardConnectionException(hresult=SCARD_W_REMOVED_CARD, message="foo")
    assert exc.hresult == SCARD_W_REMOVED_CARD
    text = str(exc)
    assert text == expected


def test_hresult():
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult == SCARD_S_SUCCESS:
        hresult, _, _ = SCardConnect(
            hcontext, "INVALID READER NAME", SCARD_SHARE_SHARED, SCARD_PROTOCOL_ANY
        )
        assert hresult == SCARD_E_UNKNOWN_READER
    else:
        assert hresult == SCARD_E_NO_SERVICE


@pytest.mark.parametrize("arg", ([0], "foo"))
def test_wrong_type(arg):
    # SCardEstablishContext() argument should be int
    with pytest.raises(TypeError):
        SCardEstablishContext(arg)


def test_card_request_timeout_exception():
    exc = CardRequestTimeoutException()
    assert str(exc) == "Time-out during card request"
    exc = CardRequestTimeoutException(SCARD_E_NOT_TRANSACTED)
    if platform.system() == "Windows":
        expected = (
            "Time-out during card request: "
            "An attempt was made to end a non-existent transaction.  (0x80100016)"
        )
    else:
        expected = "Time-out during card request: Transaction failed. (0x80100016)"
    assert str(exc) == expected
    exc = CardRequestTimeoutException(hresult=SCARD_E_NOT_TRANSACTED)
    assert str(exc) == expected


def test_invalid_atr_mask_length_exception():
    exc = InvalidATRMaskLengthException("3B 00")
    assert str(exc) == "Invalid ATR mask length: 3B 00"


def test_no_card_exception():
    exc = NoCardException("foo bar", -1)
    assert str(exc) == "foo bar"

    exc = NoCardException("foo bar", SCARD_E_NOT_TRANSACTED)
    if platform.system() == "Windows":
        expected = (
            "foo bar: "
            "An attempt was made to end a non-existent transaction.  (0x80100016)"
        )
    else:
        expected = "foo bar: Transaction failed. (0x80100016)"
    assert str(exc) == expected

import platform

from smartcard.pcsc.PCSCExceptions import *
from smartcard.scard import *


def test_list_readers_exception():
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
    if platform.system() == "Windows":
        expected = (
            "Failed to list readers: "
            "The network resource type is not correct.  (0x00000042)"
        )
    else:
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


def test_establish_context_exception():
    exc = EstablishContextException(SCARD_E_NO_SERVICE)
    assert exc.hresult == SCARD_E_NO_SERVICE
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to establish context: "
            "The Smart Card Resource Manager is not running.  (0x8010001D)"
        )
    else:
        expected = "Failed to establish context: Service not available. (0x8010001D)"
    assert text == expected


def test_introduce_reader_exception():
    exc = IntroduceReaderException(SCARD_E_DUPLICATE_READER, "foobar")
    assert exc.hresult == SCARD_E_DUPLICATE_READER
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to introduce a new reader: foobar: "
            "The reader driver did not produce a unique reader name.  (0x8010001B)"
        )
    else:
        expected = (
            "Failed to introduce a new reader: foobar: "
            "Reader already exists. (0x8010001B)"
        )
    assert text == expected


def test_remove_reader_from_group_exception():
    exc = RemoveReaderFromGroupException(
        SCARD_E_INVALID_HANDLE, "readername", "readergroup"
    )
    assert exc.hresult == SCARD_E_INVALID_HANDLE
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to remove reader: readername from group: readergroup: "
            "The supplied handle was invalid.  (0x80100003)"
        )
    else:
        expected = (
            "Failed to remove reader: readername from group: readergroup: "
            "Invalid handle. (0x80100003)"
        )
    assert text == expected


def test_add_reader_to_group_exception():
    exc = AddReaderToGroupException(SCARD_E_INVALID_HANDLE, "reader", "group")
    assert exc.hresult == SCARD_E_INVALID_HANDLE
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to add reader: reader to group: group: "
            "The supplied handle was invalid.  (0x80100003)"
        )
    else:
        expected = (
            "Failed to add reader: reader to group: group: "
            "Invalid handle. (0x80100003)"
        )
    assert text == expected


def test_release_context_exception():
    exc = ReleaseContextException(SCARD_E_INVALID_HANDLE)
    assert exc.hresult == SCARD_E_INVALID_HANDLE
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "Failed to release context: The supplied handle was invalid.  (0x80100003)"
        )
    else:
        expected = "Failed to release context: Invalid handle. (0x80100003)"
    assert text == expected


def test_base_scard_exception():
    exc = BaseSCardException(SCARD_E_UNKNOWN_READER)
    assert exc.hresult == SCARD_E_UNKNOWN_READER
    text = str(exc)
    if platform.system() == "Windows":
        expected = (
            "scard exception: "
            "The specified reader name is not recognized.  (0x80100009)"
        )
    else:
        expected = "scard exception: Unknown reader specified. (0x80100009)"
    assert text == expected

    exc = BaseSCardException(hresult=-1)
    assert exc.hresult == -1
    text = str(exc)
    expected = "scard exception"
    assert text == expected

    exc = BaseSCardException(hresult=-1, message="foo bar")
    assert exc.hresult == -1
    text = str(exc)
    expected = "foo bar"
    assert text == expected

    exc = BaseSCardException(message="foo", hresult=SCARD_E_NOT_TRANSACTED)
    assert exc.hresult == SCARD_E_NOT_TRANSACTED
    text = str(exc)
    if platform.system() == "Windows":
        expected = "An attempt was made to end a non-existent transaction. "
    else:
        expected = "Transaction failed."
    expected = "foo: " + expected + " (0x80100016)"
    assert text == expected

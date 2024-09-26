import platform

from smartcard.scard import (
    SCARD_F_INTERNAL_ERROR,
    SCARD_S_SUCCESS,
    SCardGetErrorMessage,
)


def test_scard_get_error_message():
    res = SCardGetErrorMessage(SCARD_S_SUCCESS)

    # do not test on Windows
    # the error messages are different and localized
    if platform.system() == "Windows":
        return

    expected = "Command successful."
    assert res == expected

    res = SCardGetErrorMessage(SCARD_F_INTERNAL_ERROR)
    expected = "Internal error."
    assert res == expected

    res = SCardGetErrorMessage(1)
    expected = "Unknown error: 0x00000001"
    # macOS bug not yet fixed
    macos_bug_expected = "Unkown error: 0x00000001"
    assert res in (expected, macos_bug_expected)

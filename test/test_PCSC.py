# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

from smartcard.scard import (
    SCARD_E_NO_READERS_AVAILABLE,
    SCARD_E_NO_SERVICE,
    SCARD_S_SUCCESS,
    SCARD_SCOPE_USER,
    SCardEstablishContext,
    SCardListReaders,
    SCardReleaseContext,
)


def test_low_level():
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    assert hresult in (SCARD_S_SUCCESS, SCARD_E_NO_SERVICE)

    if hresult == SCARD_E_NO_SERVICE:
        return

    hresult, _ = SCardListReaders(hcontext, [])
    assert hresult in (SCARD_S_SUCCESS, SCARD_E_NO_READERS_AVAILABLE)

    # the computer we are using may not have a reader connected
    # so we can't do much

    hresult = SCardReleaseContext(hcontext)
    assert hresult == SCARD_S_SUCCESS

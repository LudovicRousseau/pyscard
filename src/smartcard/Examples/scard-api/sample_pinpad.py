#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: send a Control Code to a card or
reader

__author__ = "Ludovic Rousseau"

Copyright 2009-2010 Ludovic Rousseau
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

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

import sys
import traceback

from smartcard.pcsc.PCSCExceptions import (
    BaseSCardException,
    EstablishContextException,
    ListReadersException,
    ReleaseContextException,
)
from smartcard.scard import (
    SCARD_CTL_CODE,
    SCARD_PROTOCOL_T0,
    SCARD_PROTOCOL_T1,
    SCARD_S_SUCCESS,
    SCARD_SCOPE_USER,
    SCARD_SHARE_SHARED,
    SCARD_UNPOWER_CARD,
    SCardConnect,
    SCardControl,
    SCardDisconnect,
    SCardEstablishContext,
    SCardListReaders,
    SCardReleaseContext,
    SCardTransmit,
    error,
)

# pylint: disable=missing-function-docstring


def can_do_verify_pin(hCard):
    FEATURE_VERIFY_PIN_DIRECT = 6
    return parse_get_feature_request(hCard, FEATURE_VERIFY_PIN_DIRECT)


def can_do_modify_pin(hCard):
    FEATURE_MODIFY_PIN_DIRECT = 7
    return parse_get_feature_request(hCard, FEATURE_MODIFY_PIN_DIRECT)


def parse_get_feature_request(hCard, feature):
    # check the reader can do a verify pin
    CM_IOCTL_GET_FEATURE_REQUEST = SCARD_CTL_CODE(3400)
    hresult, response = SCardControl(hCard, CM_IOCTL_GET_FEATURE_REQUEST, [])
    if hresult != SCARD_S_SUCCESS:
        raise BaseSCardException(hresult)
    print(response)
    while len(response) > 0:
        tag = response[0]
        if feature == tag:
            return (
                ((((response[2] << 8) + response[3]) << 8) + response[4]) << 8
            ) + response[5]
        response = response[6:]

    return None


def verifypin(hCard, control=None):
    if control is None:
        control = can_do_verify_pin(hCard)
        if control is None:
            raise BaseSCardException(message="Not a pinpad")

    command = [
        0x00,  # bTimerOut
        0x00,  # bTimerOut2
        0x82,  # bmFormatString
        0x08,  # bmPINBlockString
        0x00,  # bmPINLengthFormat
        0x08,
        0x04,  # wPINMaxExtraDigit
        0x02,  # bEntryValidationCondition
        0x01,  # bNumberMessage
        0x04,
        0x09,  # wLangId
        0x00,  # bMsgIndex
        0x00,
        0x00,
        0x00,  # bTeoPrologue
        13,
        0,
        0,
        0,  # ulDataLength
        0x00,
        0x20,
        0x00,
        0x00,
        0x08,
        0x30,
        0x30,
        0x30,
        0x30,
        0x30,
        0x30,
        0x30,
        0x30,
    ]  # abData
    hresult, response = SCardControl(hCard, control, command)
    if hresult != SCARD_S_SUCCESS:
        raise BaseSCardException(hresult)
    return hresult, response


def main():
    # pylint: disable=too-many-nested-blocks
    # pylint: disable=too-many-branches
    try:
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != SCARD_S_SUCCESS:
            raise EstablishContextException(hresult)
        print("Context established!")

        try:
            hresult, readers = SCardListReaders(hcontext, [])
            if hresult != SCARD_S_SUCCESS:
                raise ListReadersException(hresult)
            print("PCSC Readers:", readers)

            if len(readers) < 1:
                raise BaseSCardException(message="No smart card readers")

            for zreader in readers:

                print("Trying to Control reader:", zreader)

                try:
                    hresult, hcard, dwActiveProtocol = SCardConnect(
                        hcontext,
                        zreader,
                        SCARD_SHARE_SHARED,
                        SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1,
                    )
                    if hresult != SCARD_S_SUCCESS:
                        raise BaseSCardException(hresult)
                    print("Connected with active protocol", dwActiveProtocol)

                    try:
                        SELECT = [
                            0x00,
                            0xA4,
                            0x04,
                            0x00,
                            0x06,
                            0xA0,
                            0x00,
                            0x00,
                            0x00,
                            0x18,
                            0xFF,
                        ]
                        hresult, response = SCardTransmit(
                            hcard, dwActiveProtocol, SELECT
                        )
                        if hresult != SCARD_S_SUCCESS:
                            raise BaseSCardException(hresult)

                        cmd_verify = can_do_verify_pin(hcard)
                        if cmd_verify:
                            print(f"can do verify pin: 0x{cmd_verify:08X}")

                        cmd_modify = can_do_modify_pin(hcard)
                        if cmd_modify:
                            print(f"can do modify pin: 0x{cmd_modify:08X}")

                        hresult, response = verifypin(hcard, cmd_verify)
                        print("Control:", response)
                    except BaseSCardException as ex:
                        print("Exception:", ex)
                        traceback.print_exc()
                    finally:
                        hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                        if hresult != SCARD_S_SUCCESS:
                            raise BaseSCardException(hresult)
                        print("Disconnected")

                except BaseSCardException as ex:
                    print("SCard Exception:", ex)

        finally:
            hresult = SCardReleaseContext(hcontext)
            if hresult != SCARD_S_SUCCESS:
                raise ReleaseContextException(hresult)
            print("Released context.")

    except error as e:
        print(e)


if __name__ == "__main__":
    main()

    if "win32" == sys.platform:
        print("press Enter to continue")
        sys.stdin.read(1)

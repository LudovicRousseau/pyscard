#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: List card attributes

__author__ = "https://www.gemalto.com/"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
Copyright 2010 Ludovic Rousseau
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

import struct
import sys

import smartcard.util
from smartcard.scard import *

attributes = {
    SCARD_ATTR_ATR_STRING: "SCARD_ATTR_ATR_STRING",
    SCARD_ATTR_CHANNEL_ID: "SCARD_ATTR_CHANNEL_ID",
    SCARD_ATTR_CHARACTERISTICS: "SCARD_ATTR_CHARACTERISTICS",
    SCARD_ATTR_CURRENT_BWT: "SCARD_ATTR_CURRENT_BWT",
    SCARD_ATTR_CURRENT_CLK: "SCARD_ATTR_CURRENT_CLK",
    SCARD_ATTR_CURRENT_CWT: "SCARD_ATTR_CURRENT_CWT",
    SCARD_ATTR_CURRENT_D: "SCARD_ATTR_CURRENT_D",
    SCARD_ATTR_CURRENT_EBC_ENCODING: "SCARD_ATTR_CURRENT_EBC_ENCODING",
    SCARD_ATTR_CURRENT_F: "SCARD_ATTR_CURRENT_F",
    SCARD_ATTR_CURRENT_IFSC: "SCARD_ATTR_CURRENT_IFSC",
    SCARD_ATTR_CURRENT_IFSD: "SCARD_ATTR_CURRENT_IFSD",
    SCARD_ATTR_CURRENT_IO_STATE: "SCARD_ATTR_CURRENT_IO_STATE",
    SCARD_ATTR_CURRENT_N: "SCARD_ATTR_CURRENT_N",
    SCARD_ATTR_CURRENT_PROTOCOL_TYPE: "SCARD_ATTR_CURRENT_PROTOCOL_TYPE",
    SCARD_ATTR_CURRENT_W: "SCARD_ATTR_CURRENT_W",
    SCARD_ATTR_DEFAULT_CLK: "SCARD_ATTR_DEFAULT_CLK",
    SCARD_ATTR_DEFAULT_DATA_RATE: "SCARD_ATTR_DEFAULT_DATA_RATE",
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_A: "SCARD_ATTR_DEVICE_FRIENDLY_NAME_A",
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_W: "SCARD_ATTR_DEVICE_FRIENDLY_NAME_W",
    SCARD_ATTR_DEVICE_IN_USE: "SCARD_ATTR_DEVICE_IN_USE",
    SCARD_ATTR_DEVICE_SYSTEM_NAME_A: "SCARD_ATTR_DEVICE_SYSTEM_NAME_A",
    SCARD_ATTR_DEVICE_SYSTEM_NAME_W: "SCARD_ATTR_DEVICE_SYSTEM_NAME_W",
    SCARD_ATTR_DEVICE_UNIT: "SCARD_ATTR_DEVICE_UNIT",
    SCARD_ATTR_ESC_AUTHREQUEST: "SCARD_ATTR_ESC_AUTHREQUEST",
    SCARD_ATTR_ESC_CANCEL: "SCARD_ATTR_ESC_CANCEL",
    SCARD_ATTR_ESC_RESET: "SCARD_ATTR_ESC_RESET",
    SCARD_ATTR_EXTENDED_BWT: "SCARD_ATTR_EXTENDED_BWT",
    SCARD_ATTR_ICC_INTERFACE_STATUS: "SCARD_ATTR_ICC_INTERFACE_STATUS",
    SCARD_ATTR_ICC_PRESENCE: "SCARD_ATTR_ICC_PRESENCE",
    SCARD_ATTR_ICC_TYPE_PER_ATR: "SCARD_ATTR_ICC_TYPE_PER_ATR",
    SCARD_ATTR_MAXINPUT: "SCARD_ATTR_MAXINPUT",
    SCARD_ATTR_MAX_CLK: "SCARD_ATTR_MAX_CLK",
    SCARD_ATTR_MAX_DATA_RATE: "SCARD_ATTR_MAX_DATA_RATE",
    SCARD_ATTR_MAX_IFSD: "SCARD_ATTR_MAX_IFSD",
    SCARD_ATTR_POWER_MGMT_SUPPORT: "SCARD_ATTR_POWER_MGMT_SUPPORT",
    SCARD_ATTR_SUPRESS_T1_IFS_REQUEST: "SCARD_ATTR_SUPRESS_T1_IFS_REQUEST",
    SCARD_ATTR_USER_AUTH_INPUT_DEVICE: "SCARD_ATTR_USER_AUTH_INPUT_DEVICE",
    SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE: "SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE",
    SCARD_ATTR_VENDOR_IFD_SERIAL_NO: "SCARD_ATTR_VENDOR_IFD_SERIAL_NO",
    SCARD_ATTR_VENDOR_IFD_TYPE: "SCARD_ATTR_VENDOR_IFD_TYPE",
    SCARD_ATTR_VENDOR_IFD_VERSION: "SCARD_ATTR_VENDOR_IFD_VERSION",
    SCARD_ATTR_VENDOR_NAME: "SCARD_ATTR_VENDOR_NAME",
}
if "pcsclite" == resourceManager:
    extra_attributes = {
        SCARD_ATTR_ASYNC_PROTOCOL_TYPES: "SCARD_ATTR_ASYNC_PROTOCOL_TYPES",
        SCARD_ATTR_SYNC_PROTOCOL_TYPES: "SCARD_ATTR_SYNC_PROTOCOL_TYPES",
    }
    attributes.update(extra_attributes)


def printAttribute(attrib, value):
    print("-----------------", attributes[attrib], "-----------------")
    print(value)
    print(smartcard.util.toHexString(value, smartcard.util.HEX))
    print(struct.pack(*["<" + "B" * len(value)] + value))


if __name__ == "__main__":
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise error("Failed to establish context: " + SCardGetErrorMessage(hresult))
    print("Context established!")

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to list readers: " + SCardGetErrorMessage(hresult))
        print("PCSC Readers:", readers)

        if len(readers) < 1:
            raise error("No smart card readers")

        for reader in readers:
            print("Trying to retrieve attributes of", reader)
            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext,
                reader,
                SCARD_SHARE_SHARED,
                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1,
            )
            if hresult != SCARD_S_SUCCESS:
                print(error, "Unable to connect: " + SCardGetErrorMessage(hresult))
            else:

                print("Connected with active protocol", dwActiveProtocol)

                try:
                    for i in list(attributes.keys()):
                        hresult, attrib = SCardGetAttrib(hcard, i)
                        if hresult == SCARD_S_SUCCESS:
                            printAttribute(i, attrib)
                        else:
                            print(
                                "-----------------", attributes[i], "-----------------"
                            )
                            print("error:", SCardGetErrorMessage(hresult))

                finally:
                    hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                    if hresult != SCARD_S_SUCCESS:
                        raise error(
                            "Failed to disconnect: " + SCardGetErrorMessage(hresult)
                        )
                    print("Disconnected")

    finally:
        hresult = SCardReleaseContext(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to release context: " + SCardGetErrorMessage(hresult))
        print("Released context.")

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

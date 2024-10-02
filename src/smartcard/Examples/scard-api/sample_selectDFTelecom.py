#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: Select DF_TELECOM on a SIM card

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

import sys

import smartcard.util
from smartcard.scard import *

SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]
GET_RESPONSE = [0xA0, 0xC0, 0x00, 0x00]

try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise error("Failed to establish context : " + SCardGetErrorMessage(hresult))
    print("Context established!")

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to list readers: " + SCardGetErrorMessage(hresult))
        print("PCSC Readers:", readers)

        if len(readers) < 1:
            raise error("No smart card readers")

        for zreader in readers:

            print("Trying to select DF_TELECOM of card in", zreader)

            try:
                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext,
                    zreader,
                    SCARD_SHARE_SHARED,
                    SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1,
                )
                if hresult != SCARD_S_SUCCESS:
                    raise error("Unable to connect: " + SCardGetErrorMessage(hresult))
                print("Connected with active protocol", dwActiveProtocol)

                try:
                    hresult, response = SCardTransmit(
                        hcard, dwActiveProtocol, SELECT + DF_TELECOM
                    )
                    if hresult != SCARD_S_SUCCESS:
                        raise error(
                            "Failed to transmit: " + SCardGetErrorMessage(hresult)
                        )
                    print(
                        "Selected DF_TELECOM: "
                        + smartcard.util.toHexString(response, smartcard.util.HEX)
                    )
                    hresult, response = SCardTransmit(
                        hcard, dwActiveProtocol, GET_RESPONSE + [response[1]]
                    )
                    if hresult != SCARD_S_SUCCESS:
                        raise error(
                            "Failed to transmit: " + SCardGetErrorMessage(hresult)
                        )
                    print(
                        "GET_RESPONSE after SELECT DF_TELECOM: "
                        + smartcard.util.toHexString(response, smartcard.util.HEX)
                    )
                finally:
                    hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                    if hresult != SCARD_S_SUCCESS:
                        raise error(
                            "Failed to disconnect: " + SCardGetErrorMessage(hresult)
                        )
                    print("Disconnected")

            except error as message:
                print(error, message)

    finally:
        hresult = SCardReleaseContext(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to release context: " + SCardGetErrorMessage(hresult))
        print("Released context.")

except error as e:
    print(e)

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: send a Control Code to a card or
reader

__author__ = "Ludovic Rousseau"

Copyright 2007-2010 Ludovic Rousseau
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

from smartcard.scard import *
from smartcard.util import toASCIIString, toBytes, toHexString

try:
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

        for zreader in readers:

            print("Trying to Control reader:", zreader)

            try:
                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext, zreader, SCARD_SHARE_DIRECT, SCARD_PROTOCOL_T0
                )
                if hresult != SCARD_S_SUCCESS:
                    raise error("Unable to connect: " + SCardGetErrorMessage(hresult))
                print("Connected with active protocol", dwActiveProtocol)

                try:
                    if "winscard" == resourceManager:
                        # IOCTL_SMARTCARD_GET_ATTRIBUTE = SCARD_CTL_CODE(2)
                        hresult, response = SCardControl(
                            hcard,
                            SCARD_CTL_CODE(2),
                            toBytes("%.8lx" % SCARD_ATTR_VENDOR_NAME),
                        )
                        if hresult != SCARD_S_SUCCESS:
                            raise error(
                                "SCardControl failed: " + SCardGetErrorMessage(hresult)
                            )
                        print("SCARD_ATTR_VENDOR_NAME:", toASCIIString(response))
                    elif "pcsclite" == resourceManager:
                        # get feature request
                        hresult, response = SCardControl(
                            hcard, SCARD_CTL_CODE(3400), []
                        )
                        if hresult != SCARD_S_SUCCESS:
                            raise error(
                                "SCardControl failed: " + SCardGetErrorMessage(hresult)
                            )
                        print("CM_IOCTL_GET_FEATURE_REQUEST:", toHexString(response))
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

import sys

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

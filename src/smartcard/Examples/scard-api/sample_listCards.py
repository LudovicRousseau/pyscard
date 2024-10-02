#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: List cards introduced in the system

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

from smartcard.scard import *

if "winscard" == resourceManager:
    # Cryptoflex 8k v2 is introduced in standard Windows 2000
    slbCryptoFlex8kv2ATR = [0x3B, 0x95, 0x15, 0x40, 0x00, 0x68, 0x01, 0x02, 0x00, 0x00]
    try:
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to establish context: " + SCardGetErrorMessage(hresult))
        print("Context established!")

        try:
            hresult, card = SCardListCards(hcontext, slbCryptoFlex8kv2ATR, [])
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failure to locate Schlumberger Cryptoflex 8k v2 card: "
                    + SCardGetErrorMessage(hresult)
                )
            print("Located by ATR:", card)

            hresult, cards = SCardListCards(hcontext, [], [])
            if hresult != SCARD_S_SUCCESS:
                raise error("Failure to list cards: " + SCardGetErrorMessage(hresult))
            print("Cards:", cards)

            for i in cards:
                hresult, providerguid = SCardGetCardTypeProviderName(
                    hcontext, i, SCARD_PROVIDER_PRIMARY
                )
                if hresult == SCARD_S_SUCCESS:
                    print(i, "Primary provider:", providername)
                hresult, providername = SCardGetCardTypeProviderName(
                    hcontext, i, SCARD_PROVIDER_CSP
                )
                if hresult == SCARD_S_SUCCESS:
                    print(i, "CSP Provider:", providername)

        finally:
            hresult = SCardReleaseContext(hcontext)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to release context: " + SCardGetErrorMessage(hresult)
                )
            print("Released context.")

    except error as e:
        print(e)

elif "pcsclite" == resourceManager:
    print("SCardListCards not supported by pcsc lite")


if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

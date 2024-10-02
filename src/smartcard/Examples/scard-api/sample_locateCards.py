#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: Locate cards in the system

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

    znewcardName = "dummy-card"
    znewcardATR = [
        0x3B,
        0x77,
        0x94,
        0x00,
        0x00,
        0x82,
        0x30,
        0x00,
        0x13,
        0x6C,
        0x9F,
        0x22,
    ]
    znewcardMask = [
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
    ]

    try:
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != SCARD_S_SUCCESS:
            raise scard.error(
                "Failed to establish context: " + SCardGetErrorMessage(hresult)
            )
        print("Context established!")

        try:
            hresult, readers = SCardListReaders(hcontext, [])
            if hresult != SCARD_S_SUCCESS:
                raise scard.error(
                    "Failed to list readers: " + SCardGetErrorMessage(hresult)
                )
            print("PCSC Readers:", readers)

            # introduce a card (forget first in case it is already present)
            hresult = SCardForgetCardType(hcontext, znewcardName)
            print("Introducing card " + znewcardName)
            hresult = SCardIntroduceCardType(
                hcontext, znewcardName, [], [], znewcardATR, znewcardMask
            )
            if hresult != SCARD_S_SUCCESS:
                if hresult == ERROR_ALREADY_EXISTS:
                    print("Card already exists")
                else:
                    raise error(
                        "Failed to introduce card type: "
                        + SCardGetErrorMessage(hresult)
                    )

            hresult, cards = SCardListCards(hcontext, [], [])
            if hresult != SCARD_S_SUCCESS:
                raise error("Failure to list cards")
            print("Cards:", cards)

            readerstates = []
            for i in range(len(readers)):
                readerstates += [(readers[i], SCARD_STATE_UNAWARE)]
            print(readerstates)

            hresult, newstates = SCardLocateCards(hcontext, cards, readerstates)
            for i in newstates:
                reader, eventstate, atr = i
                print(reader, end=" ")
                for b in atr:
                    print("0x%.2X" % b, end=" ")
                print("")
                if eventstate & SCARD_STATE_ATRMATCH:
                    print("Card found")
                if eventstate & SCARD_STATE_UNAWARE:
                    print("State unware")
                if eventstate & SCARD_STATE_IGNORE:
                    print("Ignore reader")
                if eventstate & SCARD_STATE_UNAVAILABLE:
                    print("Reader unavailable")
                if eventstate & SCARD_STATE_EMPTY:
                    print("Reader empty")
                if eventstate & SCARD_STATE_PRESENT:
                    print("Card present in reader")
                if eventstate & SCARD_STATE_EXCLUSIVE:
                    print("Card allocated for exclusive use")
                if eventstate & SCARD_STATE_INUSE:
                    print("Card in use but can be shared")
                if eventstate & SCARD_STATE_MUTE:
                    print("Card is mute")
                if eventstate & SCARD_STATE_CHANGED:
                    print("State changed")
                if eventstate & SCARD_STATE_UNKNOWN:
                    print("State unknowned")

        finally:
            hresult = SCardForgetCardType(hcontext, znewcardName)
            hresult = SCardReleaseContext(hcontext)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to release context: " + SCardGetErrorMessage(hresult)
                )
            print("Released context.")

    except error as e:
        print(e)

elif "pcsclite" == resourceManager:
    print("SCardLocateCards not supported by pcsc lite")


if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

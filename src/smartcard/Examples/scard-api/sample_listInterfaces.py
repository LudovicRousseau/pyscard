#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: List card interfaces

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

import platform
import sys

import smartcard.guid
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
    znewcardPrimGuid = smartcard.guid.strToGUID(
        "{128F3806-4F70-4ccf-977A-60C390664840}"
    )
    znewcardSecGuid = smartcard.guid.strToGUID("{EB7F69EA-BA20-47d0-8C50-11CFDEB63BBE}")

    def main():
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != SCARD_S_SUCCESS:
            raise scard.error(
                "Failed to establish context: " + SCardGetErrorMessage(hresult)
            )
        print("Context established!")

        try:

            # list interfaces for a known card
            expectedCard = "Schlumberger Cryptoflex 8k v2"
            hresult, interfaces = SCardListInterfaces(hcontext, expectedCard)
            if hresult != SCARD_S_SUCCESS:
                raise scard.error(
                    "Failed to list interfaces: " + SCardGetErrorMessage(hresult)
                )
            print("Interfaces for ", expectedCard, ":", interfaces)

            # introduce a card (forget first in case it is already present)
            hresult = SCardForgetCardType(hcontext, znewcardName)
            print("Introducing card " + znewcardName)
            hresult = SCardIntroduceCardType(
                hcontext,
                znewcardName,
                znewcardPrimGuid,
                znewcardPrimGuid + znewcardSecGuid,
                znewcardATR,
                znewcardMask,
            )
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to introduce card type: " + SCardGetErrorMessage(hresult)
                )

            # list card interfaces
            hresult, interfaces = SCardListInterfaces(hcontext, znewcardName)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to list interfaces: " + SCardGetErrorMessage(hresult)
                )
            for i in interfaces:
                print(
                    "Interface for " + znewcardName + " :", smartcard.guid.GUIDToStr(i)
                )

            print("Forgetting card " + znewcardName)
            hresult = SCardForgetCardType(hcontext, znewcardName)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to remove card type: " + SCardGetErrorMessage(hresult)
                )

        finally:
            hresult2 = SCardReleaseContext(hcontext)
            if hresult2 != SCARD_S_SUCCESS:
                raise error(
                    "Failed to release context: " + SCardGetErrorMessage(hresult)
                )
            print("Released context.")

    main()

elif "pcsclite" == resourceManager:
    print("SCardListInterfaces not supported by pcsc lite")


if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)

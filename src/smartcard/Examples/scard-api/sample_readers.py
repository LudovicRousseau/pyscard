#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: List PCSC readers

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

from smartcard.scard import *

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

        hresult, readerGroups = SCardListReaderGroups(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise error(
                "Unable to list reader groups: " + SCardGetErrorMessage(hresult)
            )
        print("PCSC Reader groups:", readerGroups)

    finally:
        hresult = SCardReleaseContext(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to release context: " + SCardGetErrorMessage(hresult))
        print("Released context.")

    import sys

    if "win32" == sys.platform:
        print("press Enter to continue")
        sys.stdin.read(1)

except error as e:
    print(e)

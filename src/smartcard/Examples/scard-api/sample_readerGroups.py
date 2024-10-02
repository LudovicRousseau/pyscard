#! /usr/bin/env python3
"""
Sample for python PCSC wrapper module: illustrate reader groups functions

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

newgroup = "MyReaderGroup"

try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise error("Failed to establish context: " + SCardGetErrorMessage(hresult))
    print("Context established!")

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise error("Failed to list readers: " + SCardGetErrorMessage(hresult))
        print("PCSC Readers in all groups:", readers)

        hresult, readerGroups = SCardListReaderGroups(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise error(
                "Unable to list reader groups: " + SCardGetErrorMessage(hresult)
            )
        print("PCSC Reader groups:", readerGroups)

        if "winscard" == resourceManager:

            hresult = SCardIntroduceReaderGroup(hcontext, newgroup)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to introduce reader group: " + SCardGetErrorMessage(hresult)
                )

            dummyreader = readers[0] + " dummy"
            hresult = SCardIntroduceReader(hcontext, dummyreader, readers[0])
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to introduce reader: "
                    + dummyreader
                    + " : "
                    + SCardGetErrorMessage(hresult)
                )

            hresult, readers = SCardListReaders(hcontext, [])
            if hresult != SCARD_S_SUCCESS:
                raise error("Failed to list readers: " + SCardGetErrorMessage(hresult))
            print("PCSC Readers in all groups:", readers)

            hresult = SCardAddReaderToGroup(hcontext, dummyreader, newgroup)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to add reader to group: " + SCardGetErrorMessage(hresult)
                )

            hresult, readerGroups = SCardListReaderGroups(hcontext)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to list reader groups: " + SCardGetErrorMessage(hresult)
                )
            print("PCSC Reader groups:", readerGroups)

            hresult, readers = SCardListReaders(hcontext, [newgroup])
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to list readers in group "
                    + newgroup
                    + " : "
                    + SCardGetErrorMessage(hresult)
                )
            print("PCSC Readers in reader group", newgroup, ":", readers)

            hresult = SCardRemoveReaderFromGroup(hcontext, dummyreader, newgroup)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to remove reader from group: "
                    + SCardGetErrorMessage(hresult)
                )

            hresult, readerGroups = SCardListReaderGroups(hcontext)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to list reader groups: " + SCardGetErrorMessage(hresult)
                )
            print("PCSC Reader groups:", readerGroups)

            hresult = SCardForgetReaderGroup(hcontext, newgroup)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Unable to forget reader group: " + SCardGetErrorMessage(hresult)
                )

            hresult = SCardForgetReader(hcontext, dummyreader)
            if hresult != SCARD_S_SUCCESS:
                raise error("Failed to forget readers " + SCardGetErrorMessage(hresult))

            hresult, readers = SCardListReaders(hcontext, [])
            if hresult != SCARD_S_SUCCESS:
                raise error("Failed to list readers: " + SCardGetErrorMessage(hresult))
            print("PCSC Readers in all groups:", readers)

        elif "pcsclite" == resourceManager:
            hresult, readers = SCardListReaders(hcontext, readerGroups)
            if hresult != SCARD_S_SUCCESS:
                raise error(
                    "Failed to list readers in groups "
                    + repr(readerGroups)
                    + " : "
                    + SCardGetErrorMessage(hresult)
                )
            print("PCSC Readers in reader group", readerGroups, ":", readers)

            hresult = SCardIntroduceReaderGroup(hcontext, newgroup)
            if hresult != SCARD_E_UNSUPPORTED_FEATURE:
                raise error(
                    "Was expecting an error instead of: "
                    + SCardGetErrorMessage(hresult)
                )

            dummyreader = readers[0] + " dummy"
            hresult = SCardAddReaderToGroup(hcontext, dummyreader, newgroup)
            if hresult != SCARD_E_UNSUPPORTED_FEATURE:
                raise error(
                    "Was expecting an error instead of: "
                    + SCardGetErrorMessage(hresult)
                )

            dummyreader = readers[0] + " dummy"
            hresult = SCardIntroduceReader(hcontext, dummyreader, readers[0])
            if hresult != SCARD_E_UNSUPPORTED_FEATURE:
                raise error(
                    "Was expecting an error instead of: "
                    + SCardGetErrorMessage(hresult)
                )

            hresult = SCardRemoveReaderFromGroup(hcontext, dummyreader, newgroup)
            if hresult != SCARD_E_UNSUPPORTED_FEATURE:
                raise error(
                    "Was expecting an error instead of: "
                    + SCardGetErrorMessage(hresult)
                )

            hresult = SCardForgetReaderGroup(hcontext, newgroup)
            if hresult != SCARD_E_UNSUPPORTED_FEATURE:
                raise error(
                    "Was expecting an error instead of: "
                    + SCardGetErrorMessage(hresult)
                )

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

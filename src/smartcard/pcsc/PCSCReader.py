"""PCSCReader: concrete reader class for PCSC Readers

__author__ = "gemalto https://www.gemalto.com/"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

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

from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.Exceptions import *
from smartcard.pcsc.PCSCCardConnection import PCSCCardConnection
from smartcard.pcsc.PCSCExceptions import *
from smartcard.reader.Reader import Reader
from smartcard.scard import *


def __PCSCreaders__(hcontext, groups=None):
    """Returns the list of PCSC smartcard readers in PCSC group.

    If group is not specified, returns the list of all PCSC smartcard readers.
    """

    if groups is None:
        groups = []
    elif isinstance(groups, str):
        groups = [groups]
    hresult, readers = SCardListReaders(hcontext, groups)
    if hresult != SCARD_S_SUCCESS:
        if hresult == SCARD_E_NO_READERS_AVAILABLE:
            readers = []
        elif hresult == SCARD_E_SERVICE_STOPPED:
            raise CardServiceStoppedException(hresult=hresult)
        elif hresult == SCARD_E_NO_SERVICE:
            raise CardServiceNotFoundException(hresult=hresult)
        else:
            raise ListReadersException(hresult)

    return readers


class PCSCReader(Reader):
    """PCSC reader class."""

    def __init__(self, readername):
        """Constructs a new PCSC reader."""
        Reader.__init__(self, readername)

    def addtoreadergroup(self, groupname):
        """Add reader to a reader group."""

        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if SCARD_S_SUCCESS != hresult:
            raise EstablishContextException(hresult)
        try:
            hresult = SCardIntroduceReader(hcontext, self.name, self.name)
            if SCARD_S_SUCCESS != hresult and SCARD_E_DUPLICATE_READER != hresult:
                raise IntroduceReaderException(hresult, self.name)
            hresult = SCardAddReaderToGroup(hcontext, self.name, groupname)
            if SCARD_S_SUCCESS != hresult:
                raise AddReaderToGroupException(hresult, self.name, groupname)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if SCARD_S_SUCCESS != hresult:
                raise ReleaseContextException(hresult)

    def removefromreadergroup(self, groupname):
        """Remove a reader from a reader group"""

        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if SCARD_S_SUCCESS != hresult:
            raise EstablishContextException(hresult)
        try:
            hresult = SCardRemoveReaderFromGroup(hcontext, self.name, groupname)
            if SCARD_S_SUCCESS != hresult:
                raise RemoveReaderFromGroupException(hresult, self.name, groupname)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if SCARD_S_SUCCESS != hresult:
                raise ReleaseContextException(hresult)

    def createConnection(self):
        """Return a card connection thru PCSC reader."""
        return CardConnectionDecorator(PCSCCardConnection(self.name))

    class Factory:
        @staticmethod
        def create(readername):
            return PCSCReader(readername)

    @staticmethod
    def readers(groups=None):
        if groups is None:
            groups = []
        creaders = []
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if SCARD_S_SUCCESS != hresult:
            raise EstablishContextException(hresult)
        try:
            pcsc_readers = __PCSCreaders__(hcontext, groups)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if SCARD_S_SUCCESS != hresult:
                raise ReleaseContextException(hresult)

        for reader in pcsc_readers:
            creaders.append(PCSCReader.Factory.create(reader))
        return creaders


if __name__ == "__main__":
    from smartcard.util import *

    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]

    creaders = PCSCReader.readers()
    for reader in creaders:
        try:
            print(reader.name)
            connection = reader.createConnection()
            connection.connect()
            print(toHexString(connection.getATR()))
            data, sw1, sw2 = connection.transmit(SELECT + DF_TELECOM)
            print(f"{sw1:02X} {sw2:02X}")
        except NoCardException:
            print("no card in reader")

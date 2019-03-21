"""PCSCReader: concrete reader class for PCSC Readers

__author__ = "gemalto http://www.gemalto.com"

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

from __future__ import print_function
from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.reader.Reader import Reader
from smartcard.pcsc.PCSCContext import PCSCContext
from smartcard.pcsc.PCSCCardConnection import PCSCCardConnection
from smartcard.Exceptions import *
from smartcard.pcsc.PCSCExceptions import *
from smartcard.scard import *


def __PCSCreaders__(hcontext, groups=[]):
    """Returns the list of PCSC smartcard readers in PCSC group.

    If group is not specified, returns the list of all PCSC smartcard readers.
    """

    # in case we have a string instead of a list
    if isinstance(groups, type("")):
        groups = [groups]
    hresult, readers = SCardListReaders(hcontext, groups)
    if hresult != 0:
        if hresult == SCARD_E_NO_READERS_AVAILABLE:
            readers = []
        elif hresult == SCARD_E_SERVICE_STOPPED:
            raise CardServiceStoppedException()
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
        if 0 != hresult:
            raise EstablishContextException(hresult)
        try:
            hresult = SCardIntroduceReader(hcontext, self.name, self.name)
            if 0 != hresult and SCARD_E_DUPLICATE_READER != hresult:
                raise IntroduceReaderException(hresult, self.name)
            hresult = SCardAddReaderToGroup(hcontext, self.name, groupname)
            if 0 != hresult:
                raise AddReaderToGroupException(hresult, self.name, groupname)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if 0 != hresult:
                raise ReleaseContextException(hresult)

    def removefromreadergroup(self, groupname):
        """Remove a reader from a reader group"""

        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if 0 != hresult:
            raise EstablishContextException(hresult)
        try:
            hresult = SCardRemoveReaderFromGroup(hcontext, self.name,
                groupname)
            if 0 != hresult:
                raise RemoveReaderFromGroupException(hresult, self.name,
                    groupname)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if 0 != hresult:
                raise ReleaseContextException(hresult)

    def createConnection(self):
        """Return a card connection thru PCSC reader."""
        return CardConnectionDecorator(PCSCCardConnection(self.name))

    class Factory:

        def create(readername):
            return PCSCReader(readername)
        create = staticmethod(create)

    def readers(groups=[]):
        creaders = []
        hcontext = PCSCContext().getContext()

        try:
            pcsc_readers = __PCSCreaders__(hcontext, groups)
        except CardServiceStoppedException:
            hcontext = PCSCContext.renewContext()
            pcsc_readers = __PCSCreaders__(hcontext, groups)

        for reader in pcsc_readers:
            creaders.append(PCSCReader.Factory.create(reader))
        return creaders
    readers = staticmethod(readers)

if __name__ == '__main__':
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
            print("%02X %02X" % (sw1, sw2))
        except NoCardException:
            print('no card in reader')

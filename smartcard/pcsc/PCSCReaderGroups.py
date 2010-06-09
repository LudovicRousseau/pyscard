"""PCSCReaderGroups organizes smartcard readers as groups.

__author__ = "gemalto http://www.gemalto.com"

Copyright 2001-2010 gemalto
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

from smartcard.scard import *
from smartcard.reader.ReaderGroups import readergroups, innerreadergroups
from smartcard.pcsc.PCSCExceptions import *


class pcscinnerreadergroups(innerreadergroups):
    """Smartcard PCSC readers groups inner class.

    The PCSCReaderGroups singleton manages the creation of the unique
    instance of this class.
    """

    def __init__(self, initlist=None):
        """Constructor."""
        innerreadergroups.__init__(self, initlist)
        self.unremovablegroups = ['SCard$DefaultReaders']

    def getreadergroups(self):
        """ Returns the list of smartcard reader groups.

        import smartcard
        print smartcard.reader_groups()
        """
        innerreadergroups.getreadergroups(self)

        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != 0:
            raise EstablishContextException(hresult)
        hresult, readers = SCardListReaderGroups(hcontext)
        if hresult != 0:
            raise ListReadersException(hresult)
        hresult = SCardReleaseContext(hcontext)
        if hresult != 0:
            raise ReleaseContextException(hresult)
        return readers

    def addreadergroup(self, newgroup):
        """Add a reader group"""

        innerreadergroups.addreadergroup(self, newgroup)

        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if 0 != hresult:
            raise error, 'Failed to establish context: ' + SCardGetErrorMessage(hresult)
        try:
            hresult = SCardIntroduceReaderGroup(hcontext, newgroup)
            if 0 != hresult:
                raise error, 'Unable to introduce reader group: ' + SCardGetErrorMessage(hresult)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if 0 != hresult:
                raise error, 'Failed to release context: ' + SCardGetErrorMessage(hresult)

    def removereadergroup(self, group):
        """Remove a reader group"""

        innerreadergroups.removereadergroup(self, group)

        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if 0 != hresult:
            raise error, 'Failed to establish context: ' + SCardGetErrorMessage(hresult)
        try:
            hresult = SCardForgetReaderGroup(hcontext, group)
            if hresult != 0:
                raise error, 'Unable to forget reader group: ' + SCardGetErrorMessage(hresult)
        finally:
            hresult = SCardReleaseContext(hcontext)
            if 0 != hresult:
                raise error, 'Failed to release context: ' + SCardGetErrorMessage(hresult)


class PCSCReaderGroups(readergroups):
    """PCSC readers groups."""

    """The single instance of __readergroups"""
    instance = None

    """Constructor: create a single instance of __readergroups on first call"""

    def __init__(self, initlist=None):
        if None == PCSCReaderGroups.instance:
            PCSCReaderGroups.instance = pcscinnerreadergroups(initlist)

    """All operators redirected to inner class."""

    def __getattr__(self, name):
        return getattr(self.instance, name)


if __name__ == '__main__':
    print PCSCReaderGroups()
